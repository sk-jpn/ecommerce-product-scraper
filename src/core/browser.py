from types import TracebackType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser as PlaywrightBrowser
    from playwright.async_api import Page, Playwright


async def _start_playwright() -> "Playwright":
    from playwright.async_api import async_playwright

    return await async_playwright().start()


class Browser:
    """Manage the lifecycle of an asynchronous Playwright browser."""

    def __init__(self, *, headless: bool = True) -> None:
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: PlaywrightBrowser | None = None

    async def start(self) -> None:
        if self._browser is not None:
            return

        self._playwright = await _start_playwright()
        try:
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless
            )
        except BaseException:
            await self.close()
            raise

    async def new_page(self) -> "Page":
        if self._browser is None:
            raise RuntimeError("Browser has not been started")
        return await self._browser.new_page()

    async def close(self) -> None:
        try:
            if self._browser is not None:
                await self._browser.close()
        finally:
            self._browser = None
            try:
                if self._playwright is not None:
                    await self._playwright.stop()
            finally:
                self._playwright = None

    async def __aenter__(self) -> "Browser":
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
