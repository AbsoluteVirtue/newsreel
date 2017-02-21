import os.path
import tornado.ioloop
import tornado.web
import motor.motor_tornado
import crawl

from bson.json_util import dumps
from tornado import gen
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


def get_rss_bson():
    raw_data = crawl.get_sslowdown_data()
    return

# TODO: check rss result for new articles before inserting


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.settings['db']

    @property
    def collection(self):
        return self.settings['collection']


class MainHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        cursor = self.collection.find().sort([('_id', -1)])
        docs = yield cursor.to_list(length=20)
        self.render("index.html", items=docs)


class PostNewHandler(BaseHandler):
    def post(self):
        pass


def main():
    parse_command_line()
    db = motor.motor_tornado.MotorClient().news
    collection = db.articles
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/post/new", PostNewHandler),
        ],
        cookie_secret="__THERE_IS_NO_SECRET__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        db=db,
        collection=collection,
    )
    print('Listening on http://localhost:{}'.format(options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
