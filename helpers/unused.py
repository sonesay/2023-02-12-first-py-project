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


import base64
import hashlib
import json
import uuid
import six

#
# def generate_arc_id(*args, **kwargs):
#     r"""generate_arc_id(*args, **kwargs)
#     Computes a hash to generate an Arc ID
#
#     Values given to \*args and \*\*kwargs must be JSON-compatible.
#
#     It is recommended to make the organization one of the factors for computing
#     the hash IDs.  This will ensure IDs are not duplicated across organizations.
#
#     It is also recommended that this function be hidden behind another
#     function that validates input to ensure consistent behavior in practice.
#
#     For example, if Arc IDs are to be based off of an integer value, if a
#     string representation of that value is used, a different ID will result.
#     Fronting this function will allow control over the inputs by implementing
#     validation, specific to the client's use case."""
#
#     uuid_object = uuid.UUID(
#         bytes=hashlib.blake2b(
#             json.dumps((args, kwargs), sort_keys=1, separators=(",", ":")).encode("utf-8"),
#             digest_size=16,
#         ).digest()
#     )
#     return six.text_type(base64.b32encode(uuid_object.bytes), encoding="utf-8").replace("=", "")  # to remove padding
#
#
