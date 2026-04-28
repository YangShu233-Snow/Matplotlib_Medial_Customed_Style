import matplotlib

matplotlib.use("Agg")
import numpy as np
import pandas as pd

from mmcs import ChartResult, bar_chart, box_chart, scatter_chart


class TestChartResult:
    def test_to_base64(self):
        result = bar_chart([100, 200], groups=["A", "B"])
        b64 = result.to_base64()
        assert isinstance(b64, str)
        assert len(b64) > 100
        assert result.fig is not None

    def test_stats(self):
        result = bar_chart([100, 200], groups=["A", "B"])
        assert "n_groups" in result.stats


class TestBarChart:
    def test_basic(self):
        result = bar_chart([100, 200], groups=["A", "B"])
        assert isinstance(result, ChartResult)
        assert "n_groups" in result.stats

    def test_with_errors(self):
        result = bar_chart([100, 200], errors=[10, 20])
        assert isinstance(result, ChartResult)

    def test_with_stars(self):
        result = bar_chart([100, 200], stars=[3, 0])
        assert isinstance(result, ChartResult)

    def test_dataframe_input(self):
        df = pd.DataFrame({"g": ["A", "A", "B", "B"], "v": [1, 2, 3, 4]})
        result = bar_chart(df, x="g", y="v")
        assert isinstance(result, ChartResult)

    def test_save_as(self, tmp_path):
        out = tmp_path / "test.png"
        bar_chart([100, 200], save_as=str(out))
        assert out.exists()

    def test_custom_style(self):
        result = bar_chart([100, 200], groups=["A", "B"], style="graphpad_prism")
        assert isinstance(result, ChartResult)


class TestBoxChart:
    def test_basic(self):
        data = [np.random.normal(500, 150, 40) for _ in range(2)]
        result = box_chart(data, groups=["A", "B"])
        assert isinstance(result, ChartResult)

    def test_show_n(self):
        data = [np.random.normal(500, 150, 40) for _ in range(2)]
        result = box_chart(data, show_n=True)
        assert isinstance(result, ChartResult)


class TestScatterChart:
    def test_basic(self):
        x = np.random.normal(50, 10, 50)
        y = np.random.normal(60, 10, 50)
        result = scatter_chart(x, y)
        assert isinstance(result, ChartResult)

    def test_with_labels(self):
        x = np.random.normal(50, 10, 50)
        y = np.random.normal(60, 10, 50)
        result = scatter_chart(x, y, xlabel="X", ylabel="Y", title="Test")
        assert isinstance(result, ChartResult)
