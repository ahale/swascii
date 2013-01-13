# from swift.common.swob import Request, Response


class Swascii(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def __call__(self, env, start_response):
        # req = Request(env)
        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """
    paste.deploy app factory for creating WSGI proxy apps.
    """
    conf = global_conf.copy()
    conf.update(local_conf)

    def swascii_filter(app, conf):
        return Swascii(app)
    return swascii_filter
