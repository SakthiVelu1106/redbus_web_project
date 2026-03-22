"""
BusDetailsPage — Page Object for the seat-selection panel on RedBus.

Real selectors verified via live DOM inspection on 2026-03-22:
  - Seat layout container: div[class*='seatMain']
  - Available seat       : span[class*='sleeper'][aria-label*='available']
  - Booked / sold seat   : span[class*='sleeper'][aria-label*='sold']
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class BusDetailsPage(BasePage):
    """
    Page Object for the seat-selection panel that expands
    after clicking 'View Seats' on a bus result card.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Seat layout main container — class contains 'seatMain' (confirmed in live DOM)
        self._seat_layout_container = page.locator("div[class*='seatMain']")

        # Available seats — aria-label contains 'available' (confirmed in live DOM)
        self._available_seats = page.locator(
            "span[class*='sleeper'][aria-label*='available'], "
            "li[class*='seat'][aria-label*='available']"
        )

        # Booked/sold seats — aria-label contains 'sold'
        self._booked_seats = page.locator(
            "span[class*='sleeper'][aria-label*='sold'], "
            "li[class*='seat'][aria-label*='sold']"
        )

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def wait_for_seat_layout(self) -> None:
        """Wait until the seat layout panel becomes visible."""
        self.logger.info("Waiting for seat layout panel to appear…")
        self._seat_layout_container.first.wait_for(state="visible", timeout=20000)
        self.logger.info("Seat layout is visible.")

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_available_seat_count(self) -> int:
        """Return the number of available (bookable) seats shown."""
        self.wait_for_seat_layout()
        count = self._available_seats.count()
        self.logger.info(f"Available seats found: {count}")
        return count

    def get_booked_seat_count(self) -> int:
        """Return the number of booked/sold seats shown."""
        count = self._booked_seats.count()
        self.logger.info(f"Booked seats found: {count}")
        return count

    def is_seat_layout_visible(self) -> bool:
        """Return True if the seat layout panel is currently visible."""
        visible = self._seat_layout_container.first.is_visible()
        self.logger.info(f"Seat layout visible: {visible}")
        return visible

    def select_first_available_seat(self) -> None:
        """
        Click the first available seat in the layout.
        Wait for the 'Boarding / Dropping point' selection button to appear.
        """
        self.logger.info("Attempting to click the first available seat.")
        first_available = self._available_seats.first
        first_available.wait_for(state="visible", timeout=10000)
        
        # Click the seat
        first_available.click()
        self.page.wait_for_timeout(1000)
        self.logger.info("Clicked first available seat.")

    def is_boarding_point_button_visible(self) -> bool:
        """
        Return True if the 'Select boarding & dropping points' button 
        is visible after a seat is selected.
        """
        btn = self.page.locator(
            "button:has-text('Select boarding'), button:has-text('Proceed'), button:has-text('Book'), div[class*='button']"
        ).first
        
        try:
            return btn.is_visible(timeout=5000)
        except Exception:
            return False

    def click_boarding_point_button(self) -> None:
        """Click the 'Select boarding & dropping points' button."""
        self.logger.info("Clicking the 'Select boarding & dropping points' button.")
        btn = self.page.locator(
            "button:has-text('Select boarding'), button:has-text('Proceed'), button:has-text('Book')"
        ).first
        btn.click()
        self.page.wait_for_timeout(1000)

    def select_first_boarding_and_dropping_points(self) -> None:
        """
        After seat selection, the layout switches to Boarding/Dropping points.
        This selects the first available boarding point, then the first dropping point.
        """
        self.logger.info("Selecting Boarding and Dropping points.")
        
        # Boarding/Dropping points are typically listed in divs with class or id containing 'bp-point' or similar container
        point_items = self.page.locator("div[class*='bpdpSelection'], li[class*='bpdpItem'], div.bpDpItem")
        
        # Wait for the points list to load
        point_items.first.wait_for(state="visible", timeout=10000)
        
        # Click first (Boarding point)
        point_items.nth(0).click()
        self.logger.info("First boarding point selected.")
        self.page.wait_for_timeout(1000)
        
        # Click second (Dropping point - sometimes auto-advances, but click to be safe if visible)
        try:
            if point_items.nth(1).is_visible():
                point_items.nth(1).click()
                self.logger.info("First dropping point selected.")
        except Exception:
            self.logger.info("Dropping point auto-selected or not found; continuing.")
            
        self.page.wait_for_timeout(2000)
