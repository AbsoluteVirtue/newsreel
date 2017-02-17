import os.path
import tornado.ioloop
import tornado.web

from tornado.options import define, options, parse_command_line

define("debug", default=False, help="run in debug mode")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class PostNewHandler(tornado.web.RequestHandler):
    def post(self):
        pass


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/a/message/new", PostNewHandler),
        ],
        cookie_secret="__THERE_IS_NO_SECRET__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
