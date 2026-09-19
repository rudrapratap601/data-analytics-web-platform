"""
Dataset Upload Page Module

Handles CSV and Excel file uploads to PostgreSQL cloud storage.

Key Features:
    - File upload widget (CSV, XLSX)
    - Table name input and sanitization
    - Automatic column name cleaning
    - Chunked upload for large files
    - Dataset preview after upload

Safety Measures:
    - Sanitizes table names (removes special characters)
    - Cleans column names (lowercase, underscores)
    - Validates non-empty files
    - Handles encoding and file format errors
"""

import re

import streamlit as st
import pandas as pd

from backend.db import get_engine


# =========================================
# Safe Table Name
# =========================================
def safe_table_name(name):
    """
    Sanitize a user-provided table name for safe database storage.

    Removes special characters, converts to lowercase, and replaces
    spaces with underscores to create a valid PostgreSQL table identifier.

    Args:
        name (str): Raw table name from user input

    Returns:
        str: Sanitized table name safe for PostgreSQL

    Example:
        >>> safe_table_name("Monthly Sales 2024!")
        'monthlysales2024'
    """

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
    """
    Clean all column names in a DataFrame for safe database storage.

    Converts column names to lowercase, replaces spaces with underscores,
    and removes special characters to prevent SQL errors.

    Args:
        df (pd.DataFrame): DataFrame with potentially unsafe column names

    Returns:
        pd.DataFrame: Same DataFrame with sanitized column names

    Note:
        Modifies column names in place.
    """

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
    """
    Render the dataset upload page.

    User Flow:
        1. Upload CSV or Excel file via file_uploader
        2. Enter a name for the dataset
        3. Click "Upload Dataset" button
        4. File is processed, cleaned, and uploaded to PostgreSQL
        5. Preview of uploaded data is displayed

    Handles:
        - CSV and XLSX file formats
        - UTF-8 encoding for CSV
        - Chunked uploads (10,000 rows per batch)
        - Table name validation
        - Column name sanitization
    """

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
        "Enter Dataset Name"
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
                use_container_width=True,
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