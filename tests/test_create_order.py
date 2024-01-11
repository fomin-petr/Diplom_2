import allure
import helper
import requests
from data import Urls, Api


class TestCreateOrder:
    @allure.title('Проверка создания заказа зарегистрированным пользователем с корректными ингредиентами')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.orders} с токеном и корректными ингредиентами\n'
                        f'ОР: код 200, в заказе есть имя продукта и номер заказа')
    @allure.step(f'Получить хэши ингредиентов\nЗарегистрировать пользователя, получить токен\nВыбрать три случайных'
                 f'ингредиента\nОтправить Post запрос на {Urls.server}{Api.orders} с токеном и корректными '
                 f'ингредиентами\nПостусловие: удалить пользователя')
    def test_create_order_with_auth_and_ingredients_success(self):
        ingredients_hash = helper.get_ingredients_hash()
        access_token, email, user, password = helper.create_user()
        ingredients = helper.get_3_random_ingredients_from_list(ingredients_hash)
        payload = {"ingredients": ingredients}
        response = requests.post((Urls.server + Api.orders), headers={"Authorization": access_token}, data=payload)
        assert response.status_code == 200 and response.json()['success'] == True and isinstance(
            response.json()['name'], str) and response.json()['order']['number'] is not None
        helper.delete_user(access_token)

    @allure.title('Проверка создания заказа без регистрации с корректными ингредиентами')
    @allure.description(f'Отправка Post запрос на {Urls.server}{Api.orders} без токена и корректными ингредиентами\n'
                        f'ОР: код 200, в заказе есть имя продукта и номер заказа')
    @allure.step(f'Получить хэши ингредиентов\nВыбрать три случайных ингредиента'
                 f'\nОтправить Post запроса на {Urls.server}{Api.orders} с токеном и корректными ингредиентами')
    def test_create_order_without_auth_with_ingredients_success(self):
        ingredients_hash = helper.get_ingredients_hash()
        ingredients = helper.get_3_random_ingredients_from_list(ingredients_hash)
        payload = {"ingredients": ingredients}
        response = requests.post((Urls.server + Api.orders), data=payload)
        assert response.status_code == 200 and response.json()['success'] == True and isinstance(
            response.json()['name'], str) and response.json()['order']['number'] is not None

    @allure.title('Создание заказа без ингредиентов')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.orders} без токена и без ингредиентов\n'
                        f'ОР: код 400')
    @allure.step(f'Отправить Post запрос на {Urls.server}{Api.orders} с пустым списком ингредиентов')
    def test_create_order_without_ingredients_bad_request(self):
        payload = {"ingredients": []}
        response = requests.post((Urls.server + Api.orders), data=payload)
        assert response.status_code == 400 and response.json() == {"success": False,
                                                                   "message": "Ingredient ids must be provided"
                                                                   }

    @allure.title('Создание заказа с некорректными ингредиентами')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.orders} без токена и с некорректными '
                        f'ингредиентами\n'
                        f'ОР: код 500')
    @allure.step(f'Получить хэши ингредиентов\nИзменить хэши на некорректные'
                 f'Отправить Post запрос на {Urls.server}{Api.orders} с некорректными ингредиентами')
    def test_create_order_with_incorrect_ingredients_error(self):
        ingredients_hash = helper.get_ingredients_hash()
        ingredients = helper.get_incorrect_ingredient_hash(ingredients_hash)
        payload = {"ingredients": ingredients}
        response = requests.post((Urls.server + Api.orders), data=payload)
        assert response.status_code == 500
