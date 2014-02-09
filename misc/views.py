from common.views import TemplateView
from misc.models import Search


class SearchView(TemplateView):
    template_name = 'other/search.html'
    valid_users = (1, 2)

    def custom_context_data(self):
        query = self.request.GET.get('query', '')

        return {'query': query, 'results': Search.search(query, self.request.user)}
