import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from src.core.browser import Browser


class BrowserTests(unittest.IsolatedAsyncioTestCase):
    async def test_context_manager_launches_browser_and_closes_resources(self) -> None:
        page = object()
        playwright = MagicMock()
        playwright.chromium.launch = AsyncMock()
        playwright.stop = AsyncMock()

        launched_browser = MagicMock()
        launched_browser.new_page = AsyncMock(return_value=page)
        launched_browser.close = AsyncMock()
        playwright.chromium.launch.return_value = launched_browser

        with patch(
            "src.core.browser._start_playwright",
            new=AsyncMock(return_value=playwright),
        ):
            async with Browser(headless=False) as browser:
                self.assertIs(await browser.new_page(), page)

        playwright.chromium.launch.assert_awaited_once_with(headless=False)
        launched_browser.new_page.assert_awaited_once_with()
        launched_browser.close.assert_awaited_once_with()
        playwright.stop.assert_awaited_once_with()


if __name__ == "__main__":
    unittest.main()
