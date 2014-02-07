from django.shortcuts import redirect
from auth.models import Session
from common.views import TemplateView


class LogoutView(TemplateView):
    def get(self, request):
        Session.objects.filter(sessionID=request.COOKIES.get('session')).delete()
        return redirect('index')
