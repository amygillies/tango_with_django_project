from rango.TopFiveCategoriesSource import TopFiveCategoriesSource
from rango.models import Category


def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    category.save()


class TopFiveCategoriesFromStub(TopFiveCategoriesSource):

    def __init__(self):
        add_category('Python', 1, 1)
        add_category('C++', 1, 1)
        add_category('Erlang', 1, 1)

    def get_list_of_top_5_categories(self):
        return Category.objects.order_by('-likes')[:5]