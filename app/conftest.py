import pytest
import os
import django
from django.core.cache import cache


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djinnitest.settings')
django.setup()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
