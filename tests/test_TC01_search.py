"""
TC01 — Search for a bus between two cities.

Scenario:
  1. Open the RedBus home page.
  2. Enter source and destination cities from config.
  3. Select the travel date.
  4. Click the Search button.
  5. Assert the browser URL changes to the search results page.
"""
import pytest
from pages.home_page import HomePage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestSearch:
    """TC01: Verify the bus search feature works end-to-end."""

    def test_search_navigates_to_results(self, page, config):
        """
        GIVEN a user on the RedBus home page
        WHEN  they enter valid source, destination and date and click Search
        THEN  the browser navigates to the search results page
        """
        app_cfg  = config["application"]
        data_cfg = config["test_data"]

        home = HomePage(page)
        home.open(app_cfg["base_url"])

        logger.info("=== TC01: Search for buses ===")
        home.enter_source_city(data_cfg["source_city"])
        home.enter_destination_city(data_cfg["destination_city"])
        home.select_date(data_cfg["travel_date"])
        home.click_search()

        # Assertion: URL should now contain the route fragment
        current_url = home.get_current_url()
        logger.info(f"Current URL after search: {current_url}")

        assert "travels" in current_url.lower() or "bus-tickets" in current_url.lower(), (
            f"Expected search results URL, but got: {current_url}"
        )
        logger.info("TC01 PASSED — URL navigated to search results page.")
