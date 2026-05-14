import plotly.express as px


# =========================================
# Smart Chart Recommendation
# =========================================
# =========================================
# Smart Chart Recommendation
# =========================================
def recommend_chart(
    x_dtype,
    y_dtype
):

    x_dtype = x_dtype.lower()
    y_dtype = y_dtype.lower()

    # =====================================
    # Date + Numeric
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
    # Categorical + Numeric
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
    # Numeric + Numeric
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
    # Default
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
    # FALLBACK
    # =====================================
    else:

        fig = px.bar(

            df,

            x=x_col,

            y=y_col
        )

    # =====================================
    # Better Layout
    # =====================================
    fig.update_layout(

        template="plotly_white",

        height=500
    )

    return fig