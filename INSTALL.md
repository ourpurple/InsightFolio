# InsightFolio 安装说明

## 系统要求

- Python 3.8 或更高版本
- Windows 10/11, macOS 10.14+, 或 Linux
- 至少 100MB 可用磁盘空间

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone <repository-url>
cd InsightFolio
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行应用

```bash
python main.py
```

## 依赖说明

### 必需依赖

- **PySide6>=6.5.0**: Qt框架的Python绑定，提供GUI界面功能
  - 包含QtWidgets、QtWebEngineWidgets等模块
  - 用于创建桌面应用程序界面
  - 支持HTML渲染和PDF导出功能

### 可选依赖

如果需要增强功能，可以考虑安装以下包：

```bash
# 更好的PDF导出功能
pip install reportlab>=4.0.0
pip install weasyprint>=60.0

# 开发工具
pip install pytest>=7.0.0
pip install black>=23.0.0
pip install flake8>=6.0.0
```

## 故障排除

### PySide6安装问题

如果PySide6安装失败，可以尝试：

```bash
# 使用conda安装
conda install -c conda-forge pyside6

# 或者使用pip安装预编译版本
pip install --only-binary=all PySide6
```

### 权限问题

在某些系统上可能需要管理员权限：

```bash
# Windows (以管理员身份运行PowerShell)
pip install -r requirements.txt

# Linux/macOS
sudo pip install -r requirements.txt
```

## 项目结构

```
InsightFolio/
├── main.py                 # 应用入口
├── requirements.txt        # Python依赖
├── app/
│   ├── data/
│   │   └── database.py     # 数据库操作
│   │   └── mistake_service.py  # 业务逻辑
│   ├── ui/
│   │   ├── main_window.py      # 主窗口
│   │   ├── add_edit_dialog.py  # 添加/编辑对话框
│   │   └── review_dialog.py    # 复习对话框
│   └── utils/
│       ├── renderer.py         # HTML渲染器
│       └── version.py          # 版本信息
├── assets/
│   └── katex/             # KaTeX数学公式渲染库
└── database/              # SQLite数据库文件
```

## 功能特性

- 📝 错题录入和管理
- 🔍 多条件筛选和搜索
- 📊 错题复习功能
- 📄 PDF导出功能
- 🧮 KaTeX数学公式支持
- 🖼️ 图片上传和预览
- 💾 SQLite本地数据存储 