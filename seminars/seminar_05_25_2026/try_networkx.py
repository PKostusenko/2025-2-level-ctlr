"""
Listing for practice with spacy-udpipe module

0. Installation

networkx is not a standard Python library: it is not pre-installed.
Make sure to specify library name and version in the requirements.txt file!
Make sure to install the library in your working environment!
"""

try:
    import networkx as nx
    from networkx.algorithms.isomorphism import DiGraphMatcher
except ImportError:
    print("No libraries installed. Failed to import.")


def simple_graph_example() -> nx.DiGraph:
    """
    1. Simple graph: example

    Let's explore the basic structures of directed graphs
    in `networkx` library by creating a graph
    from [/images/example_1_simple_graph.png]

    Directed graphs are presented as instances of class `nx.DiGraph`.
    In this example, we create an empty graph first and then
    fill it with nodes and edges.

    To add one node, use `nx.DiGraph.add_node` method.
    The first argument to this method
    serves as a name of the node.

    To add an edge, use `nx.DiGraph.add_edge` method.
    The first argument is the name of the node
    from there the edge starts.
    The second argument is the name of the node
    to which the edge points.

    Returns:
        nx.DiGraph: graph as in [/images/example_1_simple_graph.png]
    """
    simple_graph = nx.DiGraph()
    for node in [0, 1, 2, 3]:
        simple_graph.add_node(node)
    for from_vertex, to_vertex in [(0, 1), (1, 2), (2, 3)]:
        simple_graph.add_edge(from_vertex, to_vertex)
    return simple_graph


def simple_graph_task() -> nx.DiGraph:
    """
    1. Simple graph: task

    Create a graph as in [/images/task_1_simple_graph.png]
    using `networkx` library.

    Returns:
        nx.DiGraph: graph as in [/images/task_1_simple_graph.png]
    """
    # YOUR CODE GOES HERE


def family_graph_example() -> nx.DiGraph:
    """
    1. Hard graph: example

    `networkx` library allows labeling
    edges as well as nodes.

    Take a look at graph in [/images/example_2_family_graph.png].
    Notice that in this graph nodes have not only names
    but also additional properties: eyes color, age.
    To specify such properties of the node,
    pass homonymous keyword arguments to the method
    `nx.DiGraph.add_node`.

    The same applies to the `nx.DiGraph.add_edge` method.
    Notice that in the example graph edges have labels.
    To specify them, pass a `label` keyword with
    appropriate value.

    In fact, for both `add_node` and `add_edge` method
    there are no restrictions on keyword argument names,
    you can name them anything you want as long as
    you stay consistent.

    Returns:
        nx.DiGraph: graph as in [/images/example_2_family_graph.png]
    """
    relatives = {
        "Оля": {"age": 56, "eyes": "blue"},
        "Петя": {"age": 60, "eyes": "brown"},
        "Юля": {"age": 36, "eyes": "brown"},
        "Никита": {"age": 35, "eyes": "blue"},
        "Костя": {"age": 10, "eyes": "blue"},
    }

    family_graph = nx.DiGraph()
    for name, features in relatives.items():
        family_graph.add_node(name, age=features["age"], eyes=features["eyes"])

    family_graph.add_edge("Оля", "Юля", label="mother")
    family_graph.add_edge("Петя", "Юля", label="father")
    family_graph.add_edge("Юля", "Костя", label="mother")
    family_graph.add_edge("Никита", "Костя", label="father")

    return family_graph


def family_graph_task() -> nx.DiGraph:
    """
    2. Hard graph: task

    Create a graph as in [/images/task_2_family_graph.png]
    using `networkx` library.

    Returns:
        nx.DiGraph: graph as in [/images/task_2_family_graph.png]
    """
    # relatives = {
    #     "Настя": {"age": 66, "hair": "blonde"},
    #     "Дима": {"age": 70, "hair": "ginger"},
    #     "Степа": {"age": 41, "hair": "black"},
    #     "Вика": {"age": 40, "hair": "ginger"},
    #     "Лида": {"age": 15, "hair": "black"},
    # }
    # YOUR CODE GOES HERE


def match_subgraph_example() -> list[dict[str, str]]:
    """
    3. Subgraph matching: example

    We can find isomorphic subgraphs using `DiGraphMatcher` instance.
    It accepts two graphs and traverses them in the same order.
    At each step, it compares the two nodes given the
    criteria passed as a third argument.

    Example below specified the eye color change pattern,
    matches the two graphs and extracts from the graph
    the family line with the specified eye colors.
    (see [/images/example_3_subgraph_matching.png])

    Returns:
        list[dict[str, str]]: isomorphic match as in
                              [/images/example_3_subgraph_matching.png]
    """
    family_graph = family_graph_example()

    target_features = {
        "grandparent": {"eyes": "blue"},
        "parent": {"eyes": "brown"},
        "child": {"eyes": "blue"},
    }

    target_graph = nx.DiGraph()
    for name, features in target_features.items():
        target_graph.add_node(name, eyes=features["eyes"])
    target_graph.add_edge("grandparent", "parent")
    target_graph.add_edge("parent", "child")

    matcher = DiGraphMatcher(
        family_graph,
        target_graph,
        node_match=lambda node_1, node_2: node_1["eyes"] == node_2["eyes"],
    )
    return list(matcher.subgraph_isomorphisms_iter())


def match_subgraph_task() -> list[dict[str, str]]:
    """
    3. Subgraph matching: task

    Match the specified hair color change pattern
    as in [/images/task_3_subgraph_matching.png].

    Returns:
        list[dict[str, str]]: isomorphic match as in
                              [/images/task_3_subgraph_matching.png]
    """
    # YOUR CODE GOES HERE


def main() -> None:
    """
    Entrypoint for a seminar's listing
    """

    # 1. Easy graphs
    simple_graph_sample = simple_graph_example()
    assert nx.to_dict_of_dicts(simple_graph_sample) == {
        0: {1: {}},
        1: {2: {}},
        2: {3: {}},
        3: {},
    }

    # simple_graph = simple_graph_task()
    # assert nx.to_dict_of_dicts(simple_graph) == {
    #     2: {3: {}, 4: {}},
    #     3: {},
    #     4: {5: {}},
    #     5: {},
    #     1: {2: {}},
    # }

    # 2. Hard graphs
    family_graph_sample = family_graph_example()
    assert nx.to_dict_of_dicts(family_graph_sample) == {
        "Оля": {"Юля": {"label": "mother"}},
        "Петя": {"Юля": {"label": "father"}},
        "Юля": {"Костя": {"label": "mother"}},
        "Никита": {"Костя": {"label": "father"}},
        "Костя": {},
    }

    # family_graph = family_graph_task()
    # assert nx.to_dict_of_dicts(family_graph) == {
    #     "Настя": {"Степа": {"label": "mother"}},
    #     "Дима": {"Вика": {"label": "father"}},
    #     "Степа": {"Лида": {"label": "father"}},
    #     "Вика": {"Лида": {"label": "mother"}},
    #     "Лида": {},
    # }

    # 3. Subgraph matching
    matches_sample = match_subgraph_example()
    assert matches_sample == [{"Оля": "grandparent", "Юля": "parent", "Костя": "child"}]

    # matches = match_subgraph_task()
    # assert matches == [{'Настя': 'grandparent', 'Степа': 'parent', 'Лида': 'child'}]


if __name__ == "__main__":
    main()
