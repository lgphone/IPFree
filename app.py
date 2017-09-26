#!/usr/bin/env python3
import tornado
from controllers import main

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': '43809138f51b96f812sde79b3a2cb482',
    # 'debug': True,
    # 'autoreload': True,
}

application = tornado.web.Application([
    # 主页
    (r"/index", main.IndexHandler),
    # API
    (r"/ipfree", main.IPFreeHandler),
], **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
