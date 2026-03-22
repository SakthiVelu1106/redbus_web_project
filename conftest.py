"""
conftest.py — Root-level Pytest fixtures and hooks for the RedBus automation framework.

Provides:
  - config      : Loaded YAML configuration dict
  - browser_ctx : Playwright BrowserContext (one per test)
  - page        : Playwright Page (one per test, auto-closes after test)
  - Screenshot-on-failure hook via pytest_runtest_makereport
"""
import os
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from utils.config_reader import get_config
from utils.logger import get_logger
from utils.screenshot import take_screenshot

logger = get_logger("conftest")

# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def config() -> dict:
    """Load and return the YAML configuration (cached for the entire session)."""
    cfg = get_config()
    logger.info("Configuration loaded successfully.")
    return cfg


@pytest.fixture(scope="session")
def playwright_instance():
    """Start a single Playwright instance for the entire test session."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance, config) -> Browser:
    """
    Launch a browser for the whole session based on config.
    Supported browsers: chromium (+ channel: chrome/msedge), firefox, webkit.
    """
    app_cfg = config["application"]
    browser_name: str = app_cfg.get("browser", "chromium").lower()
    headless: bool = app_cfg.get("headless", False)
    slow_mo: int = app_cfg.get("slow_mo", 150)
    channel: str = app_cfg.get("channel", "")  # e.g. "chrome", "msedge"

    launch_kwargs = dict(headless=headless, slow_mo=slow_mo)
    if channel:
        launch_kwargs["channel"] = channel

    logger.info(f"Launching browser: {browser_name} channel={channel or 'default'} | headless={headless}")

    browser_launcher = getattr(playwright_instance, browser_name)
    _browser = browser_launcher.launch(**launch_kwargs)
    yield _browser
    logger.info("Closing browser.")
    _browser.close()


# ---------------------------------------------------------------------------
# Function-scoped fixtures (fresh context + page per test)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def browser_ctx(browser, config) -> BrowserContext:
    """Create a fresh BrowserContext for every test."""
    app_cfg = config["application"]
    ctx = browser.new_context(
        viewport={
            "width": app_cfg.get("viewport_width", 1920),
            "height": app_cfg.get("viewport_height", 1080),
        }
    )
    ctx.set_default_timeout(app_cfg.get("timeout", 30000))
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(browser_ctx) -> Page:
    """Open a new Page within the browser context for each test."""
    _page = browser_ctx.new_page()
    logger.info(f"New page opened for test.")
    yield _page
    logger.info("Closing page after test.")
    _page.close()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically capture a screenshot when any test FAILS.
    The screenshot filename includes the test name and timestamp.
    """
    outcome = yield
    report = outcome.get_result()

    # Only act on the 'call' phase (the actual test body), not setup/teardown
    if report.when == "call" and report.failed:
        # Retrieve the 'page' fixture from the test's fixtures if available
        page_fixture: Page | None = item.funcargs.get("page")
        if page_fixture is not None:
            test_name = item.name
            logger.error(f"Test FAILED: {test_name} — capturing screenshot.")
            take_screenshot(page_fixture, f"FAILED_{test_name}")
        else:
            logger.warning(
                f"Test FAILED: {item.name} — no 'page' fixture found; skipping screenshot."
            )
