import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from prophet import Prophet

st.set_page_config(page_title="Advanced Daily Sales Analysis", layout="wide")
st.title("Advanced Daily Sales Analysis")

# ---------------------------
# Load data
# ---------------------------
if "data" not in st.session_state or st.session_state["data"] is None:
    st.warning(" Please upload data from the Upload Dataset page")
    st.stop()

df = st.session_state["data"].copy()

# ---------------------------
# Required columns check
# ---------------------------
required_cols = [
    "ORDER_DATE", "ORDER_ID", "AMOUNT",
    "TOTAL_QUANTITY", "CITY", "WAREHOUSE", "BRAND"
]

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f" Missing required columns: {missing_cols}")
    st.stop()

# ---------------------------
# Data preprocessing
# ---------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header(" Filters")
min_date = df["ORDER_DATE"].min().date()
max_date = df["ORDER_DATE"].max().date()
date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

city_filter = st.sidebar.multiselect("Select City", sorted(df["CITY"].dropna().unique()))
warehouse_filter = st.sidebar.multiselect("Select Warehouse", sorted(df["WAREHOUSE"].dropna().unique()))
brand_filter = st.sidebar.multiselect("Select Brand", sorted(df["BRAND"].dropna().unique()))

filtered_df = df[
    (df["ORDER_DATE"].dt.date >= date_range[0]) &
    (df["ORDER_DATE"].dt.date <= date_range[1])
]

if city_filter:
    filtered_df = filtered_df[filtered_df["CITY"].isin(city_filter)]
if warehouse_filter:
    filtered_df = filtered_df[filtered_df["WAREHOUSE"].isin(warehouse_filter)]
if brand_filter:
    filtered_df = filtered_df[filtered_df["BRAND"].isin(brand_filter)]

# ---------------------------
# Daily aggregation
# ---------------------------
daily_sales = filtered_df.groupby(filtered_df["ORDER_DATE"].dt.date).agg(
    Total_Sales_Amount=("AMOUNT", "sum"),
    Total_Quantity=("TOTAL_QUANTITY", "sum"),
    Total_Orders=("ORDER_ID", "nunique")
).reset_index()

daily_sales.rename(columns={"ORDER_DATE": "Date"}, inplace=True)

# ---------------------------
# Step 1: Week-on-Week & Month-on-Month Growth
# ---------------------------
st.subheader("1 Week-on-Week & Month-on-Month Growth")

daily_sales["Week"] = pd.to_datetime(daily_sales["Date"]).dt.isocalendar().week
daily_sales["Month"] = pd.to_datetime(daily_sales["Date"]).dt.to_period("M")

weekly_sales = daily_sales.groupby("Week")["Total_Sales_Amount"].sum().pct_change().fillna(0) * 100
monthly_sales = daily_sales.groupby("Month")["Total_Sales_Amount"].sum().pct_change().fillna(0) * 100

k1, k2 = st.columns(2)
k1.metric("Week-on-Week Growth %", f"{weekly_sales.iloc[-1]:.2f}%")
k2.metric("Month-on-Month Growth %", f"{monthly_sales.iloc[-1]:.2f}%")

# ---------------------------
# Step 2: Top 5 Cities / Warehouses / Brands
# ---------------------------
st.subheader(" 2 Top 5 Cities, Warehouses & Brands")

top_cities = filtered_df.groupby("CITY")["AMOUNT"].sum().nlargest(5).reset_index()
top_warehouses = filtered_df.groupby("WAREHOUSE")["AMOUNT"].sum().nlargest(5).reset_index()
top_brands = filtered_df.groupby("BRAND")["AMOUNT"].sum().nlargest(5).reset_index()

col1, col2, col3 = st.columns(3)
col1.bar_chart(top_cities.set_index("CITY"))
col2.bar_chart(top_warehouses.set_index("WAREHOUSE"))
col3.bar_chart(top_brands.set_index("BRAND"))

# ---------------------------
# Step 3: Sales Heatmap (Day vs Month)
# ---------------------------
st.subheader("3️ Sales Heatmap (Day vs Month)")

heatmap_data = filtered_df.copy()
heatmap_data["Day"] = heatmap_data["ORDER_DATE"].dt.day
heatmap_data["Month"] = heatmap_data["ORDER_DATE"].dt.month

heatmap_pivot = heatmap_data.pivot_table(
    index="Day", columns="Month", values="AMOUNT", aggfunc="sum", fill_value=0
)

fig_heatmap = px.imshow(
    heatmap_pivot,
    labels=dict(x="Month", y="Day", color="Sales Amount"),
    x=[str(m) for m in heatmap_pivot.columns],
    y=[str(d) for d in heatmap_pivot.index],
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ---------------------------
# Step 4: Forecast Overlay (Prophet)
# ---------------------------
st.subheader("4️ Sales Forecast Overlay")

forecast_days = st.slider("Select Forecast Days", min_value=7, max_value=90, value=30, step=1)

prophet_df = daily_sales[["Date", "Total_Sales_Amount"]].rename(columns={"Date": "ds", "Total_Sales_Amount": "y"})
model = Prophet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True)
model.fit(prophet_df)

future = model.make_future_dataframe(periods=forecast_days)
forecast = model.predict(future)

fig_forecast = px.line()
fig_forecast.add_scatter(x=prophet_df["ds"], y=prophet_df["y"], mode="lines", name="Actual")
fig_forecast.add_scatter(x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Forecast")
st.plotly_chart(fig_forecast, use_container_width=True)

# ---------------------------
# Download forecast
# ---------------------------
forecast_csv = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download Forecast CSV", data=forecast_csv, file_name="sales_forecast.csv", mime="text/csv")
