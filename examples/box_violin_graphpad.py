from pathlib import Path

import numpy as np

from mmcs import box_violin_chart, save_figure

root = Path(__file__).parent

np.random.seed(12)
data = [
    np.random.normal(200, 80, 200),
    np.random.normal(800, 500, 150),
    np.random.normal(600, 100, 180),
]

result = box_violin_chart(
    data=data,
    groups=[f"Sample {i+1}" for i in range(3)],
    ylabel="Value",
    title="Box-Violin Plot",
)

save_figure(result.fig, root / "img", "box_violin_graphpad")
