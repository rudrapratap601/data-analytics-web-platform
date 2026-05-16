import streamlit as st

from backend.schema import (
    get_tables,
    get_columns
)

from backend.relationships import (
    save_relationship,
    load_relationships,
    delete_relationship
)


# =========================================
# MAIN PAGE
# =========================================
def show():

    st.title("🔗 Relationship Builder")

    st.markdown("""
    Define relationships between datasets
    to enable multi-table analysis
    and dashboard generation.
    """)

    st.markdown("---")

    # =====================================
    # Load Tables
    # =====================================
    with st.spinner(
        "Loading datasets..."
    ):

        tables = get_tables()

    # =====================================
    # Validation
    # =====================================
    if len(tables) < 2:

        st.warning(
            "At least 2 datasets are required to create relationships."
        )

        return

    # =====================================
    # Select Tables
    # =====================================
    st.subheader(
        "Step 1: Select Tables"
    )

    table_options = [
        "🔽 Select a table"
    ] + tables

    col1, col2 = st.columns(2)

    with col1:

        table1 = st.selectbox(
            "Select First Table",
            table_options,
            key="table1"
        )

    with col2:

        table2 = st.selectbox(
            "Select Second Table",
            table_options,
            key="table2"
        )

    # =====================================
    # Validation Messages
    # =====================================
    if (
        table1 == "🔽 Select a table"
        or
        table2 == "🔽 Select a table"
    ):

        st.info(
            "Please select both tables."
        )

    elif table1 == table2:

        st.warning(
            "Please select different tables."
        )

    # =====================================
    # VALID CONFIGURATION
    # =====================================
    else:

        st.markdown("---")

        # =================================
        # Load Columns
        # =================================
        with st.spinner(
            "Loading table columns..."
        ):

            columns1 = get_columns(
                table1
            )

            columns2 = get_columns(
                table2
            )

        # =================================
        # Extract Column Names
        # =================================
        column_names1 = [

            col[0]

            for col in columns1
        ]

        column_names2 = [

            col[0]

            for col in columns2
        ]

        # =================================
        # Select Matching Columns
        # =================================
        st.subheader(
            "Step 2: Select Matching Columns"
        )

        col3, col4 = st.columns(2)

        with col3:

            column1 = st.selectbox(
                f"{table1} Column",
                column_names1
            )

        with col4:

            column2 = st.selectbox(
                f"{table2} Column",
                column_names2
            )

        st.markdown("---")

        # =================================
        # Create Relationship
        # =================================
        if st.button(
            "Create Relationship"
        ):

            relationship = {

                "table1": table1,
                "column1": column1,

                "table2": table2,
                "column2": column2
            }

            with st.spinner(
                "Creating relationship..."
            ):

                save_relationship(
                    relationship
                )

            st.success(
                "✅ Relationship created successfully!"
            )

            st.cache_data.clear()

            st.rerun()

    # =====================================
    # Existing Relationships
    # =====================================
    st.markdown("---")

    st.subheader(
        "📌 Existing Relationships"
    )

    # =====================================
    # Load Relationships
    # =====================================
    with st.spinner(
        "Loading relationships..."
    ):

        relationships = load_relationships()

    # =====================================
    # Empty State
    # =====================================
    if not relationships:

        st.info(
            "No relationships created yet."
        )

        return

    # =====================================
    # Show Relationships
    # =====================================
    for index, rel in enumerate(
        relationships
    ):

        st.write(
            f"""
            🔗 {rel['table1']}.{rel['column1']}
            ↔
            {rel['table2']}.{rel['column2']}
            """
        )

        if st.button(

            f"Delete Relationship {index + 1}",

            key=f"delete_rel_{index}"
        ):

            with st.spinner(
                "Deleting relationship..."
            ):

                delete_relationship(
                    index
                )

            st.success(
                "Relationship deleted successfully."
            )

            st.cache_data.clear()

            st.rerun()