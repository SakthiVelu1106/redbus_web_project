"""
TC02 — Validate search results returned for a bus route.

Scenario:
  1. Open home page.
  2. Perform a valid city-to-city search.
  3. Wait for results to load.
  4. Assert the 'X Buses' label is visible.
  5. Assert at least 1 bus card is displayed.
  6. Assert all visible bus names are non-empty strings.
"""
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestSearchResults:
    """TC02: Validate search results are correctly returned."""

    def test_search_results_are_displayed(self, page, config):
        """
        GIVEN a search for Hyderabad → Bangalore on a future date
        WHEN  results load
        THEN  the bus count label shows, at least 1 bus card exists,
              and every bus name is non-empty
        """
        app_cfg  = config["application"]
        data_cfg = config["test_data"]

        # Step 1 — Perform search via home page
        home = HomePage(page)
        home.open(app_cfg["base_url"])

        logger.info("=== TC02: Validate search results ===")
        home.enter_source_city(data_cfg["source_city"])
        home.enter_destination_city(data_cfg["destination_city"])
        home.select_date(data_cfg["travel_date"])
        home.click_search()

        # Step 2 — Validate results page
        results = SearchResultsPage(page)
        results.wait_for_results()

        # Assertion A: Result count label is present and non-empty
        count_text = results.get_bus_count_text()
        assert count_text != "", (
            "Bus count label is empty — results may not have loaded."
        )
        logger.info(f"Result count label: '{count_text}'")

        # Assertion B: At least 1 bus card visible
        visible_buses = results.get_total_bus_count()
        assert visible_buses > 0, (
            f"Expected at least 1 bus card, but found {visible_buses}."
        )
        logger.info(f"Visible bus cards: {visible_buses}")

        # Assertion C: All bus names are non-empty
        names = results.get_all_bus_names()
        assert len(names) > 0, "No bus operator names were found."
        for name in names:
            assert name.strip() != "", f"Empty bus name found in results: {names}"

        logger.info("TC02 PASSED — Search results validated successfully.")
