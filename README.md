Below is a **complete, production-ready GitHub README** for your project, written professionally for recruiters, managers, and real FMCG stakeholders.

You can **copy-paste this directly into `README.md`**.

---

# 📊 FMCG MFD Sales Intelligence Dashboard

A **production-grade, multi-dashboard analytics platform** built using **Streamlit + Python**, designed for **FMCG / Distribution / Retail businesses** to analyze **sales, orders, outlets, SKUs, field force performance, and future demand** — all from **any FMCG dataset**.

---

## 🚀 Project Overview

This project transforms raw FMCG order data into **actionable business intelligence dashboards** used by:

* CXOs & Business Heads
* Sales & Regional Managers
* Category & Brand Managers
* Operations & Supply Chain Teams
* Strategy & Planning Teams

The system is **dataset-agnostic**, meaning you can upload **any FMCG CSV or Excel file** and the dashboards will adapt automatically.

---

## 🎯 Key Features

✅ One-time dataset upload (shared across all pages)
✅ Automatic column detection & validation
✅ Production-safe error handling
✅ Business-ready KPIs & insights
✅ Forecasting without API keys
✅ Scalable, modular architecture

---

## 🧱 Dashboard Architecture (Pages)

### 0️⃣ Upload Dataset

**Single common uploader for entire app**

* Supports CSV / Excel
* Cleans & stores dataset in session
* Prevents repeated uploads

---

### 1️⃣ Executive Overview Dashboard (CXO View)

**Focus: How is the business doing overall?**

**KPIs**

* Total Sales
* Total Orders
* Active Outlets
* Average Order Value
* Sales Growth %

**Visuals**

* KPI cards
* Sales trend
* Top brands / states
* Contribution analysis

---

### 2️⃣ Sales Performance Dashboard

**Audience: Sales Head, Regional Managers**

**Analysis**

* Sales by State / City / Area
* Order volume trends
* MoM growth
* Order source distribution

---

### 3️⃣ Product / SKU / Brand Dashboard

**Audience: Category & Marketing Teams**

**Insights**

* Top & bottom SKUs
* Brand contribution %
* Category-wise sales
* Avg selling price

---

### 4️⃣ Outlet & Distribution Dashboard

**Audience: Distribution Managers**

**Metrics**

* Active vs inactive outlets
* Outlet category sales
* Verified vs non-verified contribution
* Coverage insights

---

### 5️⃣ Field Force Productivity Dashboard

**Audience: ASM / RSM / Sales Ops**

**KPIs**

* Sales per sales rep
* Orders per rep
* Time spent at outlets
* Manager-wise performance

---

### 6️⃣ Order & Operations Dashboard

**Audience: Operations / Supply Chain**

**Analysis**

* Order state funnel
* Accepted vs rejected orders
* Order type performance
* Time-of-day analysis

---

### 7️⃣ Sales Forecasting Dashboard

**Future planning without external APIs**

* Monthly sales forecasting
* Random Forest based model
* Trend visualization
* Business-ready forecast table

---

### 8️⃣ Outlet Segmentation Dashboard

**Data-driven outlet strategy**

* Outlet clustering
* High / medium / low value segmentation
* Targeted distribution planning

---

### 9️⃣ Daily Sales Analysis

**Granular time intelligence**

* Daily sales trends
* Day-wise contribution
* Peak & low sales days
* Operational planning support

---

### 🔟 Actionable Insights Dashboard

**Advanced decision-making layer**

Includes:

* 📈 KPI cards with traffic-light logic
* 🔥 Sales heatmaps (Day × Month)
* 📊 Growth trends (WoW / MoM)
* 🔮 Forecast overlay (Actual vs Predicted)

---

### 🔮 12️⃣ Future Sales Prediction (Next 12 Months)

**Strategic forecasting for planning & budgeting**

* Random Forest forecasting model
* Next 12 months prediction
* Peak demand identification
* Inventory & revenue planning support

---

## 🗂️ Folder Structure

```
fmcg-mfd-dashboard/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 0_Upload_Dataset.py
│   ├── 1_Executive_Overview.py
│   ├── 2_Sales_Performance.py
│   ├── 3_Product_SKU_Brand.py
│   ├── 4_Outlet_Distribution.py
│   ├── 5_Field_Force_Productivity.py
│   ├── 6_Order_Operations.py
│   ├── 7_Sales_Forecasting.py
│   ├── 8_Outlet_Segmentation.py
│   ├── 9_Daily_Sales_Analysis.py
│   ├── 11_Actionable_Insights.py
│   └── 12_Future_Sales_Prediction.py
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── column_detector.py
│   ├── data_processing.py
│   ├── metrics.py
│   ├── visualizations.py
│   ├── forecasting.py
│   ├── segmentation.py
│   ├── warehouse_metrics.py
│   ├── pricing_metrics.py
│   └── churn_analysis.py
```

---

## 🧪 Supported Data Columns (Example)

This project works with datasets similar to:

* ORDER_DATE, ORDER_ID, ORDERSTATE
* CITY, STATE, WAREHOUSE
* SKU_ID, BRAND, CATEGORY
* TOTAL_QUANTITY, AMOUNT
* DISCOUNT_AMOUNT, UNITPRICE
* OUTLET_ID, VERIFIED_OUTLET
* USER_ID, EMPLOYEE_ID

👉 Column names are **auto-detected** — strict naming is **not required**.

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **Streamlit**
* **Pandas / NumPy**
* **Plotly**
* **Scikit-learn**
* **Random Forest (Forecasting)**

❌ No API keys required
❌ No external AI dependency

---

## ▶️ How to Run Locally

```bash
# 1. Clone repository
git clone https://github.com/your-username/fmcg-mfd-dashboard.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run app
streamlit run app.py
```

---

## 🧠 Business Value

✔ Improves sales visibility
✔ Enables demand planning
✔ Identifies high-value outlets & SKUs
✔ Supports data-driven decisions
✔ Ready for enterprise deployment

## 👤 Author

**Abhay Dubey**
Data Analytics Engineer

---
