from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.static import serve
from common.views import TemplateView, get_user
from tasks.modeldir.assign import AssignSubmission


class DownloadSubmissionView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = get_user(self)
        assign = get_object_or_404(AssignSubmission, id=int(args[0]))
        if assign.task.course.teacher != user:
            raise PermissionDenied('user is not teacher')
        filename = assign.data.name
        return serve(request, filename, document_root=settings.MEDIA_ROOT)
