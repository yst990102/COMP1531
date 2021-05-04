from hypothesis import settings

from datetime import timedelta

def pytest_configure(config):
    settings.register_profile("marking", deadline=timedelta(seconds=120))
    settings.load_profile("marking")