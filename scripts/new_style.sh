#!/bin/bash

# 1. 定义目标基础路径（根据你的项目结构修改此处）
BASE_PATH="./styles"

# 2. 获取输入参数
FOLDER_NAME=$1

# 3. 检查是否提供了输入字符串
if [ -z "$FOLDER_NAME" ]; then
    echo "错误: 请提供文件夹名称。"
    echo "用法: ./scripts/new_styles.sh <folder_name>"
    exit 1
fi

# 4. 拼接完整路径
TARGET_DIR="$BASE_PATH/$FOLDER_NAME"

# 5. 检查文件夹是否已存在
if [ -d "$TARGET_DIR" ]; then
    echo "提示: 文件夹 '$TARGET_DIR' 已存在，跳过创建。"
else
    # 创建目录（-p 确保父目录不存在时也能一并创建）
    mkdir -p "$TARGET_DIR"
    echo "已成功创建目录: $TARGET_DIR"
fi

# 6. 在该目录下生成预定的空文件
# 你可以在下面的列表中添加或修改你想要的文件名
mkdir -p "$TARGET_DIR/assets"
mkdir -p "$TARGET_DIR/img"
touch "$TARGET_DIR/assets/$FOLDER_NAME.mplstyle"
touch "$TARGET_DIR/example.py"
touch "$TARGET_DIR/readme.md"

cat >> "$TARGET_DIR/example.py" << EOF
import matplotlib.pyplot as plt

from pathlib import Path

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/$FOLDER_NAME.mplstyle'
plt.style.use(style_file)

def main():
    # --- config ---
    img_name = 'example'

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
EOF

cat >> "$TARGET_DIR/assets/$FOLDER_NAME.mplstyle" << EOF
# 字体设置
font.family : sans-serif
font.sans-serif : Arial, Helvetica, DejaVu Sans

# 坐标轴和标题字体粗细
axes.labelweight : bold
axes.titleweight : bold

# 坐标轴线宽和边框隐藏
axes.linewidth : 1.5
axes.spines.top : False
axes.spines.right : False

# 刻度线粗细与长度
xtick.major.width : 1.5
ytick.major.width : 1.5
xtick.major.size : 6
ytick.major.size : 6

# 字体大小
xtick.labelsize : 12
ytick.labelsize : 12
axes.labelsize : 14
axes.titlesize : 16
EOF

echo "已在 $TARGET_DIR 中生成预定文件。"