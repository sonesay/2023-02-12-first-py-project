import sqlite3


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
