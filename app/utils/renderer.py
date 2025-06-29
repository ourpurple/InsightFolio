# app/utils/renderer.py
import os
import base64

def render_html_with_katex(mistake_data, show_answer=True):
    """
    将错题数据渲染成包含KaTeX的HTML页面。
    
    :param mistake_data: 包含错题信息的字典。
    :param show_answer: 是否显示答案和解析。
    :return: 渲染好的HTML字符串。
    """
    
    # --- In-memory KaTeX Assets ---
    # To avoid issues with local file access (file:/// protocol),
    # we embed the content of KaTeX's CSS and JS files directly into the HTML.
    
    # Get the absolute path to the assets directory
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'katex'))

    # Read the content of the asset files
    try:
        with open(os.path.join(assets_dir, 'katex.min.css'), 'r', encoding='utf-8') as f:
            katex_css = f.read()
        with open(os.path.join(assets_dir, 'katex.min.js'), 'r', encoding='utf-8') as f:
            katex_js = f.read()
        with open(os.path.join(assets_dir, 'auto-render.min.js'), 'r', encoding='utf-8') as f:
            auto_render_js = f.read()
    except FileNotFoundError as e:
        # Handle cases where asset files might be missing
        return f"Error: KaTeX asset file not found. {e}"

    # Directly use the original text; frontend CSS and JS will handle rendering
    question_desc = mistake_data['question_desc']
    correct_answer = mistake_data['correct_answer']
    mistake_reason = mistake_data['mistake_reason']

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
        try:
            # 读取图片并转换为base64
            with open(mistake_data['question_image'], 'rb') as img_file:
                img_data = img_file.read()
                base64_data = base64.b64encode(img_data).decode('utf-8')
            
            # 获取图片MIME类型
            ext = os.path.splitext(mistake_data['question_image'])[1].lower()
            mime_type = f"image/{ext[1:]}" if ext else "image/jpeg"
            
            # 构建Data URI
            data_uri = f"data:{mime_type};base64,{base64_data}"
            
            image_html = f"""
                <hr>
                <h3>题目配图:</h3>
                <img src="{data_uri}" alt="题目图片" style="max-width: 100%; height: auto;">
            """
        except Exception as e:
            print(f"Error loading image: {e}")
            image_html = f"""
                <hr>
                <h3>题目配图:</h3>
                <div style="color: red;">图片加载失败: {str(e)}</div>
            """

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>错题详情</title>
        <style>{katex_css}</style>
        <script>{katex_js}</script>
        <script>{auto_render_js}</script>
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
                white-space: pre-wrap; /* 保留换行符和空格，以便KaTeX正确处理块公式 */
            }}
            .meta-info {{
                color: #FF33FF;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 5px;
                margin-top: 15px;
                margin-bottom: 12px;
                font-size: 1em; /* Adjust font size as needed */
                text-align: center;
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
                <b>年级:</b> {mistake_data['grade']} {mistake_data['semester']}&nbsp;&nbsp;
                <b>录入日期:</b> {mistake_data['record_date']}
            </div>
            
            <h3>题目:</h3>
            <div id="question" class="content-box">{question_desc}</div>
            
            {image_html}
            {answer_html}
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: "$$", right: "$$", display: true}},
                        {{left: "$", right: "$", display: false}},
                        {{left: "\\[", right: "\\]", display: true}},
                        {{left: "\\(", right: "\\)", display: false}}
                    ],
                    // Be less strict about what is considered valid math,
                    // to allow for mixed text and math, and avoid warnings.
                    strict: false
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html_template