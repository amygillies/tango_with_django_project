from django.test import TestCase, RequestFactory
from rango.factories import UserFactory
from rango.views import RestrictedView


class RestrictedViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()

    def test_user_is_logged_in_to_see_restricted_view_fake(self):
        """
        Uses request factory and user factory (fake) to check user can view the restricted page only for users.
        """
        request = self.factory.get('rango:restricted')
        request.user = self.user
        response = RestrictedView.as_view()(request)
        self.assertEqual(response.status_code, 200)