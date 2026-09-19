"""
Home Page Module

Displays the platform welcome page with:
    - Modern Hero header and platform overview
    - Interactive 6-step workflow guide with glassmorphism cards
    - Feature grid showcase with status badges
    - Supported file formats and performance recommendations
    - Common dataset quality best practices

This is the landing page users see when they first open the application.
"""

import streamlit as st
from ui.components import (
    render_hero,
    render_step_card,
    render_metric_card
)


def show():
    """
    Render the modernized home page with platform introduction and guidance.

    Displays comprehensive information about:
        - Modern hero banner with quick statistics
        - Suggested workflow (6-step process with glass cards)
        - Dataset requirements and best practices
        - Platform features grid
        - Supported file formats (CSV, Excel)
        - Performance recommendations
    """

    # =====================================
    # Hero Banner
    # =====================================
    render_hero(
        title="Multi-Dataset Analytics Platform",
        subtitle="Connect multiple datasets, run SQL aggregations, build dashboards, and generate AI insights in real-time.",
        badge="Enterprise Analytics v2.0"
    )

    # =====================================
    # Quick KPI Summary Row
    # =====================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card("Supported Formats", "CSV & XLSX", icon="📁", subtext="UTF-8 & Excel")

    with col2:
        render_metric_card("Analysis Engine", "PostgreSQL", icon="⚡", subtext="Server-side SQL")

    with col3:
        render_metric_card("Visualization", "Plotly Express", icon="📈", subtext="Interactive Charts")

    with col4:
        render_metric_card("AI Insights", "Statistical", icon="🧠", subtext="Automated Insights")

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # =====================================
    # Suggested Workflow Section
    # =====================================
    st.subheader("🚀 Suggested Workflow")
    st.caption("Follow these 6 streamlined steps to turn raw files into actionable dashboards")

    wcol1, wcol2 = st.columns(2)

    with wcol1:
        render_step_card(
            1,
            "Upload Datasets",
            "Upload your CSV or Excel files. Table names and column names are automatically sanitized for PostgreSQL."
        )
        render_step_card(
            2,
            "Explore Data & Schema",
            "Browse data rows, inspect datatypes, and view server-side missing value quality reports."
        )
        render_step_card(
            3,
            "Clean & Format Columns",
            "Rename columns to clean names and convert datatypes to proper SQL formats."
        )

    with wcol2:
        render_step_card(
            4,
            "Define Relationships",
            "Map primary/foreign key connections between datasets to unlock multi-table JOINs."
        )
        render_step_card(
            5,
            "Build SQL Analyses",
            "Run single or multi-table aggregations (SUM, AVG, COUNT, MAX, MIN) with dynamic GROUP BY."
        )
        render_step_card(
            6,
            "Generate Dashboards",
            "Render Plotly charts, review automated statistical AI insights, and export summary CSVs."
        )

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # =====================================
    # Platform Features Grid
    # =====================================
    st.subheader("📌 Platform Capabilities")

    fcol1, fcol2, fcol3 = st.columns(3)

    with fcol1:
        st.markdown("""
        <div class="glass-card" style="min-height: 200px;">
            <div style="font-size: 1.6rem; margin-bottom: 8px;">🗄️</div>
            <h4 style="color: #f8fafc; margin-bottom: 6px;">Database Storage</h4>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Persist your datasets directly into PostgreSQL (Supabase) with chunked loading for large file handling.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with fcol2:
        st.markdown("""
        <div class="glass-card" style="min-height: 200px;">
            <div style="font-size: 1.6rem; margin-bottom: 8px;">🔗</div>
            <h4 style="color: #f8fafc; margin-bottom: 6px;">Multi-Table JOINs</h4>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Connect relational datasets via foreign keys and execute complex multi-table SQL queries seamlessly.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with fcol3:
        st.markdown("""
        <div class="glass-card" style="min-height: 200px;">
            <div style="font-size: 1.6rem; margin-bottom: 8px;">📊</div>
            <h4 style="color: #f8fafc; margin-bottom: 6px;">Smart Chart Engine</h4>
            <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">
                Automatic chart recommendation based on column datatypes with dark glassmorphic Plotly styling.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # =====================================
    # Best Practices & Guidelines
    # =====================================
    gcol1, gcol2 = st.columns(2)

    with gcol1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #10b981; margin-bottom: 10px;">✅ Recommended Dataset Practices</h4>
            <ul style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.8; padding-left: 20px; margin: 0;">
                <li>Use clean <b>CSV files</b> for fastest upload & query performance</li>
                <li>Ensure unique identifiers exist for relational table joins</li>
                <li>Keep consistent datetime formats (e.g. <code>YYYY-MM-DD</code>)</li>
                <li>Remove redundant columns before uploading large datasets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with gcol2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #f59e0b; margin-bottom: 10px;">⚠️ Important Dataset Notice</h4>
            <p style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; margin: 0;">
                The platform executes aggregations directly on PostgreSQL. For optimal results, ensure datasets
                do not contain corrupted delimiters or invalid characters. Free-tier cloud databases may take 30-60s
                to wake up from sleep mode.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    # =====================================
    # Footer
    # =====================================
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 20px 0;">
        Multi-Dataset Analytics Platform &bull; Powered by Streamlit, PostgreSQL & Plotly Express
    </div>
    """, unsafe_allow_html=True)
