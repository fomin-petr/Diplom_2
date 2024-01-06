import helper
import requests
from data import Urls, Api, DataForTests


class TestLoginUser:
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
