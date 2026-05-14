import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Data Platform", page_icon=":bar_chart:", layout="wide")

st.title("📊 Multi-Dataset Analytics Platform")
st.markdown("""
Welcome to the Multi-Dataset Analytics Platform! This tool allows you to upload multiple datasets, explore their contents, analyze relationships between them, and build custom analyses and dashboards.
""")

st.markdown("---")

st.sidebar.title("Navigation")

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

if page == "Home":
    from my_pages import home
    home.show()
elif page == "Upload Dataset":
    from my_pages import upload
    upload.show()
elif page == "Data Explorer":
    from my_pages import explorer
    explorer.show()
elif page == "Dataset Cleaner":
    from my_pages import cleaner
    cleaner.show()
elif page == "Relationships":
    from my_pages import relationships
    relationships.show()
elif page == "Analysis Builder":
    from my_pages import analysis
    analysis.show()
elif page == "Dashboard":
    from my_pages import dashboard
    dashboard.show()