import exceptions as exc
import functools
import pecan
from oslo_log import log as logging
from pecan import rest
from nca47.common.i18n import _

LOG = logging.getLogger(__name__)


def expose(function):
    """
    Packaging pecan RestController expose method. Resolving WSGi request body.
    """

    @pecan.expose('json')
    @functools.wraps(function)
    def decorated_function(self, *args, **kwargs):
        func = functools.partial(function, self, pecan.request)
        try:
            func = func(*args, **kwargs)
        except Exception:
            pecan.response.status = 500
            return {"ret_code": 500, "ret_msg": "Bad Method Request"}
        return func

    return decorated_function


class BaseRestController(rest.RestController):
    """
    A base class implement pecan RestController.
    """
    @property
    def response(self):
        return pecan.response

    @expose
    def post(self, req, *args, **kwargs):
        LOG.debug(_('args: %(args)s, kwargs: %(kwargs)s'),
                  {"args": args, "kwargs": kwargs})
        try:
            operation = args[0]
            req = pecan.request
            if operation == 'addif':
                return self.addif(req, *args, **kwargs)
            elif operation == 'delif':
                return self.delif(req, *args, **kwargs)
        except Exception as e:
            pass

        return self.create(req, *args, **kwargs)

    @expose
    def put(self, req, id, *args, **kwargs):
        LOG.debug(_('id: %(id)s, args: %(args)s, kwargs: %(kwargs)s'),
                  {"id": id, "args": args, "kwargs": kwargs})
        return self.update(req, id, *args, **kwargs)

    @expose
    def delete(self, req, id, *args, **kwargs):
        LOG.debug(_('id: %(id)s, args: %(args)s, kwargs: %(kwargs)s'),
                  {"id": id, "args": args, "kwargs": kwargs})
        return self.remove(req, id, *args, **kwargs)

    @expose
    def get_all(self, req, *args, **kwargs):
        LOG.debug(_('args: %(args)s, kwargs: %(kwargs)s'),
                  {"args": args, "kwargs": kwargs})
        return self.list(req, *args, **kwargs)

    @expose
    def get_one(self, req, id, *args, **kwargs):
        LOG.debug(_('id: %(id)s, args: %(args)s, kwargs: %(kwargs)s'),
                  {"id": id, "args": args, "kwargs": kwargs})
        return self.show(req, id, *args, **kwargs)

    def create(self, req, *args, **kwargs):
        raise exc.NotImplementedError

    def update(self, req, id, *args, **kwargs):
        raise exc.NotImplementedError

    def remove(self, req, id, *args, **kwargs):
        raise exc.NotImplementedError

    def list(self, req, *args, **kwargs):
        raise exc.NotImplementedError

    def show(self, req, id, *args, **kwargs):
        raise exc.NotImplementedError
