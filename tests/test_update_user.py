import helper
import requests
from data import Urls, Api


class TestUpdateUser:
    def test_update_user_email_success(self):
        access_token, email, user, password = helper.create_user()
        new_email = '1' + email
        payload = {
            "email": new_email
        }
        response = requests.patch((Urls.server + Api.user), headers={"Authorization": access_token}, data=payload)
        assert (response.status_code == 200 and response.json()["success"] == True
                and response.json()["user"] == {
                    "email": new_email, "name": user}
                )
        helper.delete_user(access_token)

    def test_update_user_name_success(self):
        access_token, email, user, password = helper.create_user()
        new_user = '1' + user
        payload = {
            "name": new_user
        }
        response = requests.patch((Urls.server + Api.user), headers={"Authorization": access_token}, data=payload)
        assert (response.status_code == 200 and response.json()["success"] == True
                and response.json()["user"] == {
                    "email": email, "name": new_user}
                )
        helper.delete_user(access_token)

    def test_update_user_password_success(self):
        access_token, email, user, password = helper.create_user()
        new_password = '1' + password
        payload = {
            "password": new_password
        }
        response = requests.patch((Urls.server + Api.user), headers={"Authorization": access_token}, data=payload)
        assert (response.status_code == 200 and response.json()["success"] == True
                and response.json()["user"] == {
                    "email": email, "name": user}
                )
        helper.delete_user(access_token)

    def test_update_user_without_token_not_authorized(self):
        access_token, email, user, password = helper.create_user()
        new_email = '1' + email
        new_user = '1' + user
        new_password = '1' + password
        payload = {
            "email": new_email,
            "name": new_user,
            "password": new_password
        }
        response = requests.patch((Urls.server + Api.user), headers={"Authorization": ""}, data=payload)
        assert response.status_code == 401 and response.json() == {"success": False,
                                                                   "message": "You should be authorised"
                                                                   }

        helper.delete_user(access_token)

    def test_update_user_existing_email_forbidden(self):
        access_token_1, email_1, user_1, password_1 = helper.create_user()
        access_token_2, email_2, user_2, password_2 = helper.create_user()
        payload = {
            "email": email_2,
            "name": user_2,
            "password": password_2
        }
        response = requests.patch((Urls.server + Api.user), headers={"Authorization": access_token_1}, data=payload)
        assert response.status_code == 403 and response.json() == {"success": False,
                                                                   "message": "User with such email already exists"
                                                                   }
        helper.delete_user(access_token_1)
        helper.delete_user(access_token_2)

