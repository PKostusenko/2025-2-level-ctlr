"""
Tests for validation dataset of raw texts.
"""

# pylint: disable=consider-using-with,no-name-in-module, redefined-outer-name, unused-argument
import json
import pathlib
import shutil
from typing import Generator

import pytest
from quality_control.console_logging import get_child_logger

from lab_5_scraper.tests.s2_1_crawler_config_test import assert_raises_with_message
from lab_6_pipeline.pipeline import CorpusManager, EmptyDirectoryError, InconsistentDatasetError

logger = get_child_logger(__file__)
logger.info("Stage 2A: Validating Assets Path")
logger.info("Starting tests with received assets folder")


def generate_test_directory(
    directory: pathlib.Path,
    raw_n: int = 5,
    meta_n: int = 5,
    raw_empty: bool = False,
    corrupted_filename: bool = False,
) -> pathlib.Path:
    """
    Create different kind of directories to test dataset validator implementation.

    Args:
        directory (pathlib.Path): Path to directory
        raw_n (int, optional): Number of raw articles. Defaults to 5.
        meta_n (int, optional): Number of meta. Defaults to 5.
        raw_empty (bool, optional): Whether raw article is empty or not. Defaults to False.
        corrupted_filename (bool, optional): Whether filename is corrupted or not.
            Defaults to False.

    Returns:
        pathlib.Path: The created directory path.
    """
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()

    # create n raw files
    for index in range(raw_n):
        filename = f"{index + 1}_raw.txt"
        with open(directory / filename, "w", encoding="utf-8") as file:
            text = (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore "
                "magna aliqua. Ut enim ad minim veniam, quis nostrud "
                "exercitation ullamco laboris nisi ut aliquip ex ea "
                "commodo consequat."
            )
            if not raw_empty:
                file.write(text)

        if corrupted_filename:
            with open(directory / f"{index + 1}_corrupted.txt", "w", encoding="utf-8") as file:
                text = "Lorem "
                file.write(text)

    # create m meta files
    for index in range(meta_n):
        meta_dummy = {
            "id": 0,
            "url": "https://vja.ruslang.ru/ru/archive/2021-3/7-25",
            "author": "С.В. Князев",
        }
        filename = f"{index + 1}_meta.json"
        with (directory / filename).open("w", encoding="utf-8") as file:
            json.dump(
                meta_dummy,
                file,
                sort_keys=False,
                indent=4,
                ensure_ascii=False,
                separators=(",", ": "),
            )
    return directory


@pytest.fixture(scope="module")
def test_paths() -> Generator[dict[str, pathlib.Path], None, None]:
    """
    Create test directories for pipeline path validation tests.

    Yields:
        dict[str, pathlib.Path]: Dictionary with test directory paths.
    """
    paths = {
        "empty": pathlib.Path("empty"),
        "broken_id": pathlib.Path("broken_id"),
        "imbalanced": pathlib.Path("imbalanced"),
        "empty_raw": pathlib.Path("empty_raw"),
        "normal": pathlib.Path("normal"),
        "corrupted_filename": pathlib.Path("corrupted_filename"),
        "filepath": pathlib.Path("filepath.txt"),
    }

    generate_test_directory(paths["empty"], raw_n=0, meta_n=0)
    generate_test_directory(paths["broken_id"])
    (paths["broken_id"] / "1_raw.txt").unlink()
    generate_test_directory(paths["imbalanced"], raw_n=3, meta_n=2)
    generate_test_directory(paths["empty_raw"], raw_empty=True)
    generate_test_directory(paths["normal"])
    generate_test_directory(paths["corrupted_filename"], corrupted_filename=True)
    paths["filepath"].open("w", encoding="utf-8").close()

    yield paths

    for path in [
        paths["empty"],
        paths["broken_id"],
        paths["imbalanced"],
        paths["empty_raw"],
        paths["normal"],
        paths["corrupted_filename"],
    ]:
        shutil.rmtree(path)
    paths["filepath"].unlink()


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_1_dataset_sanity_checks
@pytest.mark.lab_6_pipeline
def test_pipe_fails_given_non_existent_path() -> None:
    """
    Ensure that pipeline raises an error when given invalid path.
    """
    non_existent_path = pathlib.Path("non_existent_path")
    error_message = "Checking that scraper can handle not existing assets paths failed."
    assert_raises_with_message(error_message, FileNotFoundError, CorpusManager, non_existent_path)


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_1_dataset_sanity_checks
@pytest.mark.lab_6_pipeline
def test_pipeline_fails_given_filepath(test_paths: dict[str, pathlib.Path]) -> None:
    """
    Ensure that pipeline raises an error when given non-existing directory.

    Args:
        test_paths (dict[str, pathlib.Path]): Dictionary with test directory paths.
    """
    error_message = "Checking that pipeline fails if given not a directory path."
    assert_raises_with_message(
        error_message, NotADirectoryError, CorpusManager, test_paths["filepath"]
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_1_dataset_sanity_checks
@pytest.mark.lab_6_pipeline
def test_pipe_fails_given_empty_directory(test_paths: dict[str, pathlib.Path]) -> None:
    """
    Ensure that pipeline raises an error when given empty directory.

    Args:
        test_paths (dict[str, pathlib.Path]): Dictionary with test directory paths.
    """
    error_message = "Checking that empty directories cannot be processed."
    assert_raises_with_message(
        error_message, EmptyDirectoryError, CorpusManager, test_paths["empty"]
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_1_dataset_sanity_checks
@pytest.mark.lab_6_pipeline
def test_pipe_fails_given_inconsistent_dataset(test_paths: dict[str, pathlib.Path]) -> None:
    """
    Check consistent numbering.

    Args:
        test_paths (dict[str, pathlib.Path]): Dictionary with test directory paths.
    """
    error_message = "Checking that pipeline does not accept dataset with inconsistent numeration"
    assert_raises_with_message(
        error_message, InconsistentDatasetError, CorpusManager, test_paths["broken_id"]
    )


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_1_dataset_sanity_checks
@pytest.mark.lab_6_pipeline
def test_pipe_fails_given_imbalanced_dataset(test_paths: dict[str, pathlib.Path]) -> None:
    """
    Check consistent numbering among meta and text files.

    Args:
        test_paths (dict[str, pathlib.Path]): Dictionary with test directory paths.
    """
    error_message = (
        "Checking that pipeline does not accept "
        "dataset with uneven numbers of meta and text files"
    )
    assert_raises_with_message(
        error_message, InconsistentDatasetError, CorpusManager, test_paths["imbalanced"]
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_1_dataset_sanity_checks
@pytest.mark.lab_6_pipeline
def test_pipe_fails_given_dataset_with_empty_texts(test_paths: dict[str, pathlib.Path]) -> None:
    """
    Check that pipeline does not work with empty files.

    Args:
        test_paths (dict[str, pathlib.Path]): Dictionary with test directory paths.
    """
    error_message = "Checking that pipeline does not accept dataset with empty text files"
    assert_raises_with_message(
        error_message, InconsistentDatasetError, CorpusManager, test_paths["empty_raw"]
    )


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_1_dataset_sanity_checks
@pytest.mark.lab_6_pipeline
def test_pipe_skips_other_files(test_paths: dict[str, pathlib.Path]) -> None:
    """
    Check that pipeline works with only _raw.txt and _meta.json.

    Args:
        test_paths (dict[str, pathlib.Path]): Dictionary with test directory paths.
    """
    error_message = "Checking that pipeline does not accept dataset with files with corrupted names"
    assert isinstance(CorpusManager(test_paths["corrupted_filename"]), CorpusManager), error_message
