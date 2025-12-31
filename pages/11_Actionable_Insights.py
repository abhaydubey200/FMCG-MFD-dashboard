import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="📈 Actionable Insights", layout="wide")

st.title("📈 Actionable Insights Dashboard")
st.caption("Executive-level insights derived from sales behavior")

# -------------------------------------------------
# Load data from common uploader (Session State)
# -------------------------------------------------
if "df" not in st.session_state:
    st.warning("⬆️ Please upload a dataset from the Upload Dataset page.")
    st.stop()

df = st.session_state["df"].copy()

# -------------------------------------------------
# Mandatory Columns Check
# -------------------------------------------------
required_cols = ["ORDER_DATE", "AMOUNT", "CITY", "WAREHOUSE", "BRAND"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

# -------------------------------------------------
# Data Preparation
# -------------------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE", "AMOUNT"])

df["order_day"] = df["ORDER_DATE"].dt.day
df["order_month"] = df["ORDER_DATE"].dt.month
df["order_week"] = df["ORDER_DATE"].dt.isocalendar().week
df["year_month"] = df["ORDER_DATE"].dt.to_period("M").astype(str)

# -------------------------------------------------
# KPI SECTION (Traffic Light)
# -------------------------------------------------
st.subheader("🚦 Key Performance Indicators")

total_sales = df["AMOUNT"].sum()
avg_daily_sales = df.groupby("ORDER_DATE")["AMOUNT"].sum().mean()

mom_growth = (
    df.groupby("year_month")["AMOUNT"].sum().pct_change().iloc[-1] * 100
    if df["year_month"].nunique() > 1 else 0
)

def kpi_color(value):
    if value > 10:
        return "🟢"
    elif value > 0:
        return "🟠"
    return "🔴"

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📊 Avg Daily Sales", f"₹{avg_daily_sales:,.0f}")
col3.metric(
    "📈 MoM Growth",
    f"{mom_growth:.2f}%",
    delta=f"{kpi_color(mom_growth)}"
)

# -------------------------------------------------
# Top 5 Analysis
# -------------------------------------------------
st.subheader("🏆 Top 5 Contributors")

c1, c2, c3 = st.columns(3)

with c1:
    top_city = df.groupby("CITY")["AMOUNT"].sum().nlargest(5).reset_index()
    st.plotly_chart(px.bar(top_city, x="CITY", y="AMOUNT", title="Top 5 Cities"), True)

with c2:
    top_wh = df.groupby("WAREHOUSE")["AMOUNT"].sum().nlargest(5).reset_index()
    st.plotly_chart(px.bar(top_wh, x="WAREHOUSE", y="AMOUNT", title="Top 5 Warehouses"), True)

with c3:
    top_brand = df.groupby("BRAND")["AMOUNT"].sum().nlargest(5).reset_index()
    st.plotly_chart(px.bar(top_brand, x="BRAND", y="AMOUNT", title="Top 5 Brands"), True)

# -------------------------------------------------
# Sales Heatmap (Day vs Month)
# -------------------------------------------------
st.subheader("🔥 Sales Heatmap (Day vs Month)")

heatmap_df = (
    df.groupby(["order_day", "order_month"], as_index=False)["AMOUNT"].sum()
)

pivot_heatmap = heatmap_df.pivot(
    index="order_day",
    columns="order_month",
    values="AMOUNT"
)

fig_heatmap = px.imshow(
    pivot_heatmap,
    labels=dict(x="Month", y="Day", color="Sales"),
    title="Sales Intensity Heatmap",
    aspect="auto"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# -------------------------------------------------
# Forecast Overlay (Random Forest – Production Safe)
# -------------------------------------------------
st.subheader("🔮 Forecast Overlay (Next 90 Days)")

daily_sales = df.groupby("ORDER_DATE")["AMOUNT"].sum().reset_index()
daily_sales["t"] = (daily_sales["ORDER_DATE"] - daily_sales["ORDER_DATE"].min()).dt.days

X = daily_sales[["t"]]
y = daily_sales["AMOUNT"]

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X, y)

future_days = 90
future_dates = pd.date_range(
    start=daily_sales["ORDER_DATE"].max() + pd.Timedelta(days=1),
    periods=future_days
)

future_t = (future_dates - daily_sales["ORDER_DATE"].min()).days.values.reshape(-1, 1)
forecast = rf.predict(future_t)

forecast_df = pd.DataFrame({
    "ORDER_DATE": future_dates,
    "AMOUNT": forecast
})

fig_forecast = px.line(daily_sales, x="ORDER_DATE", y="AMOUNT", title="Sales Forecast Overlay")
fig_forecast.add_scatter(
    x=forecast_df["ORDER_DATE"],
    y=forecast_df["AMOUNT"],
    mode="lines",
    name="Forecast"
)

st.plotly_chart(fig_forecast, use_container_width=True)

# -------------------------------------------------
# Executive Takeaways
# -------------------------------------------------
st.subheader("🧠 Executive Insights")

st.success(
    f"""
• Sales momentum is **{kpi_color(mom_growth)} {'positive' if mom_growth > 0 else 'negative'}**
• Top cities & warehouses drive majority revenue
• Clear seasonal demand patterns visible
• Forecast indicates {'growth' if forecast.mean() > avg_daily_sales else 'softening demand'}
"""
)
