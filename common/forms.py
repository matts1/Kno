from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileField
from django.template import RequestContext
from django.template.loader import get_template


class ModelForm(ModelForm):
    placeholders = {}
    valid_users = (1, 2)

    def __init__(self, *args, view=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = view
        self.user = view.request.user if user is None and view is not None else user

        # override this method if you want to change the form based on the user

    def allowed(self, user=None) -> bool:
        if user is None:
            user = self.user
        if user is None:
            return 0 in self.valid_users
        elif not user.teacher:
            return 1 in self.valid_users
        else:
            return 2 in self.valid_users

    def as_modal(self) -> str:
        modal_template = get_template('forms/modal.html')
        if self.allowed():
            return modal_template.render(RequestContext(self.view.request, {'form': self}))
        else:
            return ''

    def as_form(self) -> str:
        form_template = get_template('forms/form.html')
        if self.allowed():
            return form_template.render(RequestContext(self.view.request, {'form': self}))
        else:
            return ''

    def _clean_fields(self):  # copied from the class it overrides and changed the calling of the function
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    newvalue = getattr(self, 'clean_%s' % name)(value)
                    if newvalue is not None:
                        value = newvalue
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]
