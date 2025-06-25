# app/ui/review_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                                 QLabel, QSpacerItem, QSizePolicy)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import Qt
import os

from app.utils.renderer import render_html_with_katex

class ReviewDialog(QDialog):
    def __init__(self, mistakes, parent=None):
        super().__init__(parent)
        self.mistakes = mistakes
        self.current_index = 0
        
        self.setWindowTitle("错题复习")
        self.setMinimumSize(800, 600)
        
        self._init_ui()
        self._connect_signals()
        
        self.load_mistake()

    def _init_ui(self):
        """初始化UI界面"""
        layout = QVBoxLayout(self)
        
        self.counter_label = QLabel()
        layout.addWidget(self.counter_label, alignment=Qt.AlignRight)
        
        self.details_area = QWebEngineView()
        self.details_area.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        layout.addWidget(self.details_area)
        
        self.answer_button = QPushButton("显示答案")
        self.next_button = QPushButton("下一题")
        self.close_button = QPushButton("关闭")
        
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.answer_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

    def _connect_signals(self):
        self.answer_button.clicked.connect(self.show_answer)
        self.next_button.clicked.connect(self.next_mistake)
        self.close_button.clicked.connect(self.accept)

    def load_mistake(self):
        """加载当前错题"""
        if self.current_index >= len(self.mistakes):
            self.details_area.setHtml("<h1>复习完成！</h1>")
            self.answer_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        self.answer_button.setEnabled(True)
        self.counter_label.setText(f"{self.current_index + 1} / {len(self.mistakes)}")
        
        mistake = self.mistakes[self.current_index]
        html_content = render_html_with_katex(mistake, show_answer=False)
        self.details_area.setHtml(html_content)

    def show_answer(self):
        """显示答案"""
        mistake = self.mistakes[self.current_index]
        html_content = render_html_with_katex(mistake, show_answer=True)
        self.details_area.setHtml(html_content)
        self.answer_button.setEnabled(False)

    def next_mistake(self):
        """加载下一题"""
        self.current_index += 1
        self.load_mistake()