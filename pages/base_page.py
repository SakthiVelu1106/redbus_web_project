"""
BasePage — Abstract base class for all Page Object classes.

Encapsulates common Playwright interactions so page classes
don't repeat boilerplate, and all element interactions are
logged uniformly.
"""
from playwright.sync_api import Page, Locator, expect
from utils.logger import get_logger


class BasePage:
    """
    Base class providing reusable helper methods for all page objects.

    Attributes:
        page    : Playwright Page instance
        logger  : Named logger for the subclass
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, url: str) -> None:
        """Navigate to the given URL and wait until network is idle."""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    # ------------------------------------------------------------------
    # Element interactions
    # ------------------------------------------------------------------

    def click(self, locator: Locator, description: str = "") -> None:
        """Click an element after waiting for it to be visible."""
        label = description or str(locator)
        self.logger.info(f"Clicking: {label}")
        locator.wait_for(state="visible")
        locator.click()

    def fill(self, locator: Locator, text: str, description: str = "") -> None:
        """Clear and fill an input element."""
        label = description or str(locator)
        self.logger.info(f"Filling '{text}' into: {label}")
        locator.wait_for(state="visible")
        locator.click()
        locator.clear()
        locator.fill(text)

    def get_text(self, locator: Locator) -> str:
        """Return the trimmed inner text of an element."""
        locator.wait_for(state="visible")
        text = locator.inner_text().strip()
        self.logger.debug(f"Got text: '{text}'")
        return text

    def is_visible(self, locator: Locator) -> bool:
        """Return True if the element is currently visible."""
        return locator.is_visible()

    def wait_for_visible(self, locator: Locator, timeout: int = 15000) -> None:
        """Explicitly wait for an element to become visible."""
        locator.wait_for(state="visible", timeout=timeout)

    def get_count(self, locator: Locator) -> int:
        """Return the number of elements matching the locator."""
        count = locator.count()
        self.logger.debug(f"Element count: {count}")
        return count

    def scroll_into_view(self, locator: Locator) -> None:
        """Scroll element into the viewport."""
        locator.scroll_into_view_if_needed()

    # ------------------------------------------------------------------
    # Assertions (thin wrappers around Playwright's expect)
    # ------------------------------------------------------------------

    def assert_visible(self, locator: Locator, timeout: int = 15000) -> None:
        """Assert the element is visible within the timeout."""
        expect(locator).to_be_visible(timeout=timeout)

    def assert_url_contains(self, fragment: str) -> None:
        """Assert the current URL contains the given fragment."""
        expect(self.page).to_have_url(f".*{fragment}.*", timeout=20000)

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.page.url
