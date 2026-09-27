# -*- coding: utf-8 -*-
"""
Plot one figure per indicator.

Reads the long-format CSV produced by data_extract.py and draws a single
line chart (one subplot) for each indicator, saving each chart as a PNG file.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ============ Configuration ============
long_csv = "data/bank_data_long.csv"
figure_dir = "figures"
os.makedirs(figure_dir, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ============ Read the long-format table ============
df = pd.read_csv(long_csv, encoding="utf-8-sig")

indicators = sorted(df["Indicator"].unique())

# ============ Plot one subplot per image ============
for indicator in indicators:
    # Create a new figure containing a single subplot.
    fig, ax = plt.subplots(figsize=(10, 6))

    plot_df = df[df["Indicator"] == indicator].sort_values("Year")
    sns.lineplot(
        data=plot_df,
        x="Year",
        y="Value",
        hue="BankAbbr",
        marker="o",
        ax=ax
    )
    ax.set_title(indicator, fontsize=14)
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.grid(alpha=0.3)
    ax.legend(title="Bank", fontsize=9, title_fontsize=10)

    # Save each indicator as its own image file.
    fig.tight_layout()
    output_path = os.path.join(figure_dir, f"{indicator}.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved figure:", output_path)
