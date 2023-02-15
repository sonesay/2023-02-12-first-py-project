from collections import namedtuple
from html2ans.default import Html2Ans
from helpers.api_request import APIRequest
from models.story import Headlines, Story
import json
import sqlite3

if __name__ == '__main__':
    api_key = 'TB7AST8FPLI9N1EA0AJCBHVOC694343Kmf6XiFTdlDld2XZBO7vikH0Mm4d4QHPLtMRASY08'
    api_request = APIRequest(api_key)
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
        print(content_elements)
        content_elements_str = str(content_elements)

        # Create a namedtuple to represent the row for convenience
        # (Optional, but recommended)
        NewsArticle = namedtuple('NewsArticle', column_names)
        news_article = NewsArticle(*row)

        # Delete any existing arc stories with matching id
        responseDelete = api_request.delete_arc_story(news_article)

        headlines = Headlines(news_article.title)
        story = Story("story", "0.10.9", "teaomaori", headlines)
        story.content_elements = content_elements;

        responsePost = api_request.post_to_arc_migration_content(
            "https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story", story)

        # Extract the id from the response
        response_data = json.loads(responsePost)
        arc_id = response_data['id']

        # Update the new_article_syncs table with the arc_id
        cursor.execute("UPDATE news_article_syncs SET arc_id=? WHERE id=?", (arc_id, row['id']))

    conn.commit()

    cursor.close()
    conn.close()
