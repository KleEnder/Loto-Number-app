#!/usr/bin/env python
import os
import jinja2
import webapp2
import random
from random import randint

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("main.html")

class LotoHandler(BaseHandler):
    def get(self):
        def loto(value):
            list_of_guesses = [randint(0, 37) for p in range(0, value)]
            # random(list_of_guesses, value)
            return str(list_of_guesses).replace('[', '').replace(']', '')

        enviornment = dict()

        enviornment['loto'] = loto(8)

        return self.render_template("loto.html", params=enviornment)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/loto', LotoHandler)
], debug=True)
