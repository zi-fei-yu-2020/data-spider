from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Selenium:
    def __init__(self, url=None):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def get_url(self, url=None):
        self.url = url or self.url
        self.driver.get(self.url)

    def find_element(self, by, value):
        return self.driver.find_element(by=by, value=value)

    def click(self, element):
        element.click()

    def send_keys(self, element, keys):
        element.send_keys(keys)

    def quit(self):
        self.driver.quit()

    def set_driver(self, driver):
        self.driver = driver


if __name__ == '__main__':
    s = Selenium("https://gitee.com/")
    s.get_url()
