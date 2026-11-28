
import uuid

from tests.base_test import BaseTest


class TestStore(BaseTest):

    def test_store_operations(self):

        # 1. Получение информации о складе
        inventory_response = self.store_api.get_inventory()

        assert inventory_response.status_code == 200
        assert isinstance(inventory_response.json(), dict)

        # Создание уникального ID заказа
        order_id = 11 + uuid.uuid4().int % 900

        order_data = {
            'id': order_id,
            'petId': 1,
            'quantity': 2,
            'shipDate': '2026-11-28T12:00:00.000Z',
            'status': 'placed',
            'complete': True
        }

        # 2. Создание заказа
        create_response = self.store_api.create_order(order_data)

        assert create_response.status_code == 200
        assert create_response.json()['id'] == order_id

        # 3. Получение заказа
        get_response = self.store_api.get_order(order_id)

        assert get_response.status_code == 200
        assert get_response.json()['id'] == order_id

        # 4. Удаление заказа
        delete_response = self.store_api.delete_order(order_id)

        assert delete_response.status_code == 200
