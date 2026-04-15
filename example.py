import numpy as np

import myplots as p

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
p.save(fig, "example.png")
