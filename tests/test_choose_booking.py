import allure
import pytest


@allure.title("UI Automation framework tesst")
@pytest.mark.smoke
def test_ui_some(ui_actions):
    ui_actions.pages.booking_homepage.go_to_home_page()
    ui_actions.pages.booking_homepage.activate_altruisto_donation()
    ui_actions.pages.booking_homepage.search_apartments_by_parameters()
    ui_actions.pages.booking_homepage.click_on_specified_offer()
    ui_actions.pages.booking_hotel_page.switch_to_hotel_page()


