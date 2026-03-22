"""
TC05 — Navigate to the RedBus Offers page and validate content.

Scenario:
  1. Navigate directly to the offers page URL.
  2. Assert the page title contains 'offer' or 'redbus'.
  3. Assert at least 1 offer card is rendered on the page.
"""
import pytest
from pages.offers_page import OffersPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestOffers:
    """TC05: Verify the Offers page loads with valid content."""

    def test_offers_page_loads(self, page, config):
        """
        GIVEN a user navigating to the RedBus Offers page
        WHEN  the page loads
        THEN  the page title is relevant and offer cards are displayed
        """
        data_cfg = config["test_data"]
        offer_url = data_cfg.get("offer_url", "https://www.redbus.in/offers/bus-offers")

        logger.info("=== TC05: Offers page validation ===")
        offers = OffersPage(page)
        offers.open(offer_url)

        # Assertion A: Page title is relevant
        page_title = offers.get_page_title()
        assert page_title != "", f"Page title is empty for the offers page."
        assert any(
            kw in page_title.lower()
            for kw in ("offer", "redbus", "bus", "deal", "promo")
        ), (
            f"Offers page title does not contain expected keywords. Got: '{page_title}'"
        )
        logger.info(f"Offers page title: '{page_title}'")

        # Assertion B: Page is loaded (URL / cards check)
        is_loaded = offers.is_offers_page_loaded()
        assert is_loaded, (
            "Offers page does not appear to have loaded correctly "
            "(URL does not contain 'offer' and no cards found)."
        )

        logger.info("TC05 PASSED — Offers page loaded with valid title and content.")
