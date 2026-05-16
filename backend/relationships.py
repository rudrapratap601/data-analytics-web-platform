import streamlit as st
import pandas as pd

from sqlalchemy import text

from backend.db import get_engine
from backend.data_loader import load_data


# =========================================
# Create Relationships Table
# =========================================
def create_relationships_table():

    engine = get_engine()

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

    create_relationships_table()

    query = """
    SELECT

        table1,
        column1,

        table2,
        column2

    FROM relationships
    """

    df = load_data(query)

    return df.to_dict(
        orient="records"
    )


# =========================================
# Save Relationship
# =========================================
def save_relationship(relationship):

    create_relationships_table()

    engine = get_engine()

    # =====================================
    # Check Existing Relationship
    # =====================================
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

            return

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

    with st.spinner(
        "Deleting relationship..."
    ):

        create_relationships_table()

        relationships = load_relationships()

        if (
            index < 0
            or
            index >= len(relationships)
        ):

            return

        relationship = relationships[index]

        engine = get_engine()

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