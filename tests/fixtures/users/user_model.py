import factory, factory.fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.models.users import User


faker = FakerFactory.create()

EXISTS_GOOGLE_USER_ID = 11
EXISTS_GOOGLE_USER_EMAIL = "google@gmail.com"


@register(_name="user_profile")
class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    password = factory.LazyFunction(lambda: faker.password())
    google_access_token = factory.LazyFunction(lambda: faker.sha256())
    yandex_access_token = factory.LazyFunction(lambda: faker.sha256())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
