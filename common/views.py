from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from auth.models import Session

def get_user(view):
    if settings.TEST:
        return getattr(view.request, 'user', None)
    else:
        return Session.get_user(view.request.COOKIES.get('session'))

class FormView(FormView):
    template_name = 'forms/post.html'
    require_login = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookies = {}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['view'] = self
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.request.user = get_user(self)
        if self.form_class(view=self).allowed(request.user):
            return super().post(request, *args, **kwargs)
        elif request.user is None:
            return self.render_to_response(self.get_context_data(redirect=reverse('index')))
        else:
            return self.render_to_response(self.get_context_data(redirect=reverse('listcourses')))

    def form_valid(self, form):
        redirect = None
        form.save()

        if form.success_url is not None:
            redirect = reverse(form.success_url, args=form.success_url_args(),
                               kwargs=form.success_url_kwargs())
        response = self.render_to_response(self.get_context_data(form=form, redirect=redirect))
        for key, value in self.cookies.items():
            response.set_cookie(key, value)
        return response


class TemplateView(TemplateView):
    valid_users = (1,)
    def get_context_data(self):
        kwargs = super().get_context_data()
        self.request.user = get_user(self)
        kwargs['info'] = (self, self.request.user)
        kwargs['user'] = self.request.user
        kwargs.update(self.custom_context_data())
        return kwargs

    def get(self, request, *args, **kwargs):
        self.args_data = args
        self.kwargs_data = kwargs
        self.request = request
        user = get_user(self)
        if user is None and 0 not in self.valid_users:
            return redirect('index')
        elif user is not None and 1 not in self.valid_users:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    def custom_context_data(self):
        return {}
