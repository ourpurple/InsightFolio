# app/logic/mistake_service.py

import os
import uuid
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QEventLoop, QTimer

from app.data.database import get_mistake_by_id, delete_mistake as db_delete_mistake
from app.utils.renderer import render_html_with_katex

class MistakeService:
    def __init__(self):
        pass

    def delete_mistake_with_assets(self, mistake_id):
        """
        删除错题记录及其关联的图片文件。
        """
        mistake_to_delete = get_mistake_by_id(mistake_id)
        if not mistake_to_delete:
            raise ValueError("找不到指定的错题记录")

        image_path = mistake_to_delete['question_image']
        db_delete_mistake(mistake_id)

        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError as e:
                print(f"删除图片文件失败: {e}")

    def export_to_pdf(self, mistakes_list, filepath):
        """
        将错题列表导出为包含KaTeX渲染的PDF文件。
        """
        # 获取 assets/katex 目录的绝对路径
        assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'katex')).replace('\\', '/')
        
        # 组合所有错题的HTML
        full_html = "<html><head>"
        # KaTeX 和 样式的头部只需要一次
        full_html += f"""
        <meta charset="UTF-8">
        <link rel="stylesheet" href="file:///{assets_path}/katex.min.css">
        <script src="file:///{assets_path}/katex.min.js"></script>
        <script src="file:///{assets_path}/auto-render.min.js"></script>
        <style>
            body {{ font-family: sans-serif; margin: 2em; }}
            .mistake-container {{ page-break-inside: avoid; border: 1px solid #ccc; margin-bottom: 20px; padding: 20px; }}
            img {{ max-width: 100%; }}
        </style>
        """
        full_html += "</head><body>"

        for mistake in mistakes_list:
            # 复用渲染逻辑，但只取其body内容
            html_content = render_html_with_katex(mistake, show_answer=True)
            # 简单地提取body内容
            if '<body>' in html_content and '</body>' in html_content:
                body_content = html_content.split('<body>').split('</body>')
                full_html += f'<div class="mistake-container">{body_content}</div>'

        full_html += """
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "$", right: "$", display: false},
                        {left: "\\\\[", right: "\\\\]", display: true},
                        {left: "\\\\(", right: "\\\\)", display: false}
                    ]
                });
            });
        </script>
        </body></html>
        """

        # 使用QWebEngineView来打印HTML到PDF
        # 注意: 这需要在Qt应用环境中运行
        view = QWebEngineView()
        view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        view.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)

        # 使用事件循环等待页面加载和渲染完成
        loop = QEventLoop()
        
        def on_load_finished(success):
            if success:
                # 给JS渲染留出一点时间
                QTimer.singleShot(2000, lambda: view.printToPdf(filepath))
                QTimer.singleShot(3000, loop.quit) # 等待打印命令发出后退出
            else:
                print("PDF导出失败：页面加载失败")
                loop.quit()

        view.loadFinished.connect(on_load_finished)
        view.setHtml(full_html)
        
        loop.exec()