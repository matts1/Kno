from django.shortcuts import redirect
from common.views import TemplateView
from auth.models import Session


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        Session.objects.filter(sessionID=request.COOKIES.get('session')).delete()
        return redirect('index')
