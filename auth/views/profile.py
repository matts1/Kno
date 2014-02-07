from django.shortcuts import get_object_or_404
from common.views import TemplateView
from auth.models import User

class ProfileView(TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['person'] = get_object_or_404(User, id=int(self.args_data[0]))
        return data
