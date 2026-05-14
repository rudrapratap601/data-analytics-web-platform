import streamlit as st

def show():

    st.title("🏠 Welcome to Multi-Dataset Analytics Platform")
    st.markdown(""" 
    ### What you can do:
    - Upload multiple datasets
    - Explore data
    - Define relationships
    - Build analysis
    - Create dashboards

    👉 Start by uploading your first dataset.
    """)

    st.markdown("---")

    st.info("""
        ✅ Recommended:
        Upload cleaned and structured CSV datasets for better analysis accuracy and dashboard performance.
        """)
    
    st.markdown("---")

    st.warning("""
        ⚠️ Datasets with inconsistent formatting, corrupted rows, or invalid delimiters may load partially.
        """)