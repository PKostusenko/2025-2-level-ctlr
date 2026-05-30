"""
Visualizer module for visualizing PosFrequencyPipeline results.
"""

from pathlib import Path
from typing import Callable

from quality_control.console_logging import get_child_logger

logger = get_child_logger(__file__)

try:
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.use("agg")
except ImportError:  # pragma: no cover
    logger.warning("No libraries installed. Failed to import.")

try:
    import networkx as nx
    from networkx import DiGraph
except ImportError:  # pragma: no cover
    DiGraph = None  # type: ignore
    logger.warning("No libraries installed. Failed to import.")

from core_utils.article.article import Article  # pylint: disable=wrong-import-position


def visualize(article: Article, path_to_save: Path) -> None:
    """
    Visualize PosFrequencyPipeline results.

    Args:
        article (Article): Article instance
        path_to_save (pathlib.Path): Path to result image
    """
    statistics = article.get_pos_freq()
    number_of_tags = len(statistics)
    sorted_frequencies = sorted(statistics.values(), reverse=True)
    get_occurrences: Callable = lambda x: statistics[x]
    sorted_tags = sorted(statistics, key=get_occurrences, reverse=True)
    pos_tags = list(range(number_of_tags))
    colors = ("b", "g", "r", "c")

    figure = plt.figure()
    axis = figure.add_subplot(1, 1, 1)
    for i in range(0, number_of_tags):
        axis.bar(
            pos_tags[i],
            sorted_frequencies[i],
            align="center",
            width=0.5,
            color=colors[i % len(colors)],
        )

    axis.set_xticks(pos_tags)
    axis.set_xticklabels(sorted_tags)
    plt.setp(sorted_tags)
    plt.xticks(rotation=20)
    y_max = max(sorted_frequencies) + 1
    plt.ylim(0, y_max)

    plt.savefig(path_to_save)


def show_graph(graph: DiGraph, graph_path: str) -> None:
    """
    Visualization for debug.

    Args:
        graph (DiGraph): Graph to check
        graph_path (str): Path to graph
    """
    # Check what to use on Windows! Below line is obviously only for macOS users
    matplotlib.use("MacOSX")

    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")

    nx.draw(
        graph,
        pos,
        with_labels=True,
        labels=nx.get_node_attributes(graph, "upos"),
        **{
            "node_color": "orange",
            "edge_color": "powderblue",
            "node_size": 400,
            "width": 2,
        },
    )
    plt.savefig(graph_path, format="png")
    plt.close()
