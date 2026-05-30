"""
Test for CorpusManager abstraction realization.
"""

# pylint: disable=redefined-outer-name, unused-argument
import shutil
from typing import Generator

import pytest

from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article.article import Article
from lab_6_pipeline.pipeline import CorpusManager
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


@pytest.fixture(scope="module")
def basic_class_setup() -> Generator[None, None, None]:
    """
    Setup and teardown for basic test environment.
    """
    pipeline_test_files_setup(meta=True)
    yield
    if TEST_PATH.is_dir():
        shutil.rmtree(TEST_PATH)


@pytest.fixture(scope="function")
def corpus_manager_basic(basic_class_setup: None) -> Generator[CorpusManager, None, None]:
    """
    Create a CorpusManager instance for basic tests.
    """
    manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    yield manager


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_2_corpus_manager_checks
@pytest.mark.lab_6_pipeline
def test_corpus_manager_instantiation(corpus_manager_basic: CorpusManager) -> None:
    """
    Ensure that CorpusManager instances are instantiated correctly.

    Args:
        corpus_manager_basic (CorpusManager): Basic CorpusManager fixture for testing.
    """
    assert hasattr(
        corpus_manager_basic, "_storage"
    ), "CorpusManager instance must have _storage field"
    articles = corpus_manager_basic.get_articles()
    assert isinstance(articles, dict), "CorpusManager attribute _storage must be dict object"
    assert (
        articles
    ), "CorpusManager attribute _storage must be filled right away during initialisation"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_2_corpus_manager_checks
@pytest.mark.lab_6_pipeline
def test_raw_files_are_found(corpus_manager_basic: CorpusManager) -> None:
    """
    Ensure that CorpusManager finds all saved raw files.

    Args:
        corpus_manager_basic (CorpusManager): Basic CorpusManager fixture for testing.
    """
    assert (
        1 in corpus_manager_basic.get_articles()
    ), "Corpus Manager does not create article instances given raw files only"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_2_corpus_manager_checks
@pytest.mark.lab_6_pipeline
def test_corrupted_file_names(corpus_manager_basic: CorpusManager) -> None:
    """
    Ensure that CorpusManager does not work with files with corrupted names.

    Args:
        corpus_manager_basic (CorpusManager): Basic CorpusManager fixture for testing.
    """
    shutil.copyfile(PIPE_TEST_FILES_FOLDER / "1_raw.txt", TEST_PATH / "None.txt")
    new_corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    assert len(new_corpus_manager.get_articles()) == 1


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_2_corpus_manager_checks
@pytest.mark.lab_6_pipeline
def test_article_instance_is_created(corpus_manager_basic: CorpusManager) -> None:
    """
    Ensure CorpusManager creates Article instances.

    Args:
        corpus_manager_basic (CorpusManager): Basic CorpusManager fixture for testing.
    """
    assert isinstance(
        corpus_manager_basic.get_articles()[1], Article
    ), "CorpusManager _storage values must be Article instances"


@pytest.mark.mark4
@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_2_corpus_manager_checks
@pytest.mark.lab_6_pipeline
def test_article_instance_is_filled(corpus_manager_basic: CorpusManager) -> None:
    """
    Ensure CorpusManager creates Article instances with text.

    Args:
        corpus_manager_basic (CorpusManager): Basic CorpusManager fixture for testing.
    """
    text = (
        "Красивая - мама красиво, училась в ПДД и "
        + "ЖКУ по адресу Львовская 10 лет с почтой test ."
    )
    assert (
        corpus_manager_basic.get_articles()[1].text == text
    ), "CorpusManager must store filled Article instances"


@pytest.fixture(scope="module")
def advanced_class_setup() -> Generator[None, None, None]:
    """
    Setup and teardown for advanced test environment.
    """
    pipeline_test_files_setup()
    yield
    if TEST_PATH.is_dir():
        shutil.rmtree(TEST_PATH)


@pytest.fixture(scope="function")
def corpus_manager_advanced(advanced_class_setup: None) -> Generator[CorpusManager, None, None]:
    """
    Create a CorpusManager instance for advanced tests.
    """
    manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    yield manager


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_2_corpus_manager_checks
@pytest.mark.lab_6_pipeline
def test_meta_files_are_found(corpus_manager_advanced: CorpusManager) -> None:
    """
    Ensure CorpusManager finds all saved meta files.

    Args:
        corpus_manager_advanced (CorpusManager): Advanced CorpusManager fixture for testing.
    """
    assert (
        1 in corpus_manager_advanced.get_articles()
    ), "Corpus Manager does not create article instances given both raw and meta files"
