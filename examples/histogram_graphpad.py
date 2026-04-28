from pathlib import Path

import numpy as np

from mmcs import histogram_chart, save_figure

root = Path(__file__).parent

np.random.seed(12)
data = np.random.normal(loc=50, scale=10, size=1000)

result = histogram_chart(
    data=data,
    xlabel="Value",
    ylabel="Frequency",
    title="Histogram",
)

save_figure(result.fig, root / "img", "histogram_graphpad")
