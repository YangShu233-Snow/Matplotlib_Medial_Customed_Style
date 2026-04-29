# 入门指南

## 安装

```bash
pip install mmcs
```

开发环境：

```bash
git clone https://github.com/anomalyco/Matplotlib_Medical_Customized_Styles
cd Matplotlib_Medical_Customized_Styles
pip install -e ".[dev]"
```

!!! warning "字体依赖（Linux）"

    GraphPad Prism 风格依赖 Arial / Helvetica / DejaVu Sans 字体。Linux 用户请安装：

    ```bash
    sudo apt install fonts-liberation msttcorefonts
    ```

    缺少字体会导致视觉效果出现细微差异，但不影响运行。

## 验证安装

```python
import mmcs

print(mmcs.list_styles())
# [{'name': 'graphpad_prism', 'category': 'GraphPad Prism', ...}, ...]
```

## 第一个图表

```python
import mmcs

result = mmcs.profile.single_column(
    values=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    save_as="my_first_chart.png",
)
```

<figure class="preview-card">
  <img src="/assets/preview_bar.png" alt="柱状图" loading="lazy">
  <figcaption>单列柱状图</figcaption>
</figure>

一个函数调用，一张出版级图表。

## 理解 Profile 预设

`mmcs.profile` 提供 12 个零配置预设，按图表类别组织：

| 类别 | 预设 | 底层 API |
|---|---|---|
| 柱状图 | `single_column` | `bar_chart` |
| 柱状图 | `bar_scatter` | `bar_chart` |
| 柱状图 | `grouped_columns` | `clustered_columns_chart` |
| 分布图 | `boxplot` | `box_chart` |
| 分布图 | `violin` | `violin_chart` |
| 分布图 | `box_violin` | `box_violin_chart` |
| XY 图 | `scatter` | `scatter_chart` |
| XY 图 | `correlation` | `regression_chart` |
| 1D 图 | `histogram` | `histogram_chart` |
| 1D 图 | `density` | `density_chart` |
| 多维图 | `bubble` | `bubble_chart` |
| 多维图 | `heatmap` | `heatmap_chart` |

每个预设置已选好最佳默认参数。如需完全控制，可直接使用 Quick API。

详细参数请查看各预设的独立页面。

## 选择风格

三种风格家族可用。通过 `style=` 参数传递给任意预设或 Quick API：

| 风格 | 适用场景 | 预览 |
|---|---|---|
| `graphpad_prism` | 柱状图、箱线图、小提琴图、散点图、直方图、密度图、回归图 | ![GraphPad](/assets/preview_bar.png) |
| `ggplot` | 气泡图 | ![ggplot](/assets/preview_bubble.png) |
| `deeptools` | 热图、基因组轨道图 | ![DeepTools](/assets/preview_heatmap.png) |

```python
# 自由切换风格
mmcs.profile.boxplot(data, style="graphpad_prism")
mmcs.profile.heatmap(data, style="deeptools")
```

查找兼容某类图表的风格：

```python
mmcs.list_styles_for("bar")
# [{'name': 'graphpad_prism', ...}]
```

## DataFrame 输入

mmcs 自动检测列名以推断分组列和数值列：

```python
import pandas as pd

df = pd.DataFrame({
    "Group": ["Con", "Con", "KO", "KO"],
    "Expression": [100, 120, 340, 360],
})

mmcs.profile.boxplot(df)  # "Group" → 分组列  "Expression" → 数值列
```

对于非标准列名，显式指定：

```python
mmcs.bar_chart(df, x="Condition", y="Signal")
```

## 下一步

- [样式系统](styles.md) — 深入了解风格自定义
- [快捷预设](profile/single-column.md) — 每类图表的详细选项
- API Reference — 自动从 docstring 生成
