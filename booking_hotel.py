import allure
from selenium.webdriver.common.by import By

from base_page import BasePage
from constants import TestProfile
from element import Element
from helpers.browser_manager import BrowserManager
from helpers.retry import retry


class BookingHotel(BasePage):

    def __init__(self, browser):
        super().__init__(browser)
        self.hotel_reserve_button_locator = \
            (By.XPATH,
             "//*[@id='wrap-hotelpage-top']//span[@class='bui-button__text' and contains(text(), 'Reserve')]/..")

        self.hotel_reserve_button = Element(self.driver, self.hotel_reserve_button_locator)

    @allure.step("Got to hotel page")
    @retry(timeout=TestProfile.timeout, tries=10)
    def switch_to_hotel_page(self):
        BrowserManager.switch_to_next_tab(self.driver)
        self.hotel_reserve_button.is_displayed()
