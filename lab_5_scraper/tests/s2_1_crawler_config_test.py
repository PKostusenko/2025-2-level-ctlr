"""
Crawler configuration validation.
"""

# pylint: disable=no-name-in-module, redefined-outer-name
import json
import shutil
from pathlib import Path
from typing import Any, Generator

import pytest
from quality_control.console_logging import get_child_logger

from admin_utils.test_params import TEST_CRAWLER_CONFIG_PATH, TEST_PATH
from core_utils.constants import CRAWLER_CONFIG_PATH, TIMEOUT_LOWER_LIMIT, TIMEOUT_UPPER_LIMIT
from lab_5_scraper import scraper
from lab_5_scraper.scraper import (
    IncorrectEncodingError,
    IncorrectHeadersError,
    IncorrectNumberOfArticlesError,
    IncorrectSeedURLError,
    IncorrectTimeoutError,
    IncorrectVerifyError,
    NumberOfArticlesOutOfRangeError,
)
from lab_5_scraper.tests.config_generator import generate_config

logger = get_child_logger(__file__)

logger.info("Stage 1A: Validating Crawler Config")
logger.info("Starting tests with received config")


class ExceptionIsNotRaised(Exception):
    """
    No exception was raised.
    """


def assert_raises_with_message(
    msg: str, exception: type[Exception], func: Any, *args: Path, **kwargs: Any
) -> None:
    """
    Method assertRaises counterparts with enabled messaging.

    Args:
        msg (str): Error message
        exception (type[Exception]): Exception
        func (Any): Function
        *args (Path): Arguments
        **kwargs (Any): Options
    """
    try:
        func(*args, **kwargs)
        logger.error(msg)
        raise ExceptionIsNotRaised
    except ExceptionIsNotRaised:
        raise AssertionError(msg) from ExceptionIsNotRaised
    except Exception as inst:  # pylint: disable=broad-except
        assert isinstance(inst, exception), msg


@pytest.fixture(scope="function")
def config_data() -> Generator[dict[str, Any], None, None]:
    """
    Load reference configuration and prepare test data.

    Yields:
        dict[str, Any]: Dictionary with correct and incorrect config values.
    """
    with CRAWLER_CONFIG_PATH.open() as file:
        reference = json.load(file)

    data = {
        "seed_urls_correct": reference["seed_urls"],
        "num_articles_correct": reference["total_articles_to_find_and_parse"],
        "headers_correct": reference["headers"],
        "timeout_correct": reference["timeout"],
        "encoding_correct": reference["encoding"],
        "should_verify_certificate": reference["should_verify_certificate"],
        "headless_mode": reference["headless_mode"],
        "seed_urls_incorrect": ["https://sample.com/", True, 1, ["does_not_match_pattern"]],
        "num_articles_incorrect": [-5, False, {1: 2}],
        "headers_incorrect": [True, 1, "headers"],
        "timeout_incorrect": [
            "five secs",
            {False: 5},
            TIMEOUT_LOWER_LIMIT - 5,
            TIMEOUT_UPPER_LIMIT + 5,
        ],
        "encoding_incorrect": [5, False, [1, 2, 3]],
        "verify_incorrect": ["verify", {1: 2}, (1, 2)],
        "headless_incorrect": ["false", {1: 4}, (1, 2, 3)],
    }
    yield data
    if TEST_PATH.exists():
        shutil.rmtree(TEST_PATH)


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_base_urls_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    for incorrect_seed_urls in config_data["seed_urls_incorrect"]:
        generate_config(
            seed_urls=incorrect_seed_urls,
            num_articles=config_data["num_articles_correct"],
            timeout=config_data["timeout_correct"],
            headers=config_data["headers_correct"],
            encoding=config_data["encoding_correct"],
            should_verify_certificate=config_data["should_verify_certificate"],
            headless_mode=config_data["headless_mode"],
        )

        error_message = """Checking that scraper can handle incorrect seed_urls inputs.
Seed URLs must be a list of strings, not a single string"""
        assert_raises_with_message(
            error_message, IncorrectSeedURLError, scraper.Config, TEST_CRAWLER_CONFIG_PATH
        )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_num_urls_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    for incorrect_num_urls in config_data["num_articles_incorrect"]:
        generate_config(
            seed_urls=config_data["seed_urls_correct"],
            num_articles=incorrect_num_urls,
            timeout=config_data["timeout_correct"],
            headers=config_data["headers_correct"],
            encoding=config_data["encoding_correct"],
            should_verify_certificate=config_data["should_verify_certificate"],
            headless_mode=config_data["headless_mode"],
        )

        error_message = """Checking that scraper can handle incorrect num articles inputs.
Num articles must be a positive integer."""
        assert_raises_with_message(
            error_message,
            IncorrectNumberOfArticlesError,
            scraper.Config,
            TEST_CRAWLER_CONFIG_PATH,
        )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_num_urls_too_large_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    generate_config(
        seed_urls=config_data["seed_urls_correct"],
        num_articles=1000000,
        timeout=config_data["timeout_correct"],
        headers=config_data["headers_correct"],
        encoding=config_data["encoding_correct"],
        should_verify_certificate=config_data["should_verify_certificate"],
        headless_mode=config_data["headless_mode"],
    )

    error_message = """Checking that scraper can handle incorrect num articles inputs.
Num articles must not be too large"""
    assert_raises_with_message(
        error_message,
        NumberOfArticlesOutOfRangeError,
        scraper.Config,
        TEST_CRAWLER_CONFIG_PATH,
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_timeout_too_large_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    for incorrect_timeout in config_data["timeout_incorrect"]:
        generate_config(
            seed_urls=config_data["seed_urls_correct"],
            num_articles=config_data["num_articles_correct"],
            timeout=incorrect_timeout,
            headers=config_data["headers_correct"],
            encoding=config_data["encoding_correct"],
            should_verify_certificate=config_data["should_verify_certificate"],
            headless_mode=config_data["headless_mode"],
        )

        error_message = """Checking that scraper can handle incorrect timeout inputs.
    Timeout must be an integer
    {TIMEOUT_LOWER_LIMIT} and {TIMEOUT_UPPER_LIMIT}. 0 is a valid value"""
        assert_raises_with_message(
            error_message, IncorrectTimeoutError, scraper.Config, TEST_CRAWLER_CONFIG_PATH
        )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_headers_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    for incorrect_headers in config_data["headers_incorrect"]:
        generate_config(
            seed_urls=config_data["seed_urls_correct"],
            num_articles=config_data["num_articles_correct"],
            timeout=config_data["timeout_correct"],
            headers=incorrect_headers,
            encoding=config_data["encoding_correct"],
            should_verify_certificate=config_data["should_verify_certificate"],
            headless_mode=config_data["headless_mode"],
        )

    error_message = """Checking that scraper can handle incorrect headers.
Headers must be a dictionary with string keys and string values"""
    assert_raises_with_message(
        error_message, IncorrectHeadersError, scraper.Config, TEST_CRAWLER_CONFIG_PATH
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_encoding_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    for incorrect_encoding in config_data["encoding_incorrect"]:
        generate_config(
            seed_urls=config_data["seed_urls_correct"],
            num_articles=config_data["num_articles_correct"],
            timeout=config_data["timeout_correct"],
            headers=config_data["headers_correct"],
            encoding=incorrect_encoding,
            should_verify_certificate=config_data["should_verify_certificate"],
            headless_mode=config_data["headless_mode"],
        )

    error_message = """Checking that scraper can handle incorrect encoding.
Encoding must be a string"""
    assert_raises_with_message(
        error_message, IncorrectEncodingError, scraper.Config, TEST_CRAWLER_CONFIG_PATH
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_verify_cert_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    for incorrect_verify in config_data["verify_incorrect"]:
        generate_config(
            seed_urls=config_data["seed_urls_correct"],
            num_articles=config_data["num_articles_correct"],
            timeout=config_data["timeout_correct"],
            headers=config_data["headers_correct"],
            encoding=config_data["encoding_correct"],
            should_verify_certificate=incorrect_verify,
            headless_mode=config_data["headless_mode"],
        )

    error_message = """Checking that scraper can handle incorrect verify certificate argument.
Verify certificate must be either True or False"""
    assert_raises_with_message(
        error_message, IncorrectVerifyError, scraper.Config, TEST_CRAWLER_CONFIG_PATH
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_incorrect_headless_config_param(config_data: dict[str, Any]) -> None:
    """
    Config class returns error message and exit code 1 with incorrect config params.

    Args:
        config_data (dict[str, Any]): Dictionary with correct and incorrect config values.
    """
    for incorrect_headless in config_data["headless_incorrect"]:
        generate_config(
            seed_urls=config_data["seed_urls_correct"],
            num_articles=config_data["num_articles_correct"],
            timeout=config_data["timeout_correct"],
            headers=config_data["headers_correct"],
            encoding=config_data["encoding_correct"],
            should_verify_certificate=config_data["should_verify_certificate"],
            headless_mode=incorrect_headless,
        )

    error_message = """Checking that scraper can handle headless mode argument.
Headless mode must be either True or False"""
    assert_raises_with_message(
        error_message, IncorrectVerifyError, scraper.Config, TEST_CRAWLER_CONFIG_PATH
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_config_initialization(config_data: dict[str, Any]) -> None:
    """
    Test that Config class correctly initializes and stores attributes
    from a valid configuration file.

    Args:
        config_data (dict[str, Any]): Dictionary with correct config values.
    """
    generate_config(
        seed_urls=config_data["seed_urls_correct"],
        num_articles=config_data["num_articles_correct"],
        timeout=config_data["timeout_correct"],
        headers=config_data["headers_correct"],
        encoding=config_data["encoding_correct"],
        should_verify_certificate=config_data["should_verify_certificate"],
        headless_mode=config_data["headless_mode"],
    )
    attr_names = [
        "path_to_config",
        "_seed_urls",
        "_num_articles",
        "_headers",
        "_encoding",
        "_timeout",
        "_should_verify_certificate",
    ]
    config = scraper.Config(TEST_CRAWLER_CONFIG_PATH)
    all_attrs = [hasattr(config, attr_name) for attr_name in attr_names]
    error_message = """Checking that scraper saves relevant data to attributes."""
    assert all(all_attrs), error_message


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_1_crawler_config_check
@pytest.mark.lab_5_scraper
def test_config_getters(config_data: dict[str, Any]) -> None:
    """
    Test that Config getter methods return values matching
    the source configuration.

    Args:
        config_data (dict[str, Any]): Dictionary with correct config values.
    """
    generate_config(
        seed_urls=config_data["seed_urls_correct"],
        num_articles=config_data["num_articles_correct"],
        timeout=config_data["timeout_correct"],
        headers=config_data["headers_correct"],
        encoding=config_data["encoding_correct"],
        should_verify_certificate=config_data["should_verify_certificate"],
        headless_mode=config_data["headless_mode"],
    )
    config = scraper.Config(TEST_CRAWLER_CONFIG_PATH)
    getters = [
        config.get_seed_urls,
        config.get_num_articles,
        config.get_headers,
        config.get_encoding,
        config.get_timeout,
        config.get_verify_certificate,
        config.get_headless_mode,
    ]
    values = [
        config_data["seed_urls_correct"],
        config_data["num_articles_correct"],
        config_data["headers_correct"],
        config_data["encoding_correct"],
        config_data["timeout_correct"],
        config_data["should_verify_certificate"],
        config_data["headless_mode"],
    ]
    assert all(method() == value for method, value in zip(getters, values))
