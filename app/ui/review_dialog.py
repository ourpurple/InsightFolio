# app/ui/review_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                                 QLabel, QSpacerItem, QSizePolicy, QComboBox, QSpinBox)
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
        html_content = render_html_with_katex(dict(mistake), show_answer=False)
        self.details_area.setHtml(html_content)

    def show_answer(self):
        """显示答案"""
        mistake = self.mistakes[self.current_index]
        html_content = render_html_with_katex(dict(mistake), show_answer=True)
        self.details_area.setHtml(html_content)
        self.answer_button.setEnabled(False)

    def next_mistake(self):
        """加载下一题"""
        self.current_index += 1
        self.load_mistake()

class ReviewConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择复习条件")
        self.setMinimumSize(300, 200)
        layout = QVBoxLayout(self)

        # 年级
        self.grade_combo = QComboBox()
        self.grade_combo.addItem("所有年级")
        self.grade_combo.addItems(["7年级", "8年级", "9年级"])
        layout.addWidget(QLabel("年级："))
        layout.addWidget(self.grade_combo)

        # 学期
        self.semester_combo = QComboBox()
        self.semester_combo.addItem("所有学期")
        self.semester_combo.addItems(["上册", "下册"])
        layout.addWidget(QLabel("学期："))
        layout.addWidget(self.semester_combo)

        # 学科
        self.subject_combo = QComboBox()
        self.subject_combo.addItem("所有学科")
        self.subject_combo.addItems(["语文", "数学", "英语", "物理", "化学", "地理", "生物", "道法", "历史"])
        layout.addWidget(QLabel("学科："))
        layout.addWidget(self.subject_combo)

        # 题目数量
        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMaximum(100)
        self.count_spin.setValue(5)
        self.count_spin.setFixedHeight(35)  # 设置与其他控件一致的高度
        layout.addWidget(QLabel("复习题目数量："))
        layout.addWidget(self.count_spin)

        # 按钮
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.cancel_btn = QPushButton("取消")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_config(self):
        filters = {
            "grade": self.grade_combo.currentText() if self.grade_combo.currentIndex() > 0 else "",
            "semester": self.semester_combo.currentText() if self.semester_combo.currentIndex() > 0 else "",
            "subject": self.subject_combo.currentText() if self.subject_combo.currentIndex() > 0 else "",
        }
        count = self.count_spin.value()
        return filters, count