import pytest

from user.models import User


@pytest.fixture
def user():
    user = User.objects.create_user(
        email='tester@mail.com',
        password='Hard6573Password',
        first_name='John',
        last_name='Doe',
        username='doe_john',
        phone_number=3456546789
    )

    return user
