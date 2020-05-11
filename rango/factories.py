from faker import Factory
import factory
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile

faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = faker.first_name()
    email = faker.email()
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')
    is_active = True


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    name = faker.word()
    views = faker.random_number()
    likes = faker.random_number()
    slug = faker.slug()


class PageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Page

    category = factory.SubFactory(CategoryFactory)
    title = faker.word()
    url = faker.url()
