"""
HomePage — Page Object for the RedBus main/home page.
URL: https://www.redbus.in

Real selectors verified via live DOM inspection on 2026-03-22.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for the RedBus home page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Source city input  — id="srcinput" confirmed in live DOM
        self._source_input = page.locator("input#srcinput")

        # Destination city input — id="destinput" confirmed in live DOM
        self._destination_input = page.locator("input#destinput")

        # Date of Journey field — aria-label confirmed in live DOM
        self._date_picker = page.locator('div[aria-label*="Select Date of Journey"]')

        # Calendar date cells — class "calendarDate" confirmed in live DOM
        # aria-label format: "Monday, March 30, 2026"
        self._calendar = page.locator("div.calendarDate")

        # Search Buses button — id="search_button" confirmed in live DOM
        self._search_button = page.locator("button#search_button")

        # Autocomplete suggestion items — role="option" confirmed in live DOM
        self._suggestions = page.locator('div[role="option"]')

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self, base_url: str) -> None:
        """Navigate to the RedBus home page."""
        self.navigate(base_url)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1500)
        self.logger.info("Home page opened.")
        # Close any app-install banner or cookie popup
        self._dismiss_overlays()

    def _dismiss_overlays(self) -> None:
        """Silently dismiss any overlay banners/headers that may block interactions."""
        # Try to close the "Get 10% Discount / Install App" banner at top
        selectors = [
            'span.icon-close',
            'button[aria-label="Close"]',
            '[data-testid="close-button"]',
            'div.close-btn',
        ]
        for sel in selectors:
            try:
                btn = self.page.locator(sel).first
                if btn.is_visible(timeout=1000):
                    btn.click()
                    self.page.wait_for_timeout(500)
                    self.logger.info(f"Dismissed overlay: {sel}")
                    break
            except Exception:
                pass

        # Scroll to the search bar to ensure it is in view and not hidden behind header
        try:
            self._source_input.scroll_into_view_if_needed()
        except Exception:
            pass

    def enter_source_city(self, city: str) -> None:
        """
        Click the source field, clear it, type city name and
        select the first autocomplete suggestion.
        """
        self.logger.info(f"Entering source city: {city}")

        # Scroll input into view and click with force to bypass any overlay
        self._source_input.wait_for(state="visible", timeout=15000)
        self._source_input.scroll_into_view_if_needed()
        self._source_input.click(force=True)
        self._source_input.press("Control+a")
        self._source_input.press("Delete")
        self.page.wait_for_timeout(300)
        self._source_input.type(city, delay=150)
        self.page.wait_for_timeout(1500)

        # Click first autocomplete suggestion
        suggestion = self.page.locator(
            "li.suggestion-item, div[role='option']"
        ).first
        suggestion.wait_for(state="visible", timeout=15000)
        suggestion.click()
        self.logger.info(f"Source city selected: {city}")
        self.page.wait_for_timeout(500)

    def enter_destination_city(self, city: str) -> None:
        """
        Click the destination field, clear it, type city name and
        select the first autocomplete suggestion.
        """
        self.logger.info(f"Entering destination city: {city}")

        # Wait for input to be available then click it directly
        self._destination_input.wait_for(state="visible", timeout=15000)
        self._destination_input.click()
        self._destination_input.press("Control+a")
        self._destination_input.press("Delete")
        self.page.wait_for_timeout(300)
        self._destination_input.type(city, delay=150)
        self.page.wait_for_timeout(1500)

        # Click first autocomplete suggestion
        suggestion = self.page.locator(
            "li.suggestion-item, div[role='option']"
        ).first
        suggestion.wait_for(state="visible", timeout=15000)
        suggestion.click()
        self.logger.info(f"Destination city selected: {city}")
        self.page.wait_for_timeout(500)

    def select_date(self, travel_date: str) -> None:
        """
        Select a travel date from the calendar picker.

        Args:
            travel_date: Date string in 'DD Mon YYYY' format, e.g. '30 Mar 2026'.
                         Internally converted to match aria-label like 'March 30, 2026'.
        """
        self.logger.info(f"Selecting travel date: {travel_date}")

        # Open the date picker
        self._date_picker.click()
        self.page.wait_for_timeout(500)

        # Parse "30 Mar 2026" → "March 30" for aria-label matching
        parts = travel_date.split()  # ['30', 'Mar', '2026']
        month_map = {
            "Jan": "January", "Feb": "February", "Mar": "March",
            "Apr": "April",   "May": "May",      "Jun": "June",
            "Jul": "July",    "Aug": "August",   "Sep": "September",
            "Oct": "October", "Nov": "November", "Dec": "December",
        }
        full_month = month_map.get(parts[1], parts[1])
        day = parts[0]
        year = parts[2]

        # aria-label on date cells: "Monday, March 30, 2026"
        date_cell = self.page.locator(
            f'div.calendarDate[aria-label*="{full_month} {day}, {year}"]'
        ).first

        date_cell.wait_for(state="visible", timeout=10000)
        date_cell.scroll_into_view_if_needed()
        date_cell.click()
        self.logger.info(f"Travel date selected: {travel_date}")

    def click_search(self) -> None:
        """Click the 'Search Buses' button and wait for navigation."""
        self.logger.info("Clicking Search button.")
        # Try multiple possible selectors for the search button
        search_btn = self.page.locator(
            "button#search_button, button:has-text('Search buses'), button:has-text('Search Buses')"
        ).first
        search_btn.scroll_into_view_if_needed()
        search_btn.wait_for(state="visible", timeout=15000)
        search_btn.click(force=True)
        # Wait for the results page to start loading
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)
        self.logger.info("Search submitted successfully.")
