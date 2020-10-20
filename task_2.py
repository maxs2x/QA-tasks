from time import sleep
from selenium import webdriver


class CoinMarketCap():
    """

    """
    def __init__(self):
        #Инициализация браузера
        self.firefox = webdriver.Firefox()
        self.firefox.get('https://coinmarketcap.com/')


class Language(CoinMarketCap):
    def change_language(self, path_from_languages, iteration):
        """
        функция перебора языков.
        Если после смены языка, название языка в div совпадает с выбранным, то выводим Pass
        :param path_from_languages:  путь xpath к диву с нужнвм языком
        :param iteration:  количество языков
        :return:
        """
        sleep(1)
        for i in range(1, int(iteration) + 1):
            self.firefox.find_element_by_class_name("cmc-popover").click()
            sleep(1)
            lang_button = self.firefox.find_element_by_xpath(path_from_languages.format(i))
            text_lang = lang_button.text[:-3]
            lang_button.click()
            text_button_lang = self.firefox.find_element_by_xpath(
                '//*[@id="__next"]/div/div[1]/div[3]/div[1]/div/div[2]/div[3]/div/div/button/span[2]').text
            if text_lang == text_button_lang:
                print('Pass lang ' + text_lang)
            else:
                print(len(text_lang), print(len(text_button_lang)))
                print('Fail lang ' + text_lang)
        self.firefox.close()


    def change_popular_language(self):
        """
        Проверка блока смены самых популярных языков
        :return:
        """
        path_from_popular_languages = '//*[@id="__next"]/div/div[1]/div[3]/div[1]/div/div[2]/div[3]/div/div[2]/div/div[1]/div[{}]/a'
        amount_popular_lang = 5
        self.change_language(path_from_popular_languages, amount_popular_lang)


    def change_all_language(self):
        """
        Проверка блока смены всех популярных языков
        """
        path_from_all_languages = '//*[@id="__next"]/div/div[1]/div[3]/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div[{}]/a'
        amount_all_lang = 27
        self.change_language(path_from_popular_languages, amount_popular_lang)


#Запуск теста для блока популярных языков
Language().change_popular_language()
#Запуск теста для блока всех языков
Language().change_popular_language()
