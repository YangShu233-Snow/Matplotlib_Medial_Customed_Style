import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

from mmcs._utils import calculate_bandwidth, save_figure, significance_stars


class TestCalculateBandwidth:
    @pytest.fixture
    def data(self):
        np.random.seed(42)
        return np.random.normal(500, 150, 100)

    def test_scott_returns_positive(self, data):
        bw = calculate_bandwidth(data, "scott")
        assert bw > 0

    def test_silverman_returns_positive(self, data):
        bw = calculate_bandwidth(data, "silverman")
        assert bw > 0

    def test_scott_vs_silverman(self, data):
        scott = calculate_bandwidth(data, "scott")
        silver = calculate_bandwidth(data, "silverman")
        assert not np.isclose(scott, silver)

    def test_invalid_method(self, data):
        with pytest.raises(ValueError):
            calculate_bandwidth(data, "invalid")

    def test_small_data(self):
        data = np.array([1.0, 2.0, 3.0])
        bw = calculate_bandwidth(data, "scott")
        assert bw > 0


class TestSignificanceStars:
    @pytest.mark.parametrize("p,expected", [
        (0.00001, "****"),
        (0.0005, "***"),
        (0.003, "**"),
        (0.03, "*"),
        (0.07, "ns"),
        (0.5, "ns"),
    ])
    def test_thresholds(self, p, expected):
        assert significance_stars(p) == expected


class TestSaveFigure:
    def test_saves_png_pdf(self, tmp_path):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save_figure(fig, tmp_path, "test")
        assert (tmp_path / "test.png").exists()
        assert (tmp_path / "test.pdf").exists()
        assert len(paths) == 2

    def test_saves_single_format(self, tmp_path):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save_figure(fig, tmp_path, "test", formats=["png"])
        assert (tmp_path / "test.png").exists()
        assert not (tmp_path / "test.pdf").exists()
        assert len(paths) == 1
