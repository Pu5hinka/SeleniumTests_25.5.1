import pytest
from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture (autouse=True)
### подключение драйвера
def start_page():
   pytest.driver = webdriver.Chrome('chromedriver.exe')

   #авторизация
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   yield
   pytest.driver.quit()

@pytest.fixture()
### открывается авторизованная страница с питомцами
def show_my_pets():
   # Вводим email и пароль
   pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
   pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

   # Нажимаем на кнопку "Войти"
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # кликнуть на пункт меню "Мои питомцы"
   pytest.driver.find_element(By.XPATH, '//*[@href=\"/my_pets\"]').click()
