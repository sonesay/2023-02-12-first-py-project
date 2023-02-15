import sqlite3


class DbConn:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def check_news_article_syncs(self, category):
        self.cursor.execute(
            f"SELECT * FROM news_article_syncs WHERE category = '{category}' ORDER BY page DESC LIMIT 1;")
        row = self.cursor.fetchone()
        if row is not None:
            return row[1]
        else:
            return None
