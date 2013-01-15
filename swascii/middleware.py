import random
from cStringIO import StringIO
from PIL import Image
from bisect import bisect
from swift.common.swob import Response
from swift.common.utils import split_path
from swift.common.wsgi import make_pre_authed_request, WSGIContext


class _SwasciiContext(WSGIContext):
    def __init__(self, swascii, version, account, container, obj):
        WSGIContext.__init__(self, swascii.app)
        self.app = swascii.app
        self.version = version
        self.account = account
        self.container = container
        self.obj = obj
        self.greyscale = [
                         " ",
                         " ",
                         ".,-",
                         "_ivc=!/|\~=",
                         "gjez2](YL)t[+T7Vf",
                         "mdK4~GbNDXY5P*Q",
                         "W8KMA",
                         "#%$"
                         ]
        self.zonebounds = [36, 72, 108, 144, 180, 216, 252]

    def handleJPG(self, env, start_response):
        resp = make_pre_authed_request(env, 'GET', '/%s/%s/%s/%s' % (
                self.version, self.account, self.container, self.obj),
                agent="Swascii").get_response(self.app)
        body = ''.join(resp.body)
        f = open('/tmp/image.jpg', 'wb')
        f.write(resp.body)
        f.close()
        s = StringIO(body)
        s.seek(0)
        im = Image.open(s)
        im = im.resize((160, 75), Image.ANTIALIAS)
        im = im.convert("L")
        body = ''
        for y in range(0, im.size[1]):
            for x in range(0, im.size[0]):
                lum = 255 - im.getpixel((x, y))
                row = bisect(self.zonebounds, lum)
                possibles = self.greyscale[row]
                body += possibles[random.randint(0, len(possibles) - 1)]
            body += '\n'
        headers = {'Content-Type': 'text/plain'}
        resp = Response(headers=headers, body=body)
        return resp(env, start_response)


class Swascii(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        self.staticwebagent = '%(orig)s StaticWeb'

    def __call__(self, env, start_response):
        try:
            (version, account, container, obj) = \
                split_path(env['PATH_INFO'], 2, 4, True)
        except ValueError:
            return self.app(env, start_response)
        if obj.split('.')[-1] not in ('jpg'):
            return self.app(env, start_response)
        if env['HTTP_ACCEPT'] not in ('text/plain'):
            return self.app(env, start_response)
        if env['REQUEST_METHOD'] not in ('HEAD', 'GET'):
            return self.app(env, start_response)
        context = _SwasciiContext(self, version, account, container, obj)
        return context.handleJPG(env, start_response)


def filter_factory(global_conf, **local_conf):
    """
    paste.deploy app factory for creating WSGI proxy apps.
    """
    conf = global_conf.copy()
    conf.update(local_conf)

    def swascii_filter(app):
        return Swascii(app, conf)
    return swascii_filter
