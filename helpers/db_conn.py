import sqlite3
from datetime import datetime


class DbConn:
    def __init__(self):
        self.conn = sqlite3.connect(r'C:\Users\sone\Desktop\mts6\php\php8-xdebug3-docker\web\database\database.sqlite')
        self.cursor = self.conn.cursor()

    def check_news_article_syncs(self, category):
        self.cursor.execute(
            f"SELECT page FROM news_article_syncs WHERE category = '{category}' ORDER BY page DESC LIMIT 1;")
        row = self.cursor.fetchone()
        if row is not None:
            return int(row[0])
        else:
            return None

    def set_article(self, category, title, published_date, author, page, request_url, link):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # check if record already exists
        self.cursor.execute(
            f"SELECT id FROM news_article_syncs WHERE category = ? AND title = ?",
            (category, title)
        )
        row = self.cursor.fetchone()
        if row is not None:
            # update existing record
            self.cursor.execute(
                f"UPDATE news_article_syncs SET article_datetime = ?, article_credits = ?, updated_at = ? WHERE id = ?",
                (published_date, author, now, row[0])
            )
            self.conn.commit()
        else:
            # insert new record
            if page is None:
                page = 0
            self.cursor.execute(
                f"INSERT INTO news_article_syncs (category, title, published_date, author, page, request_url, link, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (category, title, published_date, author, page or 0, request_url, link, now, now)
            )
            self.conn.commit()
