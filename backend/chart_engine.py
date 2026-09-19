"""
Chart Generation Engine

This module handles chart recommendations and generation using Plotly Express.
It automatically recommends the best chart type based on column datatypes and
renders interactive, styled visualizations.

Supported Chart Types:
    - Bar Chart: Best for categorical vs numeric data
    - Line Chart: Best for time-series / trend analysis
    - Pie Chart: Best for distribution / proportion analysis
    - Scatter Plot: Best for numeric vs numeric correlation

Dependencies:
    - Plotly Express: For interactive chart rendering
"""

import plotly.express as px


# =========================================
# Smart Chart Recommendation
# =========================================
def recommend_chart(
    x_dtype,
    y_dtype
):
    """
    Recommend the optimal chart type based on column datatypes.

    Rules:
        - Datetime + Numeric -> Line Chart (trend over time)
        - Categorical (object) + Numeric -> Bar Chart (categories comparison)
        - Numeric + Numeric -> Scatter Plot (correlation)
        - Default fallback -> Bar Chart

    Args:
        x_dtype (str): Pandas dtype string of the X-axis column (e.g., 'object', 'datetime64[ns]', 'int64')
        y_dtype (str): Pandas dtype string of the Y-axis column (e.g., 'int64', 'float64')

    Returns:
        str: Recommended chart type name
             ("Line Chart", "Bar Chart", or "Scatter Plot")

    Examples:
        >>> recommend_chart("datetime64[ns]", "float64")
        'Line Chart'
        >>> recommend_chart("object", "int64")
        'Bar Chart'
        >>> recommend_chart("float64", "float64")
        'Scatter Plot'
    """
    x_dtype = x_dtype.lower()
    y_dtype = y_dtype.lower()

    # =====================================
    # Date + Numeric -> Line Chart
    # =====================================
    if (
        "datetime" in x_dtype
        and
        (
            "int" in y_dtype
            or
            "float" in y_dtype
        )
    ):

        return "Line Chart"

    # =====================================
    # Categorical + Numeric -> Bar Chart
    # =====================================
    if (
        x_dtype == "object"
        and
        (
            "int" in y_dtype
            or
            "float" in y_dtype
        )
    ):

        return "Bar Chart"

    # =====================================
    # Numeric + Numeric -> Scatter Plot
    # =====================================
    if (
        (
            "int" in x_dtype
            or
            "float" in x_dtype
        )
        and
        (
            "int" in y_dtype
            or
            "float" in y_dtype
        )
    ):

        return "Scatter Plot"

    # =====================================
    # Default Fallback
    # =====================================
    return "Bar Chart"


# =========================================
# Create Chart
# =========================================
def create_chart(
    df,
    chart_type,
    x_col,
    y_col
):
    """
    Create an interactive Plotly chart figure.

    Renders a Plotly Express figure based on the requested chart type
    with clean layout defaults (white template, fixed height).

    Args:
        df (pd.DataFrame): Data to visualize (must not be empty)
        chart_type (str): Type of chart to create
                         ("Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot")
        x_col (str): Column name for the X-axis / categories / names
        y_col (str): Column name for the Y-axis / values / metrics

    Returns:
        plotly.graph_objects.Figure: Configured interactive Plotly figure

    Raises:
        ValueError: If the input DataFrame is empty

    Layout Customizations:
        - Template: plotly_white (clean, modern look)
        - Height: 500px
    """
    # =====================================
    # Empty Dataset Protection
    # =====================================
    if df.empty:

        raise ValueError(
            "No data available for chart generation."
        )

    # =====================================
    # BAR CHART
    # =====================================
    if chart_type == "Bar Chart":

        fig = px.bar(

            df,

            x=x_col,

            y=y_col,

            title=f"{y_col} by {x_col}"
        )

    # =====================================
    # LINE CHART
    # =====================================
    elif chart_type == "Line Chart":

        fig = px.line(

            df,

            x=x_col,

            y=y_col,

            title=f"{y_col} Trend"
        )

    # =====================================
    # PIE CHART
    # =====================================
    elif chart_type == "Pie Chart":

        fig = px.pie(

            df,

            names=x_col,

            values=y_col,

            title=f"{y_col} Distribution"
        )

    # =====================================
    # SCATTER PLOT
    # =====================================
    elif chart_type == "Scatter Plot":

        fig = px.scatter(

            df,

            x=x_col,

            y=y_col,

            title=f"{x_col} vs {y_col}"
        )

    # =====================================
    # FALLBACK (Default to Bar Chart)
    # =====================================
    else:

        fig = px.bar(

            df,

            x=x_col,

            y=y_col
        )

    # =====================================
    # Layout Styling - Dark Corporate Theme
    # =====================================
    fig.update_layout(

        template="plotly_dark",

        height=500,

        # Transparent backgrounds for glassmorphism effect
        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(15, 23, 42, 0.5)",

        # Corporate color palette
        colorway=[
            "#3b82f6",  # Primary Blue
            "#06b6d4",  # Cyan
            "#6366f1",  # Indigo
            "#10b981",  # Emerald
            "#f59e0b",  # Amber
            "#8b5cf6"   # Violet
        ],

        # Modern typography
        font=dict(
            family="sans serif",
            color="#f8fafc",
            size=12
        ),

        # Title styling
        title_font=dict(
            size=18,
            color="#f8fafc",
            family="sans serif"
        ),

        # Legend styling
        legend=dict(
            bgcolor="rgba(30, 41, 59, 0.8)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1,
            font=dict(color="#f8fafc")
        ),

        # Hover label styling
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            font_size=12,
            font_color="#f8fafc",
            bordercolor="rgba(59, 130, 246, 0.5)"
        )
    )

    # =====================================
    # Axis Styling
    # =====================================
    fig.update_xaxes(

        gridcolor="rgba(255, 255, 255, 0.06)",

        zerolinecolor="rgba(255, 255, 255, 0.1)",

        linecolor="rgba(255, 255, 255, 0.2)",

        title_font=dict(color="#94a3b8"),

        tickfont=dict(color="#94a3b8")
    )

    fig.update_yaxes(

        gridcolor="rgba(255, 255, 255, 0.06)",

        zerolinecolor="rgba(255, 255, 255, 0.1)",

        linecolor="rgba(255, 255, 255, 0.2)",

        title_font=dict(color="#94a3b8"),

        tickfont=dict(color="#94a3b8")
    )

    # =====================================
    # Bar Chart Specific Styling
    # =====================================
    if chart_type == "Bar Chart":

        fig.update_traces(
            marker=dict(
                line=dict(
                    color="rgba(255, 255, 255, 0.1)",
                    width=1
                )
            )
        )

    # =====================================
    # Line Chart Specific Styling
    # =====================================
    elif chart_type == "Line Chart":

        fig.update_traces(
            line=dict(
                width=3
            ),
            mode="lines+markers",
            marker=dict(
                size=6,
                line=dict(
                    color="rgba(255, 255, 255, 0.3)",
                    width=1
                )
            )
        )

    return fig