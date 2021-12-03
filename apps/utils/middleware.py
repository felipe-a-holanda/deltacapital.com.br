from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host.startswith("www."):
            non_www_host = host[4:]
            redirect_to = f"https://{non_www_host}{request.path}"
            return HttpResponsePermanentRedirect(redirect_to)
        else:
            return self.get_response(request)
