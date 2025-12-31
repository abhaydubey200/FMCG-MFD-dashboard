# 11_Actionable_Insights.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.visualizations import line_sales_trend, bar_top
from utils.data_loader import load_dataset
from utils.forecasting import prepare_time_series, forecast_sales
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

st.set_page_config(page_title="Actionable Insights", layout="wide")

st.title(" Actionable Insights Dashboard")

# -----------------------------
# Use common dataset from page 0
# -----------------------------
if "df" in st.session_state:
    df = st.session_state["df"]
else:
    uploaded_file = st.file_uploader(
        "Upload your FMCG dataset (CSV / Excel)", type=["csv", "xlsx"]
    )
    if uploaded_file:
        df = load_dataset(uploaded_file)
    else:
        st.info("Please upload a dataset on page 0 or here to continue.")
        st.stop()

# -----------------------------
# Data Preprocessing
# -----------------------------
df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'], errors='coerce')
df = df.dropna(subset=['ORDER_DATE'])

# -----------------------------
# KPI Cards
# -----------------------------
total_sales = df['AMOUNT'].sum()
total_orders = df['ORDER_ID'].nunique()
total_quantity = df['TOTAL_QUANTITY'].sum()
avg_order_value = total_sales / total_orders

col1, col2, col3, col4 = st.columns(4)
col1.metric(" Total Sales", f"{total_sales:,.0f}")
col2.metric(" Total Orders", f"{total_orders:,}")
col3.metric(" Total Quantity", f"{total_quantity:,.0f}")
col4.metric(" Avg Order Value", f"{avg_order_value:,.2f}")

st.markdown("---")

# -----------------------------
# Sales Trend Line
# -----------------------------
st.subheader(" Sales Trend Over Time")
fig_trend = line_sales_trend(df, 'ORDER_DATE', 'AMOUNT')
st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# Top 5 Cities / Warehouses / Brands
# -----------------------------
st.subheader(" Top 5 Cities / Warehouses / Brands")

col1, col2, col3 = st.columns(3)

fig_top_cities = bar_top(df, 'CITY', 'AMOUNT', "Top 5 Cities by Sales")
col1.plotly_chart(fig_top_cities, use_container_width=True)

fig_top_warehouses = bar_top(df, 'WAREHOUSE', 'AMOUNT', "Top 5 Warehouses by Sales")
col2.plotly_chart(fig_top_warehouses, use_container_width=True)

fig_top_brands = bar_top(df, 'BRAND', 'AMOUNT', "Top 5 Brands by Sales")
col3.plotly_chart(fig_top_brands, use_container_width=True)

st.markdown("---")

# -----------------------------
# Heatmap: Day vs Month
# -----------------------------
st.subheader(" Sales Heatmap (Day vs Month)")
df['day'] = df['ORDER_DATE'].dt.day
df['month'] = df['ORDER_DATE'].dt.month
heatmap_data = df.groupby(['day', 'month'])['AMOUNT'].sum().reset_index()
fig_heatmap = px.density_heatmap(
    heatmap_data, x='day', y='month', z='AMOUNT',
    color_continuous_scale='Viridis',
    title="Sales Heatmap"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# -----------------------------
# Forecast Overlay (Prophet / RF)
# -----------------------------
st.subheader("🔮 Sales Forecast")

# Aggregate monthly sales
monthly_sales = df.groupby(pd.Grouper(key='ORDER_DATE', freq='M'))['AMOUNT'].sum().reset_index()
monthly_sales.rename(columns={'ORDER_DATE': 'ds', 'AMOUNT': 'y'}, inplace=True)

# Prophet Forecast
prophet_model = Prophet()
prophet_model.fit(monthly_sales)
future = prophet_model.make_future_dataframe(periods=12, freq='M')
forecast = prophet_model.predict(future)
fig_prophet = px.line(forecast, x='ds', y='yhat', title="Prophet Forecast Overlay")
fig_prophet.add_scatter(x=monthly_sales['ds'], y=monthly_sales['y'], mode='lines', name='Actual')
st.plotly_chart(fig_prophet, use_container_width=True)

# Random Forest Forecast
rf_df = monthly_sales.copy()
rf_df['month'] = rf_df['ds'].dt.month
rf_df['year'] = rf_df['ds'].dt.year
X = rf_df[['year', 'month']]
y = rf_df['y']

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Predict next 12 months
future_dates = pd.date_range(start=rf_df['ds'].max() + pd.Timedelta(days=1), periods=12, freq='M')
future_df = pd.DataFrame({'ds': future_dates})
future_df['month'] = future_df['ds'].dt.month
future_df['year'] = future_df['ds'].dt.year
future_df['yhat'] = rf_model.predict(future_df[['year', 'month']])

fig_rf = px.line(future_df, x='ds', y='yhat', title="Random Forest Forecast Overlay")
fig_rf.add_scatter(x=monthly_sales['ds'], y=monthly_sales['y'], mode='lines', name='Actual')
st.plotly_chart(fig_rf, use_container_width=True)
