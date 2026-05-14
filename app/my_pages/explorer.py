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
    # Load Columns
    # =====================================
    with st.spinner("Loading Dataset information..."):
        try:

            columns = get_columns(
                selected_table
            )

        except Exception as e:

            st.error(
                f"Failed to load columns: {e}"
            )

            return

        column_names = [
            col[0]
            for col in columns
        ]

        column_types = [
            col[1]
            for col in columns
        ]

        # =====================================
        # Dataset Information
        # =====================================
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

        # =====================================
        # Database Engine
        # =====================================
        engine = get_engine()

        # =====================================
        # PostgreSQL Query
        # =====================================
        query = f'''
        SELECT *
        FROM "{selected_table}"
        '''

        # =====================================
        # Load Dataset
        # =====================================
        try:

            df = pd.read_sql(
                query,
                con=engine
            )

        except Exception as e:

            st.error(
                f"Failed to load dataset: {e}"
            )

            return

        # =====================================
        # Empty Dataset Check
        # =====================================
        if df.empty:

            st.warning(
                "Dataset is empty."
            )

            return

        # =====================================
        # Data Preview
        # =====================================
        st.subheader("📌 Data Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")

        # =====================================
        # Dataset Summary
        # =====================================
        st.subheader("📊 Dataset Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Rows",
                df.shape[0]
            )

        with col2:

            st.metric(
                "Columns",
                df.shape[1]
            )

        with col3:

            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        st.markdown("---")

        # =====================================
        # Missing Values Report
        # =====================================
        st.subheader(
            "⚠️ Missing Values Report"
        )

        missing_df = pd.DataFrame({

            "Column": df.columns,

            "Missing Values": [
                int(df[col].isnull().sum())
                for col in df.columns
            ],

            "Missing %": [
                round(
                    (
                        df[col].isnull().sum()
                        /
                        len(df)
                    ) * 100,
                    2
                )
                for col in df.columns
            ]
        })

        st.dataframe(
            missing_df,
            use_container_width=True
        )