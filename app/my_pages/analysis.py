import streamlit as st
import pandas as pd

from backend.schema import (
    get_tables,
    get_columns
)

from backend.query_builder import (
    build_query
)

from backend.data_loader import (
    load_data
)


# =========================================
# Get Numeric Columns Only
# =========================================
def get_numeric_columns(columns):

    numeric_types = [
        "INT",
        "BIGINT",
        "FLOAT",
        "DOUBLE",
        "DECIMAL",
        "NUMERIC",
        "REAL"
    ]

    numeric_columns = []

    for col_name, col_type in columns:

        col_type = str(col_type).upper()

        if any(
            num_type in col_type
            for num_type in numeric_types
        ):

            numeric_columns.append(
                col_name
            )

    return numeric_columns


# =========================================
# MAIN PAGE
# =========================================
def show():

    st.title(
        "📊 Dynamic Analysis Builder"
    )

    st.markdown("""
    Build dynamic analytics queries using your uploaded datasets.

    You can:
    - analyze single datasets
    - perform multi-table analysis
    - generate aggregations
    - group data dynamically
    """)

    st.markdown("---")

    # =========================================
    # Load Tables
    # =========================================
    with st.spinner(
        "Loading datasets..."
    ):

        tables = get_tables()

    # =========================================
    # Validation
    # =========================================
    if not tables:

        st.warning(
            "No datasets available. Please upload datasets first."
        )

        return

    # =========================================
    # Analysis Type
    # =========================================
    st.subheader(
        "Step 1: Select Analysis Type"
    )

    analysis_type = st.radio(
        "Choose Analysis Mode",
        [
            "Single Table Analysis",
            "Multi Table Analysis"
        ]
    )

    st.markdown("---")

    # =========================================
    # SINGLE TABLE ANALYSIS
    # =========================================
    if analysis_type == "Single Table Analysis":

        st.subheader(
            "Step 2: Select Dataset"
        )

        table_options = [
            "🔽 Select a table"
        ] + tables

        table1 = st.selectbox(
            "Select Table",
            table_options,
            key="single_table"
        )

        # =====================================
        # Validation
        # =====================================
        if table1 == "🔽 Select a table":

            st.info(
                "Please select a dataset to continue."
            )

            return

        st.markdown("---")

        # =====================================
        # Load Columns
        # =====================================
        with st.spinner(
            "Loading columns..."
        ):

            columns = get_columns(
                table1
            )

        column_names = [

            col[0]

            for col in columns
        ]

        numeric_columns = get_numeric_columns(
            columns
        )

        # =====================================
        # Validation
        # =====================================
        if not numeric_columns:

            st.error(
                "No numeric columns found in this dataset."
            )

            return

        # =====================================
        # Configure Analysis
        # =====================================
        st.subheader(
            "Step 3: Configure Analysis"
        )

        metric_column = st.selectbox(
            "Select Metric Column",
            numeric_columns
        )

        aggregation = st.selectbox(
            "Select Aggregation",
            [
                "SUM",
                "AVG",
                "COUNT",
                "MAX",
                "MIN"
            ]
        )

        # =====================================
        # Group By
        # =====================================
        use_groupby = st.checkbox(
            "Use Group By"
        )

        group_by_column = None

        if use_groupby:

            group_by_column = st.selectbox(
                "Group By Column",
                column_names
            )

        st.markdown("---")

        # =====================================
        # Generate Analysis
        # =====================================
        if st.button(
            "Generate Analysis"
        ):

            with st.spinner(
                "Running single table analysis..."
            ):

                try:

                    query = build_query(
                        table1=table1,
                        metric_column=metric_column,
                        aggregation=aggregation,
                        group_by_column=group_by_column
                    )

                    df = load_data(
                        query
                    )

                    # =============================
                    # Save Results
                    # =============================
                    st.session_state[
                        "analysis_generated"
                    ] = True

                    st.session_state[
                        "query"
                    ] = query

                    st.session_state[
                        "df"
                    ] = df

                    st.session_state[
                        "analysis_type"
                    ] = "single"

                    st.success(
                        "Analysis generated successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Analysis Failed: {e}"
                    )

        # =====================================
        # Show Results
        # =====================================
        if (
            st.session_state.get(
                "analysis_generated"
            )
            and
            st.session_state.get(
                "analysis_type"
            ) == "single"
        ):

            st.markdown("---")

            st.subheader(
                "📌 Analysis Result"
            )

            with st.spinner(
                "Loading analysis results..."
            ):

                st.dataframe(
                    st.session_state["df"],
                    use_container_width=True
                )

            st.success(
                f"""
                {st.session_state['df'].shape[0]}
                rows returned successfully.
                """
            )

            # =================================
            # SQL Toggle
            # =================================
            show_query = st.checkbox(
                "Show Generated SQL Query",
                key="single_query_toggle"
            )

            if show_query:

                st.code(
                    st.session_state["query"],
                    language="sql"
                )

    # =========================================
    # MULTI TABLE ANALYSIS
    # =========================================
    else:

        st.subheader(
            "Step 2: Select Datasets"
        )

        table_options = [
            "🔽 Select a table"
        ] + tables

        col1, col2 = st.columns(2)

        with col1:

            table1 = st.selectbox(
                "Select First Table",
                table_options,
                key="table1_multi"
            )

        with col2:

            table2 = st.selectbox(
                "Select Second Table",
                table_options,
                key="table2_multi"
            )

        # =====================================
        # Validation
        # =====================================
        if (
            table1 == "🔽 Select a table"
            or
            table2 == "🔽 Select a table"
        ):

            st.info(
                "Please select both datasets."
            )

            return

        # =====================================
        # Prevent Same Table
        # =====================================
        if table1 == table2:

            st.warning(
                "Please select different tables."
            )

            return

        st.markdown("---")

        # =====================================
        # Load Columns
        # =====================================
        with st.spinner(
            "Loading table columns..."
        ):

            columns1 = get_columns(
                table1
            )

            columns2 = get_columns(
                table2
            )

        # =====================================
        # All Columns
        # =====================================
        all_columns = (

            [
                f"{table1}.{col[0]}"
                for col in columns1
            ]

            +

            [
                f"{table2}.{col[0]}"
                for col in columns2
            ]
        )

        # =====================================
        # Numeric Columns
        # =====================================
        numeric_columns = (

            [
                f"{table1}.{col[0]}"
                for col in columns1

                if any(
                    num in str(col[1]).upper()

                    for num in [
                        "INT",
                        "BIGINT",
                        "FLOAT",
                        "DOUBLE",
                        "DECIMAL",
                        "NUMERIC",
                        "REAL"
                    ]
                )
            ]

            +

            [
                f"{table2}.{col[0]}"
                for col in columns2

                if any(
                    num in str(col[1]).upper()

                    for num in [
                        "INT",
                        "BIGINT",
                        "FLOAT",
                        "DOUBLE",
                        "DECIMAL",
                        "NUMERIC",
                        "REAL"
                    ]
                )
            ]
        )

        # =====================================
        # Validation
        # =====================================
        if not numeric_columns:

            st.error(
                "No numeric columns available for analysis."
            )

            return

        # =====================================
        # Configure Analysis
        # =====================================
        st.subheader(
            "Step 3: Configure Analysis"
        )

        metric_column = st.selectbox(
            "Select Metric Column",
            numeric_columns
        )

        aggregation = st.selectbox(
            "Select Aggregation",
            [
                "SUM",
                "AVG",
                "COUNT",
                "MAX",
                "MIN"
            ],
            key="agg_multi"
        )

        # =====================================
        # Group By
        # =====================================
        use_groupby = st.checkbox(
            "Use Group By",
            key="groupby_multi"
        )

        group_by_column = None

        if use_groupby:

            group_by_column = st.selectbox(
                "Group By Column",
                all_columns,
                key="group_col_multi"
            )

        st.markdown("---")

        # =====================================
        # Generate Analysis
        # =====================================
        if st.button(
            "Generate Analysis"
        ):

            with st.spinner(
                "Running multi-table analysis..."
            ):

                try:

                    query = build_query(
                        table1=table1,
                        table2=table2,
                        metric_column=metric_column,
                        aggregation=aggregation,
                        group_by_column=group_by_column
                    )

                    df = load_data(
                        query
                    )

                    # =============================
                    # Save Results
                    # =============================
                    st.session_state[
                        "analysis_generated"
                    ] = True

                    st.session_state[
                        "query"
                    ] = query

                    st.session_state[
                        "df"
                    ] = df

                    st.session_state[
                        "analysis_type"
                    ] = "multi"

                    st.success(
                        "Analysis generated successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Analysis Failed: {e}"
                    )

        # =====================================
        # Show Results
        # =====================================
        if (
            st.session_state.get(
                "analysis_generated"
            )
            and
            st.session_state.get(
                "analysis_type"
            ) == "multi"
        ):

            st.markdown("---")

            st.subheader(
                "📌 Analysis Result"
            )

            with st.spinner(
                "Loading analysis results..."
            ):

                st.dataframe(
                    st.session_state["df"],
                    use_container_width=True
                )

            st.success(
                f"""
                {st.session_state['df'].shape[0]}
                rows returned successfully.
                """
            )

            # =================================
            # SQL Toggle
            # =================================
            show_query = st.checkbox(
                "Show Generated SQL Query",
                key="multi_query_toggle"
            )

            if show_query:

                st.code(
                    st.session_state["query"],
                    language="sql"
                )