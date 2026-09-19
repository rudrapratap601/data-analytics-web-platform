"""
Data Quality Report Generator Module

This module generates comprehensive data quality reports directly from PostgreSQL.
It calculates row counts, column counts, missing value statistics, and unique value
counts using SQL queries for maximum efficiency.

Key Metrics:
    - Total row and column counts
    - Missing value count and percentage per column
    - Unique value counts per column (cardinality)

Dependencies:
    - Pandas: For reading SQL query results
    - SQLAlchemy Engine: For database execution
"""

import pandas as pd


# =========================================
# Convert UI Column To SQL Column
# =========================================
def convert_to_sql_column(col_name):
    """
    Convert a column name (potentially aliased from a JOIN) to a SQL-safe reference.

    Handles both plain column names and joined column names in 'table_column'
    format by splitting on the first underscore and double-quoting both parts.

    Args:
        col_name (str): Column name (e.g., "price" or "sales_price")

    Returns:
        str: SQL-safe column expression (e.g., '"price"' or '"sales"."price"')

    Examples:
        >>> convert_to_sql_column("price")
        '"price"'
        >>> convert_to_sql_column("sales_amount")
        '"sales"."amount"'
    """
    if "_" not in col_name:

        return f'''"{col_name}"'''

    split_index = col_name.find("_")

    table_part = col_name[:split_index]

    column_part = col_name[
        split_index + 1:
    ]

    return f'''"{table_part}"."{column_part}"'''


# =========================================
# Generate Quality Report
# =========================================
def generate_quality_report(
    engine,
    from_sql,
    columns
):
    """
    Generate a comprehensive data quality report using SQL queries.

    Calculates dataset health metrics including total rows, total columns,
    per-column missing value statistics, and per-column unique value counts
    directly against the PostgreSQL database.

    Args:
        engine (sqlalchemy.engine.Engine): Database connection engine
        from_sql (str): SQL FROM clause (e.g., 'FROM "sales"' or JOIN clause)
        columns (list): List of column names to analyze

    Returns:
        dict: Quality report dictionary containing:
            - "Total Rows": Formatted total row count string
            - "Total Columns": Number of columns analyzed
            - "Total Missing Values": Formatted count of all missing values
            - "Missing Value Details": Multi-line string with per-column stats
            - "Unique Value Counts": Multi-line string with per-column unique counts
            - "Error" (optional): Error message if calculation fails

    Query Strategy:
        - Executes separate COUNT(*) queries per metric to avoid loading
          the full dataset into memory
        - Calculates percentages based on total rows
        - Handles zero-row datasets gracefully

    Example:
        >>> report = generate_quality_report(engine, 'FROM "sales"', ['id', 'amount'])
        >>> print(report["Total Rows"])
        '10,000'
    """
    report = {}

    try:

        # =====================================
        # Total Rows
        # =====================================
        # Count total records in the dataset / join
        total_rows_query = f'''
        SELECT COUNT(*) AS total_rows

        {from_sql}
        '''

        total_rows = pd.read_sql(
            total_rows_query,
            con=engine
        ).iloc[0]["total_rows"]

        report["Total Rows"] = (
            f"{total_rows:,}"
        )

        # =====================================
        # Total Columns
        # =====================================
        report["Total Columns"] = len(
            columns
        )

        # =====================================
        # Missing Values
        # =====================================
        total_missing = 0

        missing_details = []

        for col in columns:

            sql_col = convert_to_sql_column(
                col
            )

            # Count NULL values for this column
            missing_query = f'''
            SELECT COUNT(*) AS missing_count

            {from_sql}

            WHERE {sql_col} IS NULL
            '''

            missing_count = pd.read_sql(
                missing_query,
                con=engine
            ).iloc[0]["missing_count"]

            total_missing += missing_count

            missing_percent = 0

            if total_rows > 0:

                missing_percent = round(
                    (
                        missing_count
                        /
                        total_rows
                    ) * 100,
                    2
                )

            missing_details.append(

                f'''
                {col}:
                {missing_count:,}
                ({missing_percent}%)
                '''
            )

        report["Total Missing Values"] = (
            f"{total_missing:,}"
        )

        report["Missing Value Details"] = (
            "\n".join(missing_details)
        )

        # =====================================
        # Unique Counts (Cardinality)
        # =====================================
        unique_details = []

        for col in columns:

            sql_col = convert_to_sql_column(
                col
            )

            # Count DISTINCT non-null values
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

            unique_details.append(

                f'''
                {col}:
                {unique_count:,}
                '''
            )

        report["Unique Value Counts"] = (
            "\n".join(unique_details)
        )

    except Exception as e:

        # Capture error without crashing
        report["Error"] = str(e)

    return report