"""
Tests for TextProcessingPipeline (score 4).
"""

# pylint: disable=redefined-outer-name, unused-argument
import shutil
from string import punctuation
from typing import Generator

import pytest

from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from lab_6_pipeline.pipeline import CorpusManager, TextProcessingPipeline
from lab_6_pipeline.tests.utils import AnalyzerMock, pipeline_setup, pipeline_test_files_setup


@pytest.fixture(scope="module")
def setup_reference_processing() -> Generator[None, None, None]:
    """
    Setup and teardown for reference processing tests.
    """
    pipeline_test_files_setup(meta=True)
    article.ASSETS_PATH = TEST_PATH
    corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    pipe = TextProcessingPipeline(corpus_manager)
    pipe.run()
    yield
    if TEST_PATH.is_dir():
        shutil.rmtree(TEST_PATH)


@pytest.fixture(scope="function")
def loaded_texts(setup_reference_processing: None) -> Generator[tuple[str, str], None, None]:
    """
    Load reference and processed texts for assertions.
    """
    ref_path = PIPE_TEST_FILES_FOLDER / "reference_score_four.txt"
    with ref_path.open("r", encoding="utf-8") as ref:
        reference = ref.read()
    proc_path = TEST_PATH / "1_cleaned.txt"
    with proc_path.open("r", encoding="utf-8") as proc:
        processed = proc.read()
    yield reference, processed


@pytest.mark.mark4
@pytest.mark.stage_3_3_admin_data_processing
@pytest.mark.lab_6_pipeline
def test_reference_preprocessed_are_equal(loaded_texts: tuple[str, str]) -> None:
    """
    Ensure equal number of tokens in processed and reference texts.

    Args:
        loaded_texts (tuple[str, str]): Fixture providing reference and processed text strings.
    """
    reference, processed = loaded_texts
    assert len(reference.split()) == len(processed.split()), (
        f"Number of tokens sequences in reference {reference} "
        f"and processed {processed} texts is different"
    )
    assert (
        reference.split() == processed.split()
    ), "Pipe does not tokenize admin text. Check how you tokenize"


@pytest.mark.mark4
@pytest.mark.stage_3_3_admin_data_processing
@pytest.mark.lab_6_pipeline
def test_overall_format(loaded_texts: tuple[str, str]) -> None:
    """
    Ensure that there is no punctuation or uppercase in clean text.

    Args:
        loaded_texts (tuple[str, str]): Fixture providing reference and processed text strings.
    """
    _, processed = loaded_texts
    assert processed.islower(), "Cleaned text must be lowercase"
    assert not (set(processed) & set(punctuation)), "Cleaned text must not have any punctuation"


@pytest.fixture(scope="function")
def pipeline_mock_env() -> Generator[None, None, None]:
    """
    Setup and teardown for mock analyzer pipeline tests.
    """
    pipeline_test_files_setup(meta=True)
    article.ASSETS_PATH = TEST_PATH
    yield
    shutil.rmtree(TEST_PATH)


@pytest.mark.mark4
@pytest.mark.stage_3_3_admin_data_processing
@pytest.mark.lab_6_pipeline
def test_score_four_pipeline_with_analyzer_mock_can_execute(pipeline_mock_env: None) -> None:
    """
    Ensure pipeline for score 4 does not depend on analyzer.

    Args:
        pipeline_mock_env (None): Fixture managing test environment for mock analyzer.
    """
    corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    pipe = TextProcessingPipeline(corpus_manager, AnalyzerMock())
    assert pipe.run() is None


@pytest.fixture(scope="function")
def student_cleaned_articles() -> Generator[dict[int, str], None, None]:
    """
    Setup and teardown for student dataset validation tests.
    """
    pipeline_setup()
    CorpusManager(TEST_PATH)
    articles = {}
    for file in TEST_PATH.iterdir():
        if file.name.endswith("_cleaned.txt"):
            with file.open("r", encoding="utf-8") as txt:
                articles[int(file.name[:-12])] = txt.read()
    yield articles
    shutil.rmtree(TEST_PATH)


@pytest.mark.mark4
@pytest.mark.stage_3_4_student_dataset_validation
@pytest.mark.lab_6_pipeline
def test_clean_tokens(student_cleaned_articles: dict[int, str]) -> None:
    """
    Ensure there is no punctuation of uppercase in cleaned text.

    Args:
        student_cleaned_articles (dict[int, str]): Fixture providing dictionary of cleaned articles.
    """
    articles = student_cleaned_articles
    punctuation_marks = [",", ".", "-", ";", ":", "!", "?", "<"]
    for article_id, article_text in articles.items():
        for token in article_text.split():
            message = f"There are some punctuation marks found in article {article_id}"
            assert token not in punctuation_marks, message
            if not token.isalpha():
                continue
            message = f"Token {token} in article {article_id} is not lowercase"
            assert token.islower(), message
