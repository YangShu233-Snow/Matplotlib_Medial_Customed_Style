import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import numpy as np
import pytest

from mmcs import Style, StyleContext

STYLES_DIR = Path(__file__).parent.parent / "mmcs" / "styles"


@pytest.fixture(autouse=True)
def close_figs():
    yield
    import matplotlib.pyplot as plt
    plt.close("all")


@pytest.fixture
def graphpad_style():
    return Style("graphpad_prism")


@pytest.fixture
def graphpad_ctxt():
    return StyleContext("graphpad_prism")


@pytest.fixture
def sample_data():
    np.random.seed(42)
    return [np.random.normal(500, 150, 40) for _ in range(3)]
