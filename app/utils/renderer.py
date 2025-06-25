# app/utils/renderer.py
import os

def render_html_with_katex(mistake_data, show_answer=True):
    """
    将错题数据渲染成包含KaTeX的HTML页面。
    
    :param mistake_data: 包含错题信息的字典。
    :param show_answer: 是否显示答案和解析。
    :return: 渲染好的HTML字符串。
    """
    
    # 获取 assets/katex 目录的绝对路径
    # The path is constructed relative to this file's location (app/utils/renderer.py)
    assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'katex')).replace('\\', '/')

    # 替换换行符为<br>，并对LaTeX内容进行转义，以便在JavaScript中正确处理
    question_desc = mistake_data['question_desc'].replace('\n', '<br>')
    correct_answer = mistake_data['correct_answer'].replace('\n', '<br>')
    mistake_reason = mistake_data['mistake_reason'].replace('\n', '<br>')

    # 构建答案和解析部分
    answer_html = ""
    if show_answer:
        answer_html = f"""
            <hr>
            <h3>正确答案:</h3>
            <div id="answer" class="content-box">{correct_answer}</div>
            
            <hr>
            <h3>错误原因分析:</h3>
            <div id="reason" class="content-box">{mistake_reason}</div>
        """

    # 构建题目图片部分
    image_html = ""
    if mistake_data.get('question_image') and os.path.exists(mistake_data['question_image']):
        # 将本地图片路径转换为 file:/// URI
        image_path = os.path.abspath(mistake_data['question_image']).replace('\\', '/')
        image_html = f"""
            <hr>
            <h3>题目配图:</h3>
            <img src="file:///{image_path}" alt="题目图片" style="max-width: 100%; height: auto;">
        """

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>错题详情</title>
        <link rel="stylesheet" href="file:///{assets_path}/katex.min.css">
        <script defer src="file:///{assets_path}/katex.min.js"></script>
        <script defer src="file:///{assets_path}/auto-render.min.js"></script>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 16px;
                line-height: 1.6;
                margin: 10px;
                background-color: #f8f9fa;
                color: #212529;
            }}
            .container {{
                max-width: 700px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 15px;
                border-radius: 6px;
                box-shadow: 0 1px 6px rgba(0,0,0,0.03);
            }}
            h2, h3 {{
                color: #0056b3;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 5px;
                margin-top: 15px;
            }}
            .content-box {{
                padding: 10px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                margin-top: 8px;
                word-wrap: break-word; /* 确保长内容能换行 */
            }}
            .meta-info {{
                font-size: 13px;
                color: #6c757d;
                margin-bottom: 12px;
            }}
            img {{
                max-width: 100%;
                height: auto;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="meta-info">
                <b>学科:</b> {mistake_data['subject']} &nbsp;&nbsp;
                <b>年级:</b> {mistake_data['grade']} ({mistake_data['semester']}) &nbsp;&nbsp;
                <b>录入日期:</b> {mistake_data['record_date']}
            </div>
            
            <h3>题目:</h3>
            <div id="question" class="content-box">{question_desc}</div>
            
            {image_html}
            {answer_html}
        </div>
        
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: "$$", right: "$$", display: true}},
                        {{left: "$", right: "$", display: false}},
                        {{left: "\\\\[", right: "\\\\]", display: true}},
                        {{left: "\\\\(", right: "\\\\)", display: false}}
                    ]
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html_template