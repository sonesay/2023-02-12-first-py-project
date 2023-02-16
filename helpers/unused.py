# for elem in content_elements:
#     if elem['type'] == 'raw_html':
#         # elem['content'] = html.unescape(elem['content']).replace('�', '')
#         # elem['content'] = elem['content'].encode('utf-8')
#         # elem['content'] = elem['content'].decode('utf-8')
#         elem['content'] = elem['content']
# cursor.execute("UPDATE news_article_syncs SET body2=? WHERE id=?", (content_elements_str, row['id'],))


# cursor.execute("SELECT * FROM news_article_syncs WHERE category = category ORDER BY page DESC LIMIT 1;")

# Converting for ARC API POST
# parser = Html2Ans()
#             content_elements = parser.generate_ans(row['body'])
#             content_elements = [elem for elem in content_elements if elem['type'] != 'image']
#             print(content_elements)
#
#             # Create a namedtuple to represent the row for convenience
#             # (Optional, but recommended)
#             NewsArticle = namedtuple('NewsArticle', column_names)
#             news_article = NewsArticle(*row)
#
#             # Delete any existing arc stories with matching id
#             response_delete = self.api_request.delete_arc_story(news_article)
#
#             headlines = Headlines(news_article.title)
#             story = Story("story", "0.10.9", "teaomaori", headlines)
#             story.content_elements = content_elements;
#
#             response_post = self.api_request.post_to_arc_migration_content(
#                 "https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story", story)
#
#             # Extract the id from the response
#             response_data = json.loads(response_post)
#             arc_id = response_data['id']
#
#             # Update the new_article_syncs table with the arc_id
#             cursor.execute("UPDATE news_article_syncs SET arc_id=? WHERE id=?", (arc_id, row['id']))
