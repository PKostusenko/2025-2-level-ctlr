"""
Tests for PatternSearchPipeline.
"""

# pylint: disable=redefined-outer-name
import json
import shutil
from typing import Generator

import pytest
from quality_control.console_logging import get_child_logger

from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from lab_6_pipeline import pipeline
from lab_6_pipeline.pipeline import CorpusManager, PatternSearchPipeline, UDPipeAnalyzer
from lab_6_pipeline.tests.utils import pipeline_test_files_setup

logger = get_child_logger(__file__)


def depth_counter(pattern_dict: dict) -> int:
    """
    Function to check the depth of the pattern matches structure.

    Args:
        pattern_dict (dict): A dictionary with one sentence pattern

    Returns:
        int: A depth of the dictionary
    """
    if isinstance(pattern_dict, dict):
        child_depths = [depth_counter(child) for child in pattern_dict.get("children", [])]
        if not child_depths:
            return 1
        max_depth = max(child_depths)
        return 1 + max_depth
    return 0


@pytest.fixture(scope="module")
def pattern_pipeline_setup() -> Generator[tuple[CorpusManager, list, dict], None, None]:
    """
    Setup and teardown for PatternSearchPipeline tests.
    """
    pipeline_test_files_setup(number_of_files=2)
    shutil.copyfile(
        PIPE_TEST_FILES_FOLDER / "reference_udpipe_test.conllu",
        TEST_PATH / "1_udpipe.conllu",
    )
    shutil.copyfile(
        PIPE_TEST_FILES_FOLDER / "2_udpipe.conllu",
        TEST_PATH / "2_udpipe.conllu",
    )

    article.ASSETS_PATH = TEST_PATH
    pipeline.ASSETS_PATH = TEST_PATH

    corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    patterns = []
    for one_article in corpus_manager.get_articles().values():
        path = one_article.get_meta_file_path()
        with open(path, "r", encoding="utf-8") as meta_file:
            meta = json.load(meta_file)
        logger.debug("Processing file: %s", one_article.article_id)
        logger.debug("Meta data: %s", meta)
        patterns.append(meta.pop("pattern_matches"))
        logger.debug("Patterns: %s", patterns)
        with open(path, "w", encoding="utf-8") as meta_file:
            json.dump(
                meta,
                meta_file,
                sort_keys=False,
                indent=4,
                ensure_ascii=False,
                separators=(",", ": "),
            )

    path_to_article = PIPE_TEST_FILES_FOLDER / "complex_pattern_matches.json"
    with open(path_to_article, "r", encoding="utf-8") as meta_file:
        complex_patterns = json.load(meta_file)
    logger.debug("Complex patterns: %s", complex_patterns)

    pattern_searcher = PatternSearchPipeline(
        corpus_manager, UDPipeAnalyzer(), ("VERB", "NOUN", "ADP")
    )
    pattern_searcher.run()

    yield corpus_manager, patterns, complex_patterns

    shutil.rmtree(TEST_PATH)


@pytest.mark.mark10
@pytest.mark.stage_5_pattern_search_pipeline_checks
@pytest.mark.lab_6_pipeline
def test_patterns_are_dict(pattern_pipeline_setup: tuple[CorpusManager, list, dict]) -> None:
    """
    Ensure patterns are matched correctly.

    Args:
        pattern_pipeline_setup (tuple[CorpusManager, list, dict]):
        Fixture providing corpus manager,
        expected patterns, and complex patterns.
    """
    corpus_manager, _, _ = pattern_pipeline_setup
    one_article = corpus_manager.get_articles()[1]
    path = one_article.get_meta_file_path()
    logger.debug("Meta file path: %s", path)
    with open(path, "r", encoding="utf-8") as meta_file:
        patterns = json.load(meta_file)["pattern_matches"]
    logger.debug("Actual patterns: %s", patterns)
    assert isinstance(patterns, dict)


@pytest.mark.mark10
@pytest.mark.stage_5_pattern_search_pipeline_checks
@pytest.mark.lab_6_pipeline
def test_json_structure_depth(pattern_pipeline_setup: tuple[CorpusManager, list, dict]) -> None:
    """
    Ensure the json structure has exact structure.

    Args:
        pattern_pipeline_setup (tuple[CorpusManager, list, dict]):
        Fixture providing corpus manager,
        expected patterns, and complex patterns.
    """
    corpus_manager, _, _ = pattern_pipeline_setup
    one_article = corpus_manager.get_articles()[2]
    path = one_article.get_meta_file_path()
    logger.debug("Meta file path: %s", path)
    with open(path, "r", encoding="utf-8") as meta_file:
        patterns = json.load(meta_file)["pattern_matches"]
    for sentence_patterns in patterns.values():
        for pattern in sentence_patterns:
            assert depth_counter(pattern) == 3


@pytest.mark.mark10
@pytest.mark.stage_5_pattern_search_pipeline_checks
@pytest.mark.lab_6_pipeline
def test_complex_patterns_are_correct(
    pattern_pipeline_setup: tuple[CorpusManager, list, dict],
) -> None:
    """
    Ensure the output of complex structure follows one of the templates.

    Args:
        pattern_pipeline_setup (tuple[CorpusManager, list, dict]):
        Fixture providing corpus manager,
        expected patterns, and complex patterns.
    """
    corpus_manager, _, complex_patterns = pattern_pipeline_setup
    one_article = corpus_manager.get_articles()[2]
    path = one_article.get_meta_file_path()
    logger.debug("Meta file path: %s", path)
    with open(path, "r", encoding="utf-8") as meta_file:
        patterns = json.load(meta_file)["pattern_matches"]

    matched = [patterns == match_pattern for match_pattern in complex_patterns["Match cases"]]
    logger.debug("Match results: %s", matched)
    assert max(matched), "Complex patterns do not match any expected template"
