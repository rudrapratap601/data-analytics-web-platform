import streamlit as st
import pandas as pd
from sqlalchemy import text
from backend.db import get_engine


# =========================================
# Load Dataset
# =========================================
@st.cache_data(ttl=300, show_spinner=False)
def load_data(query):

    engine = get_engine()

    df = pd.read_sql(
        text(query),
        con=engine
    )

    return df