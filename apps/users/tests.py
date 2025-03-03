import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(email='test_user@gmail.com', password='testpassword')
    assert user.email == 'test_user@gmail.com'
    assert user.check_password('testpassword')
    assert user.is_active
    assert not user.is_manager
    assert not user.is_admin

@pytest.mark.django_db
def test_superuser_creation():
    user = User.objects.create_superuser(email='admin@gmail.com', password='adminpassword')
    assert user.email == 'admin@gmail.com'
    assert user.check_password('adminpassword')
    assert user.is_active
    # assert user.is_manager
    assert user.is_admin



