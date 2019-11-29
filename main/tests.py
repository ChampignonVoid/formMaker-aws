from django.test import TestCase, Client  # noqa: F401


# Create your tests here.
class URLTest(TestCase):
    def test_one(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
