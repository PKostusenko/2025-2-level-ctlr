"""
Crawler instantiation validation.
"""

# pylint: disable=no-member, protected-access, redefined-outer-name
import shutil
from typing import Generator

import pytest

from admin_utils.test_params import TEST_PATH
from core_utils.constants import CRAWLER_CONFIG_PATH
from lab_5_scraper.scraper import Config, Crawler, make_request, prepare_environment


@pytest.fixture(scope="function")
def config() -> Config:
    """
    Create a Config instance for tests.

    Returns:
        Config: Configured crawler configuration instance.
    """
    return Config(CRAWLER_CONFIG_PATH)


@pytest.fixture(scope="function")
def test_dir() -> Generator[None, None, None]:
    """
    Prepare test directory and clean up after test.
    """
    TEST_PATH.mkdir(parents=True, exist_ok=True)
    yield
    if TEST_PATH.exists():
        shutil.rmtree(TEST_PATH)


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_newly_created_crawler_instance_empty(config: Config) -> None:
    """
    Ensure that field 'urls' is not filled initially.

    Args:
        config (Config): Configured crawler configuration instance.
    """
    crawler = Crawler(config=config)
    error_msg = 'Check Crawler constructor: field "urls" is supposed to initially be empty'
    assert not crawler.urls, error_msg


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_crawler_instance_is_filled_from_find_articles(config: Config) -> None:
    """
    Ensure find_articles() fills 'urls' field.

    Args:
        config (Config): Configured crawler configuration instance.
    """
    crawler = Crawler(config)
    crawler.find_articles()
    error_msg = (
        'Method find_articles() must fill field "urls" '
        "with links found with the help of seed URLs"
    )
    assert crawler.urls, error_msg


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_crawler_instance_stores_full_urls(config: Config) -> None:
    """
    Ensure URLs from 'urls' field are valid.

    Args:
        config (Config): Configured crawler configuration instance.
    """
    crawler = Crawler(config)
    crawler.find_articles()
    error_msg = (
        "Method find_articles() must fill field "
        '"urls" with ready-to-use, valid full links. Current url: {}'
    )
    for url in crawler.urls:
        status_code = make_request(url, config).status_code
        assert status_code == 200, error_msg.format(url)


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_crawler_finds_required_number_of_articles(config: Config) -> None:
    """
    Ensure Crawler is capable to collect required number of articles.

    Args:
        config (Config): Configured crawler configuration instance.
    """
    crawler = Crawler(config)
    crawler.find_articles()
    error_msg = (
        'Method find_articles() must fill field "urls" '
        "with not less articles than specified in config file."
        f"{len(crawler.urls)} != {config.get_num_articles()}"
    )
    assert len(crawler.urls) >= config.get_num_articles(), error_msg


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_crawler_stores_unique_urls(config: Config) -> None:
    """
    Ensure find_articles() fills 'urls' with unique urls.

    Args:
        config (Config): Configured crawler configuration instance.
    """
    crawler = Crawler(config)
    crawler.find_articles()
    error_msg = (
        'Method find_articles() must fill field "urls" '
        "with unique urls. Found "
        f"{len(crawler.urls) - len(set(crawler.urls))} "
        "duplicated urls."
    )
    assert len(crawler.urls) == len(set(crawler.urls)), error_msg


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_crawler_get_search_urls(config: Config) -> None:
    """
    Ensure get_search_urls retrieves seed urls.

    Args:
        config (Config): Configured crawler configuration instance.
    """
    crawler = Crawler(config)
    crawler.find_articles()
    error_msg = "Method get_search_urls() must retrieve seed urls"
    assert crawler.get_search_urls() == config.get_seed_urls(), error_msg


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_crawler_handles_unavailable_websites() -> None:
    """
    Ensure does not fail given unavailable webpage.
    """
    config = Config(CRAWLER_CONFIG_PATH)
    config._seed_urls = config._seed_urls + ["https://github.com/non-existent-page"]
    crawler = Crawler(config)
    crawler.find_articles()
    error_msg = "Crawler does not fail given unavailable webpage"
    assert crawler.urls, error_msg


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_2_crawler_check
@pytest.mark.lab_5_scraper
def test_prepare_environment_function_creates_directory(
    test_dir: None,  # pylint: disable=unused-argument
) -> None:
    """
    Ensure prepare_environment() creates the target directory and leaves it empty.

    Args:
        test_dir (None): Fixture for test directory preparation and cleanup.
    """
    prepare_environment(TEST_PATH)
    assert TEST_PATH.exists()
    assert not any(TEST_PATH.iterdir())
