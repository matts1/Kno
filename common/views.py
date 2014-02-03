from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from auth.models import Session

def get_user(view):
    return Session.get_user(view.request.COOKIES.get('session'))

class FormView(FormView):
    template_name = 'forms/post.html'
    require_login = True
    cookies = {}

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs['view'] = self
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    def post(self, request, *args, **kwargs):
        self.request.user = get_user(self)
        if self.form_class().allowed(request.user):
            return super().post(request, *args, **kwargs)
        elif request.user is None:
            return redirect('index')
        else:
            raise NotImplementedError

    def form_valid(self, form):
        redirect = None
        form.save()

        if hasattr(form, 'success_url'):
            redirect = form.success_url
        response = self.render_to_response(self.get_context_data(form=form, redirect=redirect))
        for key, value in self.cookies.items():
            response.set_cookie(key, value)
        return response


class TemplateView(TemplateView):
    def get_context_data(self):
        kwargs = super().get_context_data()
        self.request.user = get_user(self)
        kwargs['info'] = (self, self.request.user)
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=405)
