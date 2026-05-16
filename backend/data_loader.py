import streamlit as st
import pandas as pd
from sqlalchemy import text

from backend.db import get_engine


# =========================================
# Load Dataset
# =========================================
@st.cache_data(
    ttl=300,
    show_spinner=False
)
def load_data(
    query,
    chunk_size=50000
):

    engine = get_engine()

    try:

        # =====================================
        # Load Query in Chunks
        # =====================================
        chunks = pd.read_sql(
            text(query),
            con=engine,
            chunksize=chunk_size
        )

        # =====================================
        # Combine Chunks Into DataFrame
        # =====================================
        df = pd.concat(
            chunks,
            ignore_index=True
        )

        return df

    except Exception as e:

        raise Exception(
            f"Failed to load data: {e}"
        )