import helper
import requests
from data import Urls, Api


class TestCreateOrder:
    def test_create_order_with_auth_and_ingredients_success(self):
        ingredients_hash = helper.get_ingredients_hash()
        access_token, email, user, password = helper.create_user()
        ingredients = helper.get_3_random_ingredients_from_list(ingredients_hash)
        payload = {"ingredients": ingredients}
        response = requests.post((Urls.server + Api.orders), headers={"Authorization": access_token}, data=payload)
        assert response.status_code == 200 and response.json()['success'] == True and isinstance(
            response.json()['name'], str) and response.json()['order']['number'] is not None
        helper.delete_user(access_token)

    def test_create_order_without_auth_with_ingredients_success(self):
        ingredients_hash = helper.get_ingredients_hash()
        ingredients = helper.get_3_random_ingredients_from_list(ingredients_hash)
        payload = {"ingredients": ingredients}
        response = requests.post((Urls.server + Api.orders), data=payload)
        assert response.status_code == 200 and response.json()['success'] == True and isinstance(
            response.json()['name'], str) and response.json()['order']['number'] is not None

    def test_create_order_without_ingredients_bad_request(self):
        payload = {"ingredients": []}
        response = requests.post((Urls.server + Api.orders), data=payload)
        assert response.status_code == 400 and response.json() == {"success": False,
                                                                   "message": "Ingredient ids must be provided"
                                                                   }

    def test_create_order_with_incorrect_ingredients_error(self):
        ingredients_hash = helper.get_ingredients_hash()
        ingredients = helper.get_incorrect_ingredient_hash(ingredients_hash)
        payload = {"ingredients": ingredients}
        response = requests.post((Urls.server + Api.orders), data=payload)
        assert response.status_code == 500






