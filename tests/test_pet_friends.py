import os

from api import PetFriends
from settings import *

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    staus, result = pf.get_api_key(email, password)
    assert staus == 200
    assert 'key' in result

def test_get_list_of_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Boar', animal_type='cat', age="3", pet_photo='images/cattt.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname('F:\Python\QAP\pytest_first_test/tests/'), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_new_pet_with_valid_data_without_photo(name='Мяу', animal_type='кот', age='3'):
    '''Проверяем, что можно добавить питомца с корректными данными без фото по 'name'.'''
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == 'Мяу'

def test_unsuccessful_add_new_pet_with_negative_age_without_photo(name='Гав', animal_type='собака', age='-2'):
    '''Проверяем, что нельзя добавить питомца с отрицательным значением без фото по 'age'.
    Если можно, то ответ 200, если нет то 403'''
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['age'] == '-2'    # Баг: Питомец с отрицательным возрастом добавлен.

def test_unsuccessful_add_new_pet_with__spaces_name_without_photo(name='   ', animal_type='собака', age='2'):
    '''Проверяем, что нельзя добавить питомца с  группой пробелов вместо имени - значением без фото по 'name'.
    Если можно, то ответ 200, если нет то 403'''
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == '   '    # Баг: Питомец с группой пробелов вместо имени - значением добавлен.

def test_unsuccessful_add_new_pet_without_any_values_wiht_photo(name='', animal_type='', age='', pet_photo='images/cattt.jpg'):
    '''Проверяем, что нельзя добавить питомца с  пустыми значениями c фото по 'name', 'animal_type', 'age'.
    Если можно, то ответ 200, если нет то 400'''

    pet_photo = os.path.join(os.path.dirname('F:\Python\QAP\pytest_first_test/tests/'), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200         #Баг: Питомец с пустыми значениями c фото по 'name', 'animal_type', 'age' добавлен.

def test_successful_add_photo_of_pet(filter='my_pets', pet_photo='images/qq.jpg'):
    '''Проверяем, что можно добавить фото питомца с корректными данными по 'pet_id'.'''
    pet_photo = os.path.join(os.path.dirname('F:\Python\QAP\pytest_first_test/tests/'), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter)
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] != ''

def test_unsuccessful_add_photo_of_pet(filter='my_pets', pet_photo='images/empty2.gif'):
    '''Проверяем, что нельзя добавить фото питомца с неподдерживаемым форматом .gif по 'pet_id'.'''
    pet_photo = os.path.join(os.path.dirname('F:\Python\QAP\pytest_first_test/tests/'), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter)
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 500

def test_unsuccessful_add_photo_of_pet_another_user(filter='', pet_photo='images/qq.jpg'):
    '''Проверяем, что нельзя добавить фото питомца с корректными данными по 'pet_id' другова пользователя.'''
    pet_photo = os.path.join(os.path.dirname('F:\Python\QAP\pytest_first_test/tests/'), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, filter)
    pet_id = all_pets['pets'][-1]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 500

def test_get_list_of_pets_with_invalid_key(filter=''):
    """ Проверяем, что запрос всех питомцев с некорректным ключём вызовет 403 ошибку.
        Для этого сначала создаём некорректный api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев. Доступное значение параметра filter - 'my_pets' либо '' """
    auth_key = {}
    auth_key['key'] = '00ca577d7ae4c40e66eb5d1b432fb6696b86258787dd8df55f30cd9f'
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_get_api_key_with_invalid_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем, что запрос api ключа с невалидным паролем и с валидным емейлом
    возвращает статус 403 и в результате не содержится слово key'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_invalid_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем, что запрос api ключа с валидным паролем и с невалидным емейлом
    возвращает статус 403 и в результате не содержится слово key'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result