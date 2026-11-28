
from api_testing.base_request import BaseRequest


BASE_URL = 'https://petstore.swagger.io/v2'


class StoreRequest(BaseRequest):

    def __init__(self):
        super().__init__(BASE_URL)

    # 1. Получение информации о складе
    def get_inventory(self):
        return self.get('store/inventory')

    # 2. Создание заказа
    def create_order(self, order_data):
        return self.post('store/order', order_data)

    # 3. Получение заказа
    def get_order(self, order_id):
        return self.get(f'store/order/{order_id}')

    # 4. Удаление заказа
    def delete_order(self, order_id):
        return self.delete(f'store/order/{order_id}')
