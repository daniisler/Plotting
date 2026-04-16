import re
import string

import matplotlib.pyplot as plt
import numpy as np

from .style import _compute_figsize

# ============================================================
# CORE FIGURE HELPERS
# ============================================================


def new(
    nrows=1,
    ncols=1,
    sharex=False,
    sharey=False,
    figsize=None,
    aspect=0.75,
    fig_width="single",
    scale_multi_cols=0.8,
    **kwargs,
):
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
    return fig, axs


def save(fig, filename, dpi=None, **kwargs):
    """Save figure with consistent settings."""
    fig.savefig(filename, dpi=dpi, **kwargs)


def show():
    """Thin wrapper for plt.show()."""
    plt.show()


# ============================================================
# BASIC DRAWING FUNCTIONS
# ============================================================


def line(ax, x, y, label=None, **kwargs):
    """Standard line plot."""
    return ax.plot(x, y, label=label, **kwargs)


def scatter(ax, x, y, label=None, **kwargs):
    """Scatter plot."""
    return ax.scatter(x, y, label=label, **kwargs)


def errorbar(ax, x, y, yerr, label=None, **kwargs):
    """Errorbar plot with sensible defaults."""
    kwargs.setdefault("capsize", 3)
    return ax.errorbar(x, y, yerr=yerr, label=label, **kwargs)


# ============================================================
# LABELING & DECORATION
# ============================================================


def label(ax, xlabel=None, ylabel=None, title=None, **kwargs):
    """Set axis labels and title."""
    if xlabel:
        ax.set_xlabel(xlabel, **kwargs)
    if ylabel:
        ax.set_ylabel(ylabel, **kwargs)
    if title:
        ax.set_title(title, **kwargs)


def legend(ax, loc="best", **kwargs):
    """Add legend only if labeled artists exist."""
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(loc=loc, **kwargs)


def annotate_subplots(axs, x=-0.05, y=1.05):
    """Add subplot labels (a, b, c, ...)"""
    axs = np.atleast_1d(axs)
    for i, ax in enumerate(axs.flatten()):
        ax.text(x, y, string.ascii_lowercase[i], transform=ax.transAxes, weight="bold")


def finish(ax):
    """Final touches (hook for future extensions)."""
    # Placeholder for future global tweaks
    pass


# ============================================================
# DOMAIN-SPECIFIC HELPERS (MD / PHYSICS)
# ============================================================


def plot_energy(ax, t, E, **kwargs):
    """Energy vs time."""
    line(ax, t, E, **kwargs)
    label(ax, rf"${bm(t)}$", rf"${bm(E)}$ (eV)")


def plot_temperature(ax, t, T, **kwargs):
    """Temperature vs time."""
    line(ax, t, T, **kwargs)
    label(ax, rf"${bm(t)}$", rf"${bm(T)}$ (K)")


def plot_histogram(ax, data, bins=50, density=True, **kwargs):
    """Histogram with sensible defaults."""
    ax.hist(data, bins=bins, density=density, **kwargs)


def plot_with_error(ax, x, y, yerr, **kwargs):
    """Line + errorbars."""
    errorbar(ax, x, y, yerr, **kwargs)


def plot_parity(
    ax,
    x,
    y,
    add_xy=True,
    xy_color="black",
    xy_label="$x = y$",
    xy_lw=1.0,
    xy_ls="--",
    xy_alpha=0.5,
    xy_zorder=99,
    add_rmse=False,
    rmse_loc=(0.05, 0.95),
    rmse_color="black",
    rmse_fontsize=5,
    rmse_unit="",
    rmse_rescaler=1.0,
    rmse_format=".2f",
    rmse_replace_exponential=True,
    rmse_exponential_times="times",
    rmse_bbox=True,
    rmse_bbox_alpha=0.6,
    rmse_bbox_lw=0.5,
    **kwargs,
):
    """Plot parity of x and y with a dashed diagonal line."""
    ax.scatter(x, y, **kwargs)
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
            rf"$\mathrm{{RMSE}} = {rmse_sanitized}$ {rmse_unit}",
            transform=ax.transAxes,
            fontsize=rmse_fontsize,
            color=rmse_color,
            bbox=(
                dict(boxstyle="round,pad=0.2", lw=rmse_bbox_lw, alpha=rmse_bbox_alpha)
                if rmse_bbox
                else None
            ),
        )


# ============================================================
# SMALL UTILITIES
# ============================================================


def bm(x):
    """Shortcut for bold math text."""
    return rf"$\mathbfit{{{x}}}$"
