import streamlit as st

from sqlalchemy import text

from backend.db import get_engine


# =========================================
# Get All Tables
# =========================================
def get_tables():

    engine = get_engine()

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

        return [

            row[0]

            for row in result.fetchall()
        ]


# =========================================
# Get Columns
# =========================================
@st.cache_data(
    ttl=600,
    show_spinner=False
)
def get_columns(table_name):

    engine = get_engine()

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

        result = connection.execute(
            text(query),
            {
                "table_name": table_name
            }
        )

        return result.fetchall()