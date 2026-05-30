"""
Utils for lab_6_pipeline tests.
"""

# pylint: disable=too-few-public-methods
import shutil

from admin_utils.test_params import PIPE_TEST_FILES_FOLDER, TEST_PATH
from core_utils.article import article
from core_utils.constants import ASSETS_PATH
from core_utils.pipeline import LibraryWrapper
from core_utils.tests.utils import copy_student_data
from lab_6_pipeline.pipeline import CorpusManager, TextProcessingPipeline, UDPipeAnalyzer


class AnalyzerMock(LibraryWrapper):
    """
    Mock for analyzer to be used for score 4 pipeline tests.
    """


def pipeline_test_files_setup(
    txt: bool = True, meta: bool = True, number_of_files: int = 1
) -> None:
    """
    Set up TEST_PATH to work with test files.

    Args:
        txt (bool, optional): Whether txt file is needed. Defaults to True.
        meta (bool, optional): Whether meta file is needed. Defaults to True.
        number_of_files (int, optional): Number of files to copy for tests. Defaults to 1.
    """
    if TEST_PATH.exists():
        shutil.rmtree(TEST_PATH)
    TEST_PATH.mkdir()

    for i in range(1, number_of_files + 1):
        if txt:
            shutil.copyfile(PIPE_TEST_FILES_FOLDER / f"{i}_raw.txt", TEST_PATH / f"{i}_raw.txt")
        if meta:
            shutil.copyfile(PIPE_TEST_FILES_FOLDER / f"{i}_meta.json", TEST_PATH / f"{i}_meta.json")


def pipeline_setup() -> None:
    """
    Set up TEST_PATH for MorphologicalAnalysisPipeline tests.
    """
    TEST_PATH.mkdir(exist_ok=True)
    if ASSETS_PATH.exists():
        copy_student_data()
    else:
        article.ASSETS_PATH = TEST_PATH
        corpus_manager = CorpusManager(path_to_raw_txt_data=TEST_PATH)
        pipe = TextProcessingPipeline(corpus_manager, UDPipeAnalyzer())
        pipe.run()
