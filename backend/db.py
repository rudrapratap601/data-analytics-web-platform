from sqlalchemy import create_engine
from urllib.parse import quote_plus
import streamlit as st


def get_engine():

    db_user = st.secrets["DB_USER"]

    db_password = quote_plus(
        st.secrets["DB_PASSWORD"]
    )

    db_host = st.secrets["DB_HOST"]

    db_port = st.secrets["DB_PORT"]

    db_name = st.secrets["DB_NAME"]

    connection_string = (
        f"postgresql+psycopg2://"
        f"{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
        f"?sslmode=require"
    )

    engine = create_engine(
        connection_string
    )

    return engine