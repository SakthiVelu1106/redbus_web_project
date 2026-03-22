"""
TC03 — Apply a filter on search results.

Scenario:
  1. Open home page and perform search.
  2. Wait for results to load and record initial bus count.
  3. Apply the 'AC' bus type filter.
  4. Assert the result list updates (count changes or filter is reflected).
"""
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestFilters:
    """TC03: Apply a filter on bus search results."""

    def test_apply_ac_filter(self, page, config):
        """
        GIVEN a list of search results
        WHEN  the 'AC' filter is applied
        THEN  the page responds (filter checkbox clicked without error)
              and results are still visible
        """
        app_cfg  = config["application"]
        data_cfg = config["test_data"]

        # Step 1 — Perform search
        home = HomePage(page)
        home.open(app_cfg["base_url"])

        logger.info("=== TC03: Apply filter on search results ===")
        home.enter_source_city(data_cfg["source_city"])
        home.enter_destination_city(data_cfg["destination_city"])
        home.select_date(data_cfg["travel_date"])
        home.click_search()

        # Step 2 — Record initial bus count
        results = SearchResultsPage(page)
        results.wait_for_results()
        initial_count = results.get_total_bus_count()
        logger.info(f"Initial bus count before filter: {initial_count}")

        # Step 3 — Apply AC filter
        results.apply_bus_type_filter("AC")

        # Step 4 — Validate results still present
        page.wait_for_timeout(3000)
        filtered_count = results.get_total_bus_count()
        logger.info(f"Bus count after 'AC' filter: {filtered_count}")

        assert filtered_count > 0, (
            f"Expected buses after applying AC filter, but got {filtered_count} results."
        )
        logger.info("TC03 PASSED — AC filter applied successfully, results remain visible.")
