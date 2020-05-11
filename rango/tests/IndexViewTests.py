from django.test import TestCase
from rango.helpers import add_category
from rango.TopFiveCategoriesFromStub import TopFiveCategoriesFromStub
from django.urls import reverse


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
