from django.views.generic import View


class RedirectAfterLoginView(View):
    def get(self, request, *args, **kwargs):

