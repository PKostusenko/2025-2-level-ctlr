"""
Tests for POS frequency pipeline.
"""

# pylint: disable=no-name-in-module, duplicate-code, redefined-outer-name, unused-argument
import json
import shutil
from typing import Generator

import pytest
from quality_control.console_logging import get_child_logger

from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from lab_6_pipeline import pipeline
from lab_6_pipeline.pipeline import (
    CorpusManager,
    EmptyFileError,
    POSFrequencyPipeline,
    UDPipeAnalyzer,
)
from lab_6_pipeline.tests.utils import pipeline_test_files_setup

logger = get_child_logger(__file__)


@pytest.fixture(scope="module")
def pos_pipeline_setup() -> Generator[tuple[CorpusManager, dict], None, None]:
    """
    Setup and teardown for POSFrequencyPipeline tests.
    """
    pipeline_test_files_setup()
    shutil.copyfile(
        PIPE_TEST_FILES_FOLDER / "reference_udpipe_test.conllu",
        TEST_PATH / "1_udpipe.conllu",
    )

    article.ASSETS_PATH = TEST_PATH
    pipeline.ASSETS_PATH = TEST_PATH

    corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    path = corpus_manager.get_articles()[1].get_meta_file_path()
    with open(path, "r", encoding="utf-8") as meta_file:
        meta = json.load(meta_file)
    logger.debug("Meta before removing pos_frequencies: %s", meta)
    frequencies = meta.pop("pos_frequencies")
    logger.debug("Expected frequencies: %s", frequencies)
    with open(path, "w", encoding="utf-8") as meta_file:
        json.dump(
            meta,
            meta_file,
            sort_keys=False,
            indent=4,
            ensure_ascii=False,
            separators=(",", ": "),
        )

    pos_pipe = POSFrequencyPipeline(corpus_manager, UDPipeAnalyzer())
    pos_pipe.run()

    yield corpus_manager, frequencies

    shutil.rmtree(TEST_PATH)


@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_4_pos_frequency_pipeline_checks
@pytest.mark.lab_6_pipeline
def test_meta_files_readable(pos_pipeline_setup: tuple[CorpusManager, dict]) -> None:
    """
    Ensure meta files are not corrupt.

    Args:
        pos_pipeline_setup (tuple[CorpusManager, dict]):
        Fixture providing corpus manager and expected frequencies.
    """
    corpus_manager, _ = pos_pipeline_setup
    failed = False
    try:
        one_article = corpus_manager.get_articles()[1]
        path = one_article.get_meta_file_path()
        with open(path, "r", encoding="utf-8") as meta_file:
            json.load(meta_file)
    except json.decoder.JSONDecodeError:
        failed = True
    finally:
        message = "Generated meta files are corrupt: check how you update .json files"
        assert not failed, message


@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_4_pos_frequency_pipeline_checks
@pytest.mark.lab_6_pipeline
def test_frequencies_are_correct(pos_pipeline_setup: tuple[CorpusManager, dict]) -> None:
    """
    Ensure frequencies are counted correctly.

    Args:
        pos_pipeline_setup (tuple[CorpusManager, dict]):
        Fixture providing corpus manager and expected frequencies.
    """
    corpus_manager, expected_frequencies = pos_pipeline_setup
    one_article = corpus_manager.get_articles()[1]
    path = one_article.get_meta_file_path()
    logger.debug("Meta file path: %s", path)
    with open(path, "r", encoding="utf-8") as meta_file:
        frequencies = json.load(meta_file)["pos_frequencies"]
    logger.debug("Expected frequencies: %s", expected_frequencies)
    logger.debug("Actual frequencies: %s", frequencies)
    assert expected_frequencies == frequencies, "POS frequencies are calculated incorrectly"


@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_4_pos_frequency_pipeline_checks
@pytest.mark.lab_6_pipeline
def test_images_are_generated(pos_pipeline_setup: tuple[CorpusManager, dict]) -> None:
    """
    Ensure images are generated.

    Args:
        pos_pipeline_setup (tuple[CorpusManager, dict]):
        Fixture providing corpus manager and expected frequencies.
    """
    msg = (
        "POSFrequencyPipeline does not create image "
        + "file for at least one of articles available"
    )
    ids_available = set(
        map(
            lambda filename: int(str(filename.name).split("_", maxsplit=1)[0]),
            TEST_PATH.iterdir(),
        )
    )
    for identifier in ids_available:
        path = TEST_PATH / f"{identifier}_image.png"
        assert path.is_file(), msg


@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_4_pos_frequency_pipeline_checks
@pytest.mark.lab_6_pipeline
def test_pos_throws_error(pos_pipeline_setup: tuple[CorpusManager, dict]) -> None:
    """
    Ensure that POS pipe raises EmptyFileError.

    Args:
        pos_pipeline_setup (tuple[CorpusManager, dict]):
        Fixture providing corpus manager and expected frequencies.
    """
    with open(TEST_PATH / "1_udpipe.conllu", "w", encoding="utf-8") as file:
        file.write("")

    new_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    new_pipe = POSFrequencyPipeline(new_manager, UDPipeAnalyzer())
    with pytest.raises(EmptyFileError):
        new_pipe.run()
