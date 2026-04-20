# matplotlib_GraphPad_style

> A customed style similar to GraphPad.

本项目旨在通过 Python 的 `matplotlib` 库，完美复刻 GraphPad Prism 风格的学术图表。无需手动调整繁琐的格式，只需引入相应的 `.mplstyle` 样式文件，即可一键生成符合高质量期刊出版要求的精美图表。

## 🤖 AI friendly

本仓库对 AI 友好，如果你是 Agent 用户，或你的 AI 支持从链接读取本仓库内容，可以放心将仓库交给它解读，作者已尽可能在 `llms.md` 中描述清楚本项目的结构了。

## 🎯 为什么要有这个仓库？

虽然 `matplotlib` 功能强大，但其默认样式不能满足大多数严肃科研工作场景的需求，而著名的样式库 [SciencePlots](https://github.com/garrettj403/SciencePlots) 所提供的样式拓展在生命科学与医学领域领域有点水土不服。

本仓库旨在标准化绘制特定类型图表的程序，并提供可以复用的样式参考，在大多数情况下，你只需要修改图表数据，标题与坐标轴标签即可。

期望本仓库能将你从繁杂的样式调整中解放，专注于数据本身。

## 📁 包含的图表样式 (Styles Gallery)

以下是当前仓库中提供的图表风格列表，点击链接可查看具体示例、效果图及使用说明：

| 样式名称 | 描述 | 快速查看 |
| :--- | :--- | :--- |
| **Column Chart GraphPad** | 经典的双组/多组比较柱状图，支持非对称误差线和自动显著性标注。 | [👉 查看详情](./styles/single_columns_chart/readme.md) |
| **Column Chart GraphPad** | 单图多表的双组/多组比较柱状图，支持非对称误差线和自动显著性标注。 | [👉 查看详情](./styles/mutiple_columns_charts/readme.md) |
| *(待添加)* | *(更多样式开发中...)* | |

## 🛠️ 快速上手

1. 克隆本仓库到本地：
   ```bash
   git clone https://github.com/YangShu233-Snow/matplotlib_GraphPad_style
   ```
2. 进入你感兴趣的样式目录，例如柱状图：
   ```bash
   cd matplotlib_GraphPad_style/styles/column_chart_graphpad
   ```
3. 运行示例代码生成图表：
   ```bash
   python example.py
   ```

如果你想在其他地方运用样式，可以复制对应样式下`assets/`中的`mplstyle`文件，并参考示例代码中的其他样式改动。

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request 来添加新的学术图表风格！在提交 PR 时，请确保遵循本仓库现有的目录结构，并为你的样式提供 `.mplstyle` 文件、`example.py` 和对应的 `readme.md`。

## 📄 License

MIT License
