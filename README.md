---

# 📊 FMCG / MFD Analytics Dashboard (Production-Grade)

A **company-level, production-ready FMCG / MFD analytics dashboard** built using **Python, Streamlit, Pandas, and Plotly**.

This application automatically adapts to **any FMCG/MFD dataset**, detects columns intelligently, and provides **CXO to Operations-level insights** through multiple interactive dashboards.

---

## 🚀 Key Highlights

* ✅ Upload dataset **once**, use across **all dashboards**
* ✅ Works with **any FMCG / MFD data structure**
* ✅ No API key required (fully offline analytics)
* ✅ Automatic column detection
* ✅ Modular, scalable, production-ready architecture
* ✅ Streamlit Cloud deployable
* ✅ Enterprise-style dashboard segmentation

---

## 🧠 Dashboard-Wise Breakdown

### 1️⃣ Executive Overview (CXO Dashboard)

**Audience:** CEO, Business Head
**Focus:** Overall business health

**KPIs**

* Total Sales
* Total Orders
* Active Outlets
* Average Order Value
* Total Quantity
* Top State / City

**Visuals**

* KPI cards
* Sales trend line
* Top regions bar chart
* Brand contribution

---

### 2️⃣ Sales Performance Dashboard

**Audience:** Sales Head, Regional Managers

**KPIs**

* Sales by State / City
* Orders Count
* Month-on-Month Sales
* Order Source

**Visuals**

* Monthly trend charts
* Regional performance bars
* Drill-down tables

---

### 3️⃣ Product / SKU / Brand Dashboard

**Audience:** Category & Marketing Teams

**KPIs**

* Top & Bottom SKUs
* Brand Contribution %
* Category-wise Sales
* Average Selling Price

**Visuals**

* Top SKUs bar chart
* Brand share pie
* Category distribution

---

### 4️⃣ Outlet & Distribution Dashboard

**Audience:** Distribution Managers

**KPIs**

* Active vs Inactive Outlets
* Outlet Coverage
* Verified vs Non-Verified Outlets

**Visuals**

* Outlet distribution charts
* Coverage analysis

---

### 5️⃣ Field Force Productivity Dashboard

**Audience:** ASM, RSM, Sales Ops

**KPIs**

* Sales per Sales Rep
* Orders per Rep
* Average Time at Outlet
* Performance ranking

**Visuals**

* Rep ranking tables
* Productivity charts

---

### 6️⃣ Order & Operations Dashboard

**Audience:** Operations / Supply Chain

**KPIs**

* Order Acceptance Rate
* Rejected Orders %
* Order Status Distribution
* Order Type Performance

**Visuals**

* Order state pie chart
* Funnel-style summaries
* Rejection analysis

---

### 7️⃣ Sales Forecasting Dashboard

**Audience:** Sales & Strategy Teams

**Features**

* Time-series aggregation
* Trend-based forecasting
* Historical vs forecast comparison

**Visuals**

* Forecast line charts
* Monthly aggregation

---

### 8️⃣ Outlet Segmentation Dashboard

**Audience:** Strategy & Distribution Teams

**Features**

* Outlet segmentation using clustering
* High / Medium / Low value outlets
* Data-driven grouping

---

## 🗂️ Project Structure

```
fmcg-mfd-dashboard/
│
├── app.py
├── config.py
├── requirements.txt
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
│
├── utils/
│   ├── column_detector.py
│   ├── data_loader.py
│   ├── data_processing.py
│   ├── metrics.py
│   ├── visualizations.py
│   ├── forecasting.py
│   ├── segmentation.py
│   └── churn_analysis.py
```

---

## 🧪 Supported Data

The app **automatically detects columns**, but works best with datasets containing fields like:

* Order Date
* Order ID
* Outlet / Customer
* SKU / Brand / Category
* Quantity
* Amount / Sales Value
* Region / City / State
* Salesperson / User

👉 Exact column names **are NOT mandatory**

---

## ⚙️ Installation & Run

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/fmcg-mfd-dashboard.git
cd fmcg-mfd-dashboard
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run App

```bash
streamlit run app.py
```

---

## ☁️ Deployment (Streamlit Cloud)

* Main file: `app.py`
* Python version: **3.9+**
* No secrets / API keys required

---

## 🎯 Use Cases

* FMCG Companies
* MFD / Distribution Businesses
* Sales Analytics Teams
* CXO Dashboards
* Interview / Portfolio Project
* Startup MVP Analytics

---

## 🔮 Future Enhancements (Optional)

* Role-based access (CXO / Sales / Ops)
* PDF / Excel export
* Alert-based KPIs
* AI-powered insights (optional toggle)
* Data validation rules engine

---

## 🏆 Why This Project Stands Out

✔ Enterprise dashboard design
✔ No hardcoded schema
✔ Modular & scalable
✔ Real-world FMCG use case
✔ Interview & production ready

---

## 👤 Author

**Abhay Dubey**
Full Stack / Data Analytics Developer
Focused on **real-world, production-grade systems**

---
