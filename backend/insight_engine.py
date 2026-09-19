"""
AI Insights Generator Module

This module generates automated insights and observations from analyzed datasets.
It produces human-readable summaries of statistical patterns, trends, and data quality.

Key Metrics Generated:
    - Basic statistics (average, max, min)
    - Top performing categories
    - Missing value counts
    - Duplicate row detection

Dependencies:
    - Pandas DataFrame as input
"""

# =========================================
# Generate Smart Insights
# =========================================
def generate_insights(
    df,
    x_col,
    y_col
):
    """
    Generate automated insights from a DataFrame's metrics.

    Analyzes a dataset and produces a list of human-readable insight
    strings covering basic statistics, top performers, and data quality.

    Args:
        df (pd.DataFrame): Dataset to analyze (typically aggregated results)
        x_col (str): Dimension column name (e.g., category, region, date)
        y_col (str): Metric column name (e.g., revenue, count, amount)

    Returns:
        list: List of insight strings describing key observations

    Generated Insights:
        1. Dataset size (rows and columns)
        2. Average value of the metric
        3. Maximum value of the metric
        4. Minimum value of the metric
        5. Top performing category (highest metric value)
        6. Missing values count
        7. Duplicate rows count

    Example:
        >>> df = pd.DataFrame({
        ...     'region': ['North', 'South', 'East'],
        ...     'revenue': [10000, 15000, 8000]
        ... })
        >>> insights = generate_insights(df, 'region', 'revenue')
        >>> for insight in insights:
        ...     print(insight)
        Dataset contains 3 rows and 2 columns.
        Average revenue: 11000.0
        Maximum revenue: 15000
        Minimum revenue: 8000
        Highest performing region: South with value 15000.
        Dataset contains 0 missing values.
        Dataset contains 0 duplicate rows.

    Note:
        Returns a single-item list with "Dataset is empty." if input is empty.
    """
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
            f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
        )

        # =================================
        # Statistical Insights
        # =================================
        # Calculate average metric value
        avg_value = round(
            df[y_col].mean(),
            2
        )

        # Find maximum metric value
        max_value = df[y_col].max()

        # Find minimum metric value
        min_value = df[y_col].min()

        insights.append(
            f"Average {y_col}: {avg_value}"
        )

        insights.append(
            f"Maximum {y_col}: {max_value}"
        )

        insights.append(
            f"Minimum {y_col}: {min_value}"
        )

        # =================================
        # Top Category
        # =================================
        try:

            # Find the row with the highest metric value
            top_row = df.loc[
                df[y_col].idxmax()
            ]

            insights.append(
                f"Highest performing {x_col}: {top_row[x_col]} with value {top_row[y_col]}."
            )

        except Exception:

            pass  # Skip if unable to identify top performer

        # =================================
        # Missing Values
        # =================================
        # Count total missing values across all columns
        missing_values = int(
            df.isnull().sum().sum()
        )

        insights.append(
            f"Dataset contains {missing_values} missing values."
        )

        # =================================
        # Duplicate Rows
        # =================================
        # Count duplicate rows
        duplicate_rows = int(
            df.duplicated().sum()
        )

        insights.append(
            f"Dataset contains {duplicate_rows} duplicate rows."
        )

    except Exception as e:

        # Fallback error message if insight generation fails
        insights.append(
            f"Insight generation failed: {e}"
        )

    return insights