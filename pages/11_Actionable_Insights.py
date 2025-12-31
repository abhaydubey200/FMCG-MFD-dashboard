# pages/11_Actionable_Insights.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from utils.data_loader import load_dataset, detect_columns
from utils.visualizations import plot_heatmap

st.set_page_config(page_title="Actionable Insights", layout="wide")

st.title("📊 Actionable Insights Dashboard")

# -----------------------------
# Upload Dataset
# -----------------------------
uploaded_file = st.file_uploader("Upload your FMCG dataset (Excel/CSV)", type=["csv", "xlsx"])
if uploaded_file:
    df = load_dataset(uploaded_file)
else:
    st.warning("Please upload a dataset to continue.")
    st.stop()

# Detect date columns
date_cols = detect_columns(df, dtype='datetime')
if not date_cols:
    st.warning("No date columns detected. Make sure your dataset has a date column.")
    st.stop()

date_col = date_cols[0]
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# Filter by date range
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df[date_col].min())
end_date = st.sidebar.date_input("End Date", df[date_col].max())
filtered_df = df[(df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(end_date))]

# -----------------------------
# KPI Cards
# -----------------------------
st.header("🏆 Key Performance Indicators")
total_sales = filtered_df['AMOUNT'].sum()
total_orders = filtered_df['ORDER_ID'].nunique()
total_qty = filtered_df['TOTAL_QUANTITY'].sum()
avg_order_value = filtered_df['AMOUNT'].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Sales", f"{total_sales:,.0f}")
kpi2.metric("🛒 Total Orders", f"{total_orders:,}")
kpi3.metric("📦 Total Quantity", f"{total_qty:,.0f}")
kpi4.metric("💵 Avg Order Value", f"{avg_order_value:,.2f}")

# -----------------------------
# Alerts for Low-Performers
# -----------------------------
st.header("⚠️ Low-Performing SKUs & Outlets")

min_sales = st.sidebar.number_input("Min Sales Threshold", value=50000, step=1000)
min_qty = st.sidebar.number_input("Min Quantity Threshold", value=50, step=1)

# Low-performing SKUs
low_skus = filtered_df.groupby('SKU_PLACED')['AMOUNT'].sum().reset_index()
low_skus = low_skus[low_skus['AMOUNT'] < min_sales]
if not low_skus.empty:
    st.subheader("Low Performing SKUs")
    st.dataframe(low_skus.style.highlight_max(axis=0, color='red'))
else:
    st.success("No low-performing SKUs!")

# Low-performing Outlets
low_outlets = filtered_df.groupby('OUTLET_NAME')['AMOUNT'].sum().reset_index()
low_outlets = low_outlets[low_outlets['AMOUNT'] < min_sales]
if not low_outlets.empty:
    st.subheader("Low Performing Outlets")
    st.dataframe(low_outlets.style.highlight_max(axis=0, color='red'))
else:
    st.success("No low-performing Outlets!")

# -----------------------------
# Weekly Summary
# -----------------------------
st.header("📅 Weekly Summary")
filtered_df['WEEK'] = filtered_df[date_col].dt.isocalendar().week
weekly_summary = filtered_df.groupby('WEEK').agg(
    Total_Sales=('AMOUNT', 'sum'),
    Total_Orders=('ORDER_ID', 'nunique'),
    Total_Quantity=('TOTAL_QUANTITY', 'sum'),
    Avg_Order_Value=('AMOUNT', 'mean')
).reset_index()
st.dataframe(weekly_summary)

# Export weekly summary
import io
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    weekly_summary.to_excel(writer, index=False, sheet_name='Weekly_Summary')
    writer.save()
st.download_button(
    label="Download Weekly Summary as Excel",
    data=excel_buffer,
    file_name="weekly_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# -----------------------------
# Forecasting
# -----------------------------
st.header("📈 Sales Forecast Overlay")

forecast_model = st.selectbox("Select Forecasting Model", ["Prophet", "Random Forest"])

forecast_days = st.slider("Forecast Days", min_value=7, max_value=365, value=30, step=7)

if forecast_model == "Prophet":
    df_prophet = filtered_df.groupby(date_col)['AMOUNT'].sum().reset_index()
    df_prophet.columns = ['ds', 'y']
    m = Prophet()
    m.fit(df_prophet)
    future = m.make_future_dataframe(periods=forecast_days)
    forecast = m.predict(future)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_prophet['ds'], y=df_prophet['y'], mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    st.plotly_chart(fig, use_container_width=True)

elif forecast_model == "Random Forest":
    df_rf = filtered_df.groupby(date_col)['AMOUNT'].sum().reset_index()
    df_rf['day_number'] = np.arange(len(df_rf))
    X = df_rf[['day_number']]
    y = df_rf['AMOUNT']
    model = RandomForestRegressor(n_estimators=200)
    model.fit(X, y)
    future_days = np.arange(len(df_rf), len(df_rf) + forecast_days).reshape(-1, 1)
    forecast = model.predict(future_days)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_rf[date_col], y=df_rf['AMOUNT'], mode='lines', name='Actual'))
    future_dates = pd.date_range(df_rf[date_col].max() + pd.Timedelta(days=1), periods=forecast_days)
    fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode='lines', name='Forecast'))
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Heatmap
# -----------------------------
st.header("🌡 Sales Heatmap (Day vs Month)")

filtered_df['DAY'] = filtered_df[date_col].dt.day
filtered_df['MONTH'] = filtered_df[date_col].dt.month

heatmap_data = filtered_df.groupby(['DAY', 'MONTH'])['AMOUNT'].sum().reset_index()
fig_heat = px.density_heatmap(
    heatmap_data, x='DAY', y='MONTH', z='AMOUNT', color_continuous_scale='Viridis',
    labels={'DAY': 'Day of Month', 'MONTH': 'Month', 'AMOUNT': 'Sales Amount'}
)
st.plotly_chart(fig_heat, use_container_width=True)
