import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from backend.db import (
    database_available
)

# =========================================
# Page Config
# =========================================
st.set_page_config(
    page_title="Data Platform",
    page_icon=":bar_chart:",
    layout="wide"
)

# =========================================
# Header
# =========================================
st.title(
    "📊 Multi-Dataset Analytics Platform"
)

st.markdown("""
Welcome to the Multi-Dataset Analytics Platform!

This tool allows you to upload multiple datasets,
explore their contents, analyze relationships
between them, and build custom analyses
and dashboards.
""")

st.markdown("---")

# =========================================
# Sidebar Navigation
# =========================================
st.sidebar.title(
    "Navigation"
)

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Upload Dataset",
        "Data Explorer",
        "Dataset Cleaner",
        "Relationships",
        "Analysis Builder",
        "Dashboard"
    ]
)

# =========================================
# Home Page
# =========================================
if page == "Home":

    from my_pages import home

    home.show()

# =========================================
# Database Pages
# =========================================
else:

    # =====================================
    # Database Health Check
    # =====================================
    if not database_available():

        st.warning(
            """
⚠️ Database is currently unavailable.

The Supabase database may be waking up
from sleep mode.

Please wait 30–60 seconds and refresh
the page.

This is normal for free cloud databases.
            """
        )

        st.stop()

    # =====================================
    # Upload Dataset
    # =====================================
    if page == "Upload Dataset":

        from my_pages import upload

        upload.show()

    # =====================================
    # Data Explorer
    # =====================================
    elif page == "Data Explorer":

        from my_pages import explorer

        explorer.show()

    # =====================================
    # Dataset Cleaner
    # =====================================
    elif page == "Dataset Cleaner":

        from my_pages import cleaner

        cleaner.show()

    # =====================================
    # Relationships
    # =====================================
    elif page == "Relationships":

        from my_pages import relationships

        relationships.show()

    # =====================================
    # Analysis Builder
    # =====================================
    elif page == "Analysis Builder":

        from my_pages import analysis

        analysis.show()

    # =====================================
    # Dashboard
    # =====================================
    elif page == "Dashboard":

        from my_pages import dashboard

        dashboard.show()