import pytest
from django.core.management import call_command


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):

    fixtures = [
        'test_fixtures/User.json',
        'test_fixtures/Balance.json',
    ]

    with django_db_blocker.unblock():
        try:
            call_command('loaddata', *fixtures)
        except Exception as exc:
            pytest.fail(f'Problem in one of fixtures: {fixtures}: {exc}')
