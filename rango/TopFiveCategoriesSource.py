from abc import ABC, abstractmethod


class TopFiveCategoriesSource(ABC):

    @abstractmethod
    def get_list_of_top_5_categories(self):
        pass
