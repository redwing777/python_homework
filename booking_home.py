import allure
from selenium.webdriver.common.by import By

from base_page import BasePage
from constants import TestProfile
from element import Element
from helpers.browser_manager import BrowserManager
from helpers.retry import retry


class BookingPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.base_url = TestProfile.url
        self.altruisto_button_locator = (By.XPATH, "//a[@class='altruisto-notification__button']")
        self.altruisto_active_banner_locator = (By.XPATH,
                                                "//div[contains(text(), 'You are now collecting money for charities')]")
        self.preferred_city_input_locator = (By.XPATH, "//input[@placeholder='Where are you going?']")
        self.dates_placeholder_locator = \
            (By.XPATH, "//div[@class='xp__dates xp__group' and @data-visible='accommodation,flights,rentalcars']")
        self.next_month_button_locator = (By.XPATH, "//div[@data-bui-ref='calendar-next']")
        self.check_in_date_locator = (By.XPATH,
                                      "//div[@class='bui-calendar__content']/div[1]/div[@class='bui-calendar__month']")
        self.check_out_date_locator = (By.XPATH,
                                      "//div[@class='bui-calendar__content']/div[2]/div[@class='bui-calendar__month']")
        self.search_button_locator = (By.XPATH,
                                      "//div[@class='sb-searchbox-submit-col -submit-button ']/button")
        self.list_of_offers = (By.XPATH, "//div[@id='hotellist_inner']")
        self.see_availability_button = (By.XPATH, "//*[@class='bui-button__text js-sr-cta-text']/..")

        self.altruisto_button = Element(self.driver, self.altruisto_button_locator)
        self.altruisto_active_banner = Element(self.driver, self.altruisto_active_banner_locator)
        self.preferred_city_input = Element(self.driver, self.preferred_city_input_locator)
        self.dates_placeholder = Element(self.driver, self.dates_placeholder_locator)
        self.next_month_button = Element(self.driver, self.next_month_button_locator)
        self.check_in_date = Element(self.driver, self.check_in_date_locator)
        self.check_out_date = Element(self.driver, self.check_out_date_locator)
        self.search_button = Element(self.driver, self.search_button_locator)

    @allure.step("Open booking page.")
    def go_to_home_page(self):
        BrowserManager.close_current_tab(self.driver)
        self.go_to(self.base_url)
        self.refresh()

    @allure.step("Click on Altruisto activation popup.")
    @retry(timeout=TestProfile.timeout, tries=6)
    def click_on_altruisto_donation(self):
        self.altruisto_button.click()

    @allure.step("Wait for Alttruisto offer become active.")
    @retry(timeout=TestProfile.timeout, tries=10)
    def wait_until_altruisto_become_active(self):
        self.altruisto_active_banner.is_displayed()

    def activate_altruisto_donation(self):
        self.click_on_altruisto_donation()
        self.wait_until_altruisto_become_active()

    @allure.step("Select city.")
    def select_city_to_travel(self, city=TestProfile.prefered_city):
        self.preferred_city_input.click()
        self.preferred_city_input.send_keys(city)

    @allure.step("Open calendar and switch to next month")
    def open_calendar_on_next_month(self):
        self.dates_placeholder.click()
        self.next_month_button.click_with_js()

    @allure.step("Select dates in calendar")
    def select_dates(self, checkin=15, checkout=14):
        checkin_locator = (By.XPATH, f"//span[@aria-label='{checkin} {self.check_in_date.text}']")
        checkout_locator = (By.XPATH, f"//span[@aria-label='{checkout} {self.check_out_date.text}']")
        check_in_date = Element(self.driver, checkin_locator)
        check_in_date.click_with_js()
        check_out_month = Element(self.driver, checkout_locator)
        check_out_month.click_with_js()

    @allure.step("Search apartments by preferred parameters")
    def search_apartments_by_parameters(self, **kwargs):
        self.select_city_to_travel()
        self.open_calendar_on_next_month()
        self.select_dates(**kwargs)
        self.search_button.click()

    @allure.step("Click on specified offer.")
    @retry(timeout=TestProfile.timeout, tries=10)
    def click_on_specified_offer(self, offer_number=1):
        offer_list = self.list_of_offers[1]
        availability_buton = self.see_availability_button[1]
        preferred_offer_locator = (By.XPATH, f"{offer_list}/div[{offer_number}]{availability_buton}")
        preferred_offer = Element(self.driver, preferred_offer_locator)
        preferred_offer.click_with_js()
