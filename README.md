# Matplotlib_Medial_Customed_Style

> Collections of customed styles for medical field.

本项目旨在通过 Python 的 `matplotlib` 库，复刻包含 **GraphPad Prism** 简约风格在内的学术图表样式。无需手动调整繁琐的格式，只需引入相应的 `.mplstyle` 样式文件，即可一键生成符合高质量期刊出版要求的精美图表。

## 🤖 AI friendly

本仓库对 AI 友好，如果你是 Agent 用户，或你的 AI 支持从链接读取本仓库内容，可以放心将仓库交给它解读，作者已尽可能在 `llms.md` 中描述清楚本项目的结构了。

## 🎯 为什么要有这个仓库？

虽然 `matplotlib` 功能强大，但其默认样式不能满足大多数严肃科研工作场景的需求，而著名的样式库 [SciencePlots](https://github.com/garrettj403/SciencePlots) 所提供的样式拓展在生命科学与医学领域领域有点水土不服。

本仓库旨在标准化绘制特定类型图表的程序，并提供可以复用的样式参考，在大多数情况下，你只需要修改图表数据，标题与坐标轴标签即可。

期望本仓库能将你从繁杂的样式调整中解放，专注于数据本身。

## 📁 包含的图表样式 (Styles Gallery)

以下是当前仓库中提供的图表风格列表，点击链接可查看具体示例、效果图及使用说明：

### GraphPad Prism

| 样式名称 | 描述 | 快速查看 |
| :--- | :--- | :--- |
| **Single Columns Chart** | 经典的双组/多组比较柱状图，支持非对称误差线和自动显著性标注。 | [👉 查看详情](./styles/single_columns_chart/readme.md) |
| **Mutiple Columns Chart** | 经典的单图多表的双组/多组比较柱状图，支持非对称误差线和自动显著性标注。 | [👉 查看详情](./styles/mutiple_columns_charts/readme.md) |
| **Single Columns Scatter Chart** | 经典的柱状散点图，支持数据散点、误差线和自动显著性标注。 | [👉 查看详情](./styles/single_columns_chart/readme.md) |
| **Single Clustered Columns Scatter Chart** | 经典的分组（簇状）柱状散点图，支持数据散点、误差线和自动显著性标注。 | [👉 查看详情](./styles/single_clustered_columns_scatter_chart/readme.md) |
| *(待添加)* | *(更多样式开发中...)* | |

### DeepTools

| 样式名称 | 描述 | 快速查看 |
| :--- | :--- | :--- |
| **Mutiple Genomic Heatmaps** | 单图多表基因组学聚合热图，带有标尺与色彩条图例。 | [👉 查看详情](./styles/mutiple_genomic_heatmaps/readme.md) |
| *(待添加)* | *(更多样式开发中...)* | |

## 🛠️ 快速上手

1. 克隆本仓库到本地：
   ```bash
   git clone https://github.com/YangShu233-Snow/matplotlib_GraphPad_style
   ```
2. 安装环境
   ```bash
   # 强烈建议使用虚拟环境，假设你已经在本地准备好了对应的 Conda 虚拟环境
   # Python>=3.9 均可，推荐版本为 3.12.3
   conda activate Your_Enviroment
   pip install -r requirements.txt
   ```
3. 进入你感兴趣的样式目录，例如柱状图：
   ```bash
   cd matplotlib_GraphPad_style/styles/column_chart_graphpad
   ```
4. 运行示例代码生成图表：
   ```bash
   python example.py
   ```

如果你想在其他地方运用样式，可以复制对应样式下`assets/`中的`mplstyle`文件，并参考示例代码中的其他样式改动。

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request 来添加新的学术图表风格！

如果你想为本项目提出 Pull Request，可以参照 [贡献指南](CONTRIBUTING.md)

## 📄 License

MIT License

## 📅 更多计划

- [] 加入更多样式图表
- [] 将本项目同步重写为 Python 库
- [] 优化现有脚本的鲁棒性