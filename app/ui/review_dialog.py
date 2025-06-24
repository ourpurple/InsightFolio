# app/ui/review_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QTextBrowser, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

from app.utils.renderer import render_latex_to_pixmap

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
        
        self.details_area = QTextBrowser()
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
        
        # 显示题目
        html = f"""
        <b>学科:</b> {mistake['subject']} &nbsp;&nbsp; <b>年级:</b> {mistake['grade']} ({mistake['semester']})<hr>
        <b>题目描述:</b><br>
        {mistake['question_desc'].replace(chr(10), '<br>')}
        """
        self.details_area.setHtml(html)
        
        # 渲染题目中的LaTeX
        question_pixmap = render_latex_to_pixmap(mistake['question_desc'])
        if not question_pixmap.isNull():
            self.details_area.append("<br><b>公式渲染:</b>")
            cursor = self.details_area.textCursor()
            cursor.insertImage(question_pixmap.toImage())
            
        # 显示题目配图
        if mistake['question_image'] and os.path.exists(mistake['question_image']):
            self.details_area.append("<br><b>题目配图:</b>")
            pixmap = QPixmap(mistake['question_image'])
            width = self.details_area.width() - 50
            cursor = self.details_area.textCursor()
            cursor.insertImage(pixmap.scaledToWidth(width, Qt.SmoothTransformation).toImage())

    def show_answer(self):
        """显示答案"""
        mistake = self.mistakes[self.current_index]
        html_answer = f"""
        <hr><b>正确答案:</b><br>
        {mistake['correct_answer'].replace(chr(10), '<br>')}
        """
        self.details_area.append(html_answer)
        
        # 渲染答案中的LaTeX
        answer_pixmap = render_latex_to_pixmap(mistake['correct_answer'])
        if not answer_pixmap.isNull():
            self.details_area.append("<br><b>答案公式渲染:</b>")
            cursor = self.details_area.textCursor()
            cursor.insertImage(answer_pixmap.toImage())

        html_reason = f"""
        <hr><b>错误原因分析:</b><br>
        {mistake['mistake_reason'].replace(chr(10), '<br>')}
        """
        self.details_area.append(html_reason)
        
        self.answer_button.setEnabled(False)

    def next_mistake(self):
        """加载下一题"""
        self.current_index += 1
        self.load_mistake()