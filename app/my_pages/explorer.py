import pandas as pd
import streamlit as st

from backend.db import get_engine
from backend.schema import (
    get_tables,
    get_columns
)


# =========================================
# MAIN PAGE
# =========================================
def show():

    # =====================================
    # Page Header
    # =====================================
    st.title("🔍 Data Explorer")

    st.markdown("""
    Explore the datasets you've uploaded.

    Features:
    - Preview datasets
    - View columns and datatypes
    - Inspect dataset structure
    - Explore uploaded tables
    """)

    st.markdown("---")

    # =====================================
    # Load Tables
    # =====================================
    tables = get_tables()

    if not tables:

        st.warning(
            """
            No datasets found.
            Please upload a dataset first.
            """
        )

        return

    # =====================================
    # Select Dataset
    # =====================================
    st.subheader("Step 1: Select Dataset")

    options = [
        "🔽 Select a table"
    ] + tables

    selected_table = st.selectbox(
        "Select Table",
        options
    )

    # =====================================
    # Validation
    # =====================================
    if selected_table == "🔽 Select a table":

        st.info(
            "Please select a table to explore."
        )

        return

    st.markdown("---")

    # =====================================
    # Preview Limit
    # =====================================
    preview_limit = st.selectbox(
        "Rows to Preview",
        [
            100,
            1000,
            5000
        ],
        index=1
    )

    st.markdown("---")

    # =====================================
    # Database Engine
    # =====================================
    engine = get_engine()

    # =====================================
    # Load Dataset Information
    # =====================================
    with st.spinner("Loading dataset information..."):

        # =================================
        # Load Columns
        # =================================
        try:

            columns = get_columns(
                selected_table
            )

        except Exception as e:

            st.error(
                f"Failed to load columns: {e}"
            )

            return

        # =================================
        # Extract Column Information
        # =================================
        column_names = [
            col[0]
            for col in columns
        ]

        column_types = [
            col[1]
            for col in columns
        ]

        # =================================
        # Dataset Information
        # =================================
        st.subheader(
            f"📂 Dataset: {selected_table}"
        )

        st.write("### Columns & Datatypes")

        info_df = pd.DataFrame({

            "Column Name": column_names,

            "Datatype": [
                str(dtype)
                for dtype in column_types
            ]
        })

        st.dataframe(
            info_df,
            use_container_width=True
        )

        st.markdown("---")

        # =================================
        # Total Row Count
        # =================================
        count_query = f'''
        SELECT COUNT(*)
        FROM "{selected_table}"
        '''

        try:

            total_rows = pd.read_sql(
                count_query,
                con=engine
            ).iloc[0, 0]

        except Exception as e:

            st.error(
                f"Failed to count rows: {e}"
            )

            return

        # =================================
        # Empty Dataset Check
        # =================================
        if total_rows == 0:

            st.warning(
                "Dataset is empty."
            )

            return

        # =================================
        # Preview Query
        # =================================
        preview_query = f'''
        SELECT *
        FROM "{selected_table}"
        LIMIT {preview_limit}
        '''

        # =================================
        # Load Preview Data
        # =================================
        try:

            df = pd.read_sql(
                preview_query,
                con=engine
            )

        except Exception as e:

            st.error(
                f"Failed to load dataset: {e}"
            )

            return

    # =====================================
    # Data Preview
    # =====================================
    st.subheader("📌 Data Preview")

    st.caption(
        f"""
        Showing first
        {len(df):,} rows
        out of
        {total_rows:,} total rows
        """
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================
    # Calculate Accurate Missing Values
    # Using SQL
    # =====================================
    with st.spinner("Calculating dataset statistics..."):

        missing_data = []

        total_missing_values = 0

        for col in column_names:

            try:

                query = f'''
                SELECT
                    COUNT(*) AS total_rows,
                    COUNT("{col}") AS non_null_rows
                FROM "{selected_table}"
                '''

                result = pd.read_sql(
                    query,
                    con=engine
                )

                total = int(
                    result.iloc[0]["total_rows"]
                )

                non_null = int(
                    result.iloc[0]["non_null_rows"]
                )

                missing = total - non_null

                missing_percent = round(
                    (
                        missing
                        /
                        total
                    ) * 100,
                    2
                )

                total_missing_values += missing

                missing_data.append({

                    "Column": col,

                    "Missing Values": missing,

                    "Missing %": missing_percent
                })

            except Exception:

                missing_data.append({

                    "Column": col,

                    "Missing Values": "Error",

                    "Missing %": "Error"
                })

    # =====================================
    # Dataset Summary
    # =====================================
    st.subheader("📊 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Rows",
            f"{total_rows:,}"
        )

    with col2:

        st.metric(
            "Columns",
            len(column_names)
        )

    with col3:

        st.metric(
            "Total Missing Values",
            f"{total_missing_values:,}"
        )

    st.markdown("---")

    # =====================================
    # Missing Values Report
    # =====================================
    st.subheader(
        "⚠️ Missing Values Report"
    )

    st.caption(
        """
        Missing value statistics are
        calculated using the full dataset.
        """
    )

    missing_df = pd.DataFrame(
        missing_data
    )

    st.dataframe(
        missing_df,
        use_container_width=True
    )