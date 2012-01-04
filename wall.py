import MySQLdb as mdb

class wall:
    def __init__(self, username):
        self.username = username
        self.body = None
        self.posts = []
        
    def pull(self, username):
        con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
        with con:
          cur = con.cursor()
          query = "SELECT Id, Post FROM Message WHERE Username=\"%(username)s\"  " % locals()
          cur.execute(query)
          rows = cur.fetchall()
          for post in rows:
                self.posts.append(post)
          print rows

    def return_html(self):
        html = "<html><body>\n"
        html += self.body
        html += '\n'
        for post in self.posts:
            html += "post <br />\n"
            html += str(post[0])
            html += post[1]
            html += "<br />"
        html += "</html></body>"
        return html



        

