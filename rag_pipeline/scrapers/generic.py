from bs4 import BeautifulSoup

from rag_pipeline.scrapers.base import BaseScraper


class GenericScraper(BaseScraper):
    """Generic scraper for websites without special requirements"""

    def cleanup_html(self, html):
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "iframe",
                "header",
                "footer",
                "nav",
                "form",
                "input",
            ]
        ):
            tag.decompose()

        # remove useless spans and divs
        for tag in soup.find_all(["span", "div"]):
            if not tag.attrs:
                tag.unwrap()

        for tag in soup.find_all():
            if tag.name not in ["br", "img"] and not tag.get_text(strip=True):
                tag.decompose()

        cleaned_text = soup.prettify()
        cleaned_text = " ".join(cleaned_text.split())

        return cleaned_text


if __name__ == "__main__":
    URL = "https://www.expat.hsbc.com/expat-explorer/expat-guides/spain/tax-in-spain/"
    DESTINATION = "output.pdf"
    GenericScraper().scrape(URL, DESTINATION)
