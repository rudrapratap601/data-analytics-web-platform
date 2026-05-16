from sqlalchemy import create_engine
import streamlit as st


def get_engine():

    database_url = st.secrets["DATABASE_URL"]

    engine = create_engine(
        database_url
    )

    return engine