"""
Check raw dataset volume.
"""

# pylint: disable=redefined-outer-name, unused-argument
import shutil
from typing import Generator

import pytest

from admin_utils.test_params import TEST_PATH
from lab_5_scraper.tests.utils import scraper_setup


@pytest.fixture(scope="function")
def dataset_setup() -> Generator[None, None, None]:
    """
    Prepare dataset environment and clean up after test.
    """
    scraper_setup()
    yield
    if TEST_PATH.exists():
        shutil.rmtree(TEST_PATH)


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_4_dataset_volume_check
@pytest.mark.lab_5_scraper
def test_folder_is_not_empty(dataset_setup: None) -> None:
    """
    Ensure there are collected articles.

    Args:
        dataset_setup (None): Fixture for dataset preparation and cleanup.
    """
    assert any(TEST_PATH.iterdir()), "ASSETS_PATH directory is empty"


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_2_4_dataset_volume_check
@pytest.mark.lab_5_scraper
def test_folder_has_equal_number_of_files(dataset_setup: None) -> None:
    """
    Ensure there are equal number of raw and meta files.

    Args:
        dataset_setup (None): Fixture for dataset preparation and cleanup.
    """
    metas, raws = 0, 0
    for file in TEST_PATH.iterdir():
        if file.name.endswith("_raw.txt"):
            raws += 1
        if file.name.endswith("_meta.json"):
            metas += 1
    message = "Collected dataset do not contain equal number of raw_articles and metas"
    assert metas == raws, message
