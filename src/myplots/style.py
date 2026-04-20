import matplotlib as mpl
from cycler import cycler

# ============================================================
# STYLE SETUP (call once at program start)
# ============================================================


def _compute_figsize(
    nrows=1,
    ncols=1,
    fig_width="single",  # "single", "double", or float (inches)
    aspect=0.75,  # height / width
    scale_multi_cols=0.8,
) -> tuple[float, float]:
    """Compute standard figure widths which rescales when multiple subplots are present

    Args:
        fig_width (str, optional): "single" (3.4 in), "double" (7 in), or custom width in inches. Defaults to "single".
        nrows (int, optional): Number of rows in the figure grid. Defaults to 1.
        ncols (int, optional): Number of columns in the figure grid. Defaults to 1.
        aspect (float, optional): Height / width ratio. Defaults to 0.75.
        scale_multi_cols (float, optional): Scale to figsize when ncols>1. Defaults to 0.8.

    Raises:
        ValueError: If the fig_width is invalid.

    Returns:
        tuple[float, float]: (width_in, height_in) in inches
    """
    if fig_width == "single":
        width_in = 3.4
    elif fig_width == "double":
        width_in = 7.0
    elif isinstance(fig_width, (int, float)):
        width_in = float(fig_width)
    else:
        raise ValueError("fig_width must be 'single', 'double', or float")

    # Rescale if multiple subplots are present
    if ncols > 1:
        ncols *= scale_multi_cols
        nrows *= scale_multi_cols
    height_in = width_in * nrows * aspect
    width_in = width_in * ncols

    return width_in, height_in


def get_colors():
    """Get a list of colors for use in plots."""
    # --------------------------------------------------------
    # Color palette
    # --------------------------------------------------------
    colors = [
        "#1f77b4",
        "#2ca02c",
        "#9467bd",
        "#8c564b",
        "#8b2500",
        "#d62728",
        "#ff7f0e",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#225ea8",
        "#17becf",
        "#a52020",
        "#e2725b",
    ]
    return colors


def use_style(
    doc_fontsize=10.0,  # pt
    doc_textwidth="single",  # "single", "double", or float (inches)
    fig_width="single",  # "single", "double", or float (inches)
    aspect=0.75,
    dpi=300,
    format="png",
    **rcparams,
):
    """Set matplotlib style with font scaling.

    Args:
        doc_fontsize (float, optional): Font size of the main document (e.g. 10, 11, 12 pt). Defaults to 10.
        doc_textwidth (str or float, optional): "single" (6.26 in), "double" (3.07 in), or custom width in inches. Defaults to "single".
        fig_width (str or float, optional): "single" (3.4 in), "double" (7 in), or custom width in inches. Defaults to "single".
        aspect (float, optional): Height / width ratio. Defaults to 0.75.
        dpi (int, optional): Dots per inch, figure quality. Defaults to 300.
        format (str, optional): _description_. Defaults to "png".
        **rcparams: overwrites of matplotlib rcParams. Replace underscores with dots, e.g. axes_grid=False will update rcParams["axes.grid"] = False

    Raises:
        ValueError: If the fig_width is invalid
    """
    # --------------------------------------------------------
    # Standard figsize
    # --------------------------------------------------------
    width_in, height_in = _compute_figsize(
        fig_width=fig_width,
        nrows=1,
        ncols=1,
        aspect=aspect,
    )
    # --------------------------------------------------------
    # Font scaling (relative hierarchy)
    # --------------------------------------------------------
    if doc_textwidth == "single":
        textwidth = 6.26
    elif doc_textwidth == "double":
        textwidth = 3.07
    elif isinstance(doc_textwidth, (int, float)):
        textwidth = doc_textwidth
    else:
        raise ValueError("doc_textwidth must be 'single', 'double' or float")

    scale = width_in / textwidth
    base = doc_fontsize * scale

    sizes = {
        "font.size": base,
        "axes.labelsize": base,
        "axes.titlesize": base * 1.1,
        "xtick.labelsize": base * 0.9,
        "ytick.labelsize": base * 0.9,
        "legend.fontsize": base * 0.9,
    }

    colors = get_colors()

    # --------------------------------------------------------
    # Apply rcParams
    # --------------------------------------------------------
    mpl.rcParams.update(
        {
            # Figure
            "figure.figsize": (width_in, height_in),
            "figure.dpi": dpi,
            "figure.autolayout": True,
            # Fonts
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial"],
            # Axes
            "axes.labelweight": "bold",
            "axes.titleweight": "bold",
            "axes.linewidth": 1.0 * scale,
            "axes.grid": True,
            "axes.formatter.useoffset": False,
            # Ticks
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 4 * scale,
            "ytick.major.size": 4 * scale,
            "xtick.major.width": 1.0 * scale,
            "ytick.major.width": 1.0 * scale,
            # Grid
            "grid.alpha": 0.2,
            "grid.linewidth": 0.5 * scale,
            # Lines
            "lines.linewidth": 1.5 * scale,
            "lines.markersize": 4 * scale,
            # Colors
            "axes.prop_cycle": cycler("color", colors),
            # Legend
            "legend.frameon": True,
            # Saving
            "savefig.format": format,
            "savefig.bbox": "tight",
            "savefig.transparent": True,
            "svg.fonttype": "none",
            # Math text
            "mathtext.fontset": "custom",
            "mathtext.rm": "Arial",
            "mathtext.it": "Arial:italic",
            "mathtext.bf": "Arial:bold",
            "mathtext.default": "regular",
        }
    )

    # Apply font sizes last
    mpl.rcParams.update(sizes)

    # Apply overwrites from rcparams, by replacing _ with .
    overwrites = {k.replace("_", "."): v for k, v in rcparams.items()}
    mpl.rcParams.update(overwrites)
