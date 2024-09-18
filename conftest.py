import pytest
import yaml
import os
from api.urlhaus_client import URLhausClient

@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="session")
def urlhaus_client(config):
    base_url = config.get("base_url")
    return URLhausClient(base_url=base_url)

