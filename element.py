from time import sleep

import wrapt as wrapt
from selenium.common.exceptions import (NoSuchElementException, ElementNotVisibleException,
                                        ElementNotSelectableException, StaleElementReferenceException, TimeoutException,
                                        ElementClickInterceptedException, MoveTargetOutOfBoundsException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import constants


class retry:

    def __init__(self, tries=4, delay=3, backoff=1, exceptions=Exception, action_before_retry=None):
        """
           Retry calling the decorated function using an exponential backoff.
           Args:
               exceptions: The exception to check. may be a tuple of
                   exceptions to check.
               tries: Number of times to try (not retry) before giving up.
               delay: Initial delay between retries in seconds.
               backoff: Backoff multiplier (e.g. value of 2 will double the delay
                   each retry).
               action_before_retry: Lambda function or string which will be executed before each retry
           """
        self.tries = tries
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
        self.action_before_retry = action_before_retry

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        # pylint: disable=unused-variable
        __tracebackhide__ = True
        mdelay = self.delay

        for attempt in range(1, self.tries + 1):
            try:
                return wrapped(*args, **kwargs)
            except self.exceptions as error:
                if attempt == self.tries:
                    raise
                Exception(f"{error}, Retrying in {mdelay} seconds... Try #{attempt}")
                sleep(mdelay)
                if self.action_before_retry:
                    self.action_before_retry()
                mdelay *= self.backoff


class Element:
    DEFAULT_PAGE_LOAD_TIMEOUT = constants.TestProfile.timeout

    def __init__(self, browser, locator):
        self.driver = browser
        self.locator = tuple(locator[:2])
        self.description = (locator[2] if len(locator) > 2
                            else "Unknown name of element. Please describe the locator name.")

    @property
    def text(self):
        """finds element and returns the text"""
        return self.find_element().text

    def get_attribute(self, name, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """
        Gets the given attribute or property text value on the element
        :param name: attribute name to check
        :type name: str
        :param timeout: timeout to wait before throw timeout exception
        :type timeout: int
        :return: attribute or property value, or None
        :rtype: str
        """
        return self.find_element(timeout).get_attribute(name)

    @property
    def is_validation_error(self):
        """
        Checks whether element has validation error and highlighted with red border
        :return: "True" if element's classes list contains "ng-invalid", else "False"
        :rtype: bool
        """
        return "ng-invalid" in self.get_attribute("class")

    @property
    def is_enabled(self):
        """
        Checks whether the element is "enabled" on page
        :return: "True" if element is enabled, else: "False"
        :rtype: bool
        """
        return not bool(self.get_attribute("disabled"))

    @retry(exceptions=StaleElementReferenceException, tries=3, delay=1)
    def is_displayed(self, timeout=2):
        """
        Checks whether element is displayed on page
        :param timeout: time in seconds to wait until try to check whether is element is displayed on page
        :type timeout: int
        :return: <bool>
        """
        try:
            element = self.find_element(timeout=timeout)
            return element.is_displayed()
        except TimeoutException:
            return False

    def find_element(self, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """waits and returns element in case element was found"""
        return self._wait(timeout=timeout).until(EC.presence_of_element_located(self.locator))

    def find_elements(self, locator):
        """ finds elements in webelement"""
        return self.find_element().find_elements(*locator[:2])

    def click(self, wait_to_be_clickable=True):
        """waits element to be clickable and clicks it, if wait_to_be_clickable parameter is False skips
         "wait to be clickable" check for element and just clicks it.
        :param wait_to_be_clickable skip "wait to be clickable" check for element
        :type wait_to_be_clickable bool
        """
        if wait_to_be_clickable:
            self.wait_for_clickable()
        self.find_element().click()

    def click_with_js(self):
        """clicks on element using JavaScript"""
        element = self.find_element()
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, text):
        """waits element to be clickable, clears input and sends text"""
        self.wait_for_clickable()
        element = self.find_element()
        element.clear()
        element.send_keys(text)

    def wait_for_visible(self, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """returns element in case element is displayed """
        element = self._wait(timeout).until(EC.visibility_of_any_elements_located(self.locator))
        return element

    def wait_for_clickable(self, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """returns element in case element is displayed and is enabled"""
        element = self._wait(timeout).until(EC.element_to_be_clickable(self.locator))
        return element

    def _wait(self, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """explicit wait to use in custom waiters"""
        wait = WebDriverWait(driver=self.driver, timeout=timeout, ignored_exceptions=(
            NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException,
            StaleElementReferenceException, ElementClickInterceptedException))
        return wait

    def get_css_value(self, name):
        """
        Returns value of CSS property of the element
        :param name: CSS property name to check
        :type name: str
        :return: value of CSS property
        :rtype: str
        """
        return self.find_element().value_of_css_property(name)

    def get_property(self, name):
        """
        Gets the given property of the element
        :param name: name of the element property
        :type name: str
        :return: property value
        """
        return self.find_element().get_property(name)

    def scroll_into_view(self, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """
        Scrolls to element
        """
        try:
            if not self.is_displayed():
                element = self.find_element(timeout)
                actions = ActionChains(self.driver)
                actions.move_to_element(element)
                actions.perform()
                sleep(0.1)
                # Do not touch. Fix for FF
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except MoveTargetOutOfBoundsException:
            # Workaround for gecko driver issue with move_to method.
            pass

    def scroll_to_element_and_click(self):
        element = self.find_element()
        if element.is_enabled():
            self.scroll_into_view()
        element.click()

    def scroll_down(self):
        """
        scrolls down to the end of page
        """
        document = self.driver.find_element_by_tag_name("html")
        document.send_keys(Keys.END)

    def has_children(self, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """
        Checks if element have children elements
        :return: bool
        """
        return len(self.find_element(timeout).find_elements(By.XPATH, "./*")) > 0

    def wait_for_not_visible(self, timeout=DEFAULT_PAGE_LOAD_TIMEOUT):
        """returns element in case element is not displayed """
        element = self._wait(timeout).until(EC.invisibility_of_element_located(self.locator))
        return element
