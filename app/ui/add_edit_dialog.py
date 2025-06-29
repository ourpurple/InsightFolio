# app/ui/add_edit_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QComboBox,
                               QTextEdit, QPushButton, QLabel,
                               QFileDialog, QHBoxLayout, QMessageBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QThread, Signal, Qt
from datetime import datetime
import uuid
import os

from app.data.database import add_mistake, get_mistake_by_id, update_mistake

# 定义资源目录
ASSETS_DIR = "assets/images"

class ImageCopyThread(QThread):
    copy_finished = Signal(str)

    def __init__(self, src_path, dest_path):
        super().__init__()
        self.src_path = src_path
        self.dest_path = dest_path

    def run(self):
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(self.dest_path), exist_ok=True)
        with open(self.src_path, 'rb') as f_in, open(self.dest_path, 'wb') as f_out:
            f_out.write(f_in.read())
        self.copy_finished.emit(self.dest_path)

class AddEditDialog(QDialog):
    def __init__(self, mistake_id=None, parent=None):
        super().__init__(parent)
        self.mistake_id = mistake_id
        self.image_path = None

        if self.mistake_id:
            self.setWindowTitle("编辑错题")
        else:
            self.setWindowTitle("新增错题")
        
        self.setMinimumSize(600, 500)

        self._init_ui()
        self._connect_signals()

        if self.mistake_id:
            self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        # 分类选择
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["7年级", "8年级", "9年级"])
        self.semester_combo = QComboBox()
        self.semester_combo.addItems(["上册", "下册"])
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["语文", "数学", "英语", "物理", "化学", "地理", "生物", "道法", "历史"])

        category_layout = QHBoxLayout()
        category_layout.addWidget(self.grade_combo)
        category_layout.addWidget(self.semester_combo)
        category_layout.addWidget(self.subject_combo)
        form_layout.addRow("分类:", category_layout)

        # 题目
        self.question_edit = QTextEdit()
        form_layout.addRow("题目:", self.question_edit)

        # 正确答案
        self.answer_edit = QTextEdit()
        form_layout.addRow("正确答案:", self.answer_edit)

        # 错误原因
        self.reason_edit = QTextEdit()
        form_layout.addRow("错误原因:", self.reason_edit)

        # 图片上传
        self.upload_button = QPushButton("上传图片")
        self.image_preview = QLabel("无图片")
        self.image_preview.setFixedSize(200, 100)
        self.image_preview.setScaledContents(True)
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.upload_button)
        image_layout.addWidget(self.image_preview)
        form_layout.addRow("题目配图:", image_layout)

        layout.addLayout(form_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def _connect_signals(self):
        self.upload_button.clicked.connect(self._upload_image)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _load_data(self):
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
                self.image_preview.setPixmap(pixmap.scaled(self.image_preview.size().width(), self.image_preview.size().height(), Qt.KeepAspectRatio))

    def _upload_image(self):
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)

        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            root, ext = os.path.splitext(file_path)
            new_filename = f"{uuid.uuid4()}{ext}"
            dest_path = os.path.join(ASSETS_DIR, new_filename).replace("\\", "/")

            def on_copy_finished(path):
                import os
                self.image_path = os.path.abspath(path)
                pixmap = QPixmap(self.image_path)
                print(f"pixmap size: {pixmap.size()}, label size: {self.image_preview.size()}")
                if pixmap.isNull():
                    print(f"Failed to load image from {self.image_path}")
                else:
                    self.image_preview.clear()
                    self.image_preview.setPixmap(pixmap.scaled(self.image_preview.size().width(), self.image_preview.size().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    self.image_preview.repaint()

            self.copy_thread = ImageCopyThread(file_path, dest_path)
            self.copy_thread.copy_finished.connect(on_copy_finished)
            self.copy_thread.start()

    def get_data(self):
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

    def accept(self):
        data = self.get_data()
        try:
            if self.mistake_id:
                update_mistake(self.mistake_id, data)
            else:
                add_mistake(data)
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {e}")