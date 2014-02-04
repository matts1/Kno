from django.shortcuts import redirect, get_object_or_404
from common.views import TemplateView
from auth.models import Session, User


class LogoutView(TemplateView):
    def get(self, request):
        Session.objects.filter(sessionID=request.COOKIES.get('session')).delete()
        return redirect('index')

class ProfileView(TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['person'] = get_object_or_404(User, id=int(self.args_data[0]))
        return data
