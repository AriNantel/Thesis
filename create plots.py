import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# ── Global style ──────────────────────────────────────────────────────────────
rcParams.update({
    "font.family": "serif",
    "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
    "figure.dpi": 150,
})

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_excel("Wildfire_Burning_Alg_WS.xlsx", sheet_name="WS K9")

COL_P = "parameter"
COL_DENS = "nx.density(G)"
COL_CLUSTER = "nx,average_clustering(G)"
COL_ECC = "nx.eccentricity(G,starting_node)"
COL_STEPS = "steps"

for col in [COL_P, COL_DENS, COL_CLUSTER, COL_ECC, COL_STEPS]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

p = df[COL_P].to_numpy()
steps = df[COL_STEPS].to_numpy()

def make_plot(x, xlabel, title):

    fig, ax = plt.subplots(figsize=(7,4.2))

    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#d9d9d9", linewidth=1.0, alpha=0.6)

    sc = ax.scatter(
        x,
        steps,
        c=p,
        cmap="viridis",
        s=28,
        alpha=0.75,
        edgecolors="white",
        linewidths=0.3,
    )

    # log regression
    mask = x > 0
    log_x = np.log(x[mask])
    coeffs = np.polyfit(log_x, steps[mask], 1)

    x_line = np.linspace(min(x), max(x), 300)
    y_line = coeffs[0] * np.log(x_line) + coeffs[1]

    ax.plot(x_line, y_line, color="black", linewidth=1.5)

    ax.set_xlabel(xlabel, labelpad=8)
    ax.set_ylabel("Number of Steps", labelpad=8)
    ax.set_title(title, pad=10)

    cbar = fig.colorbar(sc, ax=ax, pad=0.03)
    cbar.set_label(r"$p$", rotation=0, labelpad=12)

    plt.tight_layout()
    plt.show()


# Graph 1
make_plot(df[COL_DENS].to_numpy(),"Density","Watts-Strogatz (K = 9): Density vs Steps")

# Graph 2
make_plot(df[COL_CLUSTER].to_numpy(),"Average Clustering","Watts-Strogatz (K = 9): Average Clustering vs Steps")

# Graph 3
make_plot(df[COL_ECC].to_numpy(),"Eccentricity (Starting Node)","Watts-Strogatz (K = 9): Eccentricity vs Steps")