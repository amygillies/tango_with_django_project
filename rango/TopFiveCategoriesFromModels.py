from rango.TopFiveCategoriesSource import TopFiveCategoriesSource


class TopFiveCategoriesFromModels(TopFiveCategoriesSource):

    def __init__(self, categories):
        self.categories = categories

    def get_list_of_top_5_categories(self):
        return self.categories.objects.order_by('-likes')[:5]