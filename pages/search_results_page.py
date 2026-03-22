"""
SearchResultsPage — Page Object for the RedBus bus search results page.

Real selectors verified via live DOM inspection on 2026-03-22:
  - Bus cards     : li.tupleWrapper (class contains 'tupleWrapper')
  - Bus name      : div[class*='travels']  inside card
  - Count label   : span[class*='totalBuses']
  - View Seats btn: button[class*='viewSeatsBtn']
  - Filters       : div[aria-label^='AC'], div[aria-label^='NONAC']
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """Page Object for the bus search results listing page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Each bus result card — confirmed: li elements with class containing 'tupleWrapper'
        self._bus_items = page.locator("li[class*='tupleWrapper']")

        # Bus operator name inside each card — class contains 'travels'
        self._bus_names = page.locator("li[class*='tupleWrapper'] div[class*='travels']")

        # Total buses count label — class contains 'totalBuses'
        self._result_count_label = page.locator("span[class*='totalBuses']")

        # Filter section container (aside on the left side)
        self._filter_section = page.locator("aside[class*='filterSection']")

        # AC filter label — confirmed aria-label="AC" in live DOM
        self._ac_filter = page.locator("div[aria-label='AC']")

        # Non-AC filter label
        self._nonac_filter = page.locator("div[aria-label='NONAC']")

    # ------------------------------------------------------------------
    # Page State
    # ------------------------------------------------------------------

    def wait_for_results(self) -> None:
        """Wait until at least one bus card is rendered on the page."""
        self.logger.info("Waiting for search results to load…")
        self._bus_items.first.wait_for(state="visible", timeout=30000)
        self.logger.info("Search results loaded.")

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_bus_count_text(self) -> str:
        """
        Return the text of the result count label.
        Example: '42 Buses'
        """
        self._result_count_label.first.wait_for(state="visible", timeout=20000)
        text = self._result_count_label.first.inner_text().strip()
        self.logger.info(f"Result count label: '{text}'")
        return text

    def get_total_bus_count(self) -> int:
        """Return the number of bus cards currently visible on the page."""
        count = self._bus_items.count()
        self.logger.info(f"Visible bus cards: {count}")
        return count

    def get_all_bus_names(self) -> list[str]:
        """Return a list of all visible bus operator names."""
        self.wait_for_results()
        names = self._bus_names.all_inner_texts()
        self.logger.info(f"Bus names retrieved ({len(names)} total): {names[:5]}")
        return names

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def apply_bus_type_filter(self, filter_label: str) -> None:
        """
        Click a filter by aria-label.

        Args:
            filter_label: 'AC' or 'NONAC' (as confirmed in live DOM).
        """
        self.logger.info(f"Applying filter: '{filter_label}'")
        filter_el = self.page.locator(f"div[aria-label='{filter_label}']").first
        filter_el.wait_for(state="visible", timeout=10000)
        filter_el.scroll_into_view_if_needed()
        filter_el.click()
        self.page.wait_for_timeout(2000)
        self.logger.info(f"Filter '{filter_label}' applied.")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def click_view_seats_on_first_bus(self) -> None:
        """
        Click the 'View Seats' button on the first individual bus result.
        Scrolls down to find the first visible viewSeatsBtn button.
        """
        self.logger.info("Looking for 'View Seats' button on first bus result.")
        self.wait_for_results()

        # Scroll down a bit to get past any promo/header banners
        self.page.mouse.wheel(0, 400)
        self.page.wait_for_timeout(1000)

        # Find the first "View Seats" button anywhere on the page
        view_seats_btn = self.page.locator(
            "button[class*='viewSeatsBtn'], button:has-text('VIEW SEATS'), button:has-text('View Seats')"
        ).first

        # Scroll it into view and click
        view_seats_btn.scroll_into_view_if_needed()
        view_seats_btn.wait_for(state="visible", timeout=15000)
        view_seats_btn.click(force=True)
        self.page.wait_for_timeout(1500)
        self.logger.info("'View Seats' clicked on first bus.")

