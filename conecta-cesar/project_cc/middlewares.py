from django.middleware.csrf import CsrfViewMiddleware
from django.http import HttpResponseRedirect
from django.urls import resolve

class CSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except CsrfViewMiddleware as e:
            # Pegue o nome da view atual para redirecionamento
            current_url_name = resolve(request.path_info).url_name
            return HttpResponseRedirect(current_url_name or '/')  # Redirecione para a página atual ou para a raiz