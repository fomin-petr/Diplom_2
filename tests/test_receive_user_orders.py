import helper
import requests
from data import Urls, Api


class TestReceiveUserOrders:
    def test_receive_authorized_user_order_list_success(self):
        access_token, email, user, password = helper.create_user()
        orders_numbers = helper.create_two_orders(access_token)
        response = requests.get((Urls.server + Api.orders), headers={"Authorization": access_token})
        assert response.status_code == 200 and response.json()['orders'][0]['number'] in orders_numbers and response.json()['orders'][1]['number'] in orders_numbers
        helper.delete_user(access_token)

    def test_receive_unauthorized_user_order_list_fail(self):
        access_token, email, user, password = helper.create_user()
        orders_numbers = helper.create_two_orders(access_token)
        response = requests.get(Urls.server + Api.orders)
        assert response.status_code == 401 and response.json() == {"success": False, "message": "You should be "
                                                                                                "authorised"}
        helper.delete_user(access_token)
