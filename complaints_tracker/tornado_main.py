#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings testsite/tornado.py
# Serves by default at
# http://localhost:8080/hello-tornado and
# http://localhost:8080/hello-django


from tornado.options import options
from tornado.options import define
from tornado.options import parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print sys.path
os.environ["DJANGO_SETTINGS_MODULE"] = "complaints_tracker.settings"

define('port', type=int, default=8888)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')


settings = {
    'static_path': os.path.join((os.path.dirname(__file__)), 'static'),
}


def main():
    parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    tornado_app = tornado.web.Application(
        [
            ('/hello-tornado', HelloHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
            ('.*', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
        ], **settings)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
    # ,