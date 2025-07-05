# Insight Folio - v1.0.0

Insight Folio is a desktop application designed for primary and secondary school students to manage their incorrect test answers. It aims to help students efficiently record, categorize, review, and print their mistakes, thereby reinforcing knowledge and improving learning outcomes.

## ✨ Features

- **Categorization**: Supports fine-grained classification of mistakes by "Grade," "Semester," and "Subject."
- **Rich Text Input**: Supports rich text editing for questions and answers, with perfect rendering of **LaTeX** mathematical and physical formulas.
- **Image Support**: Allows uploading an accompanying image for each mistake, such as geometric figures or experimental setup diagrams.
- **Smart Filtering**: Enables combined searching based on one or more classification criteria to quickly locate target mistakes.
- **Detailed Preview**: Preview the complete information of a mistake, including rendered formulas and images, directly on the main interface.
- **Randomized Review**: Features a "Random Draw" function to generate practice tests based on filter conditions, with support for showing/hiding answers.
- **One-Click Export**: Supports exporting a collection of filtered or randomly selected mistakes into a beautifully formatted **PDF file**, ready for printing.
- **Safe Deletion**: Automatically cleans up associated image files when a mistake is deleted, freeing up disk space.

## 🛠️ Technology Stack

- **Programming Language**: Python 3.8+
- **GUI Framework**: PySide6
- **Database**: SQLite 3
- **LaTeX Rendering**: KaTeX (JavaScript)
- **PDF Generation**: Qt WebEngine
- **Image Processing**: Qt Graphics

## 🚀 How to Run

1.  **Clone the Repository**
    ```bash
    git clone https://your-repo-url.git
    cd InsightFolio
    ```

2.  **Create a Virtual Environment and Install Dependencies**
    It is recommended to use a virtual environment to isolate project dependencies.
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    python main.py
    ```

## 📂 Project Structure

```
InsightFolio/
├── main.py                     # Application entry point
├── app/
│   ├── ui/                     # UI modules
│   ├── logic/                  # Business logic modules
│   ├── data/                   # Data access modules
│   └── utils/                  # Utility function modules
├── assets/
│   └── images/                 # Stores all mistake images
├── database/
│   └── qisilu.db               # SQLite database file
├── VERSION                     # Version file
├── README.md                   # Project description (English)
└── README_CN.md                # Project description (Chinese)
```

## 📝 Changelog

Please see the [CHANGELOG.md](CHANGELOG.md) file.