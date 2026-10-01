import re
import string
from typing import Tuple, List
from matplotlib.collections import PathCollection
from matplotlib.container import ErrorbarContainer
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from .style import _compute_figsize

# ============================================================
# CORE FIGURE HELPERS
# ============================================================


def new(
    nrows: int = 1,
    ncols: int = 1,
    sharex: bool = False,
    sharey: bool = False,
    figsize: Tuple[float, float] | None = None,
    aspect: float = 0.75,
    fig_width: str | float = "single",
    scale_multi_cols: float = 0.8,
    **kwargs,
) -> Tuple[Figure, Axes | List[Axes]]:
    """Create a new figure with consistent defaults."""
    if figsize is None:
        # Get figure size
        figsize = _compute_figsize(
            nrows=nrows,
            ncols=ncols,
            aspect=aspect,
            fig_width=fig_width,
            scale_multi_cols=scale_multi_cols,
        )

    fig, axs = plt.subplots(
        nrows,
        ncols,
        sharex=sharex,
        sharey=sharey,
        figsize=figsize,
        constrained_layout=True,
        **kwargs,
    )
    axs = axs
    if isinstance(axs, np.ndarray):
        axs = list(axs.flatten())
    return fig, axs


def save(fig: Figure, filename: str | Path, dpi: int | None = None, **kwargs) -> None:
    """Save figure with consistent settings."""
    fig.savefig(str(filename), dpi=dpi, **kwargs)


def show(*args, **kwargs) -> None:
    """Thin wrapper for plt.show()."""
    plt.show(*args, **kwargs)


# ============================================================
# BASIC DRAWING FUNCTIONS
# ============================================================


def line(ax: Axes, x: np.ndarray, y: np.ndarray, label: str | None = None, **kwargs) -> list:
    """Standard line plot."""
    return ax.plot(x, y, label=label, **kwargs)


def scatter(ax: Axes, x: np.ndarray, y: np.ndarray, label: str | None = None, **kwargs) -> PathCollection:
    """Scatter plot."""
    return ax.scatter(x, y, label=label, **kwargs)


def errorbar(ax: Axes, x: np.ndarray, y: np.ndarray, yerr: np.ndarray, label: str | None = None, **kwargs) -> ErrorbarContainer:
    """Errorbar plot with sensible defaults."""
    kwargs.setdefault("capsize", 3)
    return ax.errorbar(x, y, yerr=yerr, label=label, **kwargs)


# ============================================================
# LABELING & DECORATION
# ============================================================


def label(
    ax: Axes, xlabel: str | None = None, ylabel: str | None = None, title: str | None = None, x_rotation: int = 0, y_rotation: int = 0, **kwargs
):
    """Set axis labels and title."""
    if xlabel:
        ax.set_xlabel(xlabel, **kwargs)
    if ylabel:
        ax.set_ylabel(ylabel, **kwargs)
    if title:
        ax.set_title(title, **kwargs)
    if x_rotation != 0:
        ax.tick_params(axis="x", labelrotation=x_rotation)
        for label in ax.get_xticklabels():
            label.set_ha("right")  # type: ignore
    if y_rotation != 0:
        ax.tick_params(axis="y", labelrotation=y_rotation)
        for label in ax.get_yticklabels():
            label.set_ha("right")  # type: ignore


def legend(ax: Axes, loc: str = "best", **kwargs):
    """Add legend only if labeled artists exist."""
    handles, _ = ax.get_legend_handles_labels()
    if handles:
        ax.legend(loc=loc, **kwargs)  # type: ignore


def annotate_subplots(
    axs: Axes | List | np.ndarray, x: float = -0.05, y: float = 1.05, capicalize: bool = False, add_before: str = "", add_after: str = "", **kwargs
):
    """Add subplot labels (a, b, c, ...)"""
    axes = np.atleast_1d(axs) if isinstance(axs, (list, np.ndarray)) else np.array([axs])  # type: np.ndarray
    for i, ax in enumerate(axes.flatten()):
        label = string.ascii_uppercase[i] if capicalize else string.ascii_lowercase[i]
        ax.text(
            x,
            y,
            add_before + label + add_after,
            transform=ax.transAxes,
            weight="bold",
            **kwargs,
        )


def finish(ax):
    """Final touches (hook for future extensions)."""
    # Placeholder for future global tweaks
    pass


# ============================================================
# DOMAIN-SPECIFIC HELPERS (MD / PHYSICS)
# ============================================================


def plot_energy(ax, t, E, **kwargs):
    """Energy vs time."""
    label(ax, rf"${bm(t)}$", rf"${bm(E)}$ (eV)")
    return line(ax, t, E, **kwargs)


def plot_temperature(ax, t, T, **kwargs):
    """Temperature vs time."""
    label(ax, rf"${bm(t)}$", rf"${bm(T)}$ (K)")
    return line(ax, t, T, **kwargs)


def plot_histogram(ax, data, bins=50, density=True, **kwargs):
    """Histogram with sensible defaults."""
    return ax.hist(data, bins=bins, density=density, **kwargs)


def plot_with_error(ax, x, y, yerr, **kwargs):
    """Line + errorbars."""
    return errorbar(ax, x, y, yerr, **kwargs)


def plot_parity(
    ax: Axes,
    x: np.ndarray,
    y: np.ndarray,
    xy_annotations: list[Tuple[str, Tuple[float, float], Tuple[float, float]]] | None = None,
    add_xy: bool = True,
    xy_color: str = "black",
    xy_label: str = "$x = y$",
    xy_lw: float = 1.0,
    xy_ls: str = "--",
    xy_alpha: float = 0.5,
    xy_zorder: int = 99,
    add_rmse: bool = False,
    rmse_loc: Tuple[float, float] = (0.05, 0.95),
    rmse_color: str = "black",
    rmse_fontsize: float = 5,
    rmse_unit: str = "",
    rmse_rescaler: float = 1.0,
    rmse_format: str = ".2f",
    rmse_replace_exponential: bool = True,
    rmse_exponential_times: str = "times",
    rmse_bbox: bool = True,
    rmse_bbox_alpha: float = 0.6,
    rmse_bbox_lw: float = 0.5,
    **kwargs,
) -> Axes:
    """Plot parity of x and y with a dashed diagonal line."""
    ax.scatter(x, y, **kwargs)
    if xy_annotations:
        for xy_annotation in xy_annotations:
            ax.annotate(
                xy_annotation[0],
                xy_annotation[1],
                xy_annotation[2],
                ha="center",
                va="center",
                color=xy_color,
            )
    if add_xy:
        lo = np.min([np.min(x), np.min(y)])
        hi = np.max([np.max(x), np.max(y)])
        ax.plot(
            [lo, hi],
            [lo, hi],
            color=xy_color,
            label=xy_label,
            lw=xy_lw,
            ls=xy_ls,
            alpha=xy_alpha,
            zorder=xy_zorder,
        )
    if add_rmse:
        rmse = np.sqrt(np.mean((x - y) ** 2)) * rmse_rescaler
        rmse_sanitized = f"{rmse:{rmse_format}}".replace("%", r"\%")
        if rmse_replace_exponential:
            rmse_sanitized = re.sub(
                r"[eE]\+?(\d+)",
                rf"\\{rmse_exponential_times} 10^{{\1}}",
                rmse_sanitized,
            )
            rmse_sanitized = re.sub(
                r"[eE]-(\d+)", rf"\\{rmse_exponential_times} 10^{{-\1}}", rmse_sanitized
            )
        ax.text(
            rmse_loc[0],
            rmse_loc[1],
            rf"$\mathrm{{RMSE}} = {rmse_sanitized}${rmse_unit}",
            transform=ax.transAxes,
            fontsize=rmse_fontsize,
            color=rmse_color,
            bbox=(
                dict(boxstyle="round,pad=0.2", lw=rmse_bbox_lw, alpha=rmse_bbox_alpha)
                if rmse_bbox
                else None
            ),
        )

    return ax


# ============================================================
# SMALL UTILITIES
# ============================================================


def bm(x: str) -> str:
    """Shortcut for bold math text."""
    return rf"$\mathbfit{{{x}}}$"
