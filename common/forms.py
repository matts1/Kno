from django.forms import ModelForm
from django.template import Context
from django.template.loader import get_template


class ModelForm(ModelForm):
    placeholders = {}
    def __init__(self, view, *args, user=None, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.view = view
        self.user = view.request.user if user is None and view is not None else user

        # override this method if you want to change the form based on the user

    def clean(self):
        print(self.cleaned_data)

    def as_modal(self) -> str:
        modal_template = get_template('forms/modal.html')
        return modal_template.render(Context({'form': self}))

    def as_form(self) -> str:
        form_template = get_template('forms/form.html')
        return form_template.render(Context({'form': self}))
