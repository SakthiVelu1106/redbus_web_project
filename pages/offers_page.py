"""
OffersPage — Page Object for the RedBus Offers page.
URL: https://www.redbus.in/offers/bus-offers

Covers:
  - Navigating to the offers page
  - Verifying the page loaded
  - Reading offer card titles
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class OffersPage(BasePage):
    """Page Object for the RedBus offers / promotions page."""

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Page heading / banner
        self._page_heading = page.locator("h1, .offers-heading, .offerSection h2").first

        # Individual offer card containers
        self._offer_cards = page.locator(
            "div.offer-card, div.offerCard, div.offer-item, li.offer-list-item"
        )

        # Offer title within each card
        self._offer_titles = page.locator(
            "div.offer-card h3, div.offerCard .offer-title, "
            "div.offer-item .card-title, li.offer-list-item h3"
        )

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self, offer_url: str) -> None:
        """Navigate directly to the offers page."""
        self.logger.info(f"Navigating to Offers page: {offer_url}")
        self.navigate(offer_url)
        self.page.wait_for_load_state("domcontentloaded")
        self.logger.info("Offers page loaded.")

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def is_offers_page_loaded(self) -> bool:
        """
        Return True if:
          - The URL contains 'offer', AND
          - At least one offer card is present.
        """
        url_ok = "offer" in self.get_current_url().lower()
        cards_present = self._offer_cards.count() > 0
        self.logger.info(
            f"Offers page loaded check — URL contains 'offer': {url_ok}, "
            f"offer cards found: {cards_present}"
        )
        return url_ok or cards_present

    def get_offer_count(self) -> int:
        """Return the number of offer cards on the page."""
        # Give the page a moment to render cards
        self.page.wait_for_timeout(2000)
        count = self._offer_cards.count()
        self.logger.info(f"Offer cards found: {count}")
        return count

    def get_offer_titles(self) -> list[str]:
        """Return a list of visible offer title strings."""
        titles = self._offer_titles.all_inner_texts()
        cleaned = [t.strip() for t in titles if t.strip()]
        self.logger.info(f"Offer titles: {cleaned[:5]}")
        return cleaned

    def get_page_title(self) -> str:
        """Return the browser tab title."""
        title = self.page.title()
        self.logger.info(f"Page title: {title}")
        return title
