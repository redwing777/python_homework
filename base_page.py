from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, browser):
        self.driver = browser
        self.default_locator = (By.XPATH, "")  # Used as dummy for objects initialization

    def go_to(self, url):
        self.driver.get(url)

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def refresh(self):
        self.driver.refresh()

    @property
    def title(self):
        return self.driver.title
