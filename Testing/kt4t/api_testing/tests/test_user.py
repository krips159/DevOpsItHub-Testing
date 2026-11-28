
import uuid

from tests.base_test import BaseTest


class TestUser(BaseTest):

    def test_user_crud(self):

        username = 'test_user_' + uuid.uuid4().hex[:8]

        user_data = {
            'id': uuid.uuid4().int % 100000,
            'username': username,
            'firstName': 'Danil',
            'lastName': 'Test',
            'email': 'danil@example.com',
            'password': '123456',
            'phone': '123456789',
            'userStatus': 1
        }

        # 1. Создание пользователя
        create_response = self.user_api.create_user(user_data)
        assert create_response.status_code == 200

        # 2. Получение пользователя
        get_response = self.user_api.get_user(username)
        assert get_response.status_code == 200
        assert get_response.json()['username'] == username

        # 3. Обновление пользователя
        updated_data = user_data.copy()
        updated_data['firstName'] = 'UpdatedDanil'

        update_response = self.user_api.update_user(
            username,
            updated_data
        )
        assert update_response.status_code == 200

        # Проверка обновления
        get_updated_response = self.user_api.get_user(username)
        assert get_updated_response.status_code == 200
        assert get_updated_response.json()['firstName'] == 'UpdatedDanil'

        # 4. Удаление пользователя
        delete_response = self.user_api.delete_user(username)
        assert delete_response.status_code == 200
