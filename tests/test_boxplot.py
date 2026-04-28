import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from mmcs.charts import boxplot


@pytest.fixture(autouse=True)
def apply_style():
    from mmcs import Style
    Style("graphpad_prism").apply(plt.rcParams, "boxplot")
    yield


class TestBoxplotRender:
    def test_basic(self):
        fig, ax = plt.subplots()
        data = [np.random.normal(500, 150, 40) for _ in range(3)]
        result = boxplot.render(ax, data)
        assert result is ax

    def test_with_labels(self):
        fig, ax = plt.subplots()
        data = [np.random.normal(500, 150, 40) for _ in range(2)]
        boxplot.render(ax, data, labels=["A", "B"])
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["A", "B"]

    def test_single_group(self):
        fig, ax = plt.subplots()
        data = [np.random.normal(500, 150, 40)]
        boxplot.render(ax, data)

    def test_custom_facecolor(self):
        fig, ax = plt.subplots()
        data = [np.random.normal(500, 150, 40)]
        boxplot.render(ax, data, patch_facecolor="#FF0000")
