# tests/test_examples.py
import os
import runpy
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
STYLE_DIR = PROJECT_ROOT / "styles"

# 动态获取所有 example.py 文件的路径
example_files = list(STYLE_DIR.glob("**/example.py"))

@pytest.mark.parametrize("example_path", example_files, ids=lambda x: x.parent.name)
def test_examples_run_without_errors(example_path, monkeypatch):
    """测试每个图表目录下的 example.py 是否能成功执行而没有报错"""

    # 禁用 plt.show()，防止运行测试时弹出图表窗口阻塞进程
    monkeypatch.setattr(plt, 'show', lambda *args, **kwargs: None)

    # 保存当前工作目录
    original_cwd = os.getcwd()

    try:
        # 很多脚本可能使用了相对路径（比如保存图片到 img/ 目录），
        # 切换到示例脚本所在的目录以确保相对路径正确工作
        os.chdir(example_path.parent)

        # 像运行普通 Python 脚本一样运行它
        runpy.run_path(example_path.name)

        # 关闭所有可能生成的 figure
        plt.close('all')
    except Exception as e:
        pytest.fail(f"执行 {example_path.parent.name} 的 example.py 失败: {e}")
    finally:
        # 恢复工作目录
        os.chdir(original_cwd)
