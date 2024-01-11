import allure
import helper
import requests
from data import Urls, Api, DataForTests


class TestLoginUser:
    @allure.title('Проверка авторизации существующего пользователя')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.login} с зарегистрированными кредами\n'
                        f'ОР: код 200, в теле ответа получаем True, данные пользователя,\n'
                        f'accessToken "Bearer ..." и refreshToken')
    @allure.step(f'Сгененрировать случайного пользователя\nЗарегистрировать пользователя\n'
                 f'Подготовить данные для запроса\n'
                 f'Отправить Post запрос на {Urls.server}{Api.login} с подготовленными данными\n'
                 f'Постусловие: удалить пользователя')
    def test_login_existing_user_success(self):
        access_token, email, user, password = helper.create_user()
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post((Urls.server + Api.login), data=payload)
        assert (response.status_code == 200 and response.json()["success"] == True
                and response.json()["user"] == {
                    "email": email, "name": user}
                and response.json()["accessToken"][:6] == 'Bearer'
                and "refreshToken" is not None)
        helper.delete_user(access_token)

    @allure.title('Проверка авторизации с неправильным email')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.login} с неправильным email\n'
                        f'ОР: код 401, в теле ответа получаем False и сообщение о некорректных кредах\n')
    @allure.step(f'Сгененрировать случайного пользователя\nЗарегистрировать пользователя\n'
                 f'Подготовить данные для запроса, указать некорректный email\n'
                 f'Отправить Post запрос на {Urls.server}{Api.login} с подготовленными данными\n'
                 f'Постусловие: удалить пользователя')
    def test_login_user_incorrect_email_fail(self):
        access_token, email, user, password = helper.create_user()
        payload = {
            "email": DataForTests.incorrect_email,
            "password": password
        }
        response = requests.post((Urls.server + Api.login), data=payload)
        assert response.status_code == 401 and response.json() == {"success": False,
                                                                   "message": "email or password are incorrect"}
        helper.delete_user(access_token)

    @allure.title('Проверка авторизации с неправильным password')
    @allure.description(f'Отправка Post запроса на {Urls.server}{Api.login} с неправильным password\n'
                        f'ОР: код 401, в теле ответа получаем False и сообщение о некорректных кредах\n')
    @allure.step(f'Сгененрировать случайного пользователя\nЗарегистрировать пользователя\n'
                 f'Подготовить данные для запроса, указать некорректный password\n'
                 f'Отправить Post запрос на {Urls.server}{Api.login} с подготовленными данными\n'
                 f'Постусловие: удалить пользователя')
    def test_login_user_incorrect_password_fail(self):
        access_token, email, user, password = helper.create_user()
        payload = {
            "email": email,
            "password": DataForTests.incorrect_password
        }
        response = requests.post((Urls.server + Api.login), data=payload)
        assert response.status_code == 401 and response.json() == {"success": False,
                                                                   "message": "email or password are incorrect"}
        helper.delete_user(access_token)
