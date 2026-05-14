# =========================================
# Generate Smart Insights
# =========================================
def generate_insights(
    df,
    x_col,
    y_col
):

    insights = []

    # =====================================
    # Empty Dataset Validation
    # =====================================
    if df.empty:

        return [
            "Dataset is empty."
        ]

    try:

        # =================================
        # Basic Information
        # =================================
        insights.append(
            f"""
            Dataset contains
            {df.shape[0]} rows and
            {df.shape[1]} columns.
            """
        )

        # =================================
        # Statistical Insights
        # =================================
        avg_value = round(
            df[y_col].mean(),
            2
        )

        max_value = df[y_col].max()

        min_value = df[y_col].min()

        insights.append(
            f"""
            Average {y_col}:
            {avg_value}
            """
        )

        insights.append(
            f"""
            Maximum {y_col}:
            {max_value}
            """
        )

        insights.append(
            f"""
            Minimum {y_col}:
            {min_value}
            """
        )

        # =================================
        # Top Category
        # =================================
        try:

            top_row = df.loc[
                df[y_col].idxmax()
            ]

            insights.append(
                f"""
                Highest performing
                {x_col}:
                {top_row[x_col]}
                with value
                {top_row[y_col]}.
                """
            )

        except Exception:

            pass

        # =================================
        # Missing Values
        # =================================
        missing_values = int(
            df.isnull().sum().sum()
        )

        insights.append(
            f"""
            Dataset contains
            {missing_values}
            missing values.
            """
        )

        # =================================
        # Duplicate Rows
        # =================================
        duplicate_rows = int(
            df.duplicated().sum()
        )

        insights.append(
            f"""
            Dataset contains
            {duplicate_rows}
            duplicate rows.
            """
        )

    except Exception as e:

        insights.append(
            f"Insight generation failed: {e}"
        )

    return insights