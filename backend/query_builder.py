from backend.relationships import load_relationships


# =========================================
# Format SQL Column Safely
# PostgreSQL Compatible
# =========================================
def format_column(column_name):

    # =====================================
    # Multi-table column
    # Example:
    # sales.price
    # =====================================
    if "." in column_name:

        table, column = column_name.split(".")

        return f'"{table}"."{column}"'

    # =====================================
    # Single-table column
    # =====================================
    return f'"{column_name}"'


# =========================================
# Format Table Name Safely
# =========================================
def format_table(table_name):

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