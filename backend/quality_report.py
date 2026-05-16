import pandas as pd


# =========================================
# Convert UI Column To SQL Column
# =========================================
def convert_to_sql_column(col_name):

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

    report = {}

    try:

        # =====================================
        # Total Rows
        # =====================================
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
        # Unique Counts
        # =====================================
        unique_details = []

        for col in columns:

            sql_col = convert_to_sql_column(
                col
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

        report["Error"] = str(e)

    return report