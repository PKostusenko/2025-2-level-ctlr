"""
Tests udpipe analyzer.
"""

# pylint: disable=redefined-outer-name
from typing import Generator

import pytest

from admin_utils.test_params import PIPE_TEST_FILES_FOLDER
from lab_6_pipeline.pipeline import UDPipeAnalyzer


@pytest.fixture(scope="function")
def udpipe_setup() -> Generator[tuple[str, list[str], UDPipeAnalyzer], None, None]:
    """
    Setup test data and analyzer instance.
    """
    path = PIPE_TEST_FILES_FOLDER / "reference_udpipe_test.conllu"
    with path.open("r", encoding="utf-8") as ref:
        conllu_reference = ref.read()
    texts = [
        "Красивая - мама красиво, училась в ПДД и ЖКУ"
        + " по адресу Львовская 10 лет с почтой test ."
    ]
    udpipe_analyzer = UDPipeAnalyzer()
    yield conllu_reference, texts, udpipe_analyzer


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_4_student_dataset_validation
@pytest.mark.lab_6_pipeline
def test_xpos_tag_replacement_in_analyzer(
    udpipe_setup: tuple[str, list[str], UDPipeAnalyzer],
) -> None:
    """
    Ensure that XPOS tags are replaced with '_' in CoNLL-U format.

    Args:
        udpipe_setup (tuple[str, list[str], UDPipeAnalyzer]):
        Fixture providing reference conllu string,
        input texts, and analyzer instance.
    """
    _, texts, udpipe_analyzer = udpipe_setup
    conllu_format = udpipe_analyzer.analyze(texts)
    assert conllu_format[0].split("\t")[4] == "_"


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_4_student_dataset_validation
@pytest.mark.lab_6_pipeline
def test_headers_are_included(udpipe_setup: tuple[str, list[str], UDPipeAnalyzer]) -> None:
    """
    Check id of sentence.

    Args:
        udpipe_setup (tuple[str, list[str], UDPipeAnalyzer]):
        Fixture providing reference conllu string,
        input texts, and analyzer instance.
    """
    _, texts, udpipe_analyzer = udpipe_setup
    conllu_format = udpipe_analyzer.analyze(texts)[0].format()
    header_line = conllu_format.split("\n")[0]
    assert "sent_id" in header_line
    assert header_line.split()[-1] == "1"


@pytest.mark.mark6
@pytest.mark.mark8
@pytest.mark.mark10
@pytest.mark.stage_3_4_student_dataset_validation
@pytest.mark.lab_6_pipeline
def test_analyze_method(udpipe_setup: tuple[str, list[str], UDPipeAnalyzer]) -> None:
    """
    Ensure that reference and processed conllu are equal.

    Args:
        udpipe_setup (tuple[str, list[str], UDPipeAnalyzer]):
        Fixture providing reference conllu string,
        input texts, and analyzer instance.
    """
    conllu_reference, texts, udpipe_analyzer = udpipe_setup
    conllu_format = udpipe_analyzer.analyze(texts)
    for reference, ud_analysis in zip(conllu_reference.splitlines(), conllu_format[0].splitlines()):
        assert reference == ud_analysis
