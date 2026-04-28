from pathlib import Path

import numpy as np

from mmcs import density_chart, save_figure

root = Path(__file__).parent

np.random.seed(42)
data = [
    np.random.normal(100, 20, 200),
    np.random.normal(130, 25, 200),
]

result = density_chart(
    data=data,
    groups=["Control", "Treatment"],
    xlabel="Value",
    ylabel="Density",
    title="Density Plot",
)

save_figure(result.fig, root / "img", "density_graphpad")
