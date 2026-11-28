
from api_testing.base_request import BaseRequest


BASE_URL = 'https://petstore.swagger.io/v2'


class UserRequest(BaseRequest):

    def __init__(self):
        super().__init__(BASE_URL)

    # 1. Создание пользователя
    def create_user(self, user_data):
        return self.post('user', user_data)

    # 2. Получение пользователя
    def get_user(self, username):
        return self.get(f'user/{username}')

    # 3. Обновление пользователя
    def update_user(self, username, user_data):
        return self.put(f'user/{username}', user_data)

    # 4. Удаление пользователя
    def delete_user(self, username):
        return self.delete(f'user/{username}')
