import pytest
from obsidian_boy.web_scraper import WebScraper
from unittest.mock import patch, Mock
from requests.exceptions import RequestException

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.text = """
    <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="This is a test page">
            <meta property="og:title" content="Open Graph Test Title">
        </head>
        <body>
            <h1>Welcome to the Test Page</h1>
            <p>This is some test content.</p>
        </body>
    </html>
    """
    mock.apparent_encoding = 'utf-8'
    return mock

def test_web_scraper(mock_response):
    with patch('requests.get', return_value=mock_response):
        scraper = WebScraper("https://example.com")
        result = scraper.scrape()

    assert "Welcome to the Test Page" in result
    assert "This is some test content" in result

def test_web_scraper_error():
    with patch('requests.get', side_effect=RequestException("Test error")):
        scraper = WebScraper("https://example.com")
        result = scraper.scrape()

    assert "Error scraping https://example.com" in result
    assert "Test error" in result

def test_web_scraper_no_url():
    scraper = WebScraper()
    with pytest.raises(ValueError):
        scraper.scrape()

def test_extract_title(mock_response):
    with patch('requests.get', return_value=mock_response):
        scraper = WebScraper("https://example.com")
        scraper.scrape()  # This will populate the soup object
        title = scraper._extract_title(scraper.soup)
    
    assert title == "Test Page"

def test_extract_metadata(mock_response):
    with patch('requests.get', return_value=mock_response):
        scraper = WebScraper("https://example.com")
        scraper.scrape()  # This will populate the soup object
        metadata = scraper._extract_metadata(scraper.soup)
    
    assert metadata['description'] == "This is a test page"
    assert metadata['og:title'] == "Open Graph Test Title"
