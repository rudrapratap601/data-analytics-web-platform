import pandas as pd

from io import BytesIO


# =========================================
# Convert DataFrame to CSV
# =========================================
def convert_to_csv(df):

    # =====================================
    # Empty Validation
    # =====================================
    if df.empty:

        raise ValueError(
            "Cannot export empty dataframe."
        )

    return df.to_csv(
        index=False
    ).encode("utf-8")


# =========================================
# Convert DataFrame to Excel
# =========================================
def convert_to_excel(df):

    # =====================================
    # Empty Validation
    # =====================================
    if df.empty:

        raise ValueError(
            "Cannot export empty dataframe."
        )

    output = BytesIO()

    # =====================================
    # Create Excel File
    # =====================================
    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="Analysis"
        )

    # =====================================
    # Return Binary Data
    # =====================================
    return output.getvalue()