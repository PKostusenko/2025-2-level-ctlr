"""
Interface definitions for text processing pipelines.
"""

# pylint: disable=too-few-public-methods, unused-argument
from dataclasses import dataclass
from typing import Protocol

from quality_control.console_logging import get_child_logger

from core_utils.article.article import Article

logger = get_child_logger(__file__)
try:
    from spacy.language import Language
    from spacy.tokens import Doc
except ImportError:
    Language = None  # type: ignore
    Doc = None  # type: ignore
    logger.warning("No libraries installed. Failed to import.")


class PipelineProtocol(Protocol):
    """
    Interface definition for pipeline.
    """

    def run(self) -> None:
        """
        Key API method.
        """


class LibraryWrapper(Protocol):
    """
    Interface definition for text analyzers.
    """

    _analyzer: Language

    def _bootstrap(self) -> Language:
        """
        Bootstrap analyzer with required models and settings.

        Returns:
            Language: Instance of analyzer.
        """

    def analyze(self, texts: list[str]) -> list[str]:
        """
        Analyze given texts.

        Args:
            texts (list[str]): Texts to analyze.

        Returns:
            list[str]: Collection of processed documents.
        """

    def to_conllu(self, article: Article) -> None:
        """
        Write ConLLU content to a file.

        Args:
            article (Article): Article to save
        """

    def from_conllu(self, article: Article) -> Doc:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            Doc: Document ready for parsing
        """


@dataclass
class TreeNode:
    """
    Interface definition for node in the graph.
    """

    upos: str
    text: str
    children: list["TreeNode"]
