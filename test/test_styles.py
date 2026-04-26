# tests/test_styles.py
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

# 获取项目根目录下的 styles 文件夹路径
PROJECT_ROOT = Path(__file__).parent.parent
STYLE_DIR = PROJECT_ROOT / "styles"

# 动态获取所有 .mplstyle 文件的路径
style_files = list(STYLE_DIR.glob("**/*.mplstyle"))

@pytest.mark.parametrize("style_path", style_files, ids=lambda x: x.parent.parent.name)
def test_style_loads(style_path):
    """测试所有的 .mplstyle 文件能否被正确解析和加载"""
    try:
        # 使用 context manager 临时应用样式，防止污染全局设置
        with plt.style.context(style_path):
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 4, 9])
            # 画图后关闭，避免内存泄漏
            plt.close(fig)
    except Exception as e:
        pytest.fail(f"无法加载样式文件 {style_path.name}，错误信息: {e}")
