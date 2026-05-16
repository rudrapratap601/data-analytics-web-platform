import streamlit as st


def show():

    # =====================================
    # Page Title
    # =====================================
    st.title(
        "🏠 Multi-Dataset Analytics Platform"
    )

    # =====================================
    # Getting Started
    # =====================================
    st.subheader("🚀 Getting Started")

    st.markdown("""
    ### Suggested Workflow

    1. Upload your datasets
    2. Explore dataset structure
    3. Clean column names and datatypes
    4. Create relationships between tables
    5. Build dashboards and analysis
    6. Export reports and charts

    👉 Start by visiting the
    **Upload Dataset** section.
    """)

    st.markdown("---")


    # =====================================
    # Important Notice
    # =====================================
    st.warning("""
    ⚠️ Important Dataset Notice

    This platform works best with
    already cleaned and structured datasets.

    The Dataset Cleaner currently supports
    only BASIC cleaning operations such as:

    - Column name formatting
    - Datatype conversion

    It DOES NOT automatically:

    - Fix inconsistent values
    - Replace missing/null values
    - Remove duplicate rows
    - Correct corrupted records
    - Standardize mixed formatting
    - Detect invalid values

    For accurate analysis and dashboards,
    datasets should be properly cleaned
    before upload.

    ✅ Recommended:
    Use clean CSV datasets for faster
    loading and better performance.

    ⚠️ Large datasets are supported,
    but upload, loading, analysis,
    and dashboard generation may
    take more time.
    """)

    st.markdown("---")

    # =====================================
    # Platform Introduction
    # =====================================
    st.markdown("""
    Build dashboards, perform analysis,
    explore insights, and connect
    multiple datasets in one platform.
    """)

    st.markdown("---")

    # =====================================
    # Features
    # =====================================
    st.subheader("📌 Platform Features")

    st.markdown("""
    ### 📂 Dataset Management
    - Upload multiple datasets
    - Support for CSV and Excel files
    - Store datasets in PostgreSQL

    ### 🔍 Data Exploration
    - Preview datasets
    - View datatypes and columns
    - Generate quality reports
    - Inspect missing values

    ### 🧹 Dataset Cleaning
    - Rename columns
    - Convert datatypes
    - Save cleaned datasets
    
    ### 🔗 Relationship Builder
    - Define relationships between tables

    ### 🔎 Dataset Analysis
    - Genarate insights and trends
    - Perform aggregations

    ### 📊 Dashboard Builder
    - Generate charts dynamically
    - Perform aggregations
    - Time-series analysis
    - Export dashboard results
    """)

    st.markdown("---")

    # =====================================
    # Supported Formats
    # =====================================
    st.subheader("📂 Supported File Formats")

    st.markdown("""
    ✅ CSV (.csv)

    ✅ Excel (.xlsx)
    """)

    st.info("""
    CSV files are strongly recommended
    because they usually:

    - Load faster
    - Use less memory
    - Improve dashboard performance
    - Reduce upload issues
    """)

    st.markdown("---")

    # =====================================
    # Dataset Recommendations
    # =====================================
    st.subheader("✅ Recommended Dataset Practices")

    st.markdown("""
    For best performance and accurate analysis:

    - Use clean datasets
    - Remove duplicate rows
    - Handle missing values beforehand
    - Use meaningful column names
    - Keep consistent datatypes
    - Validate date formats
    - Remove unnecessary columns
    - Avoid corrupted rows
    """)

    st.markdown("---")

    # =====================================
    # Performance Notes
    # =====================================
    st.subheader("⚡ Performance Notes")

    st.warning("""
    Large datasets are supported,
    but they may require more time for:

    - Uploading
    - Loading
    - Cleaning
    - Joining datasets
    - Aggregation
    - Dashboard generation
    - Chart rendering

    Smaller optimized datasets
    will provide faster performance.
    """)

    st.markdown("---")

    # =====================================
    # Common Dataset Problems
    # =====================================
    st.subheader("⚠️ Common Dataset Problems")

    st.warning("""
    Datasets with the following issues
    may produce incorrect analysis
    or visualization problems:

    - Mixed datatypes
    - Invalid delimiters
    - Corrupted rows
    - Inconsistent formatting
    - Duplicate records
    - Missing values
    - Invalid dates
    - Extremely high-cardinality columns
    """)

    st.markdown("---")

    
    # =====================================
    # Footer
    # =====================================
    st.caption("""
    Multi-Dataset Analytics Platform
    | Streamlit + PostgreSQL + Pandas
    """)