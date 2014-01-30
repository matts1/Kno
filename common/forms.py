from django.forms import ModelForm
from django.template import Context
from django.template.loader import get_template


class ModelForm(ModelForm):
    placeholders = {}
    valid_users = (1, 2)

    def __init__(self, view, *args, user=None, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.view = view
        self.user = view.request.user if user is None and view is not None else user

        # override this method if you want to change the form based on the user

    def allowed(self):
        if not self.user.is_authenticated():
            return 0 in self.valid_users
        elif not self.user.teacher:
            return 1 in self.valid_users
        else:
            return 2 in self.valid_users

    def clean(self):
        print(self.cleaned_data)
        # TODO: get this to only be valid if self.allowed returns true

    def as_modal(self) -> str:
        modal_template = get_template('forms/modal.html')
        if self.allowed():
            return modal_template.render(Context({'form': self}))
        else:
            return ''

    def as_form(self) -> str:
        form_template = get_template('forms/form.html')
        if self.allowed():
            return form_template.render(Context({'form': self}))
        else:
            return ''
