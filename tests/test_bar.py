import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from mmcs.charts import bar


@pytest.fixture(autouse=True)
def apply_style():
    from mmcs import Style
    Style("graphpad_prism").apply(plt.rcParams, "bar")
    yield


class TestBarRender:
    def test_basic(self):
        fig, ax = plt.subplots()
        result = bar.render(ax, [1200, 3500])
        assert result is ax
        assert len(ax.patches) == 2

    def test_with_groups(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100, 200], groups=["A", "B"])
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["A", "B"]

    def test_with_errors(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100, 200], errors=[10, 20])
        assert len(ax.patches) == 2

    def test_upper_only_default(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100], errors=[10])
        err_lines = ax.lines
        assert len(err_lines) > 0

    def test_upper_only_false(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100, 200], errors=[10, 20], upper_only=False)

    def test_with_stars(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100, 200], errors=[10, 20], stars=[3, 0])
        texts = [t.get_text() for t in ax.texts]
        assert "***" in texts

    def test_edge_true(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100], edge=True)
        edge = ax.patches[0].get_edgecolor()
        assert edge[3] > 0

    def test_edge_false(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100], edge=False)
        edge = ax.patches[0].get_edgecolor()
        assert edge[3] == 0

    def test_custom_colors(self):
        fig, ax = plt.subplots()
        bar.render(ax, [100, 200], colors=["red", "blue"])
        colors = [p.get_facecolor()[:3] for p in ax.patches]
        assert colors[0] == pytest.approx((1.0, 0.0, 0.0))
