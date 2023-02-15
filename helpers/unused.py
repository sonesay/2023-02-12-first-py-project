# for elem in content_elements:
#     if elem['type'] == 'raw_html':
#         # elem['content'] = html.unescape(elem['content']).replace('�', '')
#         # elem['content'] = elem['content'].encode('utf-8')
#         # elem['content'] = elem['content'].decode('utf-8')
#         elem['content'] = elem['content']
# cursor.execute("UPDATE news_article_syncs SET body2=? WHERE id=?", (content_elements_str, row['id'],))


# cursor.execute("SELECT * FROM news_article_syncs WHERE category = category ORDER BY page DESC LIMIT 1;")
