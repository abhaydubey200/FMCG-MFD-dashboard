import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Daily Sales Analysis", layout="wide")
st.title("Daily Sales Analysis")
# ---------------------------------------
# Load data from session
# ---------------------------------------
if "df" not in st.session_state:
    st.warning(" Please upload dataset from Upload page")
    st.stop()

df = st.session_state.df.copy()

# ---------------------------------------
# Mandatory Columns Check
# ---------------------------------------
required_cols = ["ORDER_DATE", "AMOUNT"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f" Missing required columns: {missing}")
    st.stop()

# ---------------------------------------
# Data Preparation
# ---------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

df["DATE"] = df["ORDER_DATE"].dt.date

daily_sales = (
    df.groupby("DATE")["AMOUNT"]
    .sum()
    .reset_index()
    .sort_values("DATE")
)

# ---------------------------------------
# KPI Calculations
# ---------------------------------------
today_sales = daily_sales.iloc[-1]["AMOUNT"] if len(daily_sales) >= 1 else 0
yesterday_sales = daily_sales.iloc[-2]["AMOUNT"] if len(daily_sales) >= 2 else 0

growth_pct = (
    ((today_sales - yesterday_sales) / yesterday_sales) * 100
    if yesterday_sales > 0 else 0
)

avg_daily_sales = daily_sales["AMOUNT"].mean()

best_day = daily_sales.loc[daily_sales["AMOUNT"].idxmax()]
worst_day = daily_sales.loc[daily_sales["AMOUNT"].idxmin()]

# ---------------------------------------
# KPI Section
# ---------------------------------------
k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Today Sales", f"₹ {today_sales:,.0f}")
k2.metric("Yesterday Sales", f"₹ {yesterday_sales:,.0f}")
k3.metric("Daily Growth %", f"{growth_pct:.2f}%")
k4.metric("Avg Daily Sales", f"₹ {avg_daily_sales:,.0f}")
k5.metric("Best Sales Day", best_day["DATE"])
k6.metric("Worst Sales Day", worst_day["DATE"])

st.divider()

# ---------------------------------------
# Daily Sales Trend
# ---------------------------------------
fig_trend = px.line(
    daily_sales,
    x="DATE",
    y="AMOUNT",
    markers=True,
    title=" Daily Sales Trend"
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------
# Day of Week Performance
# ---------------------------------------
daily_sales["DAY"] = pd.to_datetime(daily_sales["DATE"]).dt.day_name()

dow_sales = (
    daily_sales.groupby("DAY")["AMOUNT"]
    .mean()
    .reset_index()
)

fig_dow = px.bar(
    dow_sales,
    x="DAY",
    y="AMOUNT",
    title=" Avg Sales by Day of Week"
)
st.plotly_chart(fig_dow, use_container_width=True)

# ---------------------------------------
# City & Brand Contribution
# ---------------------------------------
col1, col2 = st.columns(2)

if "CITY" in df.columns:
    city_sales = (
        df.groupby("CITY")["AMOUNT"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig_city = px.bar(
        city_sales,
        x="CITY",
        y="AMOUNT",
        title="Top 10 Cities by Daily Sales"
    )
    col1.plotly_chart(fig_city, use_container_width=True)

if "BRAND" in df.columns:
    brand_sales = (
        df.groupby("BRAND")["AMOUNT"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig_brand = px.bar(
        brand_sales,
        x="BRAND",
        y="AMOUNT",
        title=" Top 10 Brands by Daily Sales"
    )
    col2.plotly_chart(fig_brand, use_container_width=True)

# ---------------------------------------
# Quantity Trend (Optional)
# ---------------------------------------
if "TOTAL_QUANTITY" in df.columns:
    qty_daily = (
        df.groupby("DATE")["TOTAL_QUANTITY"]
        .sum()
        .reset_index()
    )

    fig_qty = px.line(
        qty_daily,
        x="DATE",
        y="TOTAL_QUANTITY",
        title=" Daily Quantity Trend"
    )
    st.plotly_chart(fig_qty, use_container_width=True)

# ---------------------------------------
# Data Table
# ---------------------------------------
with st.expander("📋 View Daily Sales Data"):
    st.dataframe(daily_sales, use_container_width=True)
