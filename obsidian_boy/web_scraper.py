import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional
import markdownify

class WebScraper:
    name: str = "Read website content"
    description: str = "A tool that can be used to read a website content."

    def __init__(self, website_url: Optional[str] = None, cookies: Optional[dict] = None):
        self.website_url = website_url
        self.cookies = cookies
        self.soup: Optional[BeautifulSoup] = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        if website_url:
            self.description = f"A tool that can be used to read {website_url}'s content."

    def scrape(self, url: Optional[str] = None) -> str:
        """
        Scrape content from a given URL and convert it to Markdown.

        Args:
            url (Optional[str]): The URL to scrape. If not provided, uses the instance's website_url.

        Returns:
            str: The extracted text content from the webpage converted to Markdown.
        """
        website_url = url or self.website_url
        if not website_url:
            raise ValueError("No URL provided for scraping.")

        try:
            page = requests.get(
                website_url,
                timeout=15,
                headers=self.headers,
                cookies=self.cookies or {}
            )
            page.raise_for_status()
            page.encoding = page.apparent_encoding
            self.soup = BeautifulSoup(page.text, "html.parser")
            
            # Convert the scraped HTML content to Markdown
            markdown_content = markdownify.markdownify(str(self.soup))
            
            return markdown_content
        except requests.RequestException as e:
            logging.error(f"Error scraping {website_url}: {str(e)}")
            return f"Error scraping {website_url}: {str(e)}"

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the title of the page."""
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else ''

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from the page."""
        metadata = {}
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property')
            if name:
                content = tag.get('content')
                if content:
                    metadata[name] = content
        return metadata
