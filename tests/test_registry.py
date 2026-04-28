import mmcs


def test_list_styles():
    styles = mmcs.list_styles()
    names = [s["name"] for s in styles]
    assert "graphpad_prism" in names
    assert "deeptools" in names
    assert "ggplot" in names


def test_list_styles_returns_metadata():
    for s in mmcs.list_styles():
        assert "name" in s
        assert "category" in s
        assert "chart_types" in s
        assert isinstance(s["chart_types"], list)
        assert s["base_style"] is None or s["base_style"].endswith(".mplstyle")


def test_list_styles_for_bar():
    result = mmcs.list_styles_for("bar")
    assert any(s["name"] == "graphpad_prism" for s in result)
    assert not any(s["name"] == "deeptools" for s in result)


def test_list_styles_for_heatmap():
    result = mmcs.list_styles_for("heatmap")
    assert any(s["name"] == "deeptools" for s in result)


def test_get_style_found():
    s = mmcs.get_style("graphpad_prism")
    assert s is not None
    assert s["name"] == "graphpad_prism"
    assert s["base_style"] is not None
    assert "bar" in s["chart_styles"]
    assert "bar" in s["chart_types"]


def test_get_style_not_found():
    assert mmcs.get_style("nonexistent") is None


def test_get_style_chart_styles():
    s = mmcs.get_style("deeptools")
    assert "heatmap_clustered" in s["chart_styles"]
    assert "heatmap_multi" in s["chart_styles"]
