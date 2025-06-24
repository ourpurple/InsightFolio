### **项目开发说明书：启思录 (Insight Folio)**

**版本：** 1.0
**目标：** 开发一款面向中小学生的桌面端错题管理软件，帮助用户记录、分类、复习和打印错题，提升学习效率。

#### **1. 核心功能需求 (Functional Requirements)**

1.  **错题录入 (Create)**
    *   支持按“年级”、“学期（上下册）”、“学科”进行分类。
    *   题目描述支持**富文本输入**，特别是需要渲染 **LaTeX** 数学/物理公式。
    *   支持上传**题目配图**（如几何图形、电路图等）。
    *   需录入“正确答案”和“错误原因分析”。
    *   自动记录“录入日期”。

2.  **错题管理 (Read, Update, Delete)**
    *   主界面以列表或表格形式展示所有错题。
    *   提供筛选功能，可按一个或多个分类条件（年级、学科等）组合查询错题。
    *   支持查看错题详情，包括渲染后的题目、配图、答案和分析。
    *   支持对已录入的错题进行编辑和更新。
    *   支持删除错题，并在删除记录时**同步删除关联的图片文件**。

3.  **复习与练习 (Review)**
    *   提供“随机抽取”功能。
    *   用户可以根据筛选条件（如“七年级数学上册”），指定抽取的题目数量（如5道）。
    *   程序随机展示题目，答案默认隐藏，提供“显示答案”按钮。

4.  **导出与打印 (Export)**
    *   支持将筛选或随机抽取出的错题集合**导出为 PDF 文件**。
    *   PDF 格式应清晰、美观，适合直接打印成纸质试卷。
    *   PDF 中应包含题号、题目描述（渲染后的LaTeX）、题目配图和答案区域。

#### **2. 技术栈 (Technology Stack)**

*   **编程语言:** Python 3.9+
*   **GUI 框架:** PySide6
*   **数据库:** SQLite 3 (使用内置 `sqlite3` 模块)
*   **LaTeX 渲染:** Matplotlib
*   **PDF 生成:** ReportLab
*   **桌面端打包:** PyInstaller

#### **3. 架构与设计**

采用**三层架构**以实现高内聚、低耦合，便于维护和扩展。

*   **项目目录结构:**
    ```
    QisiLu/
    ├── main.py                     # 应用主入口
    ├── app/
    │   ├── ui/                     # UI界面模块 (.py)
    │   │   ├── main_window.py
    │   │   └── add_edit_dialog.py
    │   ├── logic/                  # 业务逻辑模块
    │   │   └── mistake_service.py
    │   ├── data/                   # 数据访问模块
    │   │   └── database.py
    │   └── utils/                  # 工具函数模块
    │       └── renderer.py
    └── assets/
    │   └── images/                 # 存放所有错题配图
    └── database/
        └── qisilu.db               # SQLite 数据库文件
    ```

*   **数据库设计 (`database/qisilu.db`)**
    **表名: `mistakes`**

| 字段名 (Column) | 数据类型 (Type) | 描述 |
| :--- | :--- | :--- |
| `id` | INTEGER | 主键，自增 |
| `subject` | TEXT | 学科 (如: 数学, 物理) |
| `grade` | TEXT | 年级 (如: 七年级) |
| `semester` | TEXT | 学期 (如: 上册) |
| `record_date` | DATE | 录入日期 (格式: YYYY-MM-DD) |
| `question_desc` | TEXT | 题目描述，含原始 LaTeX 文本 |
| `question_image`| TEXT | 题目配图的**相对路径** (如: `assets/images/uuid.png`) |
| `correct_answer`| TEXT | 正确答案，含原始 LaTeX 文本 |
| `mistake_reason`| TEXT | 错误原因分析 |
| `review_count` | INTEGER | 复习次数，默认为 0 |
| `last_review_date`| DATE | 上次复习日期 |

    **SQL 创建语句:**
    ```sql
    CREATE TABLE IF NOT EXISTS mistakes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        grade TEXT NOT NULL,
        semester TEXT NOT NULL,
        record_date DATE NOT NULL,
        question_desc TEXT NOT NULL,
        question_image TEXT,
        correct_answer TEXT,
        mistake_reason TEXT,
        review_count INTEGER DEFAULT 0,
        last_review_date DATE
    );
    ```

#### **4. 模块实现指南**

1.  **数据访问层 (`app/data/database.py`)**
    *   封装所有 SQL 操作。
    *   实现 `init_db()`、`add_mistake(data)`、`update_mistake(id, data)`、`delete_mistake(id)`、`get_mistakes(filters)` 和 `get_random_mistakes(count, filters)` 等函数。
    *   `get_random_mistakes` 使用 `ORDER BY RANDOM() LIMIT ?` 实现。

2.  **工具函数层 (`app/utils/renderer.py`)**
    *   **`render_latex_to_pixmap(latex_str)`:** 使用 Matplotlib 将 LaTeX 字符串渲染为内存中的 PNG 图像 (`BytesIO`)，然后加载为 `QPixmap` 对象供UI显示。
    *   **`render_latex_to_file(latex_str, filepath)`:** 渲染 LaTeX 到一个临时图片文件，供 PDF 导出时使用。

3.  **UI - 新增/编辑对话框 (`app/ui/add_edit_dialog.py`)**
    *   使用 `QDialog`。包含用于选择分类的 `QComboBox`，录入文本的 `QTextEdit`，以及用于上传图片的 `QPushButton` 和预览的 `QLabel`。
    *   **LaTeX 实时预览**: 连接 `QTextEdit` 的 `textChanged` 信号到槽，调用 `render_latex_to_pixmap` 更新预览 `QLabel`。
    *   **图片上传逻辑**: 点击按钮后打开 `QFileDialog`，将用户选择的图片用 `uuid` 重命名后复制到 `assets/images/` 目录，并将相对路径存入变量。

4.  **UI - 主窗口 (`app/ui/main_window.py`)**
    *   使用 `QTableView` + `QStandardItemModel` 显示错题列表，性能更佳。
    *   顶部的 `QComboBox` 和 `QLineEdit` 用作筛选器。
    *   按钮“新增”、“删除”、“开始复习”、“导出PDF”等，分别连接到业务逻辑层的相应功能。
    *   设置一个详情区域，用于显示选中行的完整信息，包括渲染后的公式和配图。

5.  **业务逻辑层 (`app/logic/mistake_service.py`)**
    *   作为 UI 层和数据层的桥梁。
    *   **`export_to_pdf(mistakes_list, filepath)`:**
        *   接收一个错题数据列表。
        *   使用 `ReportLab` 创建 PDF 文档。
        *   遍历列表，对每道题：
            *   将文本部分用 `Paragraph` 添加。
            *   将 LaTeX 公式调用 `render_latex_to_file` 生成图片后用 `Image` 添加。
            *   将题目配图（如果存在）用 `Image` 添加。
        *   生成最终的 PDF 文件。
    *   **`delete_mistake_with_assets(mistake_id)`:**
        *   先从数据库查询该 ID 的记录以获取图片路径。
        *   调用 `database.delete_mistake(id)`。
        *   使用 `os.remove()` 删除磁盘上的图片文件。

#### **5. 开发流程建议**
1.  **环境搭建**: 创建 Python 虚拟环境并安装所有依赖。
2.  **后端优先**: 首先实现 `database.py` 并编写单元测试，确保数据库功能稳定。
3.  **实现核心工具**: 开发并测试 `renderer.py` 中的 LaTeX 渲染功能。
4.  **构建UI骨架**: 使用 Qt Designer 或纯代码构建 `main_window.py` 和 `add_edit_dialog.py` 的静态界面。
5.  **功能穿透开发**:
    *   先实现**新增**功能，打通 UI -> Logic -> Data 的完整流程。
    *   然后实现**显示和筛选**功能。
    *   接着实现**删除**功能，确保文件同步删除。
    *   实现**随机复习**功能。
    *   最后实现**PDF导出**功能。
6.  **打包发布**: 使用 PyInstaller 将项目打包为单个可执行文件。

这份说明书清晰地定义了项目的范围、技术选型和实施路径，任何开发者（包括AI）都可以基于此文档高效地开展工作。祝您和您的孩子能早日用上这款充满父爱的软件！