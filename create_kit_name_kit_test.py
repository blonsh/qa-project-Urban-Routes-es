from sender_stand_request import post_new_user, post_new_client_kit
from data import kit_body
import copy

def get_new_user_token():
    response = post_new_user()
    return response.json()["authToken"]

def get_kit_body(name):
    body = copy.copy(kit_body)
    body["name"] = name
    return body

def positive_assert(kit_body):
    token = get_new_user_token()
    response = post_new_client_kit(kit_body, token)
    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]

def negative_assert_code_400(kit_body):
    token = get_new_user_token()
    response = post_new_client_kit(kit_body, token)
    assert response.status_code == 400

def test_1_create_kit_with_minimum_name_length():
    ###Crear kit con longitud mínima permitida
    body = get_kit_body("a")
    positive_assert(body)

def test_2_max_allowed_chars_511():
    ###Crear kit con el máximo permitido de caracteres (511)
    from data import kit_name_511
    body = get_kit_body(kit_name_511)
    positive_assert(body)

def test_3_create_kit_with_empty_name():
    ###Crear kit con nombre vacío
    body = get_kit_body("")
    positive_assert(body)

def test_4_exceeds_max_chars_512():
    ###Crear kit con longitud mayor a la permitida (512 caracteres)
    from data import kit_name_512
    body = get_kit_body(kit_name_512)
    negative_assert_code_400(body)

def test_5_special_characters():
    ### Crear kit con caracteres especiales
    body = get_kit_body("№%@")
    positive_assert(body)

def test_6_spaces_allowed():
    ###Crar kit con espacios en el nombre
    body = get_kit_body(" A Aaa ")
    positive_assert(body)

def test_7_numbers_as_string():
    ###Crear kit con números (como string)
    body = get_kit_body("123")
    positive_assert(body)

def test_8_missing_parameter():
    ###Crear kit sin el parametro "name"
    token = get_new_user_token()
    response = post_new_client_kit({}, token)
    assert response.status_code == 400

def test_9_name_as_number():
    ###Crear kit con nombre como número
    body = {"name": 123}
    negative_assert_code_400(body)

