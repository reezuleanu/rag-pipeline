from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright


class BaseScraper(ABC):
    """Base Scraper interface, to be used as a blueprint to make concrete
    scrapers."""

    def scrape(self, url: str, destination: str, wait: int = None) -> str:
        """Scrape a given url and return the path to the resulted pdf

        Args:
            url (str): the url to scrape
            destination (str): output path

        Returns:
            str: path of output
        """

        html = self.url_to_html(url, wait)

        if not html:
            raise Exception(f"{url} download attempts resulted in an empty page")

        cleaned_html = self.cleanup_html(html)

        if not cleaned_html:
            raise Exception(f"{url} is empty after html cleanup")

        return self.html_to_pdf(cleaned_html, destination)

    def url_to_html(self, url: str, wait: int = None) -> str:
        """Download the content of a website as html

        Args:
            url (str): url to download
            wait (float): milliseconds to wait for the page to load
            ( useful for pages using react )

        Returns:
            str: downloaded html
        """

        with sync_playwright() as scraper:
            browser = scraper.chromium

            context = browser.launch(headless=True).new_context()
            page = context.new_page()
            page.wait_for_load_state()

            page.goto(url, wait_until="domcontentloaded")

            if wait:
                page.wait_for_timeout()

            return page.content()

    def html_to_pdf(self, html: str, destination: str) -> str:
        """Render html as a pdf file

        Args:
            html (str): html to render
            destination (str): pdf path

        Returns:
            str: pdf path
        """

        with sync_playwright() as playwright:
            context = playwright.chromium.launch(headless=True)

            page = context.new_page()
            page.set_content(html)

            page.pdf(path=destination)

        return destination

    @abstractmethod
    def cleanup_html(self, html: str) -> str:
        """Scraper specific logic to cleanup the html from a given
        website

        Args:
            html (str): html to clean up

        Returns:
            str: cleaned up html
        """
        raise NotImplementedError
