import requests
import random
import string
import json
from data import Urls, Api


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def generate_email():
    email = generate_random_string(10) + '@' + generate_random_string(6) + '.ru'
    return email


def generate_new_creds():
    email = generate_email()
    user = generate_random_string(10)
    password = generate_random_string(10)
    return email, user, password


def generate_random_number(min_int, max_int):
    return random.randint(min_int, max_int)


def delete_user(access_token):
    requests.delete((Urls.server + Api.user), headers={"Authorization": access_token})


def create_user():
    email, user, password = generate_new_creds()
    payload = {
        "email": email,
        "password": password,
        "name": user
    }
    response = requests.post((Urls.server + Api.register_user), data=payload)
    access_token = response.json()["accessToken"]
    return access_token, email, user, password


def get_ingredients_hash():
    response = requests.get(Urls.server + Api.ingredients)
    ingredients_hash = []
    ingredients_data = response.json()["data"]
    for ingredient in ingredients_data:
        ingredients_hash.append(ingredient["_id"])
    return ingredients_hash


def get_3_random_ingredients_from_list(ingredients_hash):
    ingredients = []
    for i in range(3):
        while True:
            n = generate_random_number(0, len(ingredients_hash)-1)
            if ingredients_hash[n] not in ingredients:
                ingredients.append(ingredients_hash[n])
                break
    return ingredients


def get_incorrect_ingredient_hash(ingredients_hash):
    ingredients = []
    n = generate_random_number(0, len(ingredients_hash) - 1)
    ingredients.append(ingredients_hash[n] + 'nnn')
    return ingredients


def create_order_for_authorized_user(access_token):
    ingredients_hash = get_ingredients_hash()
    ingredients = get_3_random_ingredients_from_list(ingredients_hash)
    payload = {"ingredients": ingredients}
    response = requests.post((Urls.server + Api.orders), headers={"Authorization": access_token}, data=payload)
    return response.json()['order']['number']


def create_two_orders(access_token):
    order_numbers = [create_order_for_authorized_user(access_token), create_order_for_authorized_user(access_token)]
    return order_numbers

