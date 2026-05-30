"""
Dataset validation.
"""

# pylint: disable=assignment-from-no-return, redefined-outer-name
import json
import re
import shutil
from typing import Any, Generator

import pytest
from quality_control.console_logging import get_child_logger

from admin_utils.test_params import TEST_PATH
from core_utils.constants import CRAWLER_CONFIG_PATH
from lab_5_scraper.scraper import Config, make_request
from lab_5_scraper.tests.utils import scraper_setup

logger = get_child_logger(__file__)


def check_title_in_html(title: str, html: str) -> bool:
    """
    Check that all words from title are present in article's text.

    Args:
        title (str): Article's title
        html (str): HTML given

    Returns:
        bool: Whether all words from title are present in article's text
    """
    split_markers = (
        r"&nbsp;|&#160;|&#32;|&#9248;|&#9248;|&#xA0;|&#x20;|&#x2420;|&#x2423;|&#9251;|\s"
    )
    title = " ".join(re.split(split_markers, title)).strip()
    html = " ".join(re.split(split_markers, html))
    if "&quot;" in html:
        html = re.sub(r"&quot;", '"', html)
        title = re.sub(r"&quot;", '"', title)
    elif "\\" in html:
        html = re.sub(r"\\", "", html)
        title = re.sub(r"\\", "", title)
    return title in html


@pytest.fixture(scope="function")
def raw_basic_setup() -> Generator[tuple[tuple[int, str], ...], None, None]:
    """
    Prepare raw text files dataset and clean up after test.

    Yields:
        tuple[tuple[int, str], ...]: Tuple of (article_id, content) pairs.
    """
    scraper_setup(articles_number=2)
    texts = []
    for file_name in TEST_PATH.iterdir():
        if file_name.name.endswith("_raw.txt"):
            with file_name.open(encoding="utf-8") as file:
                texts.append((int(file_name.name.split("_")[0]), file.read()))
    yield tuple(texts)
    if TEST_PATH.exists():
        shutil.rmtree(TEST_PATH)


@pytest.fixture(scope="function")
def raw_medium_setup() -> Generator[dict[str, Any], None, None]:
    """
    Prepare metadata files dataset and config for medium checks.

    Yields:
        dict[str, Any]: Dictionary with metadata tuple and config instance.
    """
    scraper_setup(articles_number=2)
    metadata = []
    for file_name in TEST_PATH.iterdir():
        if file_name.name.endswith("_meta.json"):
            with file_name.open(encoding="utf-8") as file:
                article_meta = json.load(file)
                metadata.append((article_meta["id"], article_meta))
    config = Config(CRAWLER_CONFIG_PATH)
    yield {"metadata": tuple(metadata), "config": config}
    if TEST_PATH.exists():
        shutil.rmtree(TEST_PATH)


@pytest.fixture(scope="function")
def raw_advanced_setup() -> Generator[dict[str, Any], None, None]:
    """
    Prepare metadata files dataset, config and date pattern for advanced checks.

    Yields:
        dict[str, Any]: Dictionary with metadata, config and date pattern.
    """
    scraper_setup()
    data_pattern = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
    metadata = []
    for file_name in TEST_PATH.iterdir():
        if file_name.name.endswith("_meta.json"):
            with file_name.open(encoding="utf-8") as file:
                article_meta = json.load(file)
                metadata.append((article_meta["id"], article_meta))
    config = Config(CRAWLER_CONFIG_PATH)
    yield {"metadata": tuple(metadata), "config": config, "data_pattern": data_pattern}
    if TEST_PATH.exists():
        shutil.rmtree(TEST_PATH)


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_5_dataset_validation
def test_validate_sort_raw(raw_basic_setup: tuple[tuple[int, str], ...]) -> None:
    """
    Ensure raw files numeration is homogeneous.

    Args:
        raw_basic_setup (tuple[tuple[int, str], ...]):
        Fixture yielding tuple of (article_id, content) pairs.
    """
    list_ids = [pair[0] for pair in raw_basic_setup]
    for i in range(1, len(list_ids) + 1):
        assert i in list_ids, "Articles ids are not homogeneous. E.g. numbers are not from 1 to N"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_5_dataset_validation
def test_texts_are_not_empty(raw_basic_setup: tuple[tuple[int, str], ...]) -> None:
    """
    Ensure text files are not empty.

    Args:
        raw_basic_setup (tuple[tuple[int, str], ...]):
        Fixture yielding tuple of (article_id, content) pairs.
    """
    msg = (
        "Text with ID: %s seems to be empty (less than 5 characters). "
        "Check if you collected article correctly"
    )
    for file_id, content in raw_basic_setup:
        if len(content) <= 5:
            with (TEST_PATH / f"{file_id}_meta.json").open("r", encoding="utf-8") as f:
                logger.error("Meta content: %s", f.read())
            assert False, msg % file_id


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_5_dataset_validation
@pytest.mark.lab_5_scraper
def test_folder_is_filled_with_no_duplicates(raw_basic_setup: tuple[tuple[int, str], ...]) -> None:
    """
    Ensure the collected article texts are unique.

    Args:
        raw_basic_setup (tuple[tuple[int, str], ...]):
        Fixture yielding tuple of (article_id, content) pairs.
    """
    assert len(raw_basic_setup) == len(set(raw_basic_setup))


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_5_dataset_validation
@pytest.mark.lab_5_scraper
def test_validate_sort_metadata(raw_medium_setup: dict[str, Any]) -> None:
    """
    Ensure meta files numeration is homogeneous.

    Args:
        raw_medium_setup (dict[str, Any]): Fixture yielding metadata and config.
    """
    list_ids = [pair[0] for pair in raw_medium_setup["metadata"]]
    for i in range(1, len(list_ids) + 1):
        assert i in list_ids, "Meta file ids are not homogeneous. E.g. numbers are not from 1 to N"


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_5_dataset_validation
@pytest.mark.lab_5_scraper
def test_validate_metadata_medium(raw_medium_setup: dict[str, Any]) -> None:
    """
    Ensure collected metadata is valid.

    Args:
        raw_medium_setup (dict[str, Any]): Fixture yielding metadata and config.
    """
    for _, meta in raw_medium_setup["metadata"]:
        msg = "Can not open URL: %s. Check how you collect URLs"
        response = make_request(meta["url"], raw_medium_setup["config"])
        assert response, msg % meta["url"]

        html_source = response.text
        msg = (
            f"Title is not found by specified in metadata "
            f"URL {meta['url']}. Check how you collect titles"
        )
        assert check_title_in_html(meta["title"], html_source), msg

        error_message = f"Author field {meta['author']} has incorrect type. List is expected."
        assert isinstance(meta["author"], list), error_message

        if not all(author in html_source for author in meta["author"]):
            message = (
                f"Author field {meta['author']} "
                f"(url <{meta['url']}>) is incorrect. "
                "Collect author from the page or specify it "
                "with special keyword <NOT FOUND> "
                "if it is not presented at the page."
            )
            assert meta["author"] == ["NOT FOUND"], message


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_5_dataset_validation
@pytest.mark.lab_5_scraper
def test_folder_is_filled_with_no_duplicated_meta(raw_medium_setup: dict[str, Any]) -> None:
    """
    Ensure the collected meta files are unique.

    Args:
        raw_medium_setup (dict[str, Any]): Fixture yielding metadata and config.
    """
    metadata = raw_medium_setup["metadata"]
    for i, (meta_id, meta) in enumerate(metadata[:-1]):
        for compare_id, compare_meta in metadata[i + 1 :]:
            assert meta_id != compare_id, "Meta IDs of different articles are the same."
            assert (
                meta["url"] != compare_meta["url"]
            ), "Meta urls of different articles are the same."


@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_5_dataset_validation
@pytest.mark.lab_5_scraper
def test_validate_metadata_advanced(raw_advanced_setup: dict[str, Any]) -> None:
    """
    Ensure that collected data includes correct date and topics.

    Args:
        raw_advanced_setup (dict[str, Any]): Fixture yielding metadata, config and date pattern.
    """
    data_pattern = raw_advanced_setup["data_pattern"]
    for _, meta in raw_advanced_setup["metadata"]:
        html_source = make_request(meta["url"], raw_advanced_setup["config"]).text

        message = (
            f"Date <{meta['date']}> do not match given "
            f"format <{data_pattern}> "
            f"(url <{meta['url']}>). "
            f"Check how you write dates."
        )
        assert re.search(data_pattern, meta["date"]), message

        topics = meta["topics"]
        if topics:
            for topic in topics:
                message = (
                    f"Topics <{meta['topics']}> "
                    f"(topic <{topic}>) for url "
                    f"<{meta['url']}> are not found. "
                    f"Check how you create topics."
                )
                assert topic in html_source, message
