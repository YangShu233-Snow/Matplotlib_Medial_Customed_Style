# Introduction

非常感谢你愿意为本项目贡献代码与创意，Matplotlib_Medial_Customed_Style 项目将因此受益良多。

本项目旨在收集、编写与整理各种适于医学领域论文风格的图表样式，并用 Python 库 `matplotlib` 来实现它们，本项目期望这些已有的脚本代码能够帮助科研工作者免于每次烦扰的样式调整。

无论是脚本、样式调整与建议、甚至是脚本中所使用的示例数据纠错，都欢迎你的补充与分享！！

## 提交前准备

### 开发环境配置

在开始贡献之前，请确保你已经配置好了开发环境。我们使用 `pyproject.toml` 来管理依赖，你可以通过以下命令安装包含测试工具在内的所有开发依赖：

```bash
git clone https://github.com/YangShu233-Snow/matplotlib_GraphPad_style
cd matplotlib-medial-customed-style
pip install -e ".[dev]"
```

### 运行自动化测试

为了确保项目的稳定性，我们编写了自动化测试与代码检查脚本。**在提交任何 Pull Request 之前，请务必在本地完整运行一遍检查。**

在项目根目录下执行：

```bash
./scripts/check.sh
```

该脚本会依次执行：

1. **ruff** — Python 代码风格检查（必需，未安装则报错）
2. **rumdl** — Markdown 风格检查（可选，未安装则跳过并提示）
3. **markdownlint-cli** — Markdown 风格检查（可选，通过 `npx` 运行，未安装则跳过）
4. **pytest** — 自动化测试（必需，未安装则报错）

测试主要涵盖以下内容：

1. **样式合法性测试**：确保所有的 `.mplstyle` 文件都能被 `matplotlib` 正确解析。
2. **示例脚本运行测试**：模拟运行每个样式下的 `example.py`，确保脚本没有语法错误且能正常生成图表。

如果你的代码修改导致测试失败或 lint 报错，请务必在修复后再提交。

> 提示：你也可以跳过可选检查单独运行 `pytest -v`。可选工具（rumdl、markdownlint-cli）仅在你本地已安装时才会生效。

### 提交类型

本项目欢迎的提交类型包括：

- 完整的样式，它至少应当包含如下的文件结构：

    ```text
    style_name
        |-- assets
        |   `-- your_style.mplstyle
        |-- example.py
        |-- img
        |   `-- example.png
        `-- readme.md
    ```

- 对任何已经存在的样式调整，包含修改 `mplstyle` 文件或 `example.py` 代码
- 对样式示例数据的纠正，如果它不符合特定图标的需求（请原谅我可能缺乏特定领域的专业知识）

可能会被拒绝的提交类型包括：

- 仅有示例图片的提交（如果你需要项目实现或加入某种图表样式，应当在 Issue 中提出）
- 示例图片、样式、代码和 `readme.md` 描述不统一。
- 一个样式的提交，但样式耦合在 `example.py`中。（如果你想贡献一个新样式，请尽可能将大多数样式独立到 `mplstyle` 文件中）

### 提交规范

根据你想提交类型的不同，请阅读对应类型的规范。

#### 完整样式贡献

请确保你的 Pull Request 符合以下规范：

- 完整的项目结构：

    ```text
    style_name
        |-- assets
        |   `-- your_style.mplstyle
        |-- example.py
        |-- img
        |   `-- example.png
        `-- readme.md
    ```

- 在 Pull Requests 中包含样式名称、样式介绍与例图（这一部分完全可以复制样式中的 `readme.md`）
- `example.py` 应尽可能遵循项目原有的代码风格：

  ```py
  # import something
  import matplotlib.pyplot as plt

  # 最好能有必要类型注释
  data: np.ndarray

  # 清晰的脚本风格
  def sub_func(arg_1: int, arg_2: dict):
      pass

  def main():
      sub_func()

  if __name__ == '__main__':
      main()
  ```

这里有一份你可以参照的模板：

```markdown
# Single Columns Chart

这是一个用于复刻 GraphPad Prism 经典双组/多组比较柱状图（带非对称误差线和显著性星号）的 matplotlib 示例。

![example picture](url)
```

如果你已经写好了 `readme.md`，直接复制它作为 Pull Request 的文本内容提交即可。

### 样式修改与数据纠错

如果你只想修改某些不合适的样式，或纠正示例数据的错误，直接修改对应文件，并重新生成示例图片后，参照如下模板提交 Pull Request:

```markdown
# The style name you modify

- <此处应当说明先前样式存在的问题>
- <此处应当说明你修改的具体内容>

![example picture](url)
```

## 贡献流程

### 完整样式贡献

1. Fork 本仓库
2. 新建一个分支（推荐分支名与样式名相同）
3. 在 `styles/` 目录下新建一个目录，名字与你的样式名相同，并创建完整的样式结构。

    ```sh
    # 你现在可以通过项目内预定的脚本创建一个styles
    ./scripts/new_style.sh <your_style_name>
    ```

4. 运行 `./scripts/check.sh` 确保所有测试与 lint 通过
5. 提交 Pull Request，等待审核。

### 样式修改与数据纠错

1. Fork 本仓库
2. 新建一个分支（推荐分支名与使用 "fix-" + 样式名，例如 "fix-single_columns_chart"）
3. 在 `styles/` 目录下对应样式中完整您的修改
4. 运行 `./scripts/check.sh` 确保所有测试与 lint 通过
5. 提交 Pull Request，等待审核。

## 致谢

感谢每一位 Matplotlib_Medial_Customed_Style 的贡献者，你的贡献与创意让更多人因此收益！

Heart~ <3 <3 <3
