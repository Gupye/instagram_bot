import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from pages import HomePage
from time import sleep
import requests


def main():
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    count_max = int(config['settings']['count'])
    password = config['settings']['password']
    username = config['settings']['username']
    delay = int(config['settings']['delay'])
    with open('list.txt', 'r', encoding='utf-8') as f:
        dic = f.readlines()

    browser = webdriver.Firefox()
    browser.implicitly_wait(delay)

    home_page = HomePage(browser)
    login_page = home_page.go_to_login_page()
    login_page.login(username, password)
    sleep(delay)
    count = 0
    for i in dic:
        browser.get(f'https://www.instagram.com/{i}/')
        soup = BeautifulSoup(browser.page_source, 'lxml')
        for link in soup.find_all('a'):
            if (link.get('href')[1] == 'p') and (link.get('href')[2] == '/'):
                linker = link.get('href')
                break
        browser.get(f'https://www.instagram.com{linker}')
        soup = BeautifulSoup(browser.page_source, 'lxml')
        assa = soup.find_all('svg')[0]
        nrav = assa.get('aria-label')
        if nrav == 'Нравится':
            btn_like = browser.find_element_by_class_name("wpO6b")
            btn_like.click()
            count = count + 1
            if count >= count_max:
                break


if __name__ == "__main__":
    main()
# browser.close()
