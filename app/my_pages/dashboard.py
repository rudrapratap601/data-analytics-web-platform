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
# MAIN DASHBOARD PAGE
# =========================================
def show():

    # =====================================
    # Page Header
    # =====================================
    st.title("📈 Dashboard Builder")

    st.markdown("""
    Create dynamic visualizations and dashboards
    from your datasets.
    """)

    st.info(
        """
        For multi-dataset dashboards,
        relationships must be created first.
        """
    )

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

        # =================================
        # Validation
        # =================================
        if table == "🔽 Select Dataset":

            st.info(
                "Please select a dataset."
            )

            return

        # =================================
        # PostgreSQL Query
        # =================================
        with st.spinner("Loading dataset..."):
            query = f'''
            SELECT *
            FROM "{table}"
            '''

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
                key="dashboard_table1"
            )

        with col2:

            table2 = st.selectbox(
                "Select Second Table",
                options,
                key="dashboard_table2"
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
        # Relationship Validation
        # =================================
        relationship = get_matching_relationship(
            table1,
            table2
        )

        if not relationship:

            st.error(
                """
                No relationship found between
                selected tables.
                """
            )

            return

        # =================================
        # Relationship Info
        # =================================
        left_table = relationship["table1"]

        left_column = relationship["column1"]

        right_table = relationship["table2"]

        right_column = relationship["column2"]

        # =================================
        # Load Columns for Safe Aliasing
        # =================================
        columns1_query = f'''
        SELECT *
        FROM "{table1}"
        LIMIT 1
        '''

        columns2_query = f'''
        SELECT *
        FROM "{table2}"
        LIMIT 1
        '''

        columns1_df = pd.read_sql(
            columns1_query,
            con=engine
        )

        columns2_df = pd.read_sql(
            columns2_query,
            con=engine
        )

        # =================================
        # Create Aliased Columns
        # =================================
        table1_columns = [

            f'''"{table1}"."{col}" AS "{table1}_{col}"'''

            for col in columns1_df.columns
        ]

        table2_columns = [

            f'''"{table2}"."{col}" AS "{table2}_{col}"'''

            for col in columns2_df.columns
        ]

        select_columns = (
            table1_columns
            +
            table2_columns
        )

        select_sql = ",\n".join(
            select_columns
        )

        # =================================
        # PostgreSQL JOIN Query
        # =================================
        with st.spinner(
            "Loading joined dataset..."
        ):

            query = f'''
            SELECT

            {select_sql}

            FROM "{table1}"

            JOIN "{table2}"

            ON
            "{left_table}"."{left_column}"
            =
            "{right_table}"."{right_column}"
            '''

            try:

                df = pd.read_sql(
                    query,
                    con=engine
                )

            except Exception as e:

                st.error(
                    f"Failed to load joined dataset: {e}"
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
    # Dataset Preview
    # =====================================
    st.subheader("📌 Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.write(
        f"""
        Rows: {df.shape[0]}
        | Columns: {df.shape[1]}
        """
    )

    st.markdown("---")

    # =====================================
    # Detect Columns
    # =====================================
    numeric_columns = df.select_dtypes(
        include=[
            "int64",
            "float64",
            "Int64"
        ]
    ).columns.tolist()

    all_columns = df.columns.tolist()

    # =====================================
    # Validation
    # =====================================
    if not numeric_columns:

        st.error(
            "No numeric columns available."
        )

        return

    # =====================================
    # Visualization Settings
    # =====================================
    st.subheader(
        "📊 Visualization Settings"
    )

    x_col = st.selectbox(
        "Select Dimension Column",
        all_columns
    )

    y_col = st.selectbox(
        "Select Metric Column",
        numeric_columns
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
    # Aggregation Mapping
    # =====================================
    aggregation_map = {

        "SUM": "sum",

        "AVG": "mean",

        "COUNT": "count",

        "MAX": "max",

        "MIN": "min"
    }

    # =====================================
    # Aggregate Data
    # =====================================
    try:

        summary_df = (
            df.groupby(x_col)[y_col]
            .agg(
                aggregation_map[
                    aggregation
                ]
            )
            .reset_index()
        )

    except Exception as e:

        st.error(
            f"Aggregation failed: {e}"
        )

        return

    # =====================================
    # Rename Result Column
    # =====================================
    summary_df.columns = [
        x_col,
        "result"
    ]

    y_col = "result"

    st.markdown("---")

    # =====================================
    # Smart Chart Recommendation
    # =====================================
    recommended_chart = recommend_chart(

        str(summary_df[x_col].dtype),

        str(summary_df[y_col].dtype)
    )

    st.success(
        f"""
        Recommended Chart:
        {recommended_chart}
        """
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
    # Data Quality Report
    # =====================================
    st.subheader(
        "📋 Data Quality Report"
    )

    try:

        report = generate_quality_report(
            df
        )

        for key, value in report.items():

            st.write(
                f"**{key}:** {value}"
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