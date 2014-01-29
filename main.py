import logging
import os
import urllib

from google.appengine.api import mail
from google.appengine.ext import ndb


import jinja2
import webapp2



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


### Models ###

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    github_id = ndb.StringProperty()

    @classmethod
    def create(cls, name, **kwargs):
        id = name.lower().strip().replace(' ', '_')
        user = cls(id=id)
        user.populate(**kwargs)
        user.put()
        return user


class Update(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.TextProperty()



### Handlers ###

class BaseHandler(webapp2.RequestHandler):
    def write_template(self, file_name, context={}):
        template = JINJA_ENVIRONMENT.get_template(file_name)
        output = template.render(context)
        self.response.write(output)


class IndexHandler(BaseHandler):
    def get(self):
        self.write_template('index.html')
        


class PersonHandler(BaseHandler):
    def get(self):
        self.write_template('index.html')


class EmailHandler(BaseHandler):
    def post(self):
        message = mail.InboundEmailMessage(self.request.body)
        logging.debug(message.sender)
        logging.debug(message.subject)

        for msg_type, text in message.bodies('text/plain'):
            body = ''
            for line in text.decode().splitlines():
                if line.startswith('On') and line.endswith('wrote:'):
                    break
                else:
                    body += line + '\n'
            body = body.strip()
            logging.debug(body)





app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/(.+@.+)', PersonHandler),
    ('/_ah/mail/.+', EmailHandler)
], debug=True)
