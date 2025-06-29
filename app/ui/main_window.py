# app/ui/main_window.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                 QPushButton, QTableView, QComboBox, QLineEdit,
                                  QHeaderView, QLabel, QMessageBox, QInputDialog, QFileDialog, QMenu)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PySide6.QtCore import Qt

from app.ui.add_edit_dialog import AddEditDialog
from app.ui.review_dialog import ReviewDialog
from app.data.database import get_mistakes, get_mistake_by_id, get_random_mistakes
from app.logic.mistake_service import MistakeService
from app.utils.renderer import render_html_with_katex
from app.utils.version import get_version
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"启思录 (Insight Folio) {get_version()}")
        # 设置应用图标
        icon_path = os.path.join(os.path.dirname(__file__), "app.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 1600, 900)
        self.mistake_service = MistakeService()
        self._init_ui()
        self._connect_signals()
        self.load_mistakes()
        # 设置表格支持右键菜单
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self._show_context_menu)

    def _init_ui(self):
        """初始化UI界面"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左侧列表和筛选
        left_layout = QVBoxLayout()
        
        # 筛选器
        filter_layout = QHBoxLayout()
        self.grade_filter = QComboBox()
        self.grade_filter.setObjectName("filterComboBox")
        self.grade_filter.clear()
        self.grade_filter.addItem("所有年级")
        self.grade_filter.addItems(["7年级", "8年级", "9年级"])
        self.grade_filter.setCurrentIndex(1)  # 默认7年级

        self.semester_filter = QComboBox()
        self.semester_filter.setObjectName("filterComboBox")
        self.semester_filter.clear()
        self.semester_filter.addItem("所有学期")
        self.semester_filter.addItems(["上册", "下册"])
        self.semester_filter.setCurrentIndex(0)  # 默认所有学期

        self.subject_filter = QComboBox()
        self.subject_filter.setObjectName("filterComboBox")
        self.subject_filter.clear()
        self.subject_filter.addItem("所有学科")
        self.subject_filter.addItems(["语文", "数学", "英语", "物理", "化学", "地理", "生物", "道法", "历史"])
        self.subject_filter.setCurrentIndex(0)  # 默认语文
        self.keyword_filter = QLineEdit()
        self.keyword_filter.setObjectName("filterLineEdit")
        self.keyword_filter.setPlaceholderText("关键词搜索...")
        self.filter_button = QPushButton("筛选")
        
        filter_layout.addWidget(self.grade_filter)
        filter_layout.addWidget(self.subject_filter)
        filter_layout.addWidget(self.semester_filter)
        filter_layout.addWidget(self.keyword_filter)
        filter_layout.addWidget(self.filter_button)
        left_layout.addLayout(filter_layout)

        # 错题表格
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "年级", "学科", "学期", "录入日期", "错题摘要"])
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True) # 隐藏ID列
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch) # 让摘要列自动拉伸

        # 设置列宽，单位像素，估算字符宽度约8像素
        self.table_view.setColumnWidth(1, 5 * 8)  # 年级
        self.table_view.setColumnWidth(2, 4 * 8)  # 学科
        self.table_view.setColumnWidth(3, 4 * 8)  # 学期
        self.table_view.setColumnWidth(4, 6 * 8)  # 录入日期
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        left_layout.addWidget(self.table_view)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("新增")
        self.add_button.setObjectName("actionButton")
        self.edit_button = QPushButton("编辑")
        self.edit_button.setObjectName("actionButton")
        self.delete_button = QPushButton("删除")
        self.delete_button.setObjectName("actionButton")
        self.review_button = QPushButton("开始复习")
        self.review_button.setObjectName("actionButton")
        self.export_button = QPushButton("导出PDF")
        self.export_button.setObjectName("actionButton")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.review_button)
        button_layout.addWidget(self.export_button)
        self.about_button = QPushButton("关于")
        self.about_button.setObjectName("actionButton")
        button_layout.addWidget(self.about_button)
        left_layout.addLayout(button_layout)
        
        # 右侧详情区域
        right_layout = QVBoxLayout()
        self.details_area = QWebEngineView()
        self.details_area.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
# 删除“错题详情:”的 QLabel
# right_layout.addWidget(QLabel("错题详情:"))
        right_layout.addWidget(self.details_area)
        
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addLayout(right_layout, stretch=1)

    def _connect_signals(self):
        """连接信号与槽"""
        self.add_button.clicked.connect(self.add_mistake)
        self.edit_button.clicked.connect(self.edit_mistake)
        self.delete_button.clicked.connect(self.delete_mistake)
        self.review_button.clicked.connect(self.start_review)
        self.export_button.clicked.connect(self.export_to_pdf)
        self.filter_button.clicked.connect(self.load_mistakes)
        self.table_view.selectionModel().selectionChanged.connect(self.display_mistake_details)
        self.about_button.clicked.connect(self.show_about_dialog)

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def load_mistakes(self):
        """加载错题到表格"""
        filters = {
            "grade": self.grade_filter.currentText() if self.grade_filter.currentIndex() > 0 else "",
            "subject": self.subject_filter.currentText() if self.subject_filter.currentIndex() > 0 else "",
            "question_desc": self.keyword_filter.text()
        }
        
        mistakes = get_mistakes(filters)
        self.model.removeRows(0, self.model.rowCount())
        for mistake in mistakes:
            # 生成摘要
            summary = mistake['question_desc'][:50] + '...' if len(mistake['question_desc']) > 50 else mistake['question_desc']
            row = [
                QStandardItem(str(mistake['id'])),
                QStandardItem(mistake['grade']),
                QStandardItem(mistake['semester']),
                QStandardItem(mistake['subject']),
                QStandardItem(mistake['record_date']),
                QStandardItem(summary.replace('\n', ' ')), # 替换换行符，避免显示问题
            ]
            self.model.appendRow(row)

    def display_mistake_details(self, selected, deselected):
        """显示选中错题的详细信息"""
        if not selected.indexes():
            self.details_area.setHtml("")
            return
            
        row = selected.indexes()[0].row()
        mistake_id = self.model.item(row, 0).text()
        mistake = get_mistake_by_id(int(mistake_id))

        if not mistake:
            self.details_area.setHtml("")
            return
            
        mistake_dict = dict(mistake)
        html_content = render_html_with_katex(mistake_dict, show_answer=True)
        self.details_area.setHtml(html_content)


    def add_mistake(self):
        """打开新增错题对话框"""
        dialog = AddEditDialog(parent=self)
        if dialog.exec():
            self.load_mistakes()

    def edit_mistake(self):
        """打开编辑错题对话框"""
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "警告", "请先选择要编辑的错题。")
            return
        
        row = selected_indexes[0].row()
        mistake_id = int(self.model.item(row, 0).text())
        
        dialog = AddEditDialog(mistake_id=mistake_id, parent=self)
        if dialog.exec():
            self.load_mistakes()
            self.display_mistake_details(self.table_view.selectionModel().selection(), None)

    def delete_mistake(self):
        """删除选中的错题"""
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "警告", "请先选择要删除的错题。")
            return

        reply = QMessageBox.question(self, '确认删除', '确定要删除这条错题记录吗？此操作不可撤销。',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Since selection mode is SelectRows, we can get the row from the first index.
            row = selected_indexes[0].row()
            mistake_id = int(self.model.item(row, 0).text())
            try:
                self.mistake_service.delete_mistake_with_assets(mistake_id)
                self.load_mistakes()
                self.details_area.setHtml("")
                QMessageBox.information(self, "成功", "错题已删除。")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {e}")

    def start_review(self):
        """开始随机复习"""
        filters = {
            "grade": self.grade_filter.currentText() if self.grade_filter.currentIndex() > 0 else "",
            "semester": self.semester_filter.currentText() if self.semester_filter.currentIndex() > 0 else "",
            "subject": self.subject_filter.currentText() if self.subject_filter.currentIndex() > 0 else "",
        }
        # Keyword filter for review is not in the spec, but can be added if needed.
        # Let's stick to the spec for now.
        
        num, ok = QInputDialog.getInt(self, "随机抽取", "请输入要抽取的题目数量:", 5, 1, 100, 1)
        
        if ok:
            mistakes = get_random_mistakes(num, filters)
            if not mistakes:
                QMessageBox.information(self, "提示", "没有找到符合条件的错题。")
                return
            
            review_dialog = ReviewDialog(mistakes, self)
            review_dialog.exec()

    def export_to_pdf(self):
        """将当前筛选出的错题导出为PDF"""
        filters = {
            "grade": self.grade_filter.currentText() if self.grade_filter.currentIndex() > 0 else "",
            "subject": self.subject_filter.currentText() if self.subject_filter.currentIndex() > 0 else "",
            "question_desc": self.keyword_filter.text()
        }
        mistakes_to_export = get_mistakes(filters)

        if not mistakes_to_export:
            QMessageBox.information(self, "提示", "没有可导出的错题。")
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "保存PDF文件", "", "PDF Files (*.pdf)")
        if filepath:
            try:
                self.mistake_service.export_to_pdf(mistakes_to_export, filepath)
                QMessageBox.information(self, "成功", f"PDF文件已成功导出到:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出PDF失败: {e}")


    def _show_context_menu(self, pos):
        """显示表格的右键菜单"""
        menu = QMenu()
        
        # 添加菜单项
        add_action = menu.addAction("新增")
        edit_action = menu.addAction("编辑")
        delete_action = menu.addAction("删除")
        
        # 连接菜单项到现有方法
        add_action.triggered.connect(self.add_mistake)
        edit_action.triggered.connect(self.edit_mistake)
        delete_action.triggered.connect(self.delete_mistake)
        
        # 根据选择状态设置菜单项可用性
        has_selection = bool(self.table_view.selectionModel().selectedRows())
        edit_action.setEnabled(has_selection)
        delete_action.setEnabled(has_selection)
        
        # 显示菜单
        menu.exec_(self.table_view.viewport().mapToGlobal(pos))

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于 启思录 (Insight Folio)")
        self.setFixedSize(520, 320)  # 调整窗口大小以适应新布局

        # 主布局
        main_layout = QHBoxLayout(self)

        # 左侧：应用图标
        icon_label = QLabel()
        # 加载应用图标，优先使用ico
        icon_path = os.path.join(os.path.dirname(__file__), "about.png")

        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)

        # 右侧：文本信息
        info_layout = QVBoxLayout()
        
        title = QLabel("启思录 (Insight Folio)")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")

        version = QLabel(f"版本 {get_version()}")
        version.setStyleSheet("font-size: 12pt;")

        description = QLabel("一款专为学生设计的错题管理软件。")
        description.setStyleSheet("font-size: 11pt;")
        
        author = QLabel("作者: Wanderln")
        author.setStyleSheet("font-size: 11pt;")

        github_link = QLabel("<a href='https://github.com/ourpurple/InsightFolio'>GitHub Repository</a>")
        github_link.setOpenExternalLinks(True)
        github_link.setStyleSheet("font-size: 11pt;")

        info_layout.addWidget(title)
        info_layout.addWidget(version)
        info_layout.addSpacing(15)
        info_layout.addWidget(description)
        info_layout.addWidget(author)
        info_layout.addWidget(github_link)
        info_layout.addStretch()

        # 组合左右布局
        main_layout.addWidget(icon_label, 1)
        main_layout.addLayout(info_layout, 2)

        # 关闭按钮（可选，因为对话框通常有标题栏关闭按钮）
        # 如果需要明确的关闭按钮，可以取消下面的注释
        # close_button = QPushButton("关闭")
        # close_button.clicked.connect(self.accept)
        # info_layout.addWidget(close_button, alignment=Qt.AlignRight)
