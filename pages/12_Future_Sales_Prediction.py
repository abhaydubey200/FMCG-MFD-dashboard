import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Future Sales Prediction", layout="wide")
st.title("🔮 Future Sales Prediction (Next 12 Months)")

# -------------------------------------------------
# Load dataset from common uploader
# -------------------------------------------------
if "df" not in st.session_state:
    st.warning("⚠️ Please upload dataset from Upload Dataset page.")
    st.stop()

df = st.session_state["df"].copy()

# -------------------------------------------------
# Required columns check
# -------------------------------------------------
required_cols = ["ORDER_DATE", "AMOUNT"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"❌ Missing required columns: {missing}")
    st.stop()

# -------------------------------------------------
# Data preparation
# -------------------------------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

df["year"] = df["ORDER_DATE"].dt.year
df["month"] = df["ORDER_DATE"].dt.month

monthly_sales = (
    df.groupby(["year", "month"], as_index=False)["AMOUNT"]
    .sum()
    .sort_values(["year", "month"])
)

# Create continuous time index
monthly_sales["time_idx"] = np.arange(len(monthly_sales))

X = monthly_sales[["time_idx"]]
y = monthly_sales["AMOUNT"]

# -------------------------------------------------
# Train Random Forest Model
# -------------------------------------------------
model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)
model.fit(X, y)

# -------------------------------------------------
# Forecast next 12 months
# -------------------------------------------------
future_steps = 12
last_idx = monthly_sales["time_idx"].max()

future_idx = np.arange(last_idx + 1, last_idx + future_steps + 1)
future_X = pd.DataFrame({"time_idx": future_idx})

future_preds = model.predict(future_X)

# Generate future dates
last_date = pd.to_datetime(
    f"{monthly_sales.iloc[-1]['year']}-{monthly_sales.iloc[-1]['month']}-01"
)

future_dates = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=12,
    freq="MS"
)

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted_Sales": future_preds
})

# -------------------------------------------------
# Combine historical + forecast
# -------------------------------------------------
monthly_sales["Date"] = pd.to_datetime(
    monthly_sales["year"].astype(str) + "-" +
    monthly_sales["month"].astype(str) + "-01"
)

monthly_sales["Type"] = "Actual"
forecast_df["Type"] = "Forecast"
forecast_df.rename(columns={"Predicted_Sales": "AMOUNT"}, inplace=True)

final_df = pd.concat([
    monthly_sales[["Date", "AMOUNT", "Type"]],
    forecast_df[["Date", "AMOUNT", "Type"]]
])

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.subheader("📊 Forecast KPIs")

c1, c2, c3 = st.columns(3)

c1.metric(
    "📈 Total Forecast (12 Months)",
    f"₹ {forecast_df['AMOUNT'].sum():,.0f}"
)

c2.metric(
    "📆 Avg Monthly Forecast",
    f"₹ {forecast_df['AMOUNT'].mean():,.0f}"
)

c3.metric(
    "🔥 Peak Forecast Month",
    forecast_df.loc[forecast_df["AMOUNT"].idxmax(), "Date"].strftime("%b %Y")
)

st.divider()

# -------------------------------------------------
# Visualization
# -------------------------------------------------
st.subheader("📉 Sales Forecast (Actual vs Predicted)")

fig = px.line(
    final_df,
    x="Date",
    y="AMOUNT",
    color="Type",
    markers=True,
    title="Historical Sales vs 12-Month Forecast"
)
st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Forecast Table
# -------------------------------------------------
st.subheader("📄 Forecast Table")

forecast_df_display = forecast_df.copy()
forecast_df_display["Month"] = forecast_df_display["Date"].dt.strftime("%b %Y")
forecast_df_display["Predicted Sales"] = forecast_df_display["AMOUNT"].round(0)

st.dataframe(
    forecast_df_display[["Month", "Predicted Sales"]],
    use_container_width=True
)

# -------------------------------------------------
# Business Insight
# -------------------------------------------------
st.success(
    "✅ Forecast generated successfully. "
    "Use this for inventory planning, target setting & budgeting."
)
