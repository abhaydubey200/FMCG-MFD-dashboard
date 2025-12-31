import streamlit as st
from utils.data_loader import load_dataset

st.set_page_config(page_title="Upload Dataset", layout="wide")
st.header(" Upload FMCG Dataset")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    df = load_dataset(uploaded_file)

    if df is not None and not df.empty:
        # THIS IS THE MOST IMPORTANT LINE
        st.session_state["data"] = df

        st.success(" Dataset loaded successfully")
        st.info(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
        st.dataframe(df.head(), use_container_width=True)
    else:
        st.error(" Dataset is empty or invalid")
