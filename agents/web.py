from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from gemini.web_model import get_xpath, get_summarize_text
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib.parse import urljoin
import pyautogui as pg
import re


key_map = {
    "enter": Keys.ENTER,
    "tab": Keys.TAB,
    "backspace": Keys.BACKSPACE,
    "space": Keys.SPACE,
    "esc": Keys.ESCAPE,
    "delete": Keys.DELETE,
    "insert": Keys.INSERT,

    # Arrow Keys
    "arrow_up": Keys.ARROW_UP,
    "arrow_down": Keys.ARROW_DOWN,
    "arrow_left": Keys.ARROW_LEFT,
    "arrow_right": Keys.ARROW_RIGHT,

    # Function Keys (F1-F12)
    "f1": Keys.F1,
    "f2": Keys.F2,
    "f3": Keys.F3,
    "f4": Keys.F4,
    "f5": Keys.F5,
    "f6": Keys.F6,
    "f7": Keys.F7,
    "f8": Keys.F8,
    "f9": Keys.F9,
    "f10": Keys.F10,
    "f11": Keys.F11,
    "f12": Keys.F12,

    # Modifier Keys
    "shift": Keys.SHIFT,
    "ctrl": Keys.CONTROL,
    "alt": Keys.ALT,
    "meta": Keys.META,   # Windows/Command key

    # Numeric Keypad
    "numpad_0": Keys.NUMPAD0,
    "numpad_1": Keys.NUMPAD1,
    "numpad_2": Keys.NUMPAD2,
    "numpad_3": Keys.NUMPAD3,
    "numpad_4": Keys.NUMPAD4,
    "numpad_5": Keys.NUMPAD5,
    "numpad_6": Keys.NUMPAD6,
    "numpad_7": Keys.NUMPAD7,
    "numpad_8": Keys.NUMPAD8,
    "numpad_9": Keys.NUMPAD9,
    "numpad_add": Keys.ADD,
    "numpad_subtract": Keys.SUBTRACT,
    "numpad_multiply": Keys.MULTIPLY,
    "numpad_divide": Keys.DIVIDE,
    "numpad_decimal": Keys.DECIMAL,

    # Special Keys
    "home": Keys.HOME,
    "end": Keys.END,
    "page_up": Keys.PAGE_UP,
    "page_down": Keys.PAGE_DOWN,
    "pause": Keys.PAUSE,
}

driver = None
xpaths = []


def initialize_webdriver() -> dict:
    """
    Initializes the Chrome Webdriver.

    This function checks if a Webdriver instance exists. If not, it initializes 
    a new Chrome Webdriver with maximized window settings.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
    return {"result": "Done"}


def open_website(url: str) -> dict:
    """
    Opens a given URL in the web browser using the initialized WebDriver.

    Args:
        url (str): The URL of the website to open.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    driver.get(url)
    print(f"Opened: {url}")
    return {"result": "Done"}


def new_tab(url: str) -> dict:
    """
    Opens a new tab in the web browser and navigates to the given URL.

    Args:
        url (str): The URL to open in the new tab.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    print(f"Opened new tab: {url}")
    return {"result": "Done"}


def switch_tab(index: int) -> dict:
    """
    Switches to a specific tab in the web browser.

    Args:
        index (int): The tab index (1-based) to switch to.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    try:
        driver.switch_to.window(driver.window_handles[index - 1])
        print(f"Switched to tab {index}: {driver.current_url}")
    except (IndexError, ValueError):
        print(f"Invalid tab index: {index}")

    return {"result": "Done"}


def close_tab() -> dict:
    """
    Closes the current browser tab. If other tabs remain open, switches to the last one.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    driver.close()
    if driver.window_handles:
        driver.switch_to.window(driver.window_handles[-1])
    print("Closed current tab")

    return {"result": "Done"}


def scroll(direction: str, amount: int) -> dict:
    """
    Scrolls the webpage in the specified direction by a given amount.

    Args:
        direction (str): The direction to scroll ("up" or "down").
        amount (int): The number of pixels to scroll.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    scroll_value = amount if direction == "down" else -amount
    driver.execute_script(f"window.scrollBy(0, {scroll_value});")
    print(f"Scrolled {direction} by {amount} pixels")

    return {"result": "Done"}


def web_search(search_query: str) -> dict:
    """
    Performs a web search by simulating keyboard input.

    Args:
        search_query (str): The search query.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    try:
        sleep(3)
        pg.hotkey("ctrl", "k")
        pg.write(search_query)
        sleep(3)
        pg.press("enter")
        print(f"Typed '{search_query}'")
    except Exception as e:
        print(f"Error typing into element: {e}")

    return {"result": "Done"}


def type_text(text: str) -> dict:
    """
    Types the given text into the last selected input field.

    Args:
        text (str): The text to type.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    try:
        element = driver.find_element("xpath", xpaths[-1])
        element.clear()
        for ch in text:
            element.send_keys(ch)
        print(f"Typed '{text}' into element: {element}")
    except Exception as e:
        print(f"Error typing into element: {e}")

    return {"result": "Done"}


def click_element(description: str) -> dict:
    """
    Finds and clicks an element on the webpage using its description.

    Args:
        description (str): The description of the element.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    try:
        response = get_xpath(get_body_html(), description)
        xpath = response["xpath"]
        xpaths.append(xpath)
        print(f"Extracted XPath: {xpath}")

        if "href" in xpath:
            match = re.search(r"@href='([^']+)'", xpath)
            if match:
                link = match.group(1)
                if link.startswith("/"):
                    base_url = "/".join(driver.current_url.split("/", 3)[:3])
                    link = urljoin(base_url, link)
                    print(link, base_url)
                open_website(link)
            else:
                print("No href found in XPath.")
        else:
            element_obj = driver.find_element("xpath", xpath)
            element_obj.click()

        print(f"Clicked element: {description}")
    except Exception as e:
        print(f"Error clicking element: {e}")

    return {"result": "Done"}


def exit_webdriver() -> dict:
    """
    Closes the browser.

    Returns:
        dict: A dictionary indicating the operation result.
    """
    try:
        driver.quit() 
    except Exception as e:
        print(f"Error closing browser: {e}")

    return {"result": "Done"}





def get_body_html(self) -> str:
    """Returns the raw HTML of the page starting from the <body> tag."""
    body_element = self.driver.find_element(
        "tag name", "body")
    return body_element.get_attribute("outerHTML")


class BrowserCLI:
    def __init__(self):
        """Initialize WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        self.xpaths = []

        # Command mapping
        self.commands = {
            "open": self.open_website,
            "newtab": self.new_tab,
            "switch": self.switch_tab,
            "scroll": self.scroll,
            "close": self.close_tab,
            "exit": self.exit_browser,
            "press": self.press_key,
            "type": self.type_text,
            "click": self.click_element,
            "help": self.show_help,
            "summary": self.summarize_link,
            "search": self.web_search
        }

    def summarize_link(self) -> str:
        response = get_summarize_text(self.get_body_html())
        print(response)
        return response

    def open_website(self, url):
        self.driver.get(url)
        print(f"Opened: {url}")

    def new_tab(self, url):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        print(f"Opened new tab: {url}")

    def switch_tab(self, index):
        try:
            self.driver.switch_to.window(
                self.driver.window_handles[int(index) - 1])
            print(f"Switched to tab {index}: {self.driver.current_url}")
        except (IndexError, ValueError):
            print(f"Invalid tab index: {index}")

    def close_tab(self):
        self.driver.close()
        if self.driver.window_handles:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        print("Closed current tab")

    def scroll(self, direction, amount):
        amount = int(amount)
        scroll_value = amount if direction == "down" else -amount
        self.driver.execute_script(f"window.scrollBy(0, {scroll_value});")
        print(f"Scrolled {direction} by {amount} pixels")

    def web_search(self, *text):
        try:
            sleep(3)
            text = " ".join(text)
            pg.hotkey("ctrl", "k")
            pg.write(text)
            sleep(3)
            pg.press("enter")
            print(f"Typed '{text}'")
        except Exception as e:
            print(f"Error typing into element: {e}")

    def type_text(self, *text):
        try:
            element = self.driver.find_element("xpath", self.xpaths[-1])
            element.clear()
            for ch in text:
                element.send_keys(ch)
            print(f"Typed '{text}' into element: {element}")
        except Exception as e:
            print(f"Error typing into element: {e}")

    # def type_text(self, method, value, *text):
    #     """Type text into an input field using id, class, name, xpath, css"""

    #     text = " ".join(text)  # Combine multiple words
    #     try:
    #         element = self.driver.find_element(method, value)
    #         element.clear()
    #         element.send_keys(text)
    #         print(f"Typed '{text}' into [{method}='{value}']")
    #     except Exception as e:
    #         print(f"Error typing into [{method}='{value}']: {e}")

    def click_element(self, *element) -> None:
        try:
            element = " ".join(element)
            response = get_xpath(self.get_body_html(), element)
            xpath = response["xpath"]
            self.xpaths.append(xpath)
            print(f"Extracted XPath: {xpath}")

            if "href" in xpath:
                match = re.search(r"@href='([^']+)'", xpath)
                if match:
                    link = match.group(1)
                    if link.startswith("/"):
                        base_url = self.driver.current_url.split("/", 3)[:3]
                        base_url = "/".join(base_url)
                        link = urljoin(base_url, link)
                        print(link, base_url)
                    self.open_website(link)
                else:
                    print("No href found in XPath.")
            else:
                element = self.driver.find_element("xpath", xpath)
                element.click()

            print(f"Clicked element: {xpath}")
        except Exception as e:
            print(f"Error clicking element: {e}")

    # def click_element(self, method, value):
    #     """Click an element using different methods (id, class, name, xpath)"""
    #     try:
    #         element = self.driver.find_element(method, value)
    #         element.click()
    #         print(f"Clicked element [{method}='{value}']")
    #     except Exception as e:
    #         print(f"Error clicking element [{method}='{value}']: {e}")

    def press_key(self, key):
        """Simulates pressing a keyboard key in the browser."""

        if key.lower() in key_map:
            webdriver.ActionChains(self.driver).send_keys(
                key_map[key.lower()]).perform()
            print(f"Pressed {key}")
        else:
            print(f"Key '{key}' is not mapped!")

    def get_body_html(self):
        """Returns the raw HTML of the page starting from the <body> tag."""
        body_element = self.driver.find_element(
            "tag name", "body")  # Locate <body> tag
        return body_element.get_attribute("outerHTML")  # Get its HTML content

    def exit_browser(self):
        self.driver.quit()
        print("Browser closed. Exiting CLI.")
        exit()

    def show_help(self):
        print("\nCommands:\n"
              "  open <url>          - Open a website in the current tab\n"
              "  search query        - search in omnibox\n"
              "  newtab <url>        - Open a new tab with a website\n"
              "  click element  - Click an element\n"
              "  type <text> - Type text into an input field\n"
              "  switch <index>      - Switch to a tab (1-based index)\n"
              "  press <key>         - Press a keyboard key\n"
              "  scroll <up/down> <pixels> - Scroll up or down\n"
              "  summary             - Summarize the current page\n"
              "  close               - Close the current tab\n"
              "  exit                - Close browser and exit\n")

    def run(self):
        print("\n🚀 Browser Automation CLI started! Type 'help' for commands.")
        while True:
            cmd = input("\n>>> ").strip().split()
            if not cmd:
                continue

            action = cmd[0].lower()
            args = cmd[1:]

            if action in self.commands:
                try:
                    if args:
                        self.commands[action](*args)
                    else:
                        self.commands[action]()
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    BrowserCLI().run()
