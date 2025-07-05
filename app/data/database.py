# app/data/database.py
import sqlite3
import os

# 使用绝对路径，确保数据库文件在项目根目录下
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "database", "qisilu.db")
DB_DIR = os.path.dirname(DB_FILE)

def init_db():
    """
    初始化数据库，创建表。
    """
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
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
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    """
    获取数据库连接。
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def add_mistake(data):
    """
    向数据库中添加一条新的错题记录。
    data 是一个包含错题信息的字典。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mistakes (subject, grade, semester, record_date, question_desc, question_image, correct_answer, mistake_reason)
        VALUES (:subject, :grade, :semester, :record_date, :question_desc, :question_image, :correct_answer, :mistake_reason)
    """, data)
    conn.commit()
    conn.close()

def get_mistakes(filters=None):
    """
    根据筛选条件从数据库中获取错题记录。
    filters 是一个包含筛选条件的字典。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM mistakes"
    params = []
    
    if filters:
        conditions = []
        for key, value in filters.items():
            if value:
                conditions.append(f"{key} LIKE ?")
                params.append(f"%{value}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY id DESC"
            
    cursor.execute(query, params)
    mistakes = cursor.fetchall()
    conn.close()
    return mistakes

def update_mistake(mistake_id, data):
    """
    更新数据库中的一条错题记录。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE mistakes SET
            subject = :subject,
            grade = :grade,
            semester = :semester,
            question_desc = :question_desc,
            question_image = :question_image,
            correct_answer = :correct_answer,
            mistake_reason = :mistake_reason
        WHERE id = :id
    """, {**data, 'id': mistake_id})
    conn.commit()
    conn.close()

def delete_mistake(mistake_id):
    """
    从数据库中删除一条错题记录。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mistakes WHERE id = ?", (mistake_id,))
    conn.commit()
    conn.close()

def get_mistake_by_id(mistake_id):
    """
    通过ID获取单个错题记录，主要用于获取图片路径。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mistakes WHERE id = ?", (mistake_id,))
    mistake = cursor.fetchone()
    conn.close()
    return mistake

def get_random_mistakes(count, filters=None):
    """
    根据筛选条件随机获取指定数量的错题。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM mistakes"
    params = []

    if filters:
        conditions = []
        for key, value in filters.items():
            if value:
                conditions.append(f"{key} LIKE ?")
                params.append(f"%{value}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY RANDOM() LIMIT ?"
    params.append(count)
    
    cursor.execute(query, params)
    mistakes = cursor.fetchall()
    conn.close()
    return mistakes