import random
from cStringIO import StringIO
from PIL import Image
from bisect import bisect
from swift.common.swob import Request, Response
from swift.common.utils import split_path
from swift.common.wsgi import WSGIContext


class _SwasciiContext(WSGIContext):
    def __init__(self, swascii, version, account, container, obj, conf):
        WSGIContext.__init__(self, swascii.app)
        self.app = swascii.app
        self.version = version
        self.account = account
        self.container = container
        self.obj = obj
        self.greyscale = [" ",
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
        path = '/%s/%s/%s/%s' % (self.version,
                                 self.account, self.container, self.obj)
        headers = {}
        orig_method = env['REQUEST_METHOD']
        env['REQUEST_METHOD'] = 'GET'
        resp = Request.blank(path, environ=env,
                             headers=headers).get_response(self.app)
        if resp.status != '200 OK':
            return resp(env, start_response)

        body = ''.join(resp.body)
        s = StringIO(body)
        s.seek(0)
        try:
            im = Image.open(s)
        except IOError:
            body = '415 Unsupported Media Type\n'
            start_response('415 Unsupported Media Type',
                           [('Content-Type', 'text/plain'),
                           ('Content-Length', str(len(body)))])
            if orig_method == 'HEAD':
                return []
            return [body]

        ascii_width = 80
        try:
            for v in env['HTTP_ACCEPT'].split(';'):
                if v.lstrip(' ').startswith('w='):
                    ascii_width = int(v.split('=')[1])
                    if ascii_width < 1:
                        ascii_width = 1
        except:
            pass

        im_width = im.size[0]
        im_height = im.size[1]
        scale = im_width / ascii_width * 1.0
        if scale <= 0:
            scale = 1
        try:
            ascii_height = int(im_height / scale * 0.5)
        except ZeroDivisionError:
            ascii_width = 80
            scale = im_width / ascii_width * 1.0
            ascii_height = int(im_height / scale * 0.5)

        im = im.resize((ascii_width, ascii_height), Image.ANTIALIAS)
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
        if orig_method == 'HEAD':
            headers['Content-Length'] = len(body)
            body = ''
        resp = Response(headers=headers, body=body)
        return resp(env, start_response)


class Swascii(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def __call__(self, env, start_response):
        if not env['HTTP_ACCEPT'].startswith('text/plain'):
            return self.app(env, start_response)
        if env['REQUEST_METHOD'] not in ('HEAD', 'GET'):
            return self.app(env, start_response)
        try:
            (version, account, container, obj) = \
                split_path(env['PATH_INFO'], 2, 4, True)
        except ValueError:
            return self.app(env, start_response)

        if obj.split('.')[-1].lower() in ('jpg', 'jpeg', 'png'):
            context = _SwasciiContext(self, version,
                                      account, container, obj, self.conf)
            return context.handleJPG(env, start_response)
        else:
            return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """
    paste.deploy app factory for creating WSGI proxy apps.
    """
    conf = global_conf.copy()
    conf.update(local_conf)

    def swascii_filter(app):
        return Swascii(app, conf)
    return swascii_filter
