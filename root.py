import cherrypy
import MySQLdb as mdb
import wall
import html_page
from auth import AuthController, require, member_of, name_is

SESSION_KEY = '_cp_username'

class RestrictedArea:
    
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }
    
    @cherrypy.expose
    def index(self):
        return """This is the admin only area."""


class Root:
    
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }
    
    auth = AuthController()
    
    restricted = RestrictedArea()
    
    @cherrypy.expose
    @require()
    def index(self):
        
        return """
            This page only requires a valid login.
            <a href="auth/logout">LOUGOUT</a>
        """
    
    def get_postform(self, msg="post", from_page="/", username=None):
        wall1 = wall.wall(username)
        wall1.body = \
        """<form method="post" action="/post">
            <input type="hidden" name="from_page" value="%(from_page)s" />
            %(msg)s<br />
            Post: <input type="text" name="message" /> <br />
            <input type="submit" value="Post" />
        """ %locals()
        wall1.pull(username)
        return wall1.return_html()

    def post_to_database(self, message, username):
        con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
        with con:
            cur = con.cursor()
            query = "INSERT INTO Message(Username, Post) VALUES('%(username)s', '%(message)s')" %locals()
            cur.execute(query)
            return None
        return u"database error"
        

    @cherrypy.expose
    @require()
    def post(self, message=None, from_page="/"):
        username = cherrypy.session.get(SESSION_KEY)
        if message == None:
            return self.get_postform(from_page=from_page, username=username)
        error_msg = self.post_to_database(message, username)
        if error_msg:
            return self.get_postform(self, error_msg, from_page, username)
        else:
            raise cherrypy.HTTPRedirect("/post")
 
    @cherrypy.expose
    def gethint(self, q):
        print "hello"
        print q
        return "no suggestion"

        

    @cherrypy.expose
    def open(self):
        home_page = html_page.html_page("html_src/showhint")
        return home_page.get_html()
    
    @cherrypy.expose
    @require(name_is("joe"))
    def only_for_joe(self):
        return """Hello Joe - this page is available to you only"""

    # This is only available if the user name is joe _and_ he's in group admin
    @cherrypy.expose
    @require(name_is("joe"))
    @require(member_of("admin"))   # equivalent: @require(name_is("joe"), member_of("admin"))
    def only_for_joe_admin(self):
        return """Hello Joe Admin - this page is available to you only"""


if __name__ == '__main__':
    cherrypy.server.socket_port = 8081
    cherrypy.quickstart(Root())
