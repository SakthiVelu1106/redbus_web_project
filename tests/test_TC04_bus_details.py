"""
TC04 — Open bus details / seat selection panel.

Scenario:
  1. Open home page and perform search (Hyderabad → Bangalore).
  2. Wait for results to load.
  3. Click 'View Seats' on the first bus.
  4. Assert the seat layout panel becomes visible.
  5. Assert at least 1 available seat is shown.
  6. Click an available seat (verifies interaction works).
"""
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.bus_details_page import BusDetailsPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestBusDetails:
    """TC04: Verify the seat selection panel opens and a seat can be selected."""

    def test_view_seats_panel_opens(self, page, config):
        """
        GIVEN a list of bus search results
        WHEN  'View Seats' is clicked on the first result
        THEN  the seat layout panel is visible and has at least 1 available seat
        AND   a seat can be selected (clicked)
        """
        app_cfg  = config["application"]
        data_cfg = config["test_data"]

        # Step 1 — Navigate to home and perform search
        home = HomePage(page)
        home.open(app_cfg["base_url"])

        logger.info("=== TC04: Open bus details / seat selection ===")
        home.enter_source_city(data_cfg["source_city"])
        home.enter_destination_city(data_cfg["destination_city"])
        home.select_date(data_cfg["travel_date"])
        home.click_search()

        # Step 2 — Wait for results
        results = SearchResultsPage(page)
        results.wait_for_results()

        # Step 3 — Click View Seats on first bus
        results.click_view_seats_on_first_bus()

        # Step 4 — Assert seat layout visible
        bus_details = BusDetailsPage(page)
        bus_details.wait_for_seat_layout()

        assert bus_details.is_seat_layout_visible(), (
            "Seat layout panel did not become visible after clicking 'View Seats'."
        )
        logger.info("✓ Seat layout panel is visible.")

        # Step 5 — Assert available seats exist
        available = bus_details.get_available_seat_count()
        assert available > 0, (
            f"Expected at least 1 available seat, but found {available}."
        )
        logger.info(f"✓ TC04: Found {available} available seats.")

        # Step 6 — Click an available seat (verifies the seat click interaction)
        bus_details.select_first_available_seat()
        logger.info("✓ TC04 PASSED — Seat layout opened and seat clicked successfully.")
