import allure

import helper
import requests
from data import Urls, Api


class TestCreateUser:
    @allure.title('Проверка создания нового пользователя')
    @allure.description(f'Отправка корректного Post запроса на {Urls.server}{Api.register_user}\n'
                        f'ОР: код 200, в теле ответа получаем True, данные пользователя,\n'
                        f'accessToken "Bearer ..." и refreshToken')
    @allure.step(f'Сгененрировать случайного пользователя\nПодготовить данные для запроса\n'
                 f'Отправить Post запрос на {Urls.server}{Api.register_user} с подготовленными данными\n'
                 f'Постусловие: удалить пользователя')
    def test_create_new_user_success(self):
        email, user, password = helper.generate_new_creds()
        payload = {
            "email": email,
            "password": password,
            "name": user
        }
        response = requests.post((Urls.server + Api.register_user), data=payload)
        assert (response.status_code == 200 and response.json()["success"] == True
                and response.json()["user"] == {
                    "email": email, "name": user}
                and response.json()["accessToken"][:6] == 'Bearer'
                and "refreshToken" is not None)
        access_token = response.json()["accessToken"]
        helper.delete_user(access_token)

    @allure.title('Проверка создания пользователя с уже зарегистрированной почтой')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.register_user} с зарегистрированным email\n'
                        f'ОР: код 403, в теле ответа получаем False и сообщение, что пользователь уже существует')
    @allure.step(f'Сгененрировать случайного пользователя\nПодготовить данные для запроса\n'
                 f'Отправить Post запрос на {Urls.server}{Api.register_user} с подготовленными данными\n'
                 f'Отправить повторный Post запрос на {Urls.server}{Api.register_user} с теми же данными\n'
                 f'Постусловие: удалить пользователя')
    def test_create_existing_user_forbidden(self):
        email, user, password = helper.generate_new_creds()
        payload = {
            "email": email,
            "password": password,
            "name": user
        }
        response_1 = requests.post((Urls.server + Api.register_user), data=payload)
        response_2 = requests.post((Urls.server + Api.register_user), data=payload)
        assert response_2.status_code == 403 and response_2.json() == {"success": False,
                                                                       "message": "User already exists"}
        access_token = response_1.json()["accessToken"]
        helper.delete_user(access_token)

    @allure.title('Проверка создания пользователя без отправки name')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.register_user} с неполными данными\n'
                        f'ОР: код 403, в теле ответа получаем False и сообщение, что не все данные переданы')
    @allure.step(f'Сгененрировать случайного пользователя\nПодготовить данные для запроса без name\n'
                 f'Отправить Post запрос на {Urls.server}{Api.register_user} с подготовленными данными')
    def test_create_new_user_without_name_forbidden(self):
        email, user, password = helper.generate_new_creds()
        payload = {
            "email": email,
            "password": password,
        }
        response = requests.post((Urls.server + Api.register_user), data=payload)
        assert response.status_code == 403 and response.json() == {"success": False,
                                                                  "message": "Email, password and name are required fields"}

