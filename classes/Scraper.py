from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import gc

class FlightScraper:
    def __init__(self):
        """
        Initialize the FlightScraper.

        Sets up undetected Chrome WebDriver to avoid bot detection.
        """

        # Set up Chrome driver options
        options = uc.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-sync')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--mute-audio')
        options.add_argument('--no-first-run')
        options.add_argument('--safebrowsing-disable-auto-update')
        options.add_argument('--disable-backgrounding-occluded-windows')

        # Initialize undetected Chrome driver
        self.driver = uc.Chrome(options=options, version_main=144)

        # Set page load timeout (30 seconds)
        self.driver.set_page_load_timeout(30)

    def close(self):
        """
        Close the Chrome WebDriver.
        """
        if self.driver:
            self.driver.quit()

    def scrape_azul(self, url: str, date: str) -> str:
        """
        Scrape points value from Azul website.

        Args:
            url: The Azul URL to scrape.
            date: The date being checked (for logging purposes).

        Returns:
            The points value found, or None if not found.
        """
        delay = 20

        print(f'Scraping URL for date {date}:', url)

        try:
            self.driver.get(url)

            # CSS selector for the points element
            css_selector = '#FlightClassTypePrice-selectBusiness > div > div > div > div.pointsPlusMoneyContainer > div > div.cardLabelPointsPlusMoney > div.labelValuePoints'

            # Wait for the element to be present
            element = WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

            print(f"Element found for {date}! Text: {element.text}")

            # Small pause to let Chrome breathe
            sleep(0.5)

            return element.text

        except TimeoutException:
            print(f"------------- Loading took too much time or element not found for {date}! -------------")
            return None
        except NoSuchElementException:
            print(f"------------- Element not found for {date} -------------")
            return None
        except WebDriverException as e:
            if 'receiving message from renderer' in str(e):
                print(f"------------- Chrome renderer timeout for {date} - skipping -------------")
            else:
                print(f"------------- WebDriver error for {date}: {str(e)[:100]} -------------")
            return None
        except Exception as e:
            print(f"------------- Unexpected error for {date}: {str(e)[:100]} -------------")
            return None
