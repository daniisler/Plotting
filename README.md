# myplot

Minimal plotting utilities for consistently formatted scientific matplotlib figures.

## Usage

```python
import myplot as p

p.use_style()
fig, ax = p.new()
```

## Installation

Clone the repository and install in editable mode:

```bash
pip install -e .
```

## Quick start

```python
import numpy as np
import myplot as p

# Apply global plotting style
p.use_style(doc_fontsize=10, fig_width="single")

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create figure
fig, ax = p.new()

# Plot
p.line(ax, x, y, label="signal")
p.label(ax, rf"{p.bm('x')} axis", rf"{p.bm('y')} axis")
p.legend(ax)

# Save
p.save(fig, "figure.png")
```

## Plotting

```python
p.line(ax, x, y)
p.scatter(ax, x, y)
p.errorbar(ax, x, y, yerr)
```

## Subplots

```python
fig, axs = p.new(nrows=2, ncols=2)
```

## Labels and legends

```python
p.label(ax, "x", "y", "Title")
p.legend(ax)
```
## Subplot annotation

```python
p.annotate_subplots(axs)
```

## Domain specific helpers

```python
p.plot_energy(ax, t, E)
p.plot_temperature(ax, t, T)
p.plot_histogram(ax, data)
p.plot_with_error(ax, x, y, yerr)
```
