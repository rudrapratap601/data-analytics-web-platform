"""
Database Schema Inspection Module

This module provides functions to inspect and retrieve metadata about
database tables and columns using PostgreSQL's information_schema.

Key Features:
    - Get list of user tables
    - Get column names and datatypes
    - Cached schema queries for performance

Dependencies:
    - SQLAlchemy: For database queries
    - Streamlit: For caching
"""

import streamlit as st

from sqlalchemy import text

from backend.db import get_engine


# =========================================
# Get All Tables
# =========================================
def get_tables():
    """
    Retrieve list of all user-uploaded tables from the database.

    This function queries PostgreSQL's information_schema to get all
    tables in the 'public' schema, excluding the internal 'relationships'
    table used for storing table joins.

    Returns:
        list: Sorted list of table names (strings)

    Query Details:
        - Schema: public (default user schema)
        - Excludes: 'relationships' (internal metadata table)
        - Sort: Alphabetical by table name

    Example:
        >>> tables = get_tables()
        >>> print(tables)
        ['customers', 'orders', 'products']

    Note:
        Returns empty list if no user tables exist.
    """
    engine = get_engine()

    # Query information_schema for user tables
    query = """
    SELECT table_name

    FROM information_schema.tables

    WHERE table_schema = 'public'

    AND table_name != 'relationships'

    ORDER BY table_name
    """

    with engine.connect() as connection:

        result = connection.execute(
            text(query)
        )

        # Extract table names from result rows
        return [

            row[0]

            for row in result.fetchall()
        ]


# =========================================
# Get Columns
# =========================================
@st.cache_data(
    ttl=600,  # Cache for 10 minutes
    show_spinner=False
)
def get_columns(table_name):
    """
    Retrieve column metadata for a specific table.

    This function queries PostgreSQL's information_schema to get
    column names and datatypes for a given table. Results are cached
    for 10 minutes to improve performance.

    Args:
        table_name (str): Name of the table to inspect

    Returns:
        list: List of tuples containing (column_name, data_type)

    Query Details:
        - Uses parameterized query for SQL injection safety
        - Orders columns by their position in the table
        - Returns PostgreSQL native datatypes (e.g., INTEGER, TEXT, TIMESTAMP)

    Example:
        >>> columns = get_columns('customers')
        >>> print(columns)
        [('id', 'integer'), ('name', 'text'), ('created_at', 'timestamp')]

    Cache Behavior:
        - TTL: 600 seconds (10 minutes)
        - Cache key: table_name
        - No loading spinner displayed during cache retrieval

    Note:
        Returns empty list if table doesn't exist.
    """
    engine = get_engine()

    # Query information_schema for column metadata
    query = """
    SELECT

        column_name,
        data_type

    FROM information_schema.columns

    WHERE table_schema = 'public'

    AND table_name = :table_name

    ORDER BY ordinal_position
    """

    with engine.connect() as connection:

        # Execute parameterized query for safety
        result = connection.execute(
            text(query),
            {
                "table_name": table_name
            }
        )

        # Return list of (column_name, data_type) tuples
        return result.fetchall()