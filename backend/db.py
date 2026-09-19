"""
Database Connection Module

This module handles PostgreSQL database connections using SQLAlchemy.
It provides functions to create database engines and check database availability.

Dependencies:
    - SQLAlchemy: ORM and database engine
    - Streamlit: For accessing secrets and caching
    - psycopg2: PostgreSQL adapter
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus
import streamlit as st


# =========================================
# Create Database Engine
# =========================================
@st.cache_resource
def get_engine():
    """
    Create and return a cached SQLAlchemy database engine.

    This function reads database credentials from Streamlit secrets
    and creates a PostgreSQL connection engine. The engine is cached
    using Streamlit's cache_resource decorator to avoid recreating
    the connection on every function call.

    Connection Details:
        - Driver: postgresql+psycopg2
        - SSL Mode: require (secure connection)
        - Pool Pre-Ping: enabled (validates connections before use)

    Returns:
        sqlalchemy.engine.Engine: Configured database engine

    Secrets Required:
        - DB_USER: PostgreSQL username
        - DB_PASSWORD: PostgreSQL password
        - DB_HOST: Database host address
        - DB_PORT: Database port (typically 5432)
        - DB_NAME: Database name

    Note:
        Password is URL-encoded to handle special characters safely.
    """
    # Read database credentials from Streamlit secrets
    db_user = st.secrets["DB_USER"]

    # URL-encode password to handle special characters
    db_password = quote_plus(
        st.secrets["DB_PASSWORD"]
    )

    db_host = st.secrets["DB_HOST"]

    db_port = st.secrets["DB_PORT"]

    db_name = st.secrets["DB_NAME"]

    # Build PostgreSQL connection string with SSL
    connection_string = (
        f"postgresql+psycopg2://"
        f"{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
        f"?sslmode=require"
    )

    # Create engine with connection validation
    engine = create_engine(
        connection_string,
        pool_pre_ping=True  # Verify connections before using them
    )

    return engine


# =========================================
# Check Database Availability
# =========================================
def database_available():
    """
    Check if the database is currently available and responsive.

    This function attempts to establish a connection to the database
    to verify it's awake and accessible. This is particularly useful
    for cloud databases (like Supabase) that may enter sleep mode
    after periods of inactivity.

    Returns:
        bool: True if database is available, False otherwise

    Use Cases:
        - Initial connection validation
        - Handling cloud database sleep/wake cycles
        - Pre-flight checks before running queries

    Note:
        Returns False for any connection error to prevent
        app crashes during database downtime.
    """
    try:
        # Get the database engine
        engine = get_engine()

        # Attempt to establish connection
        with engine.connect():
            pass  # Connection successful

        return True

    except OperationalError:
        # Database is unreachable or sleeping
        return False

    except Exception:
        # Any other connection error
        return False