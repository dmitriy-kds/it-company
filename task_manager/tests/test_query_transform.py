from django.test import TestCase, RequestFactory
from task_manager.templatetags.query_transform import query_transform


class QueryTransformTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_adds_new_param(self):
        request = self.factory.get("/", {"search": "test"})
        result = query_transform(request, sort="name")
        self.assertIn("search=test", result)
        self.assertIn("sort=name", result)

    def test_updates_existing_param(self):
        request = self.factory.get("/", {"sort": "name", "search": "test"})
        result = query_transform(request, sort="-name")
        self.assertIn("search=test", result)
        self.assertIn("sort=-name", result)

    def test_removes_param_when_none(self):
        request = self.factory.get("/", {"sort": "name", "search": "test"})
        result = query_transform(request, search=None)
        self.assertNotIn("search", result)
        self.assertIn("sort=name", result)
