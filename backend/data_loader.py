"""
Data Loading Module

This module provides efficient data loading from PostgreSQL using chunking
and caching strategies for optimal performance with large datasets.

Key Features:
    - Chunked data reading to manage memory
    - Streamlit caching with TTL
    - Error handling for database queries

Dependencies:
    - Pandas: For DataFrame operations and SQL reading
    - SQLAlchemy: For database connections
    - Streamlit: For caching
"""

import streamlit as st
import pandas as pd
from sqlalchemy import text

from backend.db import get_engine


# =========================================
# Load Dataset
# =========================================
@st.cache_data(
    ttl=300,  # Cache results for 5 minutes
    show_spinner=False
)
def load_data(
    query,
    chunk_size=50000
):
    """
    Execute a SQL query and return results as a Pandas DataFrame.

    This function reads query results in chunks to prevent memory issues
    when loading large datasets from PostgreSQL. The entire result set
    is combined into a single DataFrame and cached.

    Args:
        query (str): SQL query to execute
        chunk_size (int, optional): Number of rows to read per chunk.
                                   Defaults to 50,000.

    Returns:
        pd.DataFrame: Query results as a Pandas DataFrame

    Raises:
        Exception: If query execution or data loading fails

    Performance Strategy:
        - Uses chunked reading to handle memory efficiently
        - Concatenates chunks into single DataFrame
        - Caches results for 5 minutes (TTL=300)
        - Prevents duplicate queries for identical requests

    Example:
        >>> query = 'SELECT * FROM "sales" LIMIT 1000'
        >>> df = load_data(query)
        >>> print(f"Loaded {len(df)} rows")

    Note:
        The query parameter is used as the cache key, so identical
        queries return cached results immediately.
    """
    engine = get_engine()

    try:

        # =====================================
        # Load Query in Chunks
        # =====================================
        # Read data in batches to optimize memory usage
        chunks = pd.read_sql(
            text(query),
            con=engine,
            chunksize=chunk_size
        )

        # =====================================
        # Combine Chunks Into DataFrame
        # =====================================
        # Merge all chunks into a single DataFrame
        df = pd.concat(
            chunks,
            ignore_index=True
        )

        return df

    except Exception as e:

        # Wrap and re-raise with informative error message
        raise Exception(
            f"Failed to load data: {e}"
        )