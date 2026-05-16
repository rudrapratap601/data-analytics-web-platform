import re

import streamlit as st
import pandas as pd

from backend.db import get_engine


# =========================================
# Safe Table Name
# =========================================
def safe_table_name(name):

    return re.sub(
        r"[^a-zA-Z0-9_]",
        "",
        name.strip()
        .lower()
        .replace(" ", "_")
    )


# =========================================
# Safe Column Names
# Infrastructure Only
# =========================================
def safe_column_names(df):

    df.columns = [

        re.sub(
            r"[^a-zA-Z0-9_]",
            "",
            str(col)
            .strip()
            .replace(" ", "_")
        ).lower()

        for col in df.columns
    ]

    return df


# =========================================
# MAIN PAGE
# =========================================
def show():

    st.title("📤 Upload Dataset")

    st.markdown("""
    Upload datasets into cloud storage.
    
     Supported formats:
    - CSV
    - XLSX (Excel)
    """)

    st.markdown("---")

    # =====================================
    # Upload File
    # =====================================
    uploaded_file = st.file_uploader(

        "Upload CSV or Excel File",

        type=["csv", "xlsx"]
    )

    if not uploaded_file:

        return

    st.markdown("---")

    # =====================================
    # Dataset Name
    # =====================================
    table_name = st.text_input(
        "Dataset Name"
    )

    st.markdown("---")

    # =====================================
    # Upload
    # =====================================
    if st.button("Upload Dataset"):

        if not table_name.strip():

            st.error(
                "Please enter dataset name."
            )

            return

        try:

            # =============================
            # Read File
            # =============================
            if uploaded_file.name.endswith(".csv"):

                df = pd.read_csv(
                    uploaded_file,
                    low_memory=False,
                    encoding="utf-8"
                )

            elif uploaded_file.name.endswith(".xlsx"):

                df = pd.read_excel(
                    uploaded_file,
                    engine="openpyxl"
                )

            else:

                st.error(
                    "Unsupported file format."
                )

                return

            # =============================
            # Validation
            # =============================
            if df.empty:

                st.error(
                    "CSV file is empty."
                )

                return

            # =============================
            # Infrastructure Safety
            # =============================
            table_name_clean = safe_table_name(
                table_name
            )

            df = safe_column_names(df)

            # =============================
            # Database Engine
            # =============================
            engine = get_engine()

            # =============================
            # Upload
            # =============================
            with st.spinner("Uploading dataset..."):

                df.to_sql(
                    table_name_clean,
                    con=engine,
                    if_exists="replace",
                    index=False,
                    method="multi",
                    chunksize=10000
                    
                )
            # =============================
            # Success
            # =============================
            st.success(
                f"""
                Dataset '{table_name_clean}'
                uploaded successfully.
                """
            )

            st.cache_data.clear()

            st.markdown("---")

            st.subheader(
                "📌 Dataset Preview"
            )

            st.dataframe(
                df.head(),
                width="stretch",
            )

            st.write(
                f"""
                Rows: {df.shape[0]}
                | Columns: {df.shape[1]}
                """
            )

        except Exception as e:

            st.error(
                f"Upload failed: {e}"
            )