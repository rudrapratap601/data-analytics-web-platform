"""
Data Export Module

This module provides functions to convert Pandas DataFrames into
downloadable file formats (CSV and Excel) for exporting analysis results.

Supported Export Formats:
    - CSV: Lightweight, universal format
    - Excel (XLSX): Formatted spreadsheet with sheets

Dependencies:
    - Pandas: DataFrame operations and export functions
    - openpyxl: Excel file generation engine
"""

import pandas as pd

from io import BytesIO


# =========================================
# Convert DataFrame to CSV
# =========================================
def convert_to_csv(df):
    """
    Convert a DataFrame to CSV format as UTF-8 encoded bytes.

    Args:
        df (pd.DataFrame): DataFrame to export

    Returns:
        bytes: UTF-8 encoded CSV file content

    Raises:
        ValueError: If DataFrame is empty

    Example:
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> csv_bytes = convert_to_csv(df)
        >>> # Can be used with st.download_button(data=csv_bytes)

    Note:
        - Index is excluded from export
        - Uses UTF-8 encoding for international character support
    """
    # =====================================
    # Empty Validation
    # =====================================
    if df.empty:

        raise ValueError(
            "Cannot export empty dataframe."
        )

    # Convert DataFrame to CSV string, then encode to bytes
    return df.to_csv(
        index=False
    ).encode("utf-8")


# =========================================
# Convert DataFrame to Excel
# =========================================
def convert_to_excel(df):
    """
    Convert a DataFrame to Excel (XLSX) format as binary data.

    Creates an Excel workbook with a single sheet named "Analysis"
    containing the DataFrame data.

    Args:
        df (pd.DataFrame): DataFrame to export

    Returns:
        bytes: Binary Excel file content (.xlsx format)

    Raises:
        ValueError: If DataFrame is empty

    Example:
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> excel_bytes = convert_to_excel(df)
        >>> # Can be used with st.download_button(data=excel_bytes, mime='application/vnd.ms-excel')

    Excel Features:
        - Engine: openpyxl (modern .xlsx format)
        - Sheet Name: "Analysis"
        - Index: Not included

    Note:
        - Returns in-memory binary data (no file written to disk)
        - Uses BytesIO for efficient memory handling
    """
    # =====================================
    # Empty Validation
    # =====================================
    if df.empty:

        raise ValueError(
            "Cannot export empty dataframe."
        )

    # Create in-memory binary stream
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