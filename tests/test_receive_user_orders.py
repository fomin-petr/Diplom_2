import allure
import helper
import requests
from data import Urls, Api


class TestReceiveUserOrders:
    @allure.title('Проверка получения списка заказов авторизованного пользователя')
    @allure.description(f'Отправка Get запроса на {Urls.server}{Api.orders} с токеном авторизации\n'
                        f'ОР: код 200, в теле ответа получаем список с номерами пресозданных заказов\n')
    @allure.step(f'Сгененрировать случайного пользователя\nЗарегистрировать пользователя\n'
                 f'Создать два заказа и сохранить их номера в списке\n'
                 f'Отправить Get запрос на {Urls.server}{Api.orders} с токеном авторизации\n'
                 f'Постусловие: удалить пользователя')
    def test_receive_authorized_user_order_list_success(self):
        access_token, email, user, password = helper.create_user()
        orders_numbers = helper.create_two_orders(access_token)
        response = requests.get((Urls.server + Api.orders), headers={"Authorization": access_token})
        assert response.status_code == 200 and response.json()['orders'][0]['number'] in orders_numbers and response.json()['orders'][1]['number'] in orders_numbers
        helper.delete_user(access_token)

    @allure.title('Проверка получения списка заказов неавторизованного пользователя')
    @allure.description(f'Отправка Get запроса на {Urls.server}{Api.orders} без токена авторизации\n'
                        f'ОР: код 401, в теле ответа получаем False и сообщение о необходимости авторизации\n')
    @allure.step(f'Сгененрировать случайного пользователя\nЗарегистрировать пользователя\n'
                 f'Создать два заказа и сохранить их номера в списке\n'
                 f'Отправить Get запрос на {Urls.server}{Api.orders} без токена авторизации\n'
                 f'Постусловие: удалить пользователя')
    def test_receive_unauthorized_user_order_list_fail(self):
        access_token, email, user, password = helper.create_user()
        orders_numbers = helper.create_two_orders(access_token)
        response = requests.get(Urls.server + Api.orders)
        assert response.status_code == 401 and response.json() == {"success": False, "message": "You should be "
                                                                                                "authorised"}
        helper.delete_user(access_token)
