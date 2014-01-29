from auth.models import Users
from common.forms import ModelForm


class RegisterForm(ModelForm):
    name = 'Sign Up'

    class Meta:
        model = Users
        fields = ('email', 'fname', 'lname')

    # TODO: add in 2 more fields for password and confirming password

    def clean(self):
        print(self.fields['email'].required)
        print(self.cleaned_data)
