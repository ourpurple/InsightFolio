# app/logic/mistake_service.py

import os
import uuid
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.data.database import get_mistake_by_id, delete_mistake as db_delete_mistake
from app.utils.renderer import render_latex_to_file

# 注册中文字体
# 注意：需要确保你的系统中存在 'simsun.ttc' 字体文件，或者换成其他中文字体
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'c:/windows/fonts/simsun.ttc'))
    FONT_NAME = 'SimSun'
except:
    print("未找到宋体，PDF导出可能无法正常显示中文")
    FONT_NAME = 'Helvetica' # fallback font

class MistakeService:
    def __init__(self):
        # 准备一个临时目录来存放渲染的公式图片
        self.temp_dir = "temp_images"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def delete_mistake_with_assets(self, mistake_id):
        # ... (之前的代码保持不变) ...
        """
        删除错题记录及其关联的图片文件。
        """
        # 1. 获取图片路径
        mistake_to_delete = get_mistake_by_id(mistake_id)
        if not mistake_to_delete:
            raise ValueError("找不到指定的错题记录")

        image_path = mistake_to_delete['question_image']

        # 2. 删除数据库记录
        db_delete_mistake(mistake_id)

        # 3. 删除图片文件
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError as e:
                print(f"删除图片文件失败: {e}")

    def export_to_pdf(self, mistakes_list, filepath):
        """
        将错题列表导出为PDF文件。
        """
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        # 自定义支持中文的样式
        styles.add(ParagraphStyle(name='Chinese', fontName=FONT_NAME, fontSize=12, leading=14))
        styles.add(ParagraphStyle(name='Chinese_Bold', fontName=FONT_NAME, fontSize=14, leading=16, spaceAfter=10))

        story = []
        
        for i, mistake in enumerate(mistakes_list):
            # 题号
            story.append(Paragraph(f"第 {i+1} 题", styles['Chinese_Bold']))
            
            # 题目描述
            story.append(Paragraph(f"题目:", styles['Chinese']))
            self._add_text_and_latex(story, mistake['question_desc'], styles)
            
            # 题目配图
            if mistake['question_image'] and os.path.exists(mistake['question_image']):
                story.append(Spacer(1, 0.2 * inch))
                img = Image(mistake['question_image'])
                img.drawWidth = 4 * inch # 限制图片宽度
                img.drawHeight = (img.drawHeight / img.drawWidth) * 4 * inch # 保持宽高比
                story.append(img)
            
            story.append(Spacer(1, 0.5 * inch))

            # 答案区域
            story.append(Paragraph("答案:", styles['Chinese']))
            # 为了美观，可以留出空白区域让学生填写，或者直接打印答案
            # 这里我们直接打印答案
            self._add_text_and_latex(story, mistake['correct_answer'], styles)

            if i < len(mistakes_list) - 1:
                story.append(PageBreak())

        doc.build(story)
        self._cleanup_temp_images()

    def _add_text_and_latex(self, story, text, styles):
        """辅助函数，处理包含LaTex的文本"""
        # 简单地通过 $...$ 分割文本和公式
        parts = text.split('$')
        for i, part in enumerate(parts):
            if i % 2 == 1: # 奇数部分是LaTex
                temp_img_path = os.path.join(self.temp_dir, f"{uuid.uuid4()}.png")
                if render_latex_to_file(part, temp_img_path):
                    img = Image(temp_img_path)
                    img.drawHeight = 0.3 * inch # 调整行内公式图片的高度
                    img.drawWidth = (img.drawWidth / img.drawHeight) * 0.3 * inch
                    story.append(img)
            else: # 偶数部分是普通文本
                if part:
                    story.append(Paragraph(part.replace(chr(10), '<br/>'), styles['Chinese']))
    
    def _cleanup_temp_images(self):
        """清理临时生成的公式图片"""
        for filename in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"清理临时文件失败: {e}")