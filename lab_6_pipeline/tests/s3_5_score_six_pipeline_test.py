"""
Tests for processing text.
"""

# pylint: disable=redefined-outer-name, unused-argument
import shutil
from typing import Generator

import pytest

from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from lab_6_pipeline.pipeline import CorpusManager, TextProcessingPipeline, UDPipeAnalyzer
from lab_6_pipeline.tests.utils import pipeline_test_files_setup


@pytest.fixture(scope="module")
def setup_pipeline_score_six() -> Generator[None, None, None]:
    """
    Setup and teardown for TextProcessingPipeline score 6 tests.
    """
    pipeline_test_files_setup()
    article.ASSETS_PATH = TEST_PATH
    corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
    pipe = TextProcessingPipeline(corpus_manager, UDPipeAnalyzer())
    pipe.run()
    yield
    shutil.rmtree(TEST_PATH)


@pytest.fixture(scope="function")
def loaded_conllu_texts(setup_pipeline_score_six: None) -> Generator[tuple[str, str], None, None]:
    """
    Load reference and processed conllu texts.
    """
    ref_path = PIPE_TEST_FILES_FOLDER / "reference_udpipe_test.conllu"
    with ref_path.open("r", encoding="utf-8") as ref:
        conllu_reference = ref.read()
    proc_path = TEST_PATH / "1_udpipe.conllu"
    with proc_path.open("r", encoding="utf-8") as file:
        conllu_processed = file.read()
    yield conllu_reference, conllu_processed


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_4_student_dataset_validation
@pytest.mark.lab_6_pipeline
def test_conllu_reference_preprocessed_are_equal(loaded_conllu_texts: tuple[str, str]) -> None:
    """
    Ensure that reference and processed conllu files have equal number of lines.

    Args:
        loaded_conllu_texts (tuple[str, str]):
        Fixture providing reference and processed conllu strings.
    """
    conllu_reference, conllu_processed = loaded_conllu_texts
    special_message = (
        f"Number of lines in reference "
        f"{conllu_reference} and processed "
        f"{conllu_processed} texts is different"
    )
    assert len(conllu_reference.split("\n")) == len(conllu_processed.split("\n")), special_message


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_4_student_dataset_validation
@pytest.mark.lab_6_pipeline
def test_conllu_tokens_are_formatted(loaded_conllu_texts: tuple[str, str]) -> None:
    """
    Ensure that reference and processed conllu files have equal tokens and length.

    Args:
        loaded_conllu_texts (tuple[str, str]):
        Fixture providing reference and processed conllu strings.
    """
    _, conllu_processed = loaded_conllu_texts
    ref_tokens = [
        "Красивая",
        "-",
        "мама",
        "красиво",
        ",",
        "училась",
        "в",
        "ПДД",
        "и",
        "ЖКУ",
        "по",
        "адресу",
        "Львовская",
        "10",
        "лет",
        "с",
        "почтой",
        "test",
        ".",
    ]
    format_lines_number = list(
        i for i in conllu_processed.split("\n") if i.split("\t")[0].isnumeric()
    )
    assert len(ref_tokens) == len(format_lines_number)

    for token_id, token in enumerate(ref_tokens):
        msg = (
            f"In conllu files, all tokens must be in lines\n"
            f"{token} is not in {format_lines_number[token_id]} at the second place"
        )
        assert token == format_lines_number[token_id].split("\t")[1], msg


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_4_student_dataset_validation
@pytest.mark.lab_6_pipeline
def test_empty_line_in_to_conllu_method(loaded_conllu_texts: tuple[str, str]) -> None:
    """
    Check number of empty lines in conllu files.

    Args:
        loaded_conllu_texts (tuple[str, str]):
        Fixture providing reference and processed conllu strings.
    """
    conllu_reference, conllu_processed = loaded_conllu_texts
    assert conllu_reference[-2:] == conllu_processed[-2:]
