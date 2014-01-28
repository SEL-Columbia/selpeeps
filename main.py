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


class Update(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.TextProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class EmailHandler(webapp2.RequestHandler):
    def post(self):
        message = mail.InboundEmailMessage(self.request.body)
        logging.debug(message.sender)
        logging.debug(message.subject)
        for body in message.bodies('text/plain'):
            logging.debug(str(body[1].decode()))





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/_ah/mail/.+', EmailHandler)
], debug=True)
