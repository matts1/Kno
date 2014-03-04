from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileField
from django.template import RequestContext
from django.template.loader import get_template
import re


class ModelForm(ModelForm):
    placeholders = {}
    valid_users = (1,)
    text = None
    update = False
    success_url = None
    success_url_args = lambda x: ()
    success_url_kwargs = lambda x: {}

    def __init__(self, *args, view=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = view
        self.user = view.request.user if user is None and view is not None else user
        if self.update:
            self._post_clean = lambda: None

        # override this method if you want to change the form based on the user

    def allowed(self, user=None) -> bool:
        if user is None:
            user = self.user
        if user is None:
            return 0 in self.valid_users
        else:
            return 1 in self.valid_users

    def as_modal(self, *args, **kwargs) -> str:
        modal_template = get_template('forms/modal.html')
        if self.allowed():
            return modal_template.render(RequestContext(
                self.view.request,
                {'form': self, 'hidden': kwargs}
            ))
        else:
            return ''

    def as_form(self, *args, **kwargs) -> str:
        form_template = get_template('forms/form.html')
        if self.allowed():
            return form_template.render(RequestContext(
                self.view.request,
                {'form': self, 'hidden': kwargs}
            ))
        else:
            return ''

    def _clean_fields(self):  # copied from the class it overrides, changed calling of clean_field
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

    @classmethod
    def test(cls, correct:list, cleaned=None, save=True, initdata=None, **kwargs):
        correct = set(correct)
        if initdata is None:
            initdata = {}

        form = cls(data=kwargs, **initdata)
        form.full_clean()
        results = set(form.errors)
        if '__all__' in results:
            results.remove('__all__')
            results.add('')
        problems = []
        for result in results ^ correct:
            if result in correct:
                problems.append('The %s field should have raised an error, but didn\'t' % (
                    result if result else 'main'
                ))
            else:
                problems.append('The %s field unexpectedly raised an error (%s)' % (
                    result if result else 'main', ', '.join(form.errors[result if result else '__all__'])
                ))

        if problems:
            raise AssertionError('Input for %s is %r\n%s' % (
                cls.__name__, kwargs, '\n'.join(problems)
            ))

        if cleaned is not None:
            for key in kwargs:
                if key not in cleaned:
                    cleaned[key] = kwargs[key]

            if cleaned != form.cleaned_data:
                problems = []
                for key in cleaned:
                    if form.cleaned_data[key] != cleaned[key]:
                        problems.append('For field %s, got %s, should have been %s' % (
                            key, form.cleaned_data[key], cleaned[key]
                        ))
                raise AssertionError('Input for %s is %r\n%s' % (
                    cls.__name__, kwargs, '\n'.join(problems)
                ))

        if form.is_valid() and save:
            form.save()

    @classmethod
    def cls_name(cls) -> str:
        return cls.__name__[:-4] if cls.__name__.endswith('Form') else cls.__name__

    def get_text(self, text=None):
        if text is None:
            text = self.text
        fn = lambda x: '<a href="#%s" data-dismiss="modal" data-toggle="modal">' % x.group(1)
        return re.sub(r'{{ ?([a-zA-Z]+) ?}}', fn, text, re.I)
