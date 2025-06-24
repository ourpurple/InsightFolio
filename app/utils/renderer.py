# app/utils/renderer.py
import matplotlib.pyplot as plt
from PySide6.QtGui import QPixmap
import io

# 配置matplotlib以支持中文和公式
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['mathtext.fontset'] = 'stix' # stix-like fonts

def render_latex_to_pixmap(latex_str):
    """
    将 LaTeX 字符串渲染为 QPixmap 对象。
    如果渲染失败，返回一个空的 QPixmap。
    """
    if not latex_str.strip():
        return QPixmap()

    try:
        fig, ax = plt.subplots(figsize=(8, 1), dpi=150)
        # 使用 $...$ 包裹以确保渲染为数学公式
        ax.text(0.5, 0.5, f"${latex_str}$", size=15, va='center', ha='center')
        ax.axis('off')
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        return pixmap
    except Exception as e:
        print(f"LaTeX渲染失败: {e}")
        # 创建一个包含错误信息的图像
        fig, ax = plt.subplots(figsize=(8, 1), dpi=150)
        ax.text(0.5, 0.5, "公式渲染失败", size=15, va='center', ha='center', color='red')
        ax.axis('off')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        return pixmap


def render_latex_to_file(latex_str, filepath):
    """
    将 LaTeX 字符串渲染为图片文件。
    """
    if not latex_str.strip():
        return False
        
    try:
        fig, ax = plt.subplots(figsize=(8, 1), dpi=300)
        ax.text(0.5, 0.5, f"${latex_str}$", size=15, va='center', ha='center')
        ax.axis('off')
        
        fig.savefig(filepath, format='png', bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        return True
    except Exception as e:
        print(f"LaTeX渲染到文件失败: {e}")
        return False