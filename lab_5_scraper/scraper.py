"""
Crawler implementation.
"""

# pylint: disable=too-many-arguments, too-many-instance-attributes, unused-import, undefined-variable, unused-argument
import datetime
import json
import pathlib
import re
import shutil
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from core_utils.article.article import Article
from core_utils.article.io import to_meta, to_raw
from core_utils.config_dto import ConfigDTO
from core_utils.constants import ASSETS_PATH, CRAWLER_CONFIG_PATH

ILIBRARY_BASE_URL = "https://ilibrary.ru"


class IncorrectSeedURLError(Exception):
    """
    Seed URL does not match standard pattern.
    """


class NumberOfArticlesOutOfRangeError(Exception):
    """
    Total number of articles is out of range from 1 to 150.
    """


class IncorrectNumberOfArticlesError(Exception):
    """
    Total number of articles to parse is not integer or less than 0.
    """


class IncorrectHeadersError(Exception):
    """
    Headers are not in a form of dictionary.
    """


class IncorrectEncodingError(Exception):
    """
    Encoding must be specified as a string.
    """


class IncorrectTimeoutError(Exception):
    """
    Timeout value must be a positive integer less than 60.
    """


class IncorrectVerifyError(Exception):
    """
    Verify certificate and headless mode values must be True or False.
    """


class Config:
    """
    Class for unpacking and validating configurations.
    """

    def __init__(self, path_to_config: pathlib.Path) -> None:
        """
        Initialize an instance of the Config class.

        Args:
            path_to_config (pathlib.Path): Path to configuration.
        """
        self.path_to_config = path_to_config
        self._validate_config_content()
        config_values = self._extract_config_content()

        self._seed_urls = config_values.seed_urls
        self._num_articles = config_values.total_articles
        self._headers = config_values.headers
        self._encoding = config_values.encoding
        self._timeout = config_values.timeout
        self._should_verify_certificate = config_values.should_verify_certificate
        self._headless_mode = config_values.headless_mode

    def _extract_config_content(self) -> ConfigDTO:
        """
        Get config values.

        Returns:
            ConfigDTO: Config values
        """
        with open(self.path_to_config, encoding="utf-8") as config_file:
            config_data = json.load(config_file)

        return ConfigDTO(
            config_data["seed_urls"],
            config_data["total_articles_to_find_and_parse"],
            config_data["headers"],
            config_data["encoding"],
            config_data["timeout"],
            config_data["should_verify_certificate"],
            config_data["headless_mode"],
        )

    def _validate_config_content(self) -> None:
        """
        Ensure configuration parameters are not corrupt.
        """
        config_values = self._extract_config_content()

        if not isinstance(config_values.seed_urls, list):
            raise IncorrectSeedURLError()

        for seed_url in config_values.seed_urls:
            if not isinstance(seed_url, str):
                raise IncorrectSeedURLError()

            if not re.match(r"^https?://(www\.)?", seed_url):
                raise IncorrectSeedURLError()

        if not isinstance(config_values.total_articles, int):
            raise IncorrectNumberOfArticlesError()

        if isinstance(config_values.total_articles, bool):
            raise IncorrectNumberOfArticlesError()

        if config_values.total_articles <= 0:
            raise IncorrectNumberOfArticlesError()

        if config_values.total_articles > 150:
            raise NumberOfArticlesOutOfRangeError()

        if not isinstance(config_values.headers, dict):
            raise IncorrectHeadersError()

        if not isinstance(config_values.encoding, str):
            raise IncorrectEncodingError()

        if not isinstance(config_values.timeout, int):
            raise IncorrectTimeoutError()

        if isinstance(config_values.timeout, bool):
            raise IncorrectTimeoutError()

        if not 0 < config_values.timeout <= 60:
            raise IncorrectTimeoutError()

        if not isinstance(config_values.should_verify_certificate, bool):
            raise IncorrectVerifyError()

        if not isinstance(config_values.headless_mode, bool):
            raise IncorrectVerifyError()

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls.

        Returns:
            list[str]: Seed urls
        """
        return self._seed_urls

    def get_num_articles(self) -> int:
        """
        Retrieve total number of articles to scrape.

        Returns:
            int: Total number of articles to scrape
        """
        return self._num_articles

    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting.

        Returns:
            dict[str, str]: Headers
        """
        return self._headers


    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing.

        Returns:
            str: Encoding
        """
        return self._encoding


    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response.

        Returns:
            int: Number of seconds to wait for response
        """
        return self._timeout


    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate.

        Returns:
            bool: Whether to verify certificate or not
        """
        return self._should_verify_certificate


    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode.

        Returns:
            bool: Whether to use headless mode or not
        """
        return self._headless_mode


def make_request(url: str, config: Config) -> requests.models.Response:
    """
    Deliver a response from a request with given configuration.

    Args:
        url (str): Site url
        config (Config): Configuration

    Returns:
        requests.models.Response: A response from a request
    """
    response = requests.get(
        url,
        headers=config.get_headers(),
        timeout=config.get_timeout(),
        verify=config.get_verify_certificate(),
    )
    response.encoding = config.get_encoding()
    return response


class Crawler:
    """
    Crawler implementation.
    """

    #: Url pattern
    url_pattern: re.Pattern | str

    def __init__(self, config: Config) -> None:
        """
        Initialize an instance of the Crawler class.

        Args:
            config (Config): Configuration
        """
        self._config = config
        self.urls = []
        self.url_pattern = re.compile(
                    r"^(https://ilibrary\.ru)?/text/\d+/(p\.\d+/)?index\.html$"
                )

    def _extract_url(self, article_bs: Tag) -> str:
        """
        Find and retrieve url from HTML.

        Args:
            article_bs (bs4.Tag): Tag instance

        Returns:
            str: Url from HTML
        """
        href = article_bs.get("href", "")

        href = re.sub(
            r"^(/text/\d+)/index\.html$",
            r"\1/p.1/index.html",
            href,
        )

        href = re.sub(
            r"^(https://ilibrary\.ru/text/\d+)/index\.html$",
            r"\1/p.1/index.html",
            href,
        )

        return urljoin(ILIBRARY_BASE_URL, href)

    def find_articles(self) -> None:
        """
        Find articles.
        """
        for seed_url in self.get_search_urls():
            try:
                response = make_request(seed_url, self._config)
            except requests.RequestException:
                continue

            if not response.ok:
                continue

            soup = BeautifulSoup(response.text, features="lxml")

            for article_bs in soup.find_all("a", href=True):
                href = article_bs.get("href", "")

                if not self.url_pattern.match(href):
                    continue

                full_url = self._extract_url(article_bs)

                if full_url not in self.urls:
                    self.urls.append(full_url)

                if len(self.urls) >= self._config.get_num_articles():
                    return

    def get_search_urls(self) -> list:
        """
        Get seed_urls param.

        Returns:
            list: seed_urls param
        """
        return self._config.get_seed_urls()

# 10


class CrawlerRecursive(Crawler):
    """
    Recursive implementation.

    Get one URL of the title page and find requested number of articles recursively.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize an instance of the CrawlerRecursive class.

        Args:
            config (Config): Configuration
        """
        super().__init__(config)
        self.start_url = self.get_search_urls()[0]
        self.num_articles = config.get_num_articles()


    def find_articles(self) -> None:
        """
        Find number of article urls requested.
        """
        super().find_articles()



# 4, 6, 8, 10


class HTMLParser:
    """
    HTMLParser implementation.
    """

    def __init__(self, full_url: str, article_id: int, config: Config) -> None:
        """
        Initialize an instance of the HTMLParser class.

        Args:
            full_url (str): Site url
            article_id (int): Article id
            config (Config): Configuration
        """
        self.full_url = full_url
        self.article_id = article_id
        self.config = config
        self.article = Article(url=full_url, article_id=article_id)

    def _fill_article_with_text(self, article_soup: BeautifulSoup) -> None:
        """
        Find text of article.

        Args:
            article_soup (bs4.BeautifulSoup): BeautifulSoup instance
        """
        text_block = article_soup.find("div", id="text")

        if text_block is None:
            self.article.text = ""
            return

        clear_text_soup = BeautifulSoup(str(text_block), features="lxml")

        for tag in clear_text_soup.find_all(["script", "style"]):
            tag.decompose()

        for selector in [
            "div.thdr",
            "div.author",
            "div.title",
            "iframe",
            "div.i0",
            "div#tbd",
        ]:
            for tag in clear_text_soup.select(selector):
                tag.decompose()

        article_text = clear_text_soup.get_text(separator="\n", strip=True)
        article_text = re.sub(r"\n+([,.!?;:])", r"\1", article_text)
        article_text = re.sub(r"[ \t]+", " ", article_text)
        article_text = re.sub(r"\n{3,}", "\n\n", article_text)
        self.article.text = article_text

    def _fill_article_with_meta_information(self, article_soup: BeautifulSoup) -> None:
        """
        Find meta information of article.

        Args:
            article_soup (bs4.BeautifulSoup): BeautifulSoup instance
        """
        author_tag = article_soup.find("div", class_="author")

        if author_tag is None:
            self.article.author = ["NOT FOUND"]
        else:
            self.article.author = [author_tag.get_text(strip=True)]

        header_tag = article_soup.find("div", class_="thdr")

        if header_tag is not None:
            header_links = header_tag.find_all("a")

            if len(header_links) >= 2:
                self.article.title = header_links[1].get_text(strip=True)
                return

        title_tag = article_soup.find("title")

        if title_tag is None:
            self.article.title = "NOT FOUND"
        else:
            title_text = title_tag.get_text(strip=True)
            self.article.title = title_text.split(". Текст произведения")[0]

    def unify_date_format(self, date_str: str) -> datetime.datetime:
        """
        Unify date format.

        Args:
            date_str (str): Date in text format

        Returns:
            datetime.datetime: Datetime object
        """
        return datetime.datetime.strptime(date_str, "%d.%m.%y")


    def parse(self) -> Article | bool:
        """
        Parse each article.

        Returns:
            Article | bool: Article instance, False in case of request error
        """
        try:
            response = make_request(self.full_url, self.config)
        except requests.RequestException:
            return False

        if not response.ok:
            return False

        article_soup = BeautifulSoup(response.text, features="lxml")

        self._fill_article_with_text(article_soup)
        self._fill_article_with_meta_information(article_soup)

        return self.article


def prepare_environment(base_path: pathlib.Path | str) -> None:
    """
    Create ASSETS_PATH folder if no created and remove existing folder.

    Args:
        base_path (pathlib.Path | str): Path where articles stores
    """
    path = pathlib.Path(base_path)

    if path.exists():
        shutil.rmtree(path)

    path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """
    Entrypoint for scraper module.
    """
    configuration = Config(path_to_config=CRAWLER_CONFIG_PATH)
    prepare_environment(ASSETS_PATH)

    crawler = Crawler(config=configuration)
    crawler.find_articles()

    parsed_articles = 0

    for article_id, article_url in enumerate(crawler.urls, start=1):
        parser = HTMLParser(
            full_url=article_url,
            article_id=article_id,
            config=configuration,
        )

        article = parser.parse()

        if not article:
            continue

        to_raw(article)
        to_meta(article)
        parsed_articles += 1

    print(f"{parsed_articles} articles from the given URL are parsed.")


if __name__ == "__main__":
    main()
