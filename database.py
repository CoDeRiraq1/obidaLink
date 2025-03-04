import sqlite3
import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """إنشاء جميع الجداول المطلوبة"""
        # جدول المستخدمين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                points INTEGER DEFAULT 0,
                invited_by INTEGER,
                join_date DATETIME
            )''')
        
        # جدول المجموعات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                name TEXT,
                link TEXT UNIQUE,
                type TEXT,
                status TEXT DEFAULT 'pending',
                owner_id INTEGER,
                priority_expiry DATETIME,
                submission_date DATETIME
            )''')
        
        # جدول الإحالات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS referrals (
                referrer_id INTEGER,
                referred_id INTEGER UNIQUE,
                date DATETIME
            )''')
        
        self.conn.commit()
    
    # ---- دوال المستخدمين ----
    def add_user(self, user_id, username, referrer_id=None):
        """إضافة مستخدم جديد مع نظام الإحالة"""
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, join_date)
            VALUES (?, ?, ?)
        ''', (user_id, username, datetime.datetime.now()))
        
        if referrer_id and referrer_id != user_id:
            try:
                self.cursor.execute('''
                    INSERT INTO referrals (referrer_id, referred_id, date)
                    VALUES (?, ?, ?)
                ''', (referrer_id, user_id, datetime.datetime.now()))
                self.cursor.execute('''
                    UPDATE users SET points = points + ? 
                    WHERE user_id = ?
                ''', (POINTS_PER_REFERRAL, referrer_id))
            except sqlite3.IntegrityError:
                pass
        
        self.conn.commit()
    
    # ---- دوال المجموعات ----
    def add_group(self, name, link, type_, owner_id):
        """إضافة مجموعة جديدة بحالة معلقة"""
        self.cursor.execute('''
            INSERT INTO groups 
            (name, link, type, owner_id, submission_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, link, type_, owner_id, datetime.datetime.now()))
        self.conn.commit()
        return self.cursor.lastrowid
    
    # ... (بقية الدوال)
