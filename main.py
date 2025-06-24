# QisiLu/main.py - 应用主入口
import sys
from PySide6.QtWidgets import QApplication
from app.data.database import init_db
from app.ui.main_window import MainWindow

def main():
    """
    应用程序主函数。
init_db()
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()