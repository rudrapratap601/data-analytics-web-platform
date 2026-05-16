import streamlit as st
import pandas as pd

from backend.db import get_engine
from backend.schema import get_tables
from backend.relationships import load_relationships

from backend.chart_engine import (
    create_chart,
    recommend_chart
)

from backend.insight_engine import (
    generate_insights
)

from backend.quality_report import (
    generate_quality_report
)


# =========================================
# Find Matching Relationship
# =========================================
def get_matching_relationship(
    table1,
    table2
):

    relationships = load_relationships()

    for rel in relationships:

        tables_match = (
            (
                rel["table1"] == table1
                and
                rel["table2"] == table2
            )
            or
            (
                rel["table1"] == table2
                and
                rel["table2"] == table1
            )
        )

        if tables_match:

            return rel

    return None


# =========================================
# Better Dimension Columns
# =========================================
def get_dimension_columns(df):

    excluded_keywords = [

        "id",

        "_id",

        "uuid",

        "key",

        "link",

        "url"
    ]

    dimension_columns = []

    for col in df.columns:

        col_lower = col.lower()

        # =====================================
        # Skip ID / URL Columns
        # =====================================
        if any(
            keyword in col_lower
            for keyword in excluded_keywords
        ):

            continue

        dimension_columns.append(col)

    return dimension_columns


# =========================================
# Convert UI Column to SQL Column
# =========================================
def convert_to_sql_column(
    col_name,
    dashboard_mode,
    table=None
):

    # =====================================
    # Single Dataset
    # =====================================
    if dashboard_mode == "Single Dataset Dashboard":

        return f'''"{table}"."{col_name}"'''

    # =====================================
    # Multi Dataset
    # =====================================
    split_index = col_name.find("_")

    table_part = col_name[:split_index]

    column_part = col_name[
        split_index + 1:
    ]

    return f'''"{table_part}"."{column_part}"'''


# =========================================
# MAIN PAGE
# =========================================
def show():

    # =====================================
    # Page Header
    # =====================================
    st.title("📈 Dashboard Builder")

    st.markdown("""
    Create dynamic visualizations
    and dashboards from datasets.
    """)

    st.info("""
    Dashboard calculations are performed
    on the FULL dataset using PostgreSQL.

    Only preview rows are partially loaded.
    """)

    st.markdown("---")

    # =====================================
    # Load Tables
    # =====================================
    tables = get_tables()

    if not tables:

        st.warning(
            "No datasets available."
        )

        return

    engine = get_engine()

    # =====================================
    # Dashboard Mode
    # =====================================
    dashboard_mode = st.radio(
        "Choose Dashboard Mode",
        [
            "Single Dataset Dashboard",
            "Multi Dataset Dashboard"
        ]
    )

    st.markdown("---")

    # =====================================
    # SINGLE DATASET MODE
    # =====================================
    if dashboard_mode == "Single Dataset Dashboard":

        st.subheader("📂 Select Dataset")

        options = [
            "🔽 Select Dataset"
        ] + tables

        table = st.selectbox(
            "Select Dataset",
            options
        )

        if table == "🔽 Select Dataset":

            st.info(
                "Please select a dataset."
            )

            return

        # =================================
        # Preview Limit
        # =================================
        preview_limit = st.selectbox(
            "Rows to Preview",
            [
                100,
                1000,
                5000
            ],
            index=1
        )

        # =================================
        # Preview Query
        # =================================
        preview_query = f'''
        SELECT *
        FROM "{table}"
        LIMIT {preview_limit}
        '''

        try:

            preview_df = pd.read_sql(
                preview_query,
                con=engine
            )

        except Exception as e:

            st.error(
                f"Failed to load dataset: {e}"
            )

            return

        # =================================
        # Base SQL
        # =================================
        from_sql = f'''
        FROM "{table}"
        '''

    # =====================================
    # MULTI DATASET MODE
    # =====================================
    else:

        st.subheader("🔗 Select Datasets")

        options = [
            "🔽 Select Dataset"
        ] + tables

        col1, col2 = st.columns(2)

        with col1:

            table1 = st.selectbox(
                "Select First Table",
                options,
                key="table1"
            )

        with col2:

            table2 = st.selectbox(
                "Select Second Table",
                options,
                key="table2"
            )

        # =================================
        # Validation
        # =================================
        if (
            table1 == "🔽 Select Dataset"
            or
            table2 == "🔽 Select Dataset"
        ):

            st.info(
                "Please select both datasets."
            )

            return

        if table1 == table2:

            st.warning(
                "Please select different tables."
            )

            return

        # =================================
        # Relationship
        # =================================
        relationship = get_matching_relationship(
            table1,
            table2
        )

        if not relationship:

            st.error(
                "No relationship found."
            )

            return

        # =================================
        # Preview Limit
        # =================================
        preview_limit = st.selectbox(
            "Rows to Preview",
            [
                100,
                1000,
                5000
            ],
            index=1,
            key="multi_preview_limit"
        )

        # =================================
        # Relationship Info
        # =================================
        left_table = relationship["table1"]
        left_column = relationship["column1"]

        right_table = relationship["table2"]
        right_column = relationship["column2"]

        # =================================
        # Get Columns
        # =================================
        columns1_df = pd.read_sql(
            f'''
            SELECT *
            FROM "{table1}"
            LIMIT 1
            ''',
            con=engine
        )

        columns2_df = pd.read_sql(
            f'''
            SELECT *
            FROM "{table2}"
            LIMIT 1
            ''',
            con=engine
        )

        # =================================
        # Aliased Columns
        # =================================
        table1_columns = [

            f'''"{table1}"."{col}" AS "{table1}_{col}"'''

            for col in columns1_df.columns
        ]

        table2_columns = [

            f'''"{table2}"."{col}" AS "{table2}_{col}"'''

            for col in columns2_df.columns
        ]

        select_sql = ",\n".join(
            table1_columns + table2_columns
        )

        # =================================
        # Preview Query
        # =================================
        preview_query = f'''
        SELECT

        {select_sql}

        FROM "{table1}"

        JOIN "{table2}"

        ON
        "{left_table}"."{left_column}"
        =
        "{right_table}"."{right_column}"

        LIMIT {preview_limit}
        '''

        try:

            preview_df = pd.read_sql(
                preview_query,
                con=engine
            )

        except Exception as e:

            st.error(
                f"Failed to load joined dataset: {e}"
            )

            return

        # =================================
        # Base SQL
        # =================================
        from_sql = f'''
        FROM "{table1}"

        JOIN "{table2}"

        ON
        "{left_table}"."{left_column}"
        =
        "{right_table}"."{right_column}"
        '''

    # =====================================
    # Empty Check
    # =====================================
    if preview_df.empty:

        st.warning(
            "Dataset is empty."
        )

        return

    # =====================================
    # Preview
    # =====================================
    st.subheader("📌 Dataset Preview")

    st.caption(
        f"""
        Showing first
        {len(preview_df):,} rows
        """
    )

    st.dataframe(
        preview_df.head(100),
        use_container_width=True
    )

    st.markdown("---")

    # =====================================
    # Detect Columns
    # =====================================
    numeric_columns = preview_df.select_dtypes(
        include=[
            "int64",
            "float64",
            "Int64"
        ]
    ).columns.tolist()

    dimension_columns = get_dimension_columns(
        preview_df
    )

    # =====================================
    # Validation
    # =====================================
    if not numeric_columns:

        st.error(
            "No numeric columns available."
        )

        return

    if not dimension_columns:

        st.error(
            "No suitable dimension columns found."
        )

        return

    # =====================================
    # Visualization Settings
    # =====================================
    st.subheader(
        "📊 Visualization Settings"
    )

    dimension_options = [
        "🔽 Select Dimension Column"
    ] + dimension_columns

    metric_options = [
        "🔽 Select Metric Column"
    ] + numeric_columns

    x_col = st.selectbox(
        "Select Dimension Column",
        dimension_options
    )

    y_col = st.selectbox(
        "Select Metric Column",
        metric_options
    )

    # =====================================
    # Prevent Auto Selection
    # =====================================
    if (
        x_col == "🔽 Select Dimension Column"
        or
        y_col == "🔽 Select Metric Column"
    ):

        st.info(
            "Please select both columns."
        )

        return

    # =====================================
    # High Cardinality Warning
    # =====================================
    unique_count = preview_df[
        x_col
    ].nunique()

    if unique_count > 100:

        st.warning(
            f"""
            '{x_col}' contains
            {unique_count:,} unique values.

            Large charts may become slow
            or difficult to read.
            """
        )

    # =====================================
    # Aggregation
    # =====================================
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
    # Time Series Detection
    # =====================================
    is_datetime = pd.api.types.is_datetime64_any_dtype(
        preview_df[x_col]
    )

    time_granularity = None

    if is_datetime:

        time_granularity = st.selectbox(
            "Time Granularity",
            [
                "Day",
                "Month",
                "Year"
            ]
        )

    # =====================================
    # SQL Aggregation Mapping
    # =====================================
    aggregation_map = {

        "SUM": "SUM",

        "AVG": "AVG",

        "COUNT": "COUNT",

        "MAX": "MAX",

        "MIN": "MIN"
    }

    sql_aggregation = aggregation_map[
        aggregation
    ]

    # =====================================
    # Convert Columns
    # =====================================
    if dashboard_mode == "Single Dataset Dashboard":

        x_col_sql = convert_to_sql_column(
            x_col,
            dashboard_mode,
            table
        )

        y_col_sql = convert_to_sql_column(
            y_col,
            dashboard_mode,
            table
        )

    else:

        x_col_sql = convert_to_sql_column(
            x_col,
            dashboard_mode
        )

        y_col_sql = convert_to_sql_column(
            y_col,
            dashboard_mode
        )

    # =====================================
    # Time Series SQL
    # =====================================
    group_dimension_sql = x_col_sql

    if is_datetime:

        granularity_map = {

            "Day": "day",

            "Month": "month",

            "Year": "year"
        }

        postgres_granularity = granularity_map[
            time_granularity
        ]

        group_dimension_sql = f'''
        DATE_TRUNC(
            '{postgres_granularity}',
            {x_col_sql}
        )
        '''

    # =====================================
    # FULL DATASET AGGREGATION
    # =====================================
    aggregation_query = f'''
    SELECT

    {group_dimension_sql} AS dimension,

    {sql_aggregation}({y_col_sql}) AS result

    {from_sql}

    GROUP BY {group_dimension_sql}

    ORDER BY dimension DESC
    '''

    try:

        summary_df = pd.read_sql(
            aggregation_query,
            con=engine
        )

    except Exception as e:

        st.error(
            f"Aggregation failed: {e}"
        )

        st.code(
            aggregation_query,
            language="sql"
        )

        return

    # =====================================
    # Empty Result Check
    # =====================================
    if summary_df.empty:

        st.warning(
            "No results found."
        )

        return

    # =====================================
    # Rename Columns
    # =====================================
    summary_df.columns = [
        x_col,
        "result"
    ]

    y_col = "result"

    st.markdown("---")

    # =====================================
    # Recommended Chart
    # =====================================
    recommended_chart = recommend_chart(

        str(summary_df[x_col].dtype),

        str(summary_df[y_col].dtype)
    )

    # =====================================
    # Better Recommendation
    # =====================================
    if is_datetime:

        recommended_chart = "Line Chart"

    st.success(
        f"Recommended Chart: {recommended_chart}"
    )

    # =====================================
    # Chart Selection
    # =====================================
    chart_options = [
        "Bar Chart",
        "Line Chart",
        "Pie Chart",
        "Scatter Plot"
    ]

    chart_type = st.selectbox(

        "Select Chart Type",

        chart_options,

        index=chart_options.index(
            recommended_chart
        )
    )

    st.markdown("---")

    # =====================================
    # Analysis Dataset
    # =====================================
    st.subheader(
        "📌 Analysis Dataset"
    )

    st.dataframe(
        summary_df,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================
    # Generate Chart
    # =====================================
    try:

        fig = create_chart(

            summary_df,

            chart_type,

            x_col,

            y_col
        )

        st.subheader(
            "📈 Dashboard Visualization"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Chart generation failed: {e}"
        )

    st.markdown("---")

    # =====================================
    # AI Insights
    # =====================================
    st.subheader("🧠 AI Insights")

    try:

        insights = generate_insights(
            summary_df,
            x_col,
            y_col
        )

        for insight in insights:

            st.info(insight)

    except Exception as e:

        st.warning(
            f"Insight generation failed: {e}"
        )

    st.markdown("---")

    # =====================================
    # Quality Report
    # =====================================
    st.subheader(
        "📋 Data Quality Report"
    )

    try:

        # =================================
        # Total Rows Query
        # =================================
        total_rows_query = f'''
        SELECT COUNT(*) AS total_rows

        {from_sql}
        '''

        total_rows = pd.read_sql(
            total_rows_query,
            con=engine
        ).iloc[0]["total_rows"]

        st.write(
            f"**Total Rows:** {total_rows:,}"
        )

        st.write(
            f"**Total Columns:** {len(preview_df.columns)}"
        )

        st.markdown("---")

        # =================================
        # Missing Value Report
        # =================================
        missing_report = []

        for col in preview_df.columns:

            sql_col = convert_to_sql_column(
                col,
                dashboard_mode,
                table if dashboard_mode ==
                "Single Dataset Dashboard"
                else None
            )

            missing_query = f'''
            SELECT COUNT(*) AS missing_count

            {from_sql}

            WHERE {sql_col} IS NULL
            '''

            missing_count = pd.read_sql(
                missing_query,
                con=engine
            ).iloc[0]["missing_count"]

            missing_percent = round(
                (
                    missing_count
                    / total_rows
                ) * 100,
                2
            )

            unique_query = f'''
            SELECT COUNT(
                DISTINCT {sql_col}
            ) AS unique_count

            {from_sql}
            '''

            unique_count = pd.read_sql(
                unique_query,
                con=engine
            ).iloc[0]["unique_count"]

            missing_report.append({

                "Column": col,

                "Missing Values": missing_count,

                "Missing %": missing_percent,

                "Unique Values": unique_count
            })

        # =================================
        # Convert to DataFrame
        # =================================
        quality_df = pd.DataFrame(
            missing_report
        )

        # =================================
        # Sort by Missing Values
        # =================================
        quality_df = quality_df.sort_values(
            by="Missing Values",
            ascending=False
        )

        # =================================
        # Display Report
        # =================================
        st.dataframe(
            quality_df,
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Quality report failed: {e}"
        )

    st.markdown("---")

    # =====================================
    # Export Results
    # =====================================
    st.subheader("📥 Export Results")

    csv = summary_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="Download CSV",

        data=csv,

        file_name="dashboard_data.csv",

        mime="text/csv"
    )