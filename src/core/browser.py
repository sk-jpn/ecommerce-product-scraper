from types import TracebackType

from playwright.sync_api import Browser as PlaywrightBrowser
from playwright.sync_api import Page, Playwright, sync_playwright


class Browser:
    """Manage the lifecycle of a Playwright Chromium browser."""

    def __init__(self, *, headless: bool = True) -> None:
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: PlaywrightBrowser | None = None
        self._page: Page | None = None

    def start(self) -> Page:
        if self._page is not None:
            return self._page

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._page = self._browser.new_page()
        return self._page

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("Browser has not been started")
        return self._page

    def close(self) -> None:
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()

        self._page = None
        self._browser = None
        self._playwright = None

    def __enter__(self) -> "Browser":
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
