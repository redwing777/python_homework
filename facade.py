import os

from base_page import BasePage
from pages.booking_home import BookingPage
from pages.booking_hotel import BookingHotel


class Pages(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.booking_homepage = BookingPage(self.driver)
        self.booking_hotel_page = BookingHotel(self.driver)


class UiActions:
    def __init__(self, browser):
        self.pages = Pages(browser)
        self.root_path = os.path.abspath(os.path.dirname(__file__))
