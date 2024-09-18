import pytest


class BaseTest:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, urlhaus_client):
        self.client = urlhaus_client
        self.before_test()
        yield
        self.teardown_test()

    def before_test(self):
        # Add presetting logic
        print("\n--- Before Test ---")

    def teardown_test(self):
        # Add post setting logic
        print("\n--- Teardown Test ---")