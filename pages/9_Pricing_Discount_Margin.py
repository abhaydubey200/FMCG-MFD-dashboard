import streamlit as st
import plotly.express as px
from utils.column_detector import auto_detect_columns
from utils.pricing_metrics import calculate_pricing_metrics, sku_level_pricing

st.header("Pricing, Discount & Margin Analysis")

df = st.session_state.get("df")
if df is None:
    st.warning("Upload dataset first")
    st.stop()

cols = auto_detect_columns(df)

required = [cols["price"], cols["quantity"], cols["discount"], cols["sku"]]
if any(v is None for v in required):
    st.error("Required pricing columns not detected")
    st.stop()

df_price = calculate_pricing_metrics(
    df,
    price_col=cols["price"],
    qty_col=cols["quantity"],
    discount_col=cols["discount"]
)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Gross Sales", f"₹{df_price['Gross_Sales'].sum():,.0f}")
c2.metric("Net Sales", f"₹{df_price['Net_Sales'].sum():,.0f}")
c3.metric("Total Discount", f"₹{df_price[cols['discount']].sum():,.0f}")
c4.metric("Avg Discount %", f"{df_price['Discount_Percent'].mean():.2f}%")

# SKU Pricing Table
sku_pricing = sku_level_pricing(df_price, cols["sku"])

st.subheader("SKU Level Discount Leakage")
st.dataframe(
    sku_pricing.sort_values("Discount_Amount", ascending=False)
)

# Discount vs Sales
fig = px.scatter(
    df_price,
    x="Discount_Percent",
    y="Net_Sales",
    color=cols["sku"],
    title="Discount vs Net Sales (Price Sensitivity)",
)

st.plotly_chart(fig, use_container_width=True)
