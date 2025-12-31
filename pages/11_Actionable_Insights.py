# 11_Forecasting_Insights.py
import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from utils.data_loader import load_dataset
from utils.visualizations import line_sales_trend, bar_top

st.set_page_config(page_title="Forecasting & Insights", layout="wide")
st.title("📊 Actionable Insights & Future Forecasting")

# -----------------------------
# Load common dataset from page 0
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

df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'], errors='coerce')
df = df.dropna(subset=['ORDER_DATE'])

# -----------------------------
# 1️⃣ Actionable Insights
# -----------------------------
st.header("🔍 Actionable Insights")
# Weekly / Monthly Growth
df['Month'] = df['ORDER_DATE'].dt.to_period('M')
monthly_sales = df.groupby('Month')['AMOUNT'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()

fig1 = px.line(monthly_sales, x='Month', y='AMOUNT', title="Monthly Sales Trend")
st.plotly_chart(fig1, use_container_width=True)

# Top 5 Cities / Brands
st.subheader("Top 5 Cities & Brands")
fig2 = bar_top(df, 'CITY', 'AMOUNT', "Top 5 Cities by Sales")
fig3 = bar_top(df, 'BRAND', 'AMOUNT', "Top 5 Brands by Sales")
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# Heatmap: Day vs Month
st.subheader("Sales Heatmap")
heatmap_data = df.groupby([df['ORDER_DATE'].dt.day, df['ORDER_DATE'].dt.month])['AMOUNT'].sum().reset_index()
heatmap_data.rename(columns={'ORDER_DATE': 'Day', 'ORDER_DATE': 'Month', 'AMOUNT': 'Sales'}, inplace=True)
heatmap_data_pivot = heatmap_data.pivot(index='day', columns='month', values='AMOUNT')
st.write("Heatmap coming soon – can implement with plotly heatmap or seaborn if needed.")

# -----------------------------
# 2️⃣ Future Forecast (Next 12 Months)
# -----------------------------
st.header("🔮 Future Forecasting")
model_option = st.selectbox("Select Forecasting Model", ["Prophet", "Random Forest"])

# Aggregate monthly sales
monthly_sales.rename(columns={'AMOUNT': 'y', 'Month': 'ds'}, inplace=True)

if model_option == "Prophet":
    st.subheader("Prophet Forecast")
    model = Prophet()
    model.fit(monthly_sales)
    future = model.make_future_dataframe(periods=12, freq='M')
    forecast = model.predict(future)
    fig_forecast = px.line(forecast, x='ds', y='yhat', title="Prophet Forecast for Next 12 Months")
    fig_forecast.add_scatter(x=monthly_sales['ds'], y=monthly_sales['y'], mode='lines', name='Actual')
    st.plotly_chart(fig_forecast, use_container_width=True)
    next_12 = forecast.tail(12)
elif model_option == "Random Forest":
    st.subheader("Random Forest Forecast")
    rf_df = monthly_sales.copy()
    rf_df['month'] = rf_df['ds'].dt.month
    rf_df['year'] = rf_df['ds'].dt.year
    X = rf_df[['year', 'month']]
    y = rf_df['y']

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    future_dates = pd.date_range(start=rf_df['ds'].max() + pd.Timedelta(days=1), periods=12, freq='M')
    future_df = pd.DataFrame({'ds': future_dates})
    future_df['month'] = future_df['ds'].dt.month
    future_df['year'] = future_df['ds'].dt.year
    future_df['yhat'] = rf_model.predict(future_df[['year', 'month']])
    fig_forecast = px.line(future_df, x='ds', y='yhat', title="Random Forest Forecast for Next 12 Months")
    fig_forecast.add_scatter(x=monthly_sales['ds'], y=monthly_sales['y'], mode='lines', name='Actual')
    st.plotly_chart(fig_forecast, use_container_width=True)
    next_12 = future_df

# Display predicted KPIs
st.subheader("Predicted KPIs for Next 12 Months")
st.metric("Predicted Total Sales", f"{next_12['yhat'].sum():,.0f}")
st.metric("Predicted Avg Monthly Sales", f"{next_12['yhat'].mean():,.0f}")

# Download forecast
st.download_button(
    "⬇️ Download Forecast CSV",
    data=next_12[['ds', 'yhat']].to_csv(index=False),
    file_name="forecast_next_12_months.csv",
    mime="text/csv"
)
