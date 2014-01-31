from django.http import HttpResponse
from django.views.generic import FormView, TemplateView


class FormView(FormView):
    template_name = 'forms/post.html'
    require_login = True
    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs['view'] = self
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        print('get')
        return HttpResponse(status=405)

class TemplateView(TemplateView):
    on_post = None

    def get_context_data(self):
        kwargs = super(TemplateView, self).get_context_data()
        print(kwargs)
        kwargs['info'] = (self, self.request.user)
        return kwargs

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=405)
