import streamlit as st
import pandas as pd
from utils.data_loader import load_dataset
from utils.visualizations import line_sales_trend, bar_top, heatmap, kpi_card

st.set_page_config(page_title="Actionable Insights", layout="wide")

st.title("📈 Actionable Insights Dashboard")

# ---------------- Upload Dataset ----------------
uploaded_file = st.file_uploader("Upload your FMCG dataset (CSV / Excel)", type=["csv", "xlsx"])
if uploaded_file:
    df = load_dataset(uploaded_file)
    
    if df is not None:
        st.success("Dataset loaded successfully!")

        # ---------------- Detect essential columns ----------------
        date_col = "ORDER_DATE" if "ORDER_DATE" in df.columns else None
        qty_col = "TOTAL_QUANTITY" if "TOTAL_QUANTITY" in df.columns else None
        amount_col = "AMOUNT" if "AMOUNT" in df.columns else None

        if not date_col or not qty_col or not amount_col:
            st.error("Dataset must contain ORDER_DATE, TOTAL_QUANTITY, and AMOUNT columns.")
        else:
            # ---------------- KPI Cards ----------------
            total_sales = df[amount_col].sum()
            total_qty = df[qty_col].sum()
            avg_order_value = df[amount_col].mean()
            active_outlets = df["OUTLET_ID"].nunique() if "OUTLET_ID" in df.columns else 0

            kpis = [
                kpi_card(total_sales, "Total Sales", "green"),
                kpi_card(total_qty, "Total Quantity", "green"),
                kpi_card(avg_order_value, "Avg Order Value", "orange"),
                kpi_card(active_outlets, "Active Outlets", "green")
            ]

            kpi_cols = st.columns(len(kpis))
            for idx, kpi in enumerate(kpis):
                with kpi_cols[idx]:
                    st.metric(label=kpi["name"], value=kpi["value"])

            st.markdown("---")

            # ---------------- Line Chart: Sales Trend ----------------
            st.subheader("Sales Trend Over Time")
            st.plotly_chart(line_sales_trend(df, date_col, amount_col), use_container_width=True)

            # ---------------- Bar Charts: Top 5 ----------------
            st.subheader("Top 5 Brands / Cities / Warehouses")
            if "BRAND" in df.columns:
                st.plotly_chart(bar_top(df, "BRAND", amount_col, title="Top 5 Brands by Sales"), use_container_width=True)
            if "CITY" in df.columns:
                st.plotly_chart(bar_top(df, "CITY", amount_col, title="Top 5 Cities by Sales"), use_container_width=True)
            if "WAREHOUSE" in df.columns:
                st.plotly_chart(bar_top(df, "WAREHOUSE", amount_col, title="Top 5 Warehouses by Sales"), use_container_width=True)

            # ---------------- Heatmap ----------------
            st.subheader("Sales Heatmap (Day vs Month)")
            df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")
            df["Day"] = df["ORDER_DATE"].dt.day
            df["Month"] = df["ORDER_DATE"].dt.month
            st.plotly_chart(heatmap(df, x_col="Month", y_col="Day", value_col=amount_col, title="Sales Heatmap"), use_container_width=True)

else:
    st.info("Please upload a dataset to view insights.")
