from html2ans.default import Html2Ans
import sqlite3

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # print_hi(content_elements)

    accessToken = "TB7AST8FPLI9N1EA0AJCBHVOC694343Kmf6XiFTdlDld2XZBO7vikH0Mm4d4QHPLtMRASY08"

    # Connect to the database
    conn = sqlite3.connect(r'C:\Users\sone\Desktop\mts6\php\php8-xdebug3-docker\web\database\database.sqlite')
    conn.row_factory = sqlite3.Row

    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()

    # Select data from the table
    cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NOT NULL ORDER BY id DESC LIMIT 1;")

    # Fetch all the data returned by the SELECT statement
    rows = cursor.fetchall()

    # Loop through the rows and print the data
    for row in rows:
        print(row)
        print(row)
        print(row['id'])

        parser = Html2Ans()
        content_elements = parser.generate_ans(row['body'])
        print(content_elements)
        content_elements_str = str(content_elements)


        cursor.execute("UPDATE news_article_syncs SET body2=? WHERE id=?", (content_elements_str, row['id'],))

    conn.commit()


    # Close the cursor and the connection
    cursor.close()
    conn.close()



