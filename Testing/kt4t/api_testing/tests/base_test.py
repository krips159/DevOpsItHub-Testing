from api_testing.user_request import UserRequest
from api_testing.store_request import StoreRequest


class BaseTest:

    def setup_method(self):
        self.user_api = UserRequest()
        self.store_api = StoreRequest()
