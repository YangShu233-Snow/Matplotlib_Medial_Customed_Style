from pathlib import Path

import numpy as np

from mmcs import heatmap_chart, save_figure

root = Path(__file__).parent

np.random.seed(12)
gene_names = [f"Gene_{i}" for i in range(50)]
sample_names = [f"Sample_{i}" for i in range(20)]
data = np.random.randn(50, 20)

result = heatmap_chart(
    data=data,
    row_labels=gene_names,
    col_labels=sample_names,
    style="deeptools",
    vmin=-3,
    vmax=3,
    cmap="RdBu_r",
    colorbar_label="$\\log_2$(Value)",
    title="Clustered Genomic Heatmap",
)

save_figure(result.fig, root / "img", "heatmap_deeptools", tight_layout=False)
