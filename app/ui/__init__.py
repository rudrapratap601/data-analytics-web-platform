"""
UI Package

Provides centralized theme loading, custom styling, and reusable HTML/CSS
components for the Multi-Dataset Analytics Platform.
"""

from ui.theme import apply_theme
from ui.components import (
    render_hero,
    render_metric_card,
    render_insight_box,
    render_card,
    render_step_card,
    render_badge
)

__all__ = [
    "apply_theme",
    "render_hero",
    "render_metric_card",
    "render_insight_box",
    "render_card",
    "render_step_card",
    "render_badge"
]
