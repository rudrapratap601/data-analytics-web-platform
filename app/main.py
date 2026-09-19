"""
Multi-Dataset Analytics Platform - Main Application Entry Point

This is the primary Streamlit application file that handles navigation,
page routing, and database health checks.

Navigation Structure:
    - Home: Welcome page with platform overview
    - Upload Dataset: Upload CSV/Excel files to PostgreSQL
    - Data Explorer: Browse and preview uploaded datasets
    - Dataset Cleaner: Clean column names and fix datatypes
    - Relationships: Create table-to-table relationships (JOINs)
    - Analysis Builder: Build dynamic SQL aggregations
    - Dashboard: Generate interactive Plotly visualizations

Database Strategy:
    - Checks database availability before loading data pages
    - Handles Supabase cloud database sleep/wake cycles gracefully
    - Routes navigation through sidebar radio buttons

Author: Rudrapratap Sarma
"""

import streamlit as st
import sys
import os

# Add parent directory to Python path for backend imports
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
# Apply Modern Corporate Glassmorphism Theme
# =========================================
from ui.theme import apply_theme

apply_theme()

# =========================================
# Sidebar Brand Banner
# =========================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 12px 0 20px 0;">
    <div style="font-size: 2.2rem; margin-bottom: 6px;">📊</div>
    <div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; letter-spacing: -0.02em;">Data Platform</div>
    <div style="font-size: 0.75rem; color: #3b82f6; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px;">Enterprise Analytics</div>
</div>
""", unsafe_allow_html=True)

# =========================================
# Sidebar Navigation
# =========================================
st.sidebar.title(
    "Navigation"
)

# Radio button navigation menu
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
    # Check if database is awake and reachable
    # (Supabase free tier sleeps after inactivity)
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