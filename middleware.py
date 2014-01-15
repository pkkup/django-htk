import re
import thread

from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone

from htk.constants import *
from htk.session_keys import *

class GlobalRequestMiddleware(object):
    """Stores the request object so that it is accessible globally

    Makes an assumption that one request runs entirely in one thread
    If a request happens to spin off other threads, I suppose the request object would not be accessible
    """
    _threadmap = {}

    @classmethod
    def get_current_request(cls):
        request = cls._threadmap.get(thread.get_ident())
        return request

    def process_request(self, request):
        self._threadmap[thread.get_ident()] = request

    def process_exception(self, request, exception):
        try:
            del self._threadmap[thread.get_ident()]
        except KeyError:
            pass

    def process_response(self, request, response):
        try:
            del self._threadmap[thread.get_ident()]
        except KeyError:
            pass
        return response

class AllowedHostsMiddleware(object):
    """Checks that host is inside ALLOWED_HOST_REGEXPS

    If not, will redirect to DEFAULT_DOMAIN

    If host ends with '.', will redirect to host with '.' stripped
    """
    def process_request(self, request):
        host = request.get_host()
        path = request.path
        redirect_uri = None
        https_prefix = 's' if request.is_secure() else ''
        if not(self._is_allowed_host(host)):
            redirect_uri = 'http%s://%s%s' % (https_prefix, DEFAULT_DOMAIN, path,)
        elif len(host) > 1 and host[-1] == '.':
            redirect_uri = 'http%s://%s%s' % (https_prefix, host[:-1], path,)

        if redirect_uri:
            return redirect(redirect_uri)

    def _is_allowed_host(self, host):
        allowed = False
        if settings.TEST:
            allowed = True
        else:
            for host_re in ALLOWED_HOST_REGEXPS:
                allowed = bool(re.match(host_re, host))
                if allowed:
                    break
        return allowed

class TimezoneMiddleware(object):
    def process_request(self, request):
        django_timezone = request.session.get(DJANGO_TIMEZONE, None)
        if not django_timezone and request.user.is_authenticated():
            user = request.user
            django_timezone = user.profile.get_django_timezone()
            request.session[DJANGO_TIMEZONE] = django_timezone
        if django_timezone:
            timezone.activate(django_timezone)
