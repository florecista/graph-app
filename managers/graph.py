from PyQt5.QtCore import QObject




class GraphManager(QObject):

    """ Graph Manager

    Provides an interface for working with Graphs from the UI.

    There are two active graphs: the global graph and the current
    active subgraph. Most operations act on the active subgraph.
    """


    def __init__(self):
        self.G = QObject()
        self.cur_G = QObject()

        self.init_graph_attributes()

    def init_graph_attributes(self):
        print('')
        # self.G.graph.setdefault("edge_font_size", 8)
        #
        # # Style Tab
        # self.G.graph.setdefault("use_node_image", False)
        # self.G.graph.setdefault("use_node_icon", True)
        # self.G.graph.setdefault("show_node_label", True)
        #
        # self.G.graph.setdefault("image_width", 30)
        # self.G.graph.setdefault("image_height", 30)
        # self.G.graph.setdefault("label_position", constants.LabelPosition.Below.value)
        # self.G.graph.setdefault("node_font_size", 8)
        # self.G.graph.setdefault("node_shape_style", 'o')
        #
        # self.G.graph.setdefault("node_foreground_color", '#000000')
        # self.G.graph.setdefault("node_background_color", '#ff0000')
        #
        # self.G.graph.setdefault("node_highlight_color", '#0000ff')
        # self.G.graph.setdefault("node_label_color", '#00ff00')
        #
        # self.G.graph.setdefault("use_edge_label", False)
        # self.G.graph.setdefault("use_edge_arrow", False)
        #
        # # Advanced Tab
        # self.G.graph.setdefault("centrality_type", constants.CentralityType.Select.value)
        # self.G.graph.setdefault("centrality_show_by", constants.CentralityShowBy.Select.value)
        # self.G.graph.setdefault("centrality_gradient", constants.CentralityGradient.Select.value)
        #
        # self.G.graph.setdefault("g_type", constants.GraphLayout.Select.value)
        # self.G.graph.setdefault("graph_hide_orphans", constants.GraphHideOrphans.No.value)

    @property
    def graph(self):
        return self._graph

    def open_graphml(self, filename: str) -> None:
        print('test')
        # G = nx.read_graphml(filename)
        # for name in G.nodes:
        #     node = G.nodes[name]
        #     js_manager.update_node(node)
        #     if 'Attributes' in node.keys():
        #         node['Attributes'] = [ast.literal_eval(item) for item in node['Attributes'].split(';')]
        #     if 'Image' in node.keys():
        #         node['Image'] = ast.literal_eval(node['Image'])
        # self.G = G
        # self.init_graph_attributes()

    def save_graphml(self, filename: str) -> None:
        print('test')
        # G = self.G.copy(as_view=False)
        # for name in G.nodes:
        #     node = G.nodes[name]
        #     node.update(self.G.nodes[name].copy())
        #     if 'Attributes' in node.keys():
        #         node['Attributes'] = ';'.join([str(item) for item in node['Attributes']])
        #     if 'Image' in node.keys():
        #         node['Image'] = str(node['Image'])
        # nx.write_graphml(G, filename)

    def clear_graph(self) -> None:
        self.G.clear()
        self.init_graph_attributes()

    def get_centrality(self):
        print('test')
        # if self.G.graph['centrality_type'] == constants.CentralityType.Degrees.value:
        #     degree_centrality = nx.degree_centrality(self.G)
        #     return np.fromiter(degree_centrality.values(), float)
        #
        # if self.G.graph['centrality_type'] == constants.CentralityType.Eigenvactor.value:
        #     eigenvector_centrality = nx.eigenvector_centrality(self.G)
        #     return np.fromiter(eigenvector_centrality.values(), float)
        #
        # if self.G.graph['centrality_type'] == constants.CentralityType.Katz.value:
        #     katz_centrality = nx.katz_centrality(self.G, alpha=0.1, beta=1.0)
        #     return np.fromiter(katz_centrality.values(), float)
        #
        # if self.G.graph['centrality_type'] == constants.CentralityType.Betweenness.value:
        #     betweenness_centrality = nx.betweenness_centrality(self.G)
        #     return np.fromiter(betweenness_centrality.values(), float)
        #
        # if self.G.graph['centrality_type'] == constants.CentralityType.PageRank.value:
        #     pagerank_centrality = nx.pagerank(self.G, alpha=0.1)
        #     return np.fromiter(pagerank_centrality.values(), float)
        #
        # if self.G.graph['centrality_type'] == constants.CentralityType.Closeness.value:
        #     closeness_centrality = nx.closeness_centrality(self.G)
        #     return np.fromiter(closeness_centrality.values(), float)

    @property
    def cur_edges(self):
        return list(self.cur_G.edges(data=True))

    def get_cur_edge_by_index(self, index):
        edges = list(self.cur_edges)
        return edges[index]

    def get_cur_edge_value(self, index, row):
        u, v, d = self.get_cur_edge_by_index(index)
        properties = self.cur_G[u][v]
        name = list(d.keys())[row]
        return properties[name]

    def set_cur_edge_value(self, index, row, value):
        u, v, d = self.get_cur_edge_by_index(index)
        properties = self.cur_G[u][v]
        name = list(d.keys())[row]
        properties[name] = value

    def get_available_node_name(self, label):
        """Takes a given label and iterates adding a numeric suffix
        until it finds an available node name.
        """
        node_label_suffix = 1
        while True:
            node_name = "{} {}".format(label, node_label_suffix)
            if node_name not in self.G.nodes:
                break
            node_label_suffix += 1
        return node_name



graphm = GraphManager()