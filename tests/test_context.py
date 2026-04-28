import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mmcs import StyleContext


class TestStyleContext:
    def test_init(self):
        ctxt = StyleContext("graphpad_prism")
        assert ctxt.name == "graphpad_prism"

    def test_init_with_style_object(self):
        from mmcs import Style
        ctxt = StyleContext(Style("graphpad_prism"))
        assert ctxt.name == "graphpad_prism"

    def test_apply(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, chart_type="bar")
        assert plt.rcParams.get("axes.spines.top") is False

    def test_info(self):
        ctxt = StyleContext("graphpad_prism")
        assert ctxt.info["name"] == "graphpad_prism"

    def test_bar_colors_single(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, "bar")
        colors = ctxt.bar_colors(1)
        assert len(colors) == 1

    def test_bar_colors_two(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, "bar")
        colors = ctxt.bar_colors(2)
        assert len(colors) == 2
        assert colors[0] == "0.1"
        assert colors[1] == "0.8"

    def test_bar_colors_three(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, "bar")
        colors = ctxt.bar_colors(3)
        assert len(colors) == 3
        assert colors[0] == "0.1"
        assert colors[1] == "0.5"
        assert colors[2] == "0.8"

    def test_bar_colors_eight(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, "bar")
        colors = ctxt.bar_colors(8)
        assert len(colors) == 8
        assert len(set(colors)) == 8

    def test_bar_colors_more_than_palette(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, "bar")
        colors = ctxt.bar_colors(10)
        assert len(colors) == 10

    def test_scatter_colors(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, "scatter")
        colors = ctxt.scatter_colors()
        assert len(colors) > 0
        assert isinstance(colors[0], str)

    def test_box_colors(self):
        ctxt = StyleContext("graphpad_prism")
        ctxt.apply(plt.rcParams, "boxplot")
        color = ctxt.box_colors()
        assert isinstance(color, str)
        assert len(color) > 0

    def test_bar_colors_other_style(self):
        import matplotlib.pyplot as plt
        ctxt = StyleContext("ggplot")
        ctxt.apply(plt.rcParams, "bubble")
        colors = ctxt.bar_colors(2)
        assert len(colors) == 2
