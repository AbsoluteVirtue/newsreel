import os.path
import datetime
import tornado.ioloop
import tornado.web
import motor.motor_tornado
from copy import deepcopy

import crawl

from bson.json_util import dumps
from tornado import gen
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.settings['db']

    @property
    def collection(self):
        return self.settings['collection']


# .strftime('%d %B %Y')
class MainHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        cursor = self.collection.find().sort([('date', -1)])
        docs = yield cursor.to_list(length=20)
        self.render("index.html", items=docs)


class PostHandler(BaseHandler):
    def post(self):
        pass


class PostNewHandler(BaseHandler):
    def post(self):
        pass


def get_datetime(date):
    sliced_date = date[5:25]
    return datetime.datetime.strptime(sliced_date, '%d %b %Y %H:%M:%S')


def build_post(text, source):
    return "{}<br><br>Original source: {}".format(text, source)


def build_json_from_raw_data():
    raw_data = crawl.get_sslowdown_data()
    result = []
    entry = {}
    for entry_key, entry_data in raw_data.items():
        entry["author"] = entry_data["author"]
        entry["date"] = get_datetime(entry_data["date"])
        entry["image"] = entry_data["image"]
        entry["summary"] = entry_data["summary"]
        entry["title"] = entry_data["title"]
        entry["text"] = build_post(entry_data["text"], entry_data["source"])
        result.append(deepcopy(entry))
    return result


# TODO: check rss result for new articles before inserting
@gen.coroutine
def bulk_insert(collection):
    articles = build_json_from_raw_data()
    yield collection.insert_many(articles)


def main():
    parse_command_line()
    db = motor.motor_tornado.MotorClient().news
    collection = db.articles
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/post/(.+)", PostHandler),
            (r"/post/new", PostNewHandler),
        ],
        cookie_secret="__THERE_IS_NO_SECRET_COOKIE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        db=db,
        collection=collection,
    )
    # tornado.ioloop.IOLoop.current().run_sync(lambda: bulk_insert(collection))
    print('Listening on http://localhost:{}'.format(options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
