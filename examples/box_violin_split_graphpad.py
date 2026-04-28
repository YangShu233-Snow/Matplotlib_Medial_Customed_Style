from pathlib import Path

import numpy as np

from mmcs import box_violin_chart, save_figure

root = Path(__file__).parent

np.random.seed(12)
data = [
    [np.random.normal(200, 50, 100), np.random.normal(250, 60, 100)],
    [np.random.normal(800, 150, 100), np.random.normal(700, 180, 100)],
    [np.random.normal(400, 80, 100), np.random.normal(500, 90, 100)],
]

result = box_violin_chart(
    data=data,
    groups=[f"Sample {i+1}" for i in range(3)],
    split=True,
    split_labels=["Control", "Treatment"],
    ylabel="Relative Expression",
    title="Split Box-Violin Plot",
)

save_figure(result.fig, root / "img", "box_violin_split_graphpad")
