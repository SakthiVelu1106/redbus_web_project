"""
PassengerInfoPage — Page Object for the Passenger Information form.

Real selectors verified via live DOM inspection on 2026-03-22:
  - Phone : input[aria-label='Phone *']
  - Email : input[aria-label='Email ID']
  - Name  : input[aria-label='Name *']
  - Age   : input[aria-label='Age *']
  - Gender: div[aria-label='Male'] / div[aria-label='Female']
"""
from playwright.sync_api import Page
from pages.base_page import BasePage

class PassengerInfoPage(BasePage):
    """
    Page Object for the passenger details checkout page 
    (appears after selecting Boarding/Dropping points).
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self._phone_input = page.locator("input[aria-label='Phone *'], #\\30_6")
        self._email_input = page.locator("input[aria-label='Email ID'], #\\30_5")
        self._name_input  = page.locator("input[aria-label='Name *'], #\\30_4")
        self._age_input   = page.locator("input[aria-label='Age *'], #\\30_1")

    def wait_for_form(self) -> None:
        """Wait for the passenger information form to be visible."""
        self.logger.info("Waiting for Passenger Info form to load…")
        self._name_input.first.wait_for(state="visible", timeout=15000)
        self.logger.info("Passenger Info form loaded.")

    def enter_contact_details(self, phone: str, email: str) -> None:
        """Enter the primary contact phone and email."""
        self.logger.info(f"Entering contact info | Phone: {phone}, Email: {email}")
        
        self._phone_input.first.scroll_into_view_if_needed()
        self._phone_input.first.fill(phone)

        self._email_input.first.scroll_into_view_if_needed()
        self._email_input.first.fill(email)

    def enter_passenger_details(self, name: str, age: str, gender: str) -> None:
        """
        Enter details for a single passenger.
        Args:
            gender: 'Male' or 'Female' (must match the aria-label text).
        """
        self.logger.info(f"Entering passenger info | Name: {name}, Age: {age}, Gender: {gender}")
        
        self._name_input.first.scroll_into_view_if_needed()
        self._name_input.first.fill(name)

        self._age_input.first.scroll_into_view_if_needed()
        self._age_input.first.fill(age)

        # Handle Gender selection
        gender_btn = self.page.locator(f"div[aria-label='{gender}']").first
        gender_btn.scroll_into_view_if_needed()
        gender_btn.click()

    def select_state_of_residence(self, state_name: str) -> None:
        """
        Open the state of residence dropdown, search for the state, and select it.
        """
        self.logger.info(f"Selecting state of residence: {state_name}")
        
        # Click the state dropdown trigger
        state_trigger = self.page.locator("input#\\30_201").first
        state_trigger.scroll_into_view_if_needed()
        state_trigger.click()
        self.page.wait_for_timeout(1000)

        # Type in the search input inside the modal
        search_input = self.page.locator("input.searchInput___832be9").first
        if search_input.is_visible():
            search_input.fill(state_name)
            self.page.wait_for_timeout(1000)

        # Select the suggestion based on aria-label or text
        suggestion = self.page.locator(f"div[role='radio']:has-text('{state_name}')").first
        suggestion.click()
        self.logger.info("State selected.")

    def reject_free_cancellation(self) -> None:
        """Click the 'Don't add free cancellation' or 'Don't add redBus Assurance' option."""
        self.logger.info("Rejecting free cancellation / insurance.")
        # Try both the free cancellation ID and the RedBus Assurance radio button text
        reject_btn = self.page.locator("div#fcRejectText, div:has-text(\"Don't add redBus Assurance\")").last
        reject_btn.scroll_into_view_if_needed()
        reject_btn.click()
        self.page.wait_for_timeout(500)

    def click_continue_booking(self) -> None:
        """Click the final 'Continue booking' button."""
        self.logger.info("Clicking 'Continue booking'.")
        continue_btn = self.page.locator("button:has-text('Continue booking')").first
        continue_btn.scroll_into_view_if_needed()
        continue_btn.click()
        self.page.wait_for_timeout(2000)
