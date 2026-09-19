"""
UI Component Helpers Module

Provides reusable HTML/CSS component rendering functions for the
Multi-Dataset Analytics Platform using the corporate glassmorphism theme.

Functions:
    render_hero: Modern hero header with gradient text and pill badge
    render_metric_card: Glassmorphic KPI / metric card with icon and value
    render_insight_box: AI insight card with glowing blue accent border
    render_card: Generic glassmorphic container card
    render_step_card: Numbered workflow step card for guides
    render_badge: Compact status/tag badge pill
    render_feature_card: Feature grid card with icon and description
"""

import streamlit as st


def render_hero(
    title,
    subtitle,
    badge=None
):
    """
    Render a modern hero banner with gradient typography and subtitle.

    Args:
        title (str): Main heading text
        subtitle (str): Descriptive subtitle text
        badge (str, optional): Pill badge text displayed above the title

    Example:
        >>> render_hero("Analytics Platform", "Explore datasets dynamically", "PRO")
    """
    badge_html = ""

    if badge:
        badge_html = f'<div class="badge-pill" style="margin-bottom: 12px;">{badge}</div>'

    html = f"""
    <div class="glass-hero">
        {badge_html}
        <div class="glass-hero-title">{title}</div>
        <div class="glass-hero-subtitle">{subtitle}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_metric_card(
    label,
    value,
    icon="📊",
    subtext=None
):
    """
    Render a glassmorphic KPI / metric card.

    Args:
        label (str): Metric label (e.g. "Total Rows", "Max Revenue")
        value (str or int or float): Main metric value displayed prominently
        icon (str, optional): Emoji or icon string. Defaults to "📊"
        subtext (str, optional): Additional contextual subtext or trend

    Example:
        >>> render_metric_card("Total Datasets", 12, icon="📂")
    """
    subtext_html = ""

    if subtext:
        subtext_html = f'<div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">{subtext}</div>'

    html = f"""
    <div class="glass-metric">
        <div class="glass-metric-icon">{icon}</div>
        <div class="glass-metric-label">{label}</div>
        <div class="glass-metric-value">{value}</div>
        {subtext_html}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_insight_box(
    text
):
    """
    Render an AI insight card with glowing blue accent border.

    Replaces standard raw markdown containers with an enhanced glass
    card featuring smooth hover animations and glowing borders.

    Args:
        text (str): Insight observation text to display

    Example:
        >>> render_insight_box("Revenue peaked in Q3 at $1.2M")
    """
    html = f"""
    <div class="glass-insight-box">
        🧠 {text}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_card(
    content_html,
    title=None
):
    """
    Render a generic glassmorphism container card.

    Args:
        content_html (str): Raw HTML content to place inside the card
        title (str, optional): Card header title

    Example:
        >>> render_card("<p>Custom content</p>", title="Overview")
    """
    title_html = ""

    if title:
        title_html = f'<h3 style="margin-top:0; color:#f8fafc; font-size:1.15rem; margin-bottom:12px;">{title}</h3>'

    html = f"""
    <div class="glass-card">
        {title_html}
        {content_html}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_step_card(
    step_num,
    title,
    description
):
    """
    Render a numbered workflow step card for guided processes.

    Args:
        step_num (int or str): Step number (e.g. 1, 2, 3)
        title (str): Step title (e.g. "Upload your datasets")
        description (str): Detailed instruction text

    Example:
        >>> render_step_card(1, "Upload Data", "Upload CSV or Excel files")
    """
    html = f"""
    <div class="glass-step-card">
        <div class="glass-step-number">0{step_num}</div>
        <div class="glass-step-content">
            <h4 style="margin: 0 0 4px 0; color: #f8fafc; font-size: 1rem;">{title}</h4>
            <p style="margin: 0; color: #94a3b8; font-size: 0.88rem; line-height: 1.5;">{description}</p>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_badge(
    text,
    variant="primary"
):
    """
    Render a compact status/tag badge pill.

    Args:
        text (str): Badge label text
        variant (str, optional): Color variant ("primary", "success", "warning", "info")

    Returns:
        str: HTML string representing the badge pill
    """
    color_map = {
        "primary": ("rgba(59, 130, 246, 0.15)", "rgba(59, 130, 246, 0.4)", "#60a5fa"),
        "success": ("rgba(16, 185, 129, 0.15)", "rgba(16, 185, 129, 0.4)", "#34d399"),
        "warning": ("rgba(245, 158, 11, 0.15)", "rgba(245, 158, 11, 0.4)", "#fbbf24"),
        "info": ("rgba(56, 189, 248, 0.15)", "rgba(56, 189, 248, 0.4)", "#38bdf8")
    }

    bg, border, color = color_map.get(variant, color_map["primary"])

    return f'<span class="badge-pill" style="background:{bg}; border-color:{border}; color:{color};">{text}</span>'
