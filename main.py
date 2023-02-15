import html
import json
from collections import namedtuple

from html2ans.default import Html2Ans
import sqlite3
import random
import string
import requests


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Story:
    def __init__(self, type, version, canonical_website, headlines):
        self._id = self.generate_unique_id()
        self.type = type
        self.version = version
        self.canonical_website = canonical_website
        self.headlines = headlines
        self.content_elements = []

    def generate_unique_id(self):
        return ''.join(random.choices(string.ascii_uppercase, k=26))


class Headlines:
    def __init__(self, basic):
        self.basic = html.unescape(basic).replace('�', '')


def delete_arc_story(news_article):
    if news_article.arc_id is not None:
        end_point = 'https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story/' + news_article.arc_id
        headers = {
            'Authorization': 'Bearer TB7AST8FPLI9N1EA0AJCBHVOC694343Kmf6XiFTdlDld2XZBO7vikH0Mm4d4QHPLtMRASY08',
            'Content-Type': 'application/json'
        }
        response = requests.delete(end_point, headers=headers, verify=True)
        return response.text
    else:
        # Handle the case where arc_id is None
        return False


def post_to_arc_migration_content(end_point, content):
    headers = {
        'Authorization': 'Bearer TB7AST8FPLI9N1EA0AJCBHVOC694343Kmf6XiFTdlDld2XZBO7vikH0Mm4d4QHPLtMRASY08',
        'Content-Type': 'application/json'
    }
    content_json = json.dumps(content, default=lambda o: o.__dict__)
    response = requests.post(end_point, headers=headers, data=content_json, verify=True)
    return response.text


if __name__ == '__main__':
    conn = sqlite3.connect(r'C:\Users\sone\Desktop\mts6\php\php8-xdebug3-docker\web\database\database.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NOT NULL ORDER BY id ASC LIMIT 1;")
    rows = cursor.fetchall()
    column_names = [d[0] for d in cursor.description]

    for row in rows:
        print(row)
        print(row['id'])
        parser = Html2Ans()
        content_elements = parser.generate_ans(row['body'])
        content_elements = [elem for elem in content_elements if elem['type'] != 'image']

        # for elem in content_elements:
        #     if elem['type'] == 'raw_html':
        #         # elem['content'] = html.unescape(elem['content']).replace('�', '')
        #         # elem['content'] = elem['content'].encode('utf-8')
        #         # elem['content'] = elem['content'].decode('utf-8')
        #         elem['content'] = elem['content']

        print(content_elements)
        content_elements_str = str(content_elements)
        # cursor.execute("UPDATE news_article_syncs SET body2=? WHERE id=?", (content_elements_str, row['id'],))

        # Create a namedtuple to represent the row for convenience
        # (Optional, but recommended)
        NewsArticle = namedtuple('NewsArticle', column_names)
        news_article = NewsArticle(*row)

        responseDelete = delete_arc_story(news_article)

        headlines = Headlines(news_article.title)
        story = Story("story", "0.10.9", "teaomaori", headlines)
        story.content_elements = content_elements;

        responsePost = post_to_arc_migration_content(
            "https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story", story)

        # Extract the id from the response
        response_data = json.loads(responsePost)
        arc_id = response_data['id']

        # Update the new_article_syncs table with the arc_id
        cursor.execute("UPDATE news_article_syncs SET arc_id=? WHERE id=?", (arc_id, row['id']))

    conn.commit()

    cursor.close()
    conn.close()
