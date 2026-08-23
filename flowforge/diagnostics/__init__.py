"""Stylized-fact diagnostics shared by both engines."""

from flowforge.diagnostics.flow import participation_stats, sign_autocorrelation
from flowforge.diagnostics.impact import (
    execution_profile,
    impact_decay,
    square_root_law,
)

__all__ = [
    "square_root_law",
    "execution_profile",
    "impact_decay",
    "sign_autocorrelation",
    "participation_stats",
]
