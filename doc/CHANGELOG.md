# 更新日志

所有此项目的显著更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
并且本项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [1.6.0] - 2025-06-25

### ✨ 新增 (Added)



## [1.4.0] - 2025-06-25

### ✨ 新增 (Added)

- 新增“关于”对话框，显示软件版本、作者和联系方式。
- 增加错题摘要列，方便快速浏览错题内容。
- 添加学期筛选功能，支持“上册”和“下册”筛选。
- 界面美化，采用现代简约风格，支持浅色和暖色调主题切换。
- 统一软件版本号管理，使用`app/utils/version.py`模块。
- 优化按钮和标题字体，提升界面一致性和美观度。
## [1.0.0] - 2025-06-24

### ✨ 新增 (Added)

- **项目初始化**: 创建了完整的项目结构，包括UI、逻辑、数据和工具层。
- **错题录入**: 实现新增/编辑错题的功能，支持按年级、学科、学期分类。
- **富文本支持**:
    - 支持题目和答案的富文本录入。
    - 使用 Matplotlib 实现 LaTeX 公式渲染和实时预览。
    - 支持上传和预览题目配图，图片文件与数据库记录关联。
- **错题管理**:
    - 主界面使用 `QTableView` 展示错题列表。
    - 实现按分类和关键词的智能筛选功能。
    - 实现错题详情展示区，可显示渲染后的公式和完整的图文信息。
    - 实现删除功能，并在删除数据库记录时同步删除关联的图片文件。
- **复习功能**:
    - 实现“随机抽取”功能，可根据筛选条件和指定数量生成复习列表。
    - 创建了专门的复习对话框，支持逐题浏览和“显示答案”功能。
- **导出功能**:
    - 使用 ReportLab 实现将筛选后的错题集导出为排版精美的 PDF 文件。
    - PDF 支持中文显示，并能正确嵌入渲染后的公式图片和题目配图。
- **文档**:
    - 添加了 `README.md` 和 `README_CN.md` 文件。
    - 添加了 `VERSION` 文件来管理版本号。
    - 添加了本 `CHANGELOG.md` 文件。