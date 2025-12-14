import requests
from configuration import BASE_URL, CREATE_USER_PATH, CREATE_KIT_PATH
from data import user_body

def post_new_user():
    return requests.post(BASE_URL + CREATE_USER_PATH, json=user_body)

#Crear un nuevo kit de producto
def post_new_client_kit(kit_body, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    return requests.post(BASE_URL + CREATE_KIT_PATH, json=kit_body, headers=headers)
