from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from rango.models import Category, Page
from rango.TopFiveCategoriesFromStub import TopFiveCategoriesFromStub
from mock import patch
from nose.tools import assert_is_not_none
from rango.bing_search import run_query
from rango.helpers import add_category, add_page


# Create your tests here.
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received for a Category are positive or zero.
        """
        category = add_category('test', -1, 0)
        category.save()

        self.assertEqual((category.views >= 0), True)

    def test_slug_line(self):
        """
        Checks to make sure that when a category is created, an
        appropriate slug is created.
        Example: "Random Category String" should be "random-category-string".
        """
        category = add_category('Random Category String')
        category.save()

        self.assertEqual(category.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        add_category('Python', 1, 1)
        add_category('C++', 1, 1)
        add_category('Erlang', 1, 1)

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "C++")
        self.assertContains(response, "Erlang")

        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)

    def test_index_view_with_categories_stub(self):
        """
        Checks whether categories are displayed correctly when present using a stub.
        """
        categories = TopFiveCategoriesFromStub()

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)

        list_of_categories = categories.get_list_of_top_5_categories()

        for category in list_of_categories:
            self.assertContains(response, category.name)


class PageMethodTests(TestCase):
    def test_not_future_last_visit(self):
        category = add_category('CSS', 10, 1)
        page = add_page(category, 'CSS Tutorial', 'https://www.w3schools.com/css/')

        self.assertTrue(page.last_visit <= timezone.now())

    def test_last_visit_updated_when_page_requested(self):
        category = add_category('HTML', 5, 6)
        page = add_page(category, 'HTML Tutorial', 'https://www.w3schools.com/html/')
        date_created = page.last_visit

        self.client.get(reverse('rango:goto'), {'page_id': page.id})
        page.refresh_from_db()
        self.assertTrue(page.last_visit >= date_created)


class BingSearchApiTests(TestCase):
    @patch('rango.bing_search.requests.get')
    def test_run_query_runs(self, mock_get):
        """
        Checks that the run query calls the bing search api, using a mock.
        """
        mock_get.return_value.ok = True
        response = run_query('Python')
        assert_is_not_none(response)

