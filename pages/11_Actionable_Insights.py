import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Actionable Insights", layout="wide")

st.title(" Actionable Insights Dashboard")

# -------------------------------------------------
# Load dataset from common uploader
# -------------------------------------------------
if "df" not in st.session_state:
    st.warning(" Please upload a dataset from the Upload Dataset page.")
    st.stop()

df = st.session_state["df"].copy()

# -------------------------------------------------
# Column validation
# -------------------------------------------------
required_cols = ["ORDER_DATE", "AMOUNT", "CITY", "WAREHOUSE", "BRAND"]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f" Missing required columns: {missing}")
    st.stop()

# -------------------------------------------------
# Data preparation
# -------------------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

df["order_day"] = df["ORDER_DATE"].dt.day
df["order_month"] = df["ORDER_DATE"].dt.month
df["order_week"] = df["ORDER_DATE"].dt.isocalendar().week
df["order_year"] = df["ORDER_DATE"].dt.year

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("🚦 Business KPIs")

total_sales = df["AMOUNT"].sum()
avg_daily_sales = df.groupby("ORDER_DATE")["AMOUNT"].sum().mean()
max_day_sales = df.groupby("ORDER_DATE")["AMOUNT"].sum().max()

col1, col2, col3 = st.columns(3)

col1.metric(
    " Total Sales",
    f"₹ {total_sales:,.0f}",
    delta="Good" if total_sales > 0 else "Bad"
)

col2.metric(
    " Avg Daily Sales",
    f"₹ {avg_daily_sales:,.0f}"
)

col3.metric(
    " Best Day Sales",
    f"₹ {max_day_sales:,.0f}"
)

st.divider()

# -------------------------------------------------
# TOP CONTRIBUTORS
# -------------------------------------------------
st.subheader(" Top Business Drivers")

c1, c2, c3 = st.columns(3)

with c1:
    top_city = (
        df.groupby("CITY", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
        .head(5)
    )
    fig = px.bar(top_city, x="CITY", y="AMOUNT", title="Top 5 Cities")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    top_wh = (
        df.groupby("WAREHOUSE", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
        .head(5)
    )
    fig = px.bar(top_wh, x="WAREHOUSE", y="AMOUNT", title="Top 5 Warehouses")
    st.plotly_chart(fig, use_container_width=True)

with c3:
    top_brand = (
        df.groupby("BRAND", as_index=False)["AMOUNT"]
        .sum()
        .sort_values("AMOUNT", ascending=False)
        .head(5)
    )
    fig = px.bar(top_brand, x="BRAND", y="AMOUNT", title="Top 5 Brands")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------
# SALES HEATMAP (FIXED)
# -------------------------------------------------
st.subheader(" Sales Heatmap (Day vs Month)")

heatmap_df = (
    df.groupby(["order_day", "order_month"], as_index=False)
    .agg({"AMOUNT": "sum"})
)

pivot_heatmap = heatmap_df.pivot(
    index="order_day",
    columns="order_month",
    values="AMOUNT"
)

fig_heatmap = px.imshow(
    pivot_heatmap,
    labels=dict(
        x="Month",
        y="Day of Month",
        color="Sales Amount"
    ),
    title="Sales Intensity Heatmap",
    aspect="auto"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()

# -------------------------------------------------
# WEEK-ON-WEEK & MONTH-ON-MONTH GROWTH
# -------------------------------------------------
st.subheader(" Growth Trends")

growth_col1, growth_col2 = st.columns(2)

with growth_col1:
    weekly_sales = (
        df.groupby(["order_year", "order_week"], as_index=False)["AMOUNT"]
        .sum()
    )
    fig = px.line(
        weekly_sales,
        x="order_week",
        y="AMOUNT",
        color="order_year",
        title="Week-on-Week Sales Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

with growth_col2:
    monthly_sales = (
        df.groupby(["order_year", "order_month"], as_index=False)["AMOUNT"]
        .sum()
    )
    fig = px.line(
        monthly_sales,
        x="order_month",
        y="AMOUNT",
        color="order_year",
        title="Month-on-Month Sales Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

st.success(" Actionable Insights Dashboard loaded successfully")
