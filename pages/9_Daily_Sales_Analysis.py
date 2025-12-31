import streamlit as st
import pandas as pd

st.set_page_config(page_title="Daily Sales Analysis", layout="wide")
st.title("Daily Sales Analysis")

# ---------------------------
# Load data safely
# ---------------------------
if "data" not in st.session_state or st.session_state["data"] is None:
    st.warning("Please upload data from 'Upload Dataset' page")
    st.stop()

df = st.session_state["data"].copy()

# ---------------------------
# Required columns check
# ---------------------------
required_cols = ["ORDER_DATE", "AMOUNT", "TOTAL_QUANTITY"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f" Missing required columns: {missing}")
    st.stop()

# ---------------------------
# Data preparation
# ---------------------------
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
df = df.dropna(subset=["ORDER_DATE"])

daily_sales = (
    df.groupby(df["ORDER_DATE"].dt.date)
      .agg(
          Total_Sales_Amount=("AMOUNT", "sum"),
          Total_Quantity=("TOTAL_QUANTITY", "sum"),
          Total_Orders=("ORDER_ID", "nunique")
      )
      .reset_index()
)

# ---------------------------
# KPI Section
# ---------------------------
c1, c2, c3 = st.columns(3)
c1.metric(" Total Sales", f"₹{daily_sales['Total_Sales_Amount'].sum():,.0f}")
c2.metric(" Total Quantity", f"{daily_sales['Total_Quantity'].sum():,.0f}")
c3.metric("Total Orders", f"{daily_sales['Total_Orders'].sum():,}")

# ---------------------------
# Charts
# ---------------------------
st.subheader("Daily Sales Trend")
st.line_chart(daily_sales.set_index("ORDER_DATE")["Total_Sales_Amount"])

st.subheader(" Daily Order Volume")
st.bar_chart(daily_sales.set_index("ORDER_DATE")["Total_Orders"])

# ---------------------------
# Data Table
# ---------------------------
st.subheader(" Daily Sales Table")
st.dataframe(daily_sales, use_container_width=True)
