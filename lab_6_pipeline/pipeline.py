"""
Pipeline for CONLL-U formatting.
"""

# pylint: disable=too-few-public-methods, unused-import, undefined-variable, too-many-nested-blocks, duplicate-code
import pathlib

import spacy_udpipe

from core_utils.article.article import Article, ArtifactType
from core_utils.article.io import from_raw, to_cleaned
from core_utils.constants import ASSETS_PATH
from core_utils.pipeline import LibraryWrapper, PipelineProtocol, TreeNode

try:
    from networkx import DiGraph
    from networkx.algorithms.isomorphism import DiGraphMatcher
except ImportError:
    DiGraph = None  # type: ignore
    print("No libraries installed. Failed to import.")

try:
    from spacy.language import Language
    from spacy.tokens import Doc
except ImportError:
    Language = None  # type: ignore
    Doc = None  # type: ignore
    print("No libraries installed. Failed to import.")


class EmptyDirectoryError(Exception):
    """
    Raised when dataset directory is empty.
    """


class InconsistentDatasetError(Exception):
    """
    Raised when dataset has wrong or incomplete structure.
    """


class EmptyFileError(Exception):
    """
    Raised when file is empty.
    """


class CorpusManager:
    """
    Work with articles and store them.
    """

    def __init__(self, path_to_raw_txt_data: pathlib.Path) -> None:
        """
        Initialize an instance of the CorpusManager class.

        Args:
            path_to_raw_txt_data (pathlib.Path): Path to raw txt data
        """
        self.path_to_raw_txt_data = pathlib.Path(path_to_raw_txt_data)
        self._validate_dataset()
        self._storage = self._scan_dataset()

    def _validate_dataset(self) -> None:
        """
        Validate folder with assets.
        """
        if not self.path_to_raw_txt_data.exists():
            raise FileNotFoundError("Dataset folder does not exist.")

        if not self.path_to_raw_txt_data.is_dir():
            raise NotADirectoryError("Dataset path is not a directory.")

        files = [file for file in self.path_to_raw_txt_data.iterdir() if file.is_file()]

        if not files:
            raise EmptyDirectoryError("Dataset folder is empty.")

        raw_files = sorted(self.path_to_raw_txt_data.glob("*_raw.txt"))
        meta_files = sorted(self.path_to_raw_txt_data.glob("*_meta.json"))

        if not raw_files:
            raise InconsistentDatasetError("Dataset does not contain raw text files.")

        if len(raw_files) != len(meta_files):
            raise InconsistentDatasetError("The number of raw and meta files is different.")

        raw_ids = sorted(int(file.stem.split("_")[0]) for file in raw_files)
        meta_ids = sorted(int(file.stem.split("_")[0]) for file in meta_files)

        if raw_ids != meta_ids:
            raise InconsistentDatasetError("Raw and meta file ids are different.")

        expected_ids = list(range(1, len(raw_ids) + 1))

        if raw_ids != expected_ids:
            raise InconsistentDatasetError("Article ids must go from 1 to N without gaps.")

        for raw_file in raw_files:
            if raw_file.stat().st_size == 0:
                raise InconsistentDatasetError(f"File {raw_file.name} is empty.")

    def _scan_dataset(self) -> None:
        """
        Register each dataset entry.

        Returns:
            dict[int, Article]: Articles storage
        """
        storage = {}

        for raw_file in sorted(self.path_to_raw_txt_data.glob("*_raw.txt")):
            article_id = int(raw_file.stem.split("_")[0])
            article = Article(url=None, article_id=article_id)
            article = from_raw(raw_file, article)
            storage[article_id] = article

        return storage

    def get_articles(self) -> dict:
        """
        Get storage params.

        Returns:
            dict: Storage params
        """
        return self._storage


class TextProcessingPipeline(PipelineProtocol):
    """
    Preprocess and morphologically annotate sentences into the CONLL-U format.
    """

    def __init__(
        self, corpus_manager: CorpusManager, analyzer: LibraryWrapper | None = None
    ) -> None:
        """
        Initialize an instance of the TextProcessingPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper | None, optional): Analyzer instance. Defaults to None.
        """
        self._corpus = corpus_manager
        self._analyzer = analyzer

    def run(self) -> None:
        """
        Perform basic preprocessing and write processed text to files.
        """
        articles = self._corpus.get_articles()

        for article in articles.values():
            to_cleaned(article)

            if isinstance(self._analyzer, UDPipeAnalyzer):
                conllu_text = self._analyzer.analyze([article.get_raw_text()])[0]
                article.set_conllu_info(conllu_text)
                self._analyzer.to_conllu(article)

class UDPipeAnalyzer(LibraryWrapper):
    """
    Wrapper for udpipe library.
    """

    #: Analyzer
    _analyzer: Language

    def __init__(self) -> None:
        """
        Initialize an instance of the UDPipeAnalyzer class.
        """
        self._analyzer = self._bootstrap()

    def _bootstrap(self) -> Language:
        """
        Load and set up the UDPipe model.

        Returns:
            Language: Analyzer instance
        """
        model_dir = pathlib.Path(__file__).parent / "assets" / "model"
        model_files = list(model_dir.glob("*.udpipe"))

        if not model_files:
            raise FileNotFoundError(
                "UDPipe model was not found in lab_6_pipeline/assets/model"
            )

        return spacy_udpipe.load_from_path(
            lang="ru",
            path=str(model_files[0]),
        )

    def analyze(self, texts: list[str]) -> list[str]:
        """
        Process texts into CoNLL-U formatted markup.

        Args:
            texts (list[str]): Collection of texts

        Returns:
            list[str]: List of documents
        """
        analyzed_texts = []

        for text in texts:
            doc = self._analyzer(text)
            conllu_lines = []
            sentence_id = 1

            for sentence in doc.sents:
                conllu_lines.append(f"# sent_id = {sentence_id}")
                conllu_lines.append(f"# text = {sentence.text}")

                for token_number, token in enumerate(sentence, start=1):
                    head_number = 0

                    if token.head != token:
                        head_number = token.head.i - sentence.start + 1

                    morph = str(token.morph) if str(token.morph) else "_"
                    misc = "_"

                    if not token.whitespace_:
                        misc = "SpaceAfter=No"

                    conllu_lines.append(
                        "\t".join(
                            [
                                str(token_number),
                                token.text,
                                token.lemma_,
                                token.pos_,
                                token.tag_ or "_",
                                morph,
                                str(head_number),
                                token.dep_,
                                "_",
                                misc,
                            ]
                        )
                    )

                conllu_lines.append("")
                sentence_id += 1

            analyzed_texts.append("\n".join(conllu_lines))

        return analyzed_texts

    def to_conllu(self, article: Article) -> None:
        """
        Save content to ConLLU format.

        Args:
            article (Article): Article containing information to save
        """
        path_to_save = article.get_file_path(ArtifactType.UDPIPE_CONLLU)
        conllu_info = article.get_conllu_info().rstrip("\n") + "\n\n"

        with open(path_to_save, "w", encoding="utf-8") as file:
            file.write(conllu_info)

    def from_conllu(self, article: Article) -> Doc:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            Doc: Document ready for parsing
        """
        raise NotImplementedError("This method is required for marks 8 and 10.")


class POSFrequencyPipeline:
    """
    Count frequencies of each POS in articles, update meta info and produce graphic report.
    """

    def __init__(self, corpus_manager: CorpusManager, analyzer: LibraryWrapper) -> None:
        """
        Initialize an instance of the POSFrequencyPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper): Analyzer instance
        """

    def _count_frequencies(self, article: Article) -> dict[str, int]:
        """
        Count POS frequency in Article.

        Args:
            article (Article): Article instance

        Returns:
            dict[str, int]: POS frequencies
        """

    def run(self) -> None:
        """
        Visualize the frequencies of each part of speech.
        """


class PatternSearchPipeline(PipelineProtocol):
    """
    Search for the required syntactic pattern.
    """

    def __init__(
        self, corpus_manager: CorpusManager, analyzer: LibraryWrapper, pos: tuple[str, ...]
    ) -> None:
        """
        Initialize an instance of the PatternSearchPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper): Analyzer instance
            pos (tuple[str, ...]): Root, Dependency, Child part of speech
        """

    def _make_graphs(self, doc: Doc) -> list[DiGraph]:
        """
        Make graphs for a document.

        Args:
            doc (Doc): Document for patterns searching

        Returns:
            list[DiGraph]: Graphs for the sentences in the document
        """

    def _add_children(
        self, graph: DiGraph, subgraph_to_graph: dict, node_id: int, tree_node: TreeNode
    ) -> None:
        """
        Add children to TreeNode.

        Args:
            graph (DiGraph): Sentence graph to search for a pattern
            subgraph_to_graph (dict): Matched subgraph
            node_id (int): ID of root node of the match
            tree_node (TreeNode): Root node of the match
        """

    def _find_pattern(self, doc_graphs: list) -> dict[int, list[TreeNode]]:
        """
        Search for the required pattern.

        Args:
            doc_graphs (list): A list of graphs for the document

        Returns:
            dict[int, list[TreeNode]]: A dictionary with pattern matches
        """

    def run(self) -> None:
        """
        Search for a pattern in documents and writes found information to JSON file.
        """


def main() -> None:
    """
    Entrypoint for pipeline module.
    """
    corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
    analyzer = UDPipeAnalyzer()
    pipeline = TextProcessingPipeline(corpus_manager, analyzer)
    pipeline.run()


if __name__ == "__main__":
    main()
