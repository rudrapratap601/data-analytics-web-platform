import streamlit as st
import pandas as pd

from sqlalchemy.types import (
    Integer,
    Float,
    Text,
    DateTime
)

from backend.db import get_engine
from backend.schema import (
    get_tables,
    get_columns
)

from backend.data_loader import load_data


# =========================================
# Clean Column Names
# =========================================
def clean_column_name(column_name):

    cleaned = (
        column_name
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("%", "percent")
    )

    return cleaned


# =========================================
# Convert Datatype
# =========================================
def convert_column_type(
    df,
    column,
    target_type
):

    try:

        # =====================================
        # INTEGER
        # =====================================
        if target_type == "INT":

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).astype("Int64")

        # =====================================
        # FLOAT
        # =====================================
        elif target_type == "FLOAT":

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).astype("float64")

        # =====================================
        # TEXT
        # =====================================
        elif target_type == "TEXT":

            df[column] = df[column].astype(
                str
            )

        # =====================================
        # DATE
        # =====================================
        elif target_type == "DATE":

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    except Exception as e:

        st.warning(
            f"Could not convert {column}: {e}"
        )

    return df


# =========================================
# MAIN PAGE
# =========================================
def show():

    st.title("🧹 Dataset Cleaner")

    st.markdown("""
    Clean and standardize datasets before analysis.

    Features:
    - Fix column names
    - Convert datatypes
    - Preview cleaned data
    - Save cleaned datasets
    """)

    st.markdown("---")

    # =========================================
    # Load Tables
    # =========================================
    with st.spinner(
        "Loading datasets..."
    ):

        tables = get_tables()

    if not tables:

        st.warning(
            "No datasets available."
        )

        return

    # =========================================
    # Select Dataset
    # =========================================
    st.subheader(
        "Step 1: Select Dataset"
    )

    options = [
        "🔽 Select a table"
    ] + tables

    selected_table = st.selectbox(
        "Choose Dataset",
        options
    )

    # =========================================
    # Validation
    # =========================================
    if selected_table == "🔽 Select a table":

        st.info(
            "Please select a dataset to continue."
        )

        return

    st.markdown("---")

    # =========================================
    # Preview Rows
    # =========================================
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

    # =========================================
    # Load FULL Dataset
    # =========================================
    with st.spinner(
        "Loading full dataset..."
    ):

        query = f'''
        SELECT *
        FROM "{selected_table}"
        '''

        try:

            df = load_data(query)

        except Exception as e:

            st.error(
                f"Failed to load dataset: {e}"
            )

            return

    # =========================================
    # Empty Dataset Check
    # =========================================
    if df.empty:

        st.warning(
            "Dataset is empty."
        )

        return

    # =========================================
    # Preview Data
    # =========================================
    preview_df = df.head(
        preview_limit
    )

    # =========================================
    # Original Preview
    # =========================================
    st.subheader(
        "📌 Original Dataset Preview"
    )

    st.caption(
        f"""
        Showing first
        {len(preview_df):,} rows
        out of
        {len(df):,} total rows
        """
    )

    st.dataframe(
        preview_df,
        use_container_width=True
    )

    st.write(
        f"""
        Total Rows: {df.shape[0]:,}
        | Columns: {df.shape[1]}
        """
    )

    st.markdown("---")

    # =========================================
    # Column Cleaning
    # =========================================
    st.subheader(
        "Step 2: Clean Column Names"
    )

    cleaned_columns = {}

    for col in df.columns:

        cleaned_name = clean_column_name(
            col
        )

        new_name = st.text_input(
            f"{col}",
            value=cleaned_name,
            key=f"rename_{col}"
        )

        cleaned_columns[col] = new_name

    # =========================================
    # Rename Columns
    # =========================================
    df = df.rename(
        columns=cleaned_columns
    )

    st.markdown("---")

    # =========================================
    # Datatype Conversion
    # =========================================
    st.subheader(
        "Step 3: Fix Datatypes"
    )

    datatype_choices = {}

    for col in df.columns:

        current_type = str(
            df[col].dtype
        )

        selected_type = st.selectbox(
            f"{col} ({current_type})",
            [
                "Keep Current",
                "INT",
                "FLOAT",
                "TEXT",
                "DATE"
            ],
            key=f"type_{col}"
        )

        datatype_choices[col] = (
            selected_type
        )

    # =========================================
    # Apply Datatype Changes
    # =========================================
    with st.spinner(
        "Applying datatype conversions..."
    ):

        for col, dtype in datatype_choices.items():

            if dtype != "Keep Current":

                df = convert_column_type(
                    df,
                    col,
                    dtype
                )

    st.markdown("---")

    # =========================================
    # Cleaned Preview
    # =========================================
    st.subheader(
        "📊 Cleaned Dataset Preview"
    )

    cleaned_preview = df.head(
        preview_limit
    )

    st.dataframe(
        cleaned_preview,
        use_container_width=True
    )

    # =========================================
    # Updated Datatypes
    # =========================================
    st.markdown(
        "### Updated Datatypes"
    )

    dtype_df = pd.DataFrame({

        "Column": df.columns,

        "Datatype": [
            str(dtype)
            for dtype in df.dtypes
        ]
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )

    st.markdown("---")

    # =========================================
    # Save Options
    # =========================================
    st.subheader(
        "Step 4: Save Cleaned Dataset"
    )

    save_mode = st.radio(

        "Save Option",

        [
            "Replace Original Dataset",
            "Save as New Dataset"
        ]
    )

    # =========================================
    # Default Table Name
    # =========================================
    final_table_name = selected_table

    # =========================================
    # New Dataset Name
    # =========================================
    if save_mode == "Save as New Dataset":

        cleaned_table_name = st.text_input(

            "New Cleaned Dataset Name",

            value=f"{selected_table}_cleaned"
        )

        final_table_name = (
            cleaned_table_name
            .strip()
            .replace(" ", "_")
            .lower()
        )

    st.markdown("---")

    # =========================================
    # Save Dataset
    # =========================================
    engine = get_engine()

    if st.button(
        "Save Cleaned Dataset"
    ):

        try:

            with st.spinner(
                "Saving cleaned dataset..."
            ):

                # =================================
                # SQL Datatype Mapping
                # =================================
                sql_dtypes = {}

                for col in df.columns:

                    dtype = str(
                        df[col].dtype
                    ).lower()

                    if "int" in dtype:

                        sql_dtypes[col] = Integer()

                    elif "float" in dtype:

                        sql_dtypes[col] = Float()

                    elif "datetime" in dtype:

                        sql_dtypes[col] = DateTime()

                    else:

                        sql_dtypes[col] = Text()

                # =================================
                # Save Dataset
                # =================================
                df.to_sql(

                    final_table_name,

                    con=engine,

                    if_exists="replace",

                    index=False,

                    method="multi",

                    chunksize=5000,

                    dtype=sql_dtypes
                )

                # =================================
                # Clear Cache
                # =================================
                st.cache_data.clear()
                st.cache_resource.clear()
            # =====================================
            # Success Messages
            # =====================================
            st.success(
                f"""
                Dataset saved successfully
                as '{final_table_name}'
                """
            )

            if (
                save_mode
                ==
                "Replace Original Dataset"
            ):

                st.info(
                    "Original dataset was replaced."
                )

            else:

                st.info(
                    "New cleaned dataset created successfully."
                )

            # =====================================
            # Rerun App
            # =====================================
            st.rerun()

        except Exception as e:

            st.error(
                f"Failed to save dataset: {e}"
            )