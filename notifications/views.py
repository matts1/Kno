from django.shortcuts import redirect, get_object_or_404
from common.views import TemplateView, get_user


class NotifyView(TemplateView):
    def get(self, request, id, *args, **kwargs):
        user = get_user(self)
        notif = get_object_or_404(user.notifications, id=id)
        url = notif.url
        user.notifications.remove(notif)
        return redirect(url)
