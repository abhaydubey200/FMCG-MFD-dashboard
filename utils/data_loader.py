import pandas as pd
import streamlit as st

def load_dataset(file):
    """
    Load CSV or Excel file into a Pandas DataFrame and store in session state.
    """
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine="openpyxl")

        st.session_state["df"] = df
        return df

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None


def detect_columns(df, dtype="datetime"):
    """
    Detect columns of a certain type in the DataFrame.
    dtype: 'datetime', 'numeric', 'categorical'
    """
    if dtype == "datetime":
        datetime_cols = df.select_dtypes(include=["datetime", "object"]).columns.tolist()
        # filter only columns that can be converted to datetime
        datetime_cols = [col for col in datetime_cols if pd.api.types.is_datetime64_any_dtype(pd.to_datetime(df[col], errors="coerce"))]
        return datetime_cols

    elif dtype == "numeric":
        return df.select_dtypes(include=["number"]).columns.tolist()

    elif dtype == "categorical":
        return df.select_dtypes(include=["object", "category"]).columns.tolist()

    else:
        return df.columns.tolist()
