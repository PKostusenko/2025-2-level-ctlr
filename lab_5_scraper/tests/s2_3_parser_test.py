"""
Parser realization validation.
"""

# pylint: disable=no-member, no-name-in-module, assignment-from-no-return, redefined-outer-name
import random
from typing import Any

import pytest

from core_utils.article.article import Article
from core_utils.constants import CRAWLER_CONFIG_PATH
from lab_5_scraper.scraper import Config, Crawler, HTMLParser


@pytest.fixture(scope="function")
def parser_setup() -> Any:
    """
    Create config, crawler, parser and parsed result for tests.

    Yields:
        dict[str, Any]: Dictionary with setup instances.
    """
    config = Config(CRAWLER_CONFIG_PATH)
    crawler = Crawler(config)
    crawler.find_articles()
    parser = HTMLParser(random.choice(crawler.urls), 1, config)
    return_value = parser.parse()
    yield {
        "config": config,
        "crawler": crawler,
        "parser": parser,
        "return_value": return_value,
    }


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_3_HTML_parser_check
@pytest.mark.lab_5_scraper
def test_html_parser_instantiation(parser_setup: dict[str, Any]) -> None:
    """
    Ensure Parser is instantiated correctly.

    Args:
        parser_setup (dict[str, Any]): Pre-configured dictionary
        containing crawler, config, and parser instances.
    """
    parser = HTMLParser(
        random.choice(parser_setup["crawler"].urls), 1, config=parser_setup["config"]
    )
    assert hasattr(parser, "article"), "Parser instance must possess 'article' attribute"
    message = "Attribute 'article' of Parser instance must be an instance of Article"
    assert isinstance(parser.article, Article), message


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_3_HTML_parser_check
@pytest.mark.lab_5_scraper
def test_html_parser_parse_return_value_basic(parser_setup: dict[str, Any]) -> None:
    """
    Ensure Parser.parser() returns Article with filled text field.

    Args:
        parser_setup (dict[str, Any]): Pre-configured dictionary
        containing parser and parsed article result.
    """
    assert isinstance(
        parser_setup["return_value"], Article
    ), "parse() method must return Article instance"
    assert parser_setup[
        "return_value"
    ].article_id, "parse() method must return Article with filled id"
    message = "parse() method must return an Article instance with filled text"
    assert parser_setup["return_value"].text, message


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_3_HTML_parser_check
@pytest.mark.lab_5_scraper
def test_html_parser_parse_return_value_medium(parser_setup: dict[str, Any]) -> None:
    """
    Ensure Parser.parser() returns Article with filled title and author.

    Args:
        parser_setup (dict[str, Any]): Pre-configured dictionary
        containing parser and parsed article result.
    """
    assert parser_setup[
        "return_value"
    ].title, "parse() method must return Article with filled title"
    message = "parse() method must return an Article instance with filled author"
    assert parser_setup["return_value"].author, message


@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_3_HTML_parser_check
@pytest.mark.lab_5_scraper
def test_html_parser_parse_method_advanced(parser_setup: dict[str, Any]) -> None:
    """
    Ensure Parser.parser() returns Article with filled date field.

    Args:
        parser_setup (dict[str, Any]): Pre-configured dictionary
        containing parser and parsed article result.
    """
    message = "parse() method must return an Article instance with filled date"
    assert parser_setup["return_value"].date, message
