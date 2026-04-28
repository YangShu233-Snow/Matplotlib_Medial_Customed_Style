import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from mmcs import Style


class TestStyle:
    def test_init_valid(self):
        s = Style("graphpad_prism")
        assert s.name == "graphpad_prism"

    def test_init_unknown(self):
        with pytest.raises(ValueError, match="Unknown style"):
            Style("nonexistent")

    def test_info(self):
        s = Style("graphpad_prism")
        info = s.info
        assert info["name"] == "graphpad_prism"
        assert "chart_types" in info
        assert info["base_style"] is not None

    @pytest.mark.parametrize("style_name", ["graphpad_prism", "deeptools", "ggplot"])
    def test_apply_modifies_rcparams(self, style_name):
        s = Style(style_name)
        s.apply(plt.rcParams)
        assert "font.family" in plt.rcParams

    def test_apply_chart_type(self):
        s = Style("graphpad_prism")
        s.apply(plt.rcParams, chart_type="bar")
        assert plt.rcParams.get("axes.spines.top") is False
        assert plt.rcParams.get("axes.spines.right") is False

    def test_apply_chart_type_unknown(self):
        s = Style("graphpad_prism")
        s.apply(plt.rcParams, chart_type="nonexistent")
        assert plt.rcParams.get("axes.spines.top") is False
