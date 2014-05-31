from misc.models import Search
from tasks.models import Task
from tests.base_request import RequestTestCase


class SearchTestCase(RequestTestCase):
    def test_search(self):
        self.assertGreater(len(Search.search('programming')), 0)

    def test_rename_delete(self):
        results = len(Search.search('random blah'))
        Search.add_words('random task', 2, Task)
        self.assertGreater(len(Search.search('random blah')), results)


        oldres = len(Search.search('proper result'))
        Search.rename_words('Proper name', 2, Task)
        self.assertGreater(len(Search.search('proper result')), oldres)
        self.assertEqual(len(Search.search('random blah')), results)

        Search.delete_words(2, Task)
        self.assertEqual(len(Search.search('proper result')), oldres)

    def test_search_url(self):
        self.assertEqual(
            self.fetch('search', data={'query': 'programming'}).status_code,
            200
        )
