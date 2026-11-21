"""Собственные тесты Медиаполки."""

import unittest
from copy import deepcopy

from mediapolka import issue, new_state, return_loan


class StudentTests(unittest.TestCase):

    # 1. Граничная проверка: разрешено выдать 3 единицы
    def test_issue_three_microphones(self):
        state = new_state()

        result = issue(state, "mic", "3")

        self.assertTrue(result["ok"])
        self.assertEqual(result["message"], "Выдано")
        self.assertEqual(result["loan_id"], 1)
        self.assertEqual(state["stock"]["mic"], 0)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["quantity"], 3)
        self.assertEqual(state["loans"][0]["status"], "issued")
        self.assertEqual(state["next_id"], 2)

    # 2. Некорректное количество: отказ без изменения состояния
    def test_invalid_quantity_does_not_change_state(self):
        invalid_values = ["", "abc", "1.5", "-1", "0", "4"]

        for value in invalid_values:
            with self.subTest(quantity=value):
                state = new_state()
                old_state = deepcopy(state)

                result = issue(state, "mic", value)

                self.assertFalse(result["ok"])
                self.assertEqual(
                    result["message"],
                    "Введите целое количество от 1 до 3"
                )
                self.assertEqual(state, old_state)

    # 3. Нельзя выдать больше, чем имеется на складе
    def test_issue_more_than_available(self):
        state = new_state()
        old_state = deepcopy(state)

        result = issue(state, "tripod", "2")

        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Недостаточно оборудования")
        self.assertEqual(state, old_state)

    # 4. Нельзя выдать оборудование с нулевым остатком
    def test_issue_light_when_stock_is_zero(self):
        state = new_state()
        old_state = deepcopy(state)

        result = issue(state, "light", "1")

        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Недостаточно оборудования")
        self.assertEqual(state, old_state)

    # 5. Возврат успешно выданного оборудования
    def test_return_loan_restores_stock(self):
        state = new_state()

        issue_result = issue(state, "mic", "2")
        loan_id = issue_result["loan_id"]

        result = return_loan(state, loan_id)

        self.assertTrue(result["ok"])
        self.assertEqual(result["message"], "Возвращено")
        self.assertEqual(state["stock"]["mic"], 3)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["status"], "returned")
        self.assertEqual(state["loans"][0]["quantity"], 2)

    # 6. Повторный возврат запрещён
    def test_repeat_return_does_not_change_state(self):
        state = new_state()

        issue_result = issue(state, "mic", "1")
        loan_id = issue_result["loan_id"]

        first_return = return_loan(state, loan_id)
        self.assertTrue(first_return["ok"])

        old_state = deepcopy(state)

        second_return = return_loan(state, loan_id)

        self.assertFalse(second_return["ok"])
        self.assertEqual(second_return["message"], "Уже возвращено")
        self.assertEqual(state, old_state)

    # 7. Возврат несуществующего ID
    def test_return_unknown_id_does_not_change_state(self):
        state = new_state()
        old_state = deepcopy(state)

        result = return_loan(state, 999)

        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Выдача не найдена")
        self.assertEqual(state, old_state)


if __name__ == "__main__":
    unittest.main()