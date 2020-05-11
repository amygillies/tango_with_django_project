from faker import Factory
import factory

from rango.models import Category, Page

faker = Factory.create()


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    name = faker.word()
    views = faker.random_number()
    likes = faker.random_number()


class PageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Page

    category = factory.SubFactory(CategoryFactory)
    title = faker.word()
    url = faker.url()
