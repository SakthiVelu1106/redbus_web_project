"""
Screenshot utility for the RedBus Automation Framework.
Captures and saves screenshots to the configured directory.
"""
import os
from datetime import datetime
from playwright.sync_api import Page

from utils.logger import get_logger
from utils.config_reader import get_config

logger = get_logger(__name__)


def take_screenshot(page: Page, name: str) -> str:
    """
    Capture a full-page screenshot and save it to the screenshots directory.

    Args:
        page: Playwright Page instance.
        name: Descriptive name for the screenshot file (no extension needed).

    Returns:
        Absolute path to the saved screenshot file.
    """
    config = get_config()
    screenshot_dir = config["reports"]["screenshot_dir"]

    # Ensure directory exists
    os.makedirs(screenshot_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize name: replace spaces and special chars
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)

    try:
        page.screenshot(path=filepath, full_page=True)
        logger.info(f"Screenshot saved: {filepath}")
    except Exception as exc:
        logger.error(f"Failed to capture screenshot '{name}': {exc}")

    return filepath
