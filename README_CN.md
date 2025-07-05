# 启思录 (Insight Folio) - v1.0.0

启思录是一款专为中小学生设计的桌面端错题管理软件。它旨在帮助学生高效地记录、管理、复习和打印错题，从而巩固知识、提升学习效率。

## ✨ 功能特性

- **分类管理**: 支持按“年级”、“学期”和“学科”对错题进行精细化分类。
- **富文本录入**: 支持题目和答案的富文本编辑，能够完美渲染 **LaTeX** 数学和物理公式。
- **图文并茂**: 支持为每道错题上传配图，如几何图形、实验装置图等。
- **智能筛选**: 可根据一个或多个分类条件组合查询，快速定位目标错题。
- **详情预览**: 在主界面即可预览错题的完整信息，包括渲染后的公式和图片。
- **随机复习**: 内置“随机抽取”功能，可根据筛选条件生成练习试卷，并支持隐藏/显示答案。
- **一键导出**: 支持将筛选或随机抽取的错题集合导出为排版精美的 **PDF 文件**，方便打印成纸质试卷。
- **安全删除**: 删除错题时，会自动清理关联的图片文件，释放磁盘空间。

## 🛠️ 技术栈

- **编程语言**: Python 3.8+
- **GUI 框架**: PySide6
- **数据库**: SQLite 3
- **LaTeX 渲染**: KaTeX (JavaScript)
- **PDF 生成**: Qt WebEngine
- **图像处理**: Qt Graphics

## 🚀 如何运行

1.  **克隆仓库**
    ```bash
    git clone https://your-repo-url.git
    cd InsightFolio
    ```

2.  **创建虚拟环境并安装依赖**
    建议使用虚拟环境以隔离项目依赖。
    ```bash
    # 创建虚拟环境
    python -m venv venv

    # 激活虚拟环境
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate

    # 安装依赖
    pip install -r requirements.txt
    ```

3.  **运行程序**
    ```bash
    python main.py
    ```

## 📂 项目结构

```
InsightFolio/
├── main.py                     # 应用主入口
├── app/
│   ├── ui/                     # UI界面模块
│   ├── logic/                  # 业务逻辑模块
│   ├── data/                   # 数据访问模块
│   └── utils/                  # 工具函数模块
├── assets/
│   └── images/                 # 存放所有错题配图
├── database/
│   └── qisilu.db               # SQLite 数据库文件
├── VERSION                     # 版本号文件
├── README.md                   # 项目说明（英文）
└── README_CN.md                # 项目说明（中文）
```

## 📝 更新日志

请参阅 [CHANGELOG.md](CHANGELOG.md) 文件。