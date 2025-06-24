# app/ui/add_edit_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QComboBox,
                               QLineEdit, QTextEdit, QPushButton, QLabel,
                               QFileDialog, QHBoxLayout, QMessageBox)
from PySide6.QtGui import QPixmap
from datetime import datetime
import uuid
import os

from app.utils.renderer import render_latex_to_pixmap
from app.data.database import add_mistake, update_mistake, get_mistake_by_id

# 定义资源目录
ASSETS_DIR = "assets/images"

class AddEditDialog(QDialog):
    def __init__(self, mistake_id=None, parent=None):
        super().__init__(parent)
        self.mistake_id = mistake_id
        self.image_path = None

        if self.mistake_id:
            self.setWindowTitle("编辑错题")
        else:
            self.setWindowTitle("新增错题")
        
        self.setMinimumSize(800, 700)
        
        self._init_ui()
        self._connect_signals()
        
        if self.mistake_id:
            self._load_mistake_data()

    def _init_ui(self):
        """初始化UI界面"""
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # 分类
        self.grade_combo = QComboBox()
        self.grade_combo.addItems([f"{g}年级" for g in range(1, 13)])
        self.semester_combo = QComboBox()
        self.semester_combo.addItems(["上册", "下册"])
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["数学", "物理", "化学", "生物", "语文", "英语"])
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(self.grade_combo)
        category_layout.addWidget(self.semester_combo)
        category_layout.addWidget(self.subject_combo)
        form_layout.addRow("分类:", category_layout)

        # 题目描述
        self.question_edit = QTextEdit()
        self.question_preview = QLabel("公式预览")
        self.question_preview.setMinimumHeight(100)
        form_layout.addRow("题目描述:", self.question_edit)
        form_layout.addRow("公式预览:", self.question_preview)

        # 题目配图
        self.upload_button = QPushButton("上传图片")
        self.image_preview = QLabel("图片预览")
        self.image_preview.setMinimumSize(200, 100)
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.upload_button)
        image_layout.addWidget(self.image_preview)
        form_layout.addRow("题目配图:", image_layout)

        # 正确答案
        self.answer_edit = QTextEdit()
        self.answer_preview = QLabel("答案公式预览")
        self.answer_preview.setMinimumHeight(100)
        form_layout.addRow("正确答案:", self.answer_edit)
        form_layout.addRow("答案预览:", self.answer_preview)

        # 错误原因
        self.reason_edit = QTextEdit()
        form_layout.addRow("错误原因:", self.reason_edit)

        layout.addLayout(form_layout)

        # 按钮
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def _connect_signals(self):
        """连接信号与槽"""
        self.question_edit.textChanged.connect(self._update_question_preview)
        self.answer_edit.textChanged.connect(self._update_answer_preview)
        self.upload_button.clicked.connect(self._upload_image)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def _update_question_preview(self):
        """更新题目公式预览"""
        latex_str = self.question_edit.toPlainText()
        pixmap = render_latex_to_pixmap(latex_str)
        self.question_preview.setPixmap(pixmap)

    def _update_answer_preview(self):
        """更新答案公式预览"""
        latex_str = self.answer_edit.toPlainText()
        pixmap = render_latex_to_pixmap(latex_str)
        self.answer_preview.setPixmap(pixmap)

    def _upload_image(self):
        """上传图片"""
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)
            
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            ext = os.path.splitext(file_path)
            new_filename = f"{uuid.uuid4()}{ext}"
            self.image_path = os.path.join(ASSETS_DIR, new_filename).replace("\\", "/")
            
            # 复制文件
            with open(file_path, 'rb') as f_in, open(self.image_path, 'wb') as f_out:
                f_out.write(f_in.read())
            
            pixmap = QPixmap(self.image_path)
            self.image_preview.setPixmap(pixmap.scaledToWidth(200))

    def get_data(self):
        """获取对话框中的数据"""
        return {
            "grade": self.grade_combo.currentText(),
            "semester": self.semester_combo.currentText(),
            "subject": self.subject_combo.currentText(),
            "record_date": datetime.now().strftime("%Y-%m-%d"),
            "question_desc": self.question_edit.toPlainText(),
            "question_image": self.image_path,
            "correct_answer": self.answer_edit.toPlainText(),
            "mistake_reason": self.reason_edit.toPlainText()
        }

    def _load_mistake_data(self):
        """加载错题数据到UI"""
        mistake = get_mistake_by_id(self.mistake_id)
        if mistake:
            self.grade_combo.setCurrentText(mistake['grade'])
            self.semester_combo.setCurrentText(mistake['semester'])
            self.subject_combo.setCurrentText(mistake['subject'])
            self.question_edit.setPlainText(mistake['question_desc'])
            self.answer_edit.setPlainText(mistake['correct_answer'])
            self.reason_edit.setPlainText(mistake['mistake_reason'])
            
            self.image_path = mistake['question_image']
            if self.image_path and os.path.exists(self.image_path):
                pixmap = QPixmap(self.image_path)
                self.image_preview.setPixmap(pixmap.scaledToWidth(200))

    def accept(self):
        """保存数据"""
        data = self.get_data()
        try:
            if self.mistake_id:
                update_mistake(self.mistake_id, data)
            else:
                add_mistake(data)
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {e}")