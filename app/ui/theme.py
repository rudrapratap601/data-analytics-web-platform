"""
Theme Loader Module

Provides centralized CSS injection for the Multi-Dataset Analytics Platform.
Loads the glassmorphism stylesheet from app/static/styles.css and injects it
into the Streamlit application using st.markdown with unsafe_allow_html.

Functions:
    apply_theme(): Load and inject the centralized CSS stylesheet
"""

import os
import streamlit as st


def apply_theme():
    """
    Load and inject the centralized glassmorphism CSS stylesheet.

    Reads the CSS file from app/static/styles.css and injects it into
    the Streamlit application DOM using st.markdown. This function should
    be called once in app/main.py immediately after st.set_page_config().

    The CSS includes:
        - Corporate dark glassmorphism color palette
        - Glass card components with backdrop blur
        - Streamlit component overrides (buttons, inputs, sidebar)
        - Navigation styling and hover effects
        - Plotly chart container styling
        - Responsive utilities

    Returns:
        None

    Side Effects:
        Injects CSS into the Streamlit DOM via st.markdown

    Example:
        >>> from ui.theme import apply_theme
        >>> st.set_page_config(page_title="App", layout="wide")
        >>> apply_theme()
    """

    # Build absolute path to the CSS file
    css_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "static",
        "styles.css"
    )

    # Check if CSS file exists
    if os.path.exists(css_path):

        # Read the CSS content
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Inject CSS into Streamlit DOM
        st.markdown(
            f"<style>{css_content}</style>",
            unsafe_allow_html=True
        )

    else:

        # Warn if stylesheet is missing
        st.warning(
            f"⚠️ Theme stylesheet not found at: {css_path}"
        )
