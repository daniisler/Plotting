import numpy as np

import myplots as p

# Apply global plotting style
p.use_style()

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)
y2 = x + np.random.uniform(-1, 1, len(x))

# Create figure
fig, axs = p.new(1, 2)

# Plot
p.line(axs[0], x, y, label="signal")
p.label(axs[0], f"{p.bm('x')} axis", f"{p.bm('y')} axis", "$\\sin(\\mathbfit{x})$")
p.legend(axs[0])

p.plot_parity(axs[1], x, y2, label="Data", add_rmse=True)
p.label(axs[1], rf"{p.bm('x')} axis", rf"{p.bm('y')} axis", "Parity Plot")
p.legend(axs[1])

# Save and show. No file extension will save as what is defined in p.use_style
p.save(fig, "example")
p.show()
