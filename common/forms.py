from django.forms import ModelForm
from django.template import Context
from django.template.loader import get_template


class ModelForm(ModelForm):
    name = None
    placeholders = {}
    def __init__(self, request, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user = user

    def clean(self):
        print(self.cleaned_data)

    def as_modal(self):
        return 'SET AS_MODAL UP PROPERLY'

    def as_form(self):

        form_template = get_template('macros/forms.html')
        return form_template.render(Context({'form': self}))
