import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from constants import desired_caps, TestProfile
from facade import UiActions


@pytest.fixture(scope="session")
def browser(request):
    host = request.config.getoption("--h")
    preferred_browser = request.config.getoption("--b")
    options = webdriver.ChromeOptions()
    options.add_extension(TestProfile.ext_file)
    options.add_argument("start-maximized")
    options.add_argument("--disable-popup-blocking")

    try:
        is_docker = request.config.getoption("--d")
    except:
        is_docker = False
    if preferred_browser and not is_docker:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  options=options,
                                  desired_capabilities=desired_caps.get(preferred_browser))
        yield driver
        driver.quit()
    else:
        driver = webdriver.Remote(command_executor=f'http://{host}:4444/wd/hub',
                                  options=options,
                                  desired_capabilities=desired_caps.get(preferred_browser))
        yield driver
        driver.quit()


@pytest.fixture(scope="session")
def ui_actions(browser) -> UiActions:
    return UiActions(browser)


def pytest_addoption(parser):
    parser.addoption("--b", action="store", help="Choose browser for using")
    parser.addoption("--d", action="store", default=False, help="Run in container?")
    parser.addoption("--h", action="store", default="localhost", help="Who webdriver host?")
