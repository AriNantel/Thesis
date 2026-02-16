import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load your CSV ---
# Example CSV structure: columns = ['p_or_m', 'steps', 'graph_type']
df = pd.read_csv("GNP scatter plot - Sheet1.csv")

# --- Set professional plotting style ---
sns.set(style="whitegrid")  # Clean background
plt.rcParams.update({
    "font.size": 12,          # Font size
    "axes.titlesize": 14,     # Title size
    "axes.labelsize": 12,     # Axis label size
    "legend.fontsize": 12,    # Legend size
})

# --- Create scatter plot ---
plt.figure(figsize=(6,4))  # Width x Height in inches

# Example: x = parameter (p or m), y = steps, color = graph type
sns.scatterplot(
    data=df,
    x="Density",
    y="Steps",
    hue="p Parameter",      # Different colors for graph types
    style="p Parameter",    # Different markers for graph types
    s=80,                  # Marker size
    palette="deep",        # Color palette
    edgecolor="k",         # Black border around points
    alpha=0.8              # Slight transparency
)

'''sns.regplot(
    data=df,
    x="Density",
    y="Steps",
    scatter=False,      # don't redraw points
    color="black",
    line_kws={"linewidth": 2, "linestyle": "--"}
) '''   

sns.regplot(
    data=df,
    x="Density",
    y="Steps",
    scatter=False,
    logx=True,
    color="black",
    line_kws={"linewidth": 2, "linestyle": "--"}
)

#plt.xscale("log")
#plt.yscale("log")

# --- Labels and title ---
plt.xlabel("Density")
plt.ylabel("Number of Steps")
plt.title("G(n,p): Density vs Steps")

# Optional: grid and layout
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# --- Save figure as vector graphic ---
plt.savefig("scatter_plot.pdf")  # PDF for crisp LaTeX
plt.savefig("scatter_plot.png", dpi=300)  # High-res PNG if needed

# --- Show plot ---
plt.show()
