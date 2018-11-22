from vertex import Vertex
from edge import Edge
from dateutil import parser
from datetime import datetime

class Graph(object):
    """ Main class of this project: allows to store and compute all information of a graph

    Args:
        list_vertices: list of all vertices of the graph
        list_edges: list of all edges of the graph
        rates: matrix representation of weight between edges of the graph
        next: transition matrix
    """

    def __init__(self):
        """ Default constructor, no parameter needed to create a graph
        The graph will be modify after reception of prices_update stream """
        self.__list_vertices = []
        self.__list_edges = []
        self.__rates = [[]]
        self.__next = [[]]

    @property
    def list_vertices(self):
        """ Get list_vertices parameter """
        return self.__list_vertices

    @property
    def list_edges(self):
        """ Get list_edges parameter """
        return self.__list_edges

    @property
    def rates(self):
        """ Get rates parameter """
        return self.__rates

    @property
    def next(self):
        """ Get next parameter """
        return self.__next

    def __str__(self):
        """" Formatting of print option for a graph: we print all edges information """
        return ''.join([str(edge) + '\n' for edge in self.list_edges])

    def add_price_updates(self, stream_price_updates):
        """ Procedure which allow to update the graph with the last prices information received """

        # A stream of price_updates can contain several updates
        for price_update in stream_price_updates:
            data = price_update.split()

            # Creation of two edges with the data provided in the price_update stream:
            # Edge(vertex_a, vertex_b, weight_from_a_b, date) and Edge(vertex_b, vertex_a, weight_from_b_a, date)
            try:
                e1, e2 = Edge(Vertex(data[1], data[2]), Vertex(data[1], data[3]), float(data[4]), data[0]), \
                         Edge(Vertex(data[1], data[3]), Vertex(data[1], data[2]), float(data[5]), data[0])
            except Exception:
                print("Error input data: price_update stream incorrect -> ", price_update, " -> error in this stream")
                continue

            # if not (e2.weight <= 1 and e2.weight >= 1/e1.weight):
            #     raise ValueError("The input price_update is not correct!")

            # For these two edges created, before we add them to the graph, we have to check if they don't already
            # exist in it. We don't do this verification by comparing the edge objects between them, because even if
            # there is already an edge corresponding to a couple (vertex_a, vertex_b), the date property of the edge
            # in the graph will be different from the date of the new edge created with last weight value
            if self.couple_vertex_exist(e1.vertex_source, e1.vertex_destination) == -1:
                # There is no edge in the graph between the couple (vertex_a, vertex_b) so we add the new edge to the graph
                self.add_edge(e1)
            elif e1.date > self.list_edges[self.couple_vertex_exist(e1.vertex_source, e1.vertex_destination)].date:
                # The couple of vertices (vertex_a, vertex_b) exists, so we have to compare the date of the old edge
                # already in the graph with the date of the new edge created with the data from price_update,
                # if the condition is satisfied, we modify the  edge in the graph with new weight value,
                # and we update the date of the edge
                self.list_edges[self.couple_vertex_exist(e1.vertex_source, e1.vertex_destination)].weight = float(
                    e1.weight)
                self.list_edges[self.couple_vertex_exist(e1.vertex_source, e1.vertex_destination)].date = str(e1.date)
            if self.couple_vertex_exist(e2.vertex_source, e2.vertex_destination) == -1:  # same test for second edge
                self.add_edge(e2)
            elif e2.date > self.list_edges[self.couple_vertex_exist(e2.vertex_source, e2.vertex_destination)].date:
                self.list_edges[self.couple_vertex_exist(e2.vertex_source, e2.vertex_destination)].weight = e2.weight
                self.list_edges[self.couple_vertex_exist(e2.vertex_source, e2.vertex_destination)].date = str(e2.date)

            # Now, we have to check if we have to create or not an edge between the two vertices with same currency
            # but different exchanges
            self.add_new_edge_same_currency_different_exchanges(e1.vertex_source)
            self.add_new_edge_same_currency_different_exchanges(e2.vertex_source)

            # The update of the graph is done so we can compute the best rates matrix using
            # the modified Floyd Warshall algorithm
        self.compute_best_rates_matrix()

    def add_edge(self, edge):
        """ Procedure which allows to add an edge on the graph and to add the corresponding vertices to the list_vertices
        attribute of the graph """
        self.__list_edges.append(edge)
        try:  # We check if the vertices we want to add are not already stored in our list of vertices
            self.__list_vertices.index(edge.vertex_source)
        except:
            self.__list_vertices.append(edge.vertex_source)

    def couple_vertex_exist(self, u, v):
        """ Function which allows to find the position of an edge composed by two vertices 'u' and 'v' in the list_edges
            of the graph:
                return -1 if there is no existing edge between (v1, v2) in the graph
                return the position of the edge in the list of all edges if an edge between v1 -> v2 exists """
        i = 0
        for e in self.list_edges:
            if e.vertex_source == u and e.vertex_destination == v:
                return i
            i += 1
        return -1

    def add_new_edge_same_currency_different_exchanges(self, vertex):
        """ Procedure which allows to add an edge between two vertices with identical currencies but different exchanges """

        # Before adding a new edge, we check if this edge already exists or not
        # We get all indexes of edges from the list_edges which have the same currency attribute as the vertex currency
        # attribut passed as a parameter
        tab_index = self.find_edge_same_currency_different_exchanges(vertex)
        for i in tab_index:
            # For each edge in list_edges at the position i, we check if an edge between the vertex we test and
            # the vertex_source of the edges at the position i in the list_edges already exists or not.
            # If the condition is not satisfied, we create two new edges with same currency and different exchanges
            if self.couple_vertex_exist(vertex, self.list_edges[i].vertex_source) == -1 and \
                            self.couple_vertex_exist(self.list_edges[i].vertex_source, vertex) == -1:
                self.list_edges.append(
                    Edge(vertex, self.list_edges[i].vertex_source, 1.0, str(datetime.now())))
                self.list_edges.append(
                    Edge(self.list_edges[i].vertex_source, vertex, 1.0, str(datetime.now())))

    def find_edge_same_currency_different_exchanges(self, vertex):
        """ Function which allows to get a list of index of edges from the list_edges, which have the same currency
            but a different exchange, compared to the vertex passed as a parameter
            We use this function to get all edges positions from the list_edges which vertex_source currency attribute
            is the same as the currency of the vertex passed as a parameter """

        list_index, i = [], 0
        for edge in self.list_edges:
            if edge.vertex_source.currency == vertex.currency and edge.vertex_source.exchange != vertex.exchange:
                list_index.append(i)
            i += 1
        return list_index

    def compute_best_rates_matrix(self):
        """ Function which allows to compute the best rates matrix
            This procedure is a modified version of the Floyd Warshall algorithm.
         """

        # Creation of two empty matrices
        rates = [[0 for i in range(len(self.list_vertices))] for j in range(len(self.list_vertices))]
        next = [[None for i in range(len(self.list_vertices))] for j in range(len(self.list_vertices))]

        # Now, we want to complete rates matrice with the weights of the edges.
        # However, the Floyd Warshall algorithm can run only if the weights w are between 0 and 1
        # So we have to normalize the weight of edges!
        # To do so, we use the formula w'=(w-Wmin)/(Wmax-Wmin)
        # w': normalized weight
        # w: normal weight
        # Wmin: min weight among all edges weight, Wmax: max weight among all edges weight

        all_weights= [edge.weight for edge in self.list_edges] #get all weights of edges
        min_rate = min(all_weights) # get minimum weight
        max_rate=max(all_weights)# get maximum weight

        # We complete the two matrices with data from the list of edges
        i, j = 0, 0
        for i in range(0, len(rates[0])):
            for j in range(0, len(rates[0])):
                if isinstance(self.get_edge_from_couple_vertices(self.list_vertices[i], self.list_vertices[j]), Edge):
                    w = self.get_edge_from_couple_vertices(self.list_vertices[i], self.list_vertices[j]).weight
                    if w == 1:
                        rates[i][j]=1.0
                    elif w == 0:
                        rates[i][j]=0
                    else:
                        rates[i][j] = (w - min_rate) / (max_rate - min_rate) #weight normalization
                    next[i][j] = next[i][j] = self.get_edge_from_couple_vertices(self.list_vertices[i], self.list_vertices[j]).vertex_destination
                else:
                    rates[i][j] =0
                    next[i][j] = None

        # We compute the best rates matrix and the next matrix thanks to the modified Floyd Warshall algorithm
        for k in range(0, len(self.list_vertices)):
            for i in range(0, len(self.list_vertices)):
                for j in range(0, len(self.list_vertices)):
                    if rates[i][j] < rates[i][k] * rates[k][j]:
                        rates[i][j] = rates[i][k] * rates[k][j]
                        next[i][j] = next[i][k]

        self.__rates = rates
        self.__next = next

    def get_edge_from_couple_vertices(self, v1, v2):
        """ Function which returns the edge corresponding to the couple of vertices (v1, v2) """

        for e in self.list_edges:
            if e.vertex_source == v1 and e.vertex_destination == v2:
                return e
        return None

    def find_best_path(self, u, v):
        """ Function which allows to browse the next matrix so as to rebuilt the path from vertex u to vertex v """

        if self.next[self.list_vertices.index(u)][self.list_vertices.index(v)] is None:
            return []
        path = []
        path.append(u)
        while u != v:
            u = self.next[self.list_vertices.index(u)][self.list_vertices.index(v)]
            path.append(u)

        return path

    def compute_best_rate_from_best_path(self, best_path):

        """ Function which allow to compute the best rate """
        best_rate=1
        for i in range(0, len(best_path)-1):
            best_rate *= self.get_edge_from_couple_vertices(best_path[i],best_path[i+1]).weight
        return best_rate

