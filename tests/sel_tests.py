import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_all_my_pets(show_my_pets):
    '''Проверяем, что на странице пользователя присутствуют все питомцы'''

    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')))

    # Получаем кол-во всех питомцев
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')
    all_pets = len(pets)

    # Получаем кол-во питомцев из информации пользователя, Выделяем из полученного списка число питомцев
    list_of_pets = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")
    num_pets = list_of_pets[0].text.split('\n')
    num_pets = num_pets[1].split(' ')
    num_pets = int(num_pets[1])

    # Проверяем, что кол-во питомцев на странице соответствует кол-ву в информации пользователя
    assert all_pets == num_pets


def test_different_name(show_my_pets):
    '''Проверяем, что у всех питомцев уникальные имена'''
    # Получаем информацию обо всех именах питомцах
    pytest.driver.implicitly_wait(10)
    name = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td:nth-child(2)')

    #Проверяем, что имена не повторяются
    assert len(set(name)) == len(name)
    print(f'Количество уникальных имен: {len(set(name))}')
    print(f'Количество имен: {len(name)}')


def test_different_pets(show_my_pets):
    '''Проверяем, что в списке нет повторяющихся питомцев'''
    # Получаем информацию обо всех питомцах
    pet_info = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Перебираем данные из pet_info, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу.
    list_info = []
    for i in range(len(pet_info)):
        data_pet = pet_info[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_info.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in list_info:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0


def test_have_full_info(show_my_pets):
    '''Проверяем, что у всех питомцев есть возраст, имя, порода'''
    # Получаем информацию обо всех питомцах
    pytest.driver.implicitly_wait(10)
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody tr')

    #Перебираем всю информацию,оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу. Находим количество элементов в получившемся списке и сравниваем их
    # с ожидаемым результатом
    for i in range(len(pets)):
        info_pets = pets[i].text.replace('\n', '').replace('×', '')
        split_info_pets = info_pets.split(' ')
        result = len(split_info_pets)
        assert result == 3


def test_have_photo(show_my_pets):
    '''Проверяем,что хотя бы у половины питомцев есть фото'''

    # Получаем кол-во всех питомцев и их фото
    pytest.driver.implicitly_wait(10)
    pets_photo = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody img')

    # Получаем кол-во питомцев из информации пользователя, Выделяем из полученного списка число питомцев
    list_of_pets = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")
    num_pets = list_of_pets[0].text.split('\n')
    num_pets = num_pets[1].split(' ')
    num_pets = int(num_pets[1])

    #Ищем питомцев без фото
    half_pets = num_pets // 2
    count = 0
    for i in range(len(pets_photo)):
        if pets_photo[i].get_attribute('src') != '':
            count += 1

    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    assert len(pets_photo) >= half_pets
