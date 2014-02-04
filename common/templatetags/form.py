from django_jinja import library
import importlib

lib = library.Library()

form_names = {
    'auth': {
        'Register',
        'Login',
        'ResetPwd',
        'ForgotPwd',
        'DoResetPwd'
    }
}

forms = {}

for modulename in form_names:
    module = importlib.import_module(modulename + '.forms')
    for cls in form_names[modulename]:
        cls = getattr(module, cls + 'Form')
        forms[cls.cls_name()] = cls

@lib.global_function
def as_form(name, info):
    return forms[name](view=info[0], user=info[1]).as_form()

@lib.global_function
def as_modal(name, info):
        return forms[name](view=info[0], user=info[1]).as_modal()

@lib.global_function
def string(s):
    return str(s)
