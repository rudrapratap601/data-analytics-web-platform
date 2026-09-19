"""
Table Relationships Management Module

This module manages relationships (foreign key connections) between uploaded
datasets to enable multi-table JOIN operations for analysis and dashboards.

Key Features:
    - Create internal 'relationships' metadata table
    - Save table-to-table relationships (column mappings)
    - Load all saved relationships
    - Delete relationships by index

Storage:
    Relationships are stored in a PostgreSQL table named 'relationships'
    with schema: (id, table1, column1, table2, column2)

Dependencies:
    - SQLAlchemy: For parameterized SQL queries
    - Pandas: For loading relationship records
    - backend.db: Database connection
    - backend.data_loader: For loading relationship data
"""

import streamlit as st
import pandas as pd

from sqlalchemy import text

from backend.db import get_engine
from backend.data_loader import load_data


# =========================================
# Create Relationships Table
# =========================================
def create_relationships_table():
    """
    Create the internal 'relationships' metadata table if it doesn't exist.

    This table stores user-defined relationships between uploaded datasets
    to support multi-table JOIN queries in analysis and dashboards.

    Schema:
        - id (SERIAL PRIMARY KEY): Auto-incrementing relationship ID
        - table1 (TEXT): Name of the first table
        - column1 (TEXT): Column name in the first table
        - table2 (TEXT): Name of the second table
        - column2 (TEXT): Column name in the second table

    Example Row:
        id=1, table1='orders', column1='customer_id',
        table2='customers', column2='id'

    Note:
        Uses IF NOT EXISTS to safely handle repeated calls.
    """
    engine = get_engine()

    # Create relationships metadata table
    query = """
    CREATE TABLE IF NOT EXISTS relationships (

        id SERIAL PRIMARY KEY,

        table1 TEXT,
        column1 TEXT,

        table2 TEXT,
        column2 TEXT
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query)
        )

        conn.commit()


# =========================================
# Load Relationships
# =========================================
def load_relationships():
    """
    Load all saved relationships from the database.

    Returns:
        list: List of dictionaries containing relationship details.
              Each dict has keys: table1, column1, table2, column2

    Example:
        >>> relationships = load_relationships()
        >>> print(relationships)
        [
            {'table1': 'orders', 'column1': 'customer_id',
             'table2': 'customers', 'column2': 'id'},
            {'table1': 'orders', 'column1': 'product_id',
             'table2': 'products', 'column2': 'id'}
        ]

    Note:
        Returns an empty list if no relationships exist.
    """
    # Ensure the relationships table exists
    create_relationships_table()

    # Query all relationships
    query = """
    SELECT

        table1,
        column1,

        table2,
        column2

    FROM relationships
    """

    df = load_data(query)

    # Convert DataFrame to list of dictionaries
    return df.to_dict(
        orient="records"
    )


# =========================================
# Save Relationship
# =========================================
def save_relationship(relationship):
    """
    Save a new relationship between two tables.

    This function checks if the exact relationship already exists before
    inserting to prevent duplicates.

    Args:
        relationship (dict): Dictionary with keys:
            - table1 (str): First table name
            - column1 (str): Column in first table
            - table2 (str): Second table name
            - column2 (str): Column in second table

    Example:
        >>> rel = {
        ...     'table1': 'orders',
        ...     'column1': 'customer_id',
        ...     'table2': 'customers',
        ...     'column2': 'id'
        ... }
        >>> save_relationship(rel)

    Note:
        Silently returns (no-op) if the relationship already exists.
    """
    # Ensure the relationships table exists
    create_relationships_table()

    engine = get_engine()

    # =====================================
    # Check Existing Relationship
    # =====================================
    # Prevent duplicate relationship entries
    check_query = """
    SELECT *

    FROM relationships

    WHERE

        table1 = :table1

        AND column1 = :column1

        AND table2 = :table2

        AND column2 = :column2
    """

    with engine.connect() as conn:

        existing = conn.execute(

            text(check_query),

            relationship

        ).fetchone()

        # =================================
        # Already Exists
        # =================================
        if existing:

            return  # Relationship already saved, no action needed

        # =================================
        # Insert Relationship
        # =================================
        insert_query = """
        INSERT INTO relationships (

            table1,
            column1,

            table2,
            column2

        )

        VALUES (

            :table1,
            :column1,

            :table2,
            :column2
        )
        """

        conn.execute(

            text(insert_query),

            relationship
        )

        conn.commit()


# =========================================
# Delete Relationship
# =========================================
def delete_relationship(index):
    """
    Delete a relationship by its position in the loaded relationships list.

    Args:
        index (int): Zero-based index of the relationship to delete
                    (from load_relationships() result)

    Example:
        >>> relationships = load_relationships()
        >>> # Delete the first relationship
        >>> delete_relationship(0)

    Note:
        - Returns silently if index is out of bounds
        - Index corresponds to the order returned by load_relationships()
    """
    # Ensure the relationships table exists
    create_relationships_table()

    # Load all current relationships
    relationships = load_relationships()

    # =====================================
    # Validate Index
    # =====================================
    if (
        index < 0
        or
        index >= len(relationships)
    ):

        return  # Invalid index, no action

    # Get the specific relationship to delete
    relationship = relationships[index]

    engine = get_engine()

    # =====================================
    # Delete Query
    # =====================================
    query = """
    DELETE FROM relationships

    WHERE

        table1 = :table1

        AND column1 = :column1

        AND table2 = :table2

        AND column2 = :column2
    """

    with engine.connect() as conn:

        conn.execute(

            text(query),

            relationship
        )

        conn.commit()