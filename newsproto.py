import os.path
import pprint
import tornado.ioloop
import tornado.web
import motor.motor_tornado

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.settings['db']


class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write('<a href="/">List of genres</a><br>')
        self.write('<ul>')
        self.db.genres.find().sort([('_id', -1)]).each(self._got_genre)
        # self.render("index.html")

    def _got_genre(self, genre, error):
        if error:
            raise tornado.web.HTTPError(500, error)
        elif genre:
            self.write('<li>{}</li>'.format(genre['name']))
        else:
            self.write('</ul>')
            self.finish()


class PostNewHandler(BaseHandler):
    def post(self):
        pass


def main():
    parse_command_line()
    db = motor.motor_tornado.MotorClient().news
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/post/new", PostNewHandler),
        ],
        cookie_secret="__THERE_IS_NO_SECRET__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        db=db,
    )
    print('Listening on http://localhost:{}'.format(options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
