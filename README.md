<div align="center">
   
<img src='./assets/MMCS_LOGO.png' width=250>

# Matplotlib_Medical_Customed_Styles

🔬 **Reusable · Instant · Professional · Evolving** 🔬   
</div>

<div>
   <p align="center">
      <a href="https://github.com/YangShu233-Snow/Matplotlib_Medical_Customed_Styles/actions/workflows/check.yaml">
         <img src="https://github.com/YangShu233-Snow/Matplotlib_Medical_Customed_Styles/actions/workflows/check.yaml/badge.svg" alt="pytest">
      </a>
      <a href="https://matplotlib.org/">
         <img src="https://img.shields.io/badge/style-Matplotlib-blue?logo=python" alt="Matiplotlib">
      </a>
      <a href="https://github.com/YangShu233-Snow/Matplotlib_Medical_Customed_Styles/pulls">
         <img src="https://img.shields.io/badge/PRs-welcome-orange.svg" alt="pull requests">
      </a>
      <a href="./LICENSE">
         <img src="https://img.shields.io/github/license/YangShu233-Snow/Matplotlib_Medical_Customed_Styles" alt="License">
      </a>
      <a href="https://github.com/YangShu233-Snow/Matplotlib_Medical_Customed_Styles/commits/main">
         <img src="https://img.shields.io/github/last-commit/YangShu233-Snow/Matplotlib_Medical_Customed_Styles" alt="Last Commit">
      </a>
      <a href="./llms.md">
         <img src="https://img.shields.io/badge/AI-Friendly-darkgreen" alt="AI Friendly">
      </a>
   </p>
</div>

本项目旨在通过 Python 的 `matplotlib` 库，复刻包含 **GraphPad Prism** 简约风格在内的学术图表样式。无需手动调整繁琐的格式，只需引入相应的 `.mplstyle` 样式文件，即可一键生成符合高质量期刊出版要求的精美图表。

## 🤖 AI friendly

本仓库对 AI 友好，如果你是 Agent 用户，或你的 AI 支持从链接读取本仓库内容，可以放心将仓库交给它解读，作者已尽可能在 [llms.md](./llms.md) 中描述清楚本项目的结构了。

## 🎯 为什么要有这个仓库？

虽然 `matplotlib` 功能强大，但其默认样式不能满足大多数严肃科研工作场景的需求，而著名的样式库 [SciencePlots](https://github.com/garrettj403/SciencePlots) 所提供的样式拓展在生命科学与医学领域领域有点水土不服。

本仓库旨在标准化绘制特定类型图表的程序，并提供可以复用的样式参考，在大多数情况下，你只需要修改图表数据，标题与坐标轴标签即可。

期望本仓库能将你从繁杂的样式调整中解放，专注于数据本身。

## 📁 包含的图表样式 (Styles Gallery)

以下是当前仓库中提供的图表风格列表，点击链接可查看具体示例、效果图及使用说明：

### GraphPad Prism

<table>
  <tr>
    <th>样式名称</th>
    <th>描述</th>
    <th>快速查看</th>
  </tr>
  <tr>
    <td><b>Single Columns Chart</b></td>
    <td>经典的双组/多组比较柱状图，支持非对称误差线和自动显著性标注。</td>
    <td nowrap><a href='./styles/single_columns_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Mutiple Columns Chart</b></td>
    <td>经典的单图多表的双组/多组比较柱状图，支持非对称误差线和自动显著性标注。</td>
    <td nowrap><a href='./styles/mutiple_columns_charts/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Columns Scatter Chart</b></td>
    <td>经典的柱状散点图，支持数据散点、误差线和自动显著性标注。</td>
    <td nowrap><a href='./styles/single_columns_scatter_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Clustered Columns Scatter Chart</b></td>
    <td>经典的分组柱状散点图，支持智能防重叠散点、误差线和自动显著性标注。</td>
    <td nowrap><a href='./styles/single_clustered_columns_scatter_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Clustered Scatter Chart</b></td>
    <td>经典的聚类散点图，集成 DBSCAN 算法并支持自动参数估计。</td>
    <td nowrap><a href='./styles/clustered_scatter_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Linear Regression Scatter Chart</b></td>
    <td>经典的单组线性回归散点图，包含线性拟合直线及 $R^2$、$P$ 值等统计信息。</td>
    <td nowrap><a href='./styles/single_linear_regression_scatter_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Boxplot Chart</b></td>
    <td>经典的简约箱线图，支持同时展示中位数与均值线。</td>
    <td nowrap><a href='./styles/single_boxplot_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Violinplot Chart</b></td>
    <td>经典的小提琴图，支持 Scott/Silverman 带宽优化与多种核函数，包含标准分布与对比分离（Split）两种模式。</td>
    <td nowrap><a href='./styles/single_violinplot_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Box-Violinplot Chart</b></td>
    <td>箱线图与小提琴图的叠加组合图，支持 Scott/Silverman 带宽优化与多种核函数，内部极简黑盒精确标定四分位数，外部小提琴展示概率密度分布。</td>
    <td nowrap><a href='./styles/single_box_violinplot_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Histogram Chart</b></td>
    <td>直方图，采用八度灰配色，内置 Freedman-Diaconis 准则自动计算最优分组数。</td>
    <td nowrap><a href='./styles/single_histogram_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Single Densityplot Chart</b></td>
    <td>密度分布图，复刻平滑曲线与半透明填充效果，内置 Scott 和 Silverman 带宽优化规则。</td>
    <td nowrap><a href='./styles/single_densityplot_chart/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><i>(待添加)</i></td>
    <td><i>(更多样式开发中...)</i></td>
    <td></td>
  </tr>
</table>

### DeepTools

<table>
  <tr>
    <th>样式名称</th>
    <th>描述</th>
    <th>快速查看</th>
  </tr>
  <tr>
    <td><b>Mutiple Genomic Heatmaps</b></td>
    <td>单图多表基因组学聚合热图，带有标尺与色彩条图例。</td>
    <td nowrap><a href='./styles/mutiple_genomic_heatmaps/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><b>Clustered Genomic Heatmap</b></td>
    <td>经典的带聚类树基因组学热图，支持行列聚类。</td>
    <td nowrap><a href='./styles/clustered_genomic_heatmap/readme.md'>👉 查看详情</a></td>
  </tr>
  <tr>
    <td><i>(待添加)</i></td>
    <td><i>(更多样式开发中...)</i></td>
    <td></td>
  </tr>
</table>

## 🛠️ 快速上手

1. 克隆本仓库到本地：

   ```bash
   git clone https://github.com/YangShu233-Snow/Matplotlib_Medical_Customed_Styles
   cd Matplotlib_Medical_Customed_Styles
   ```

2. 安装环境

   ```bash
   # 强烈建议使用虚拟环境
   # Python>=3.9 均可，推荐版本为 3.12.3

   # 仅安装使用者依赖 (Production)
   pip install .

   # 安装开发者依赖 (Development/Testing)
   pip install -e ".[dev]"
   ```

3. 进入你感兴趣的样式目录，例如柱状图：

   ```bash
   cd styles/single_columns_chart
   ```

4. 运行示例代码生成图表：

   ```bash
   python example.py
   ```

如果你想在其他地方运用样式，可以复制对应样式下`assets/`中的`mplstyle`文件，并参考示例代码中的其他样式改动。

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request 来添加新的学术图表风格！

如果你想为本项目提出 Pull Request，可以参照 [贡献指南](CONTRIBUTING.md)

## 🙇 致谢

非常感谢以下**项目/资料**，在开发**MMCS**时候，我从中得到了许多帮助：

- [From Data to viz](https://www.data-to-viz.com/)
- [Matplotlib](https://matplotlib.org/)
- [Graphpad](https://www.graphpad.com/)
- [DeepTools](https://github.com/deeptools/deepTools)

## 📄 License

MIT License

## 📅 更多计划

- [] 加入更多样式图表
- [] 将本项目同步重写为 Python 库
- [] 优化现有脚本的鲁棒性
