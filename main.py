# QisiLu/main.py - 应用主入口
import sys
from PySide6.QtWidgets import QApplication
from app.data.database import init_db
from app.ui.main_window import MainWindow

def main():
    """
    应用程序主函数。
    """
    # 初始化数据库
    init_db()
    
    app = QApplication(sys.argv)

    # 加载全局样式表
    import os
    style_file = os.path.join(os.path.dirname(__file__), "app", "ui", "style.qss")
    try:
        with open(style_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"加载样式表失败: {e}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()