"""
SQL Query Builder Module

This module constructs dynamic, PostgreSQL-compatible SQL queries for
both single-table and multi-table analysis with aggregations and grouping.

Key Features:
    - Safe column and table quoting for PostgreSQL
    - Single-table aggregation queries (SUM, AVG, COUNT, MAX, MIN)
    - Multi-table JOIN queries using saved relationships
    - Dynamic GROUP BY support

Dependencies:
    - backend.relationships: For retrieving table relationships
"""

from backend.relationships import load_relationships


# =========================================
# Format SQL Column Safely
# PostgreSQL Compatible
# =========================================
def format_column(column_name):
    """
    Format a column name safely for PostgreSQL queries.

    Handles both single-table column names and multi-table column names
    in 'table.column' format by adding double quotes around identifiers.

    Args:
        column_name (str): Column name, optionally prefixed with table name
                          (e.g., "price" or "sales.price")

    Returns:
        str: Safely quoted column identifier for PostgreSQL

    Examples:
        >>> format_column("price")
        '"price"'
        >>> format_column("sales.price")
        '"sales"."price"'
    """
    # =====================================
    # Multi-table column
    # Example:
    # sales.price -> "sales"."price"
    # =====================================
    if "." in column_name:

        table, column = column_name.split(".")

        return f'"{table}"."{column}"'

    # =====================================
    # Single-table column
    # Example:
    # price -> "price"
    # =====================================
    return f'"{column_name}"'


# =========================================
# Format Table Name Safely
# =========================================
def format_table(table_name):
    """
    Format a table name safely for PostgreSQL queries.

    Wraps the table name in double quotes to handle reserved words
    and special characters safely.

    Args:
        table_name (str): Raw table name

    Returns:
        str: Double-quoted table name

    Example:
        >>> format_table("monthly_sales")
        '"monthly_sales"'
    """
    return f'"{table_name}"'


# =========================================
# Build Dynamic SQL Query
# PostgreSQL Compatible
# =========================================
def build_query(
    table1,
    metric_column,
    aggregation,
    group_by_column=None,
    table2=None
):
    """
    Build a dynamic SQL aggregation query for single or multi-table analysis.

    Constructs a complete, safe PostgreSQL query based on user configuration.
    Supports single-table queries and multi-table JOIN queries using relationships
    saved in the database.

    Args:
        table1 (str): Primary table name
        metric_column (str): Column to aggregate (e.g., "sales" or "orders.amount")
        aggregation (str): SQL aggregate function (SUM, AVG, COUNT, MAX, MIN)
        group_by_column (str, optional): Column to group results by. Defaults to None.
        table2 (str, optional): Secondary table name for JOIN queries. Defaults to None.

    Returns:
        str: Formatted, executable PostgreSQL query string

    Raises:
        ValueError: If table2 is provided but no relationship exists between
                   table1 and table2

    Query Patterns:
        Single table, no group by:
            SELECT AGG(col) AS result FROM "table1"

        Single table, with group by:
            SELECT group_col, AGG(col) AS result FROM "table1" GROUP BY group_col

        Multi table, with JOIN:
            SELECT [group_col,] AGG(col) AS result
            FROM "table1" JOIN "table2" ON "t1"."c1" = "t2"."c2"
            [GROUP BY group_col]

    Examples:
        >>> build_query("sales", "amount", "SUM")
        'SELECT SUM("amount") AS result FROM "sales"'

        >>> build_query("sales", "amount", "AVG", group_by_column="region")
        'SELECT "region", AVG("amount") AS result FROM "sales" GROUP BY "region"'
    """
    # =====================================
    # Format SQL Safely
    # =====================================
    metric_column_sql = format_column(
        metric_column
    )

    table1_sql = format_table(
        table1
    )

    group_by_sql = None

    if group_by_column:

        group_by_sql = format_column(
            group_by_column
        )

    # =====================================
    # SINGLE TABLE ANALYSIS
    # =====================================
    if not table2:

        # ---------------------------------
        # WITHOUT GROUP BY
        # ---------------------------------
        if not group_by_column:

            query = f"""
            SELECT
                {aggregation}({metric_column_sql}) AS result

            FROM {table1_sql}
            """

            return query

        # ---------------------------------
        # WITH GROUP BY
        # ---------------------------------
        query = f"""
        SELECT
            {group_by_sql},
            {aggregation}({metric_column_sql}) AS result

        FROM {table1_sql}

        GROUP BY {group_by_sql}
        """

        return query

    # =====================================
    # MULTI TABLE ANALYSIS
    # =====================================
    relationships = load_relationships()

    matching_relationship = None

    # =====================================
    # Find Matching Relationship
    # Check both (table1, table2) and (table2, table1) orientations
    # =====================================
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

            matching_relationship = rel

            break

    # =====================================
    # Validation
    # =====================================
    if not matching_relationship:

        raise ValueError(
            "No relationship found between selected tables."
        )

    # =====================================
    # Relationship Details
    # =====================================
    left_table = matching_relationship[
        "table1"
    ]

    left_column = matching_relationship[
        "column1"
    ]

    right_table = matching_relationship[
        "table2"
    ]

    right_column = matching_relationship[
        "column2"
    ]

    # =====================================
    # Format JOIN Columns
    # =====================================
    left_join = (
        f'"{left_table}"."{left_column}"'
    )

    right_join = (
        f'"{right_table}"."{right_column}"'
    )

    table2_sql = format_table(
        table2
    )

    # =====================================
    # WITHOUT GROUP BY
    # =====================================
    if not group_by_column:

        query = f"""
        SELECT
            {aggregation}({metric_column_sql}) AS result

        FROM {table1_sql}

        JOIN {table2_sql}

        ON {left_join} = {right_join}
        """

        return query

    # =====================================
    # WITH GROUP BY
    # =====================================
    query = f"""
    SELECT
        {group_by_sql},
        {aggregation}({metric_column_sql}) AS result

    FROM {table1_sql}

    JOIN {table2_sql}

    ON {left_join} = {right_join}

    GROUP BY {group_by_sql}
    """

    return query