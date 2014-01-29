from django.views.generic import FormView, View


class FormView(FormView):
    require_login = True
    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs['view'] = self
        return kwargs

class View(View):
    on_post = None

    # POST FUNCTION WHICH USES THE ON_POST VIEW INSTEAD OF CURRENT VIEW. IF ON_POST IS NONE, METHOD NOT ALLOW
