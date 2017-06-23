#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from models import Guestbook
from jinja2 import utils

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        ime = self.request.get(utils.escape("ime"))
        if len(ime) == 0 or ime.isdigit():
            ime = "Neznanec"
        priimek = self.request.get(utils.escape("priimek"))
        email = self.request.get(utils.escape("email"))
        sporocilo = self.request.get(utils.escape("sporocilo"))
        guestbook = Guestbook(ime=ime, priimek=priimek, email=email, sporocilo=sporocilo)

        if sporocilo != None:
            guestbook.put()
            info = {"ime": ime,"zahvala": u", E-prijava v naš hotel je uspešno izvedena"}
            return self.render_template("hello.html", params=info)

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query().fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam_sporocil.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Guestbook.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/seznam', SeznamSporocilHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
], debug=True)