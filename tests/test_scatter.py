import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from mmcs.charts import scatter


@pytest.fixture(autouse=True)
def apply_style():
    from mmcs import Style
    Style("graphpad_prism").apply(plt.rcParams, "scatter")
    yield


class TestScatterRender:
    def test_basic(self):
        fig, ax = plt.subplots()
        x = np.random.normal(50, 10, 50)
        y = np.random.normal(60, 10, 50)
        result = scatter.render(ax, x, y)
        assert result is ax
        assert len(ax.collections) == 1

    def test_with_color(self):
        fig, ax = plt.subplots()
        x = np.random.normal(50, 10, 50)
        y = np.random.normal(60, 10, 50)
        scatter.render(ax, x, y, c="red", s=30)

    def test_with_cmap(self):
        fig, ax = plt.subplots()
        x = np.random.normal(50, 10, 50)
        y = np.random.normal(60, 10, 50)
        scatter.render(ax, x, y, c=np.random.rand(50), cmap="viridis")
