class BrowserManager:
    @staticmethod
    def switch_to_next_tab(driver):
        """
        Method sswitches to next window instance
        :param driver: webdriver
        :return: None
        """
        current_tab = False
        for handle in driver.window_handles:
            if current_tab:
                driver.switch_to.window(handle)
                break
            if handle == driver.current_window_handle:
                current_tab = True

    @staticmethod
    def switch_to_main_tab(driver):
        """
        Switch to main browser tab
        :param driver:
        :return:
        """
        driver.switch_to.window(driver.window_handles[0])

    @staticmethod
    def close_current_tab(driver):
        """
        Method closes current window insstance
        :param driver:
        :return:
        """
        driver.close()
        BrowserManager.switch_to_main_tab(driver)