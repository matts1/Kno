from django.http import HttpResponse
from django.shortcuts import redirect
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
        return HttpResponse(status=405)

    def post(self, request, *args, **kwargs):
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
        return self.render_to_response(self.get_context_data(form=form, redirect=redirect))


class TemplateView(TemplateView):
    on_post = None

    def get_context_data(self):
        kwargs = super(TemplateView, self).get_context_data()
        kwargs['info'] = (self, self.request.user)
        return kwargs

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=405)
