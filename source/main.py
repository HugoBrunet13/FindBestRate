from vertex import Vertex
from edge import Edge
from graph import Graph
from dateutil import parser
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt


def main():
    exchange_rate_graph = Graph()

    #stdin -> new price price_updates stream
    stream_price_updates = ["2017-11-03T09:42:23+00:00 KRAKEN BTC USD 1001.0 0.0009",
                            "2017-11-03T09:43:23+00:00 GDAX BTC USD 1000.0 0.0008"]
    # Add information to graph
    exchange_rate_graph.add_price_updates(stream_price_updates)
    # Print edges on stdout
    print("Last version of the graph:\n"+str(exchange_rate_graph))


    print("Let's add new information to the graph...")
    # stdin -> new price_updates stream (more recent data + new information)
    stream_price_updates = ["2018-11-03T09:42:23+00:00 KRAKEN BTC USD 1000.0 0.0009",
                            "2018-11-03T09:43:23+00:00 GDAX BTC USD 1001.0 0.0008",
                            "2018-11-03T09:43:23+00:00 BITFINEX BTC USD 1002.0 0.0009",
                            "2018-11-03T09:43:23+00:00 BINANCE BTC USD 1001.0 0.0008",
                            "2018-11-03T09:43:23+00:00 BITTREX ETH EUR 190.0 0.004"]
    
    # Add information to graph
    exchange_rate_graph.add_price_updates(stream_price_updates)
    # Print edges on stdout
    print("\nLast version of the graph:\n" + str(exchange_rate_graph))

    # stdin -> enter rate_request, format: <source_exchange> <source_currency> <destination_exchange> <destination_currency>
    rate_request = input_rate_request(exchange_rate_graph)

    best_path = exchange_rate_graph.find_best_path(rate_request[0], rate_request[1]) # best path computation
    best_rate = exchange_rate_graph.compute_best_rate_from_best_path(best_path) # best rate computation

    print(output_formatting(best_path,  best_rate)) # print result on stdout
    draw_graph(exchange_rate_graph.list_edges,best_path, best_rate) #draw graph with result


def input_rate_request(graph):
    while True:
        try:
            rate_request = "ECHANGE_RATE_REQUEST "+input("Type your exchange rate request: EXCHANCE_RATE_REQUEST ")
            graph.list_vertices.index(Vertex(rate_request.split(" ")[1], rate_request.split(" ")[2]))
            graph.list_vertices.index(Vertex(rate_request.split(" ")[3], rate_request.split(" ")[4]))
            u = Vertex(rate_request.split(" ")[1], rate_request.split(" ")[2])
            v = Vertex(rate_request.split(" ")[3], rate_request.split(" ")[4])
            break
        except ValueError:
            print("Error: Input incorrect, pairs ('exchange' 'currency') must exist in the graph, try an other request!!!!")
        except IndexError:
            print("Error: Incomplete request, try an other one!! \nFormat: <source_exchange> <source_currency> "
                                                                    "<destination_exchange> <destination_currency>")
        except Exception:
            print("Error: Try an other request")
    return (u,v)

def output_formatting(path, best_rate):
    """ Function which allow to display on stdout the result of the exchange rate request"""
    if path:
        return "BEST_RATES_BEGIN " + \
                 path[0].exchange + " " + \
                 path[0].currency + " " + \
                 path[-1].exchange + " " + \
                 path[-1].currency + " " + \
                 str(best_rate) + '\n' + \
                 ''.join([str(vertex)+'\n' for vertex in path]) + \
                 "BEST_RATES_END"
    else:
        return "NO PATH FOUND"

def draw_graph(data, best_path=[], best_rate=None, node_size=11000, node_color='grey', node_alpha=0.5, node_text_size=14,
               edge_color='grey', edge_alpha=1, edge_tickness=2, edge_text_pos=0.8, text_font='sans-serif',
               edge_label_font_size=15):
    """ Procedure which allow to draw and plot the graph, using Networkx (creat a graph)and Matplotlib (plot) packages

    """

    # create Networkx graph
    G=nx.Graph()

    # get edges as couple(edge_A, edge_B)
    graph=[(str(data[i].vertex_source),str(data[i].vertex_destination)) for i in range(len(data))]
    # add edges to the graph
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # fix dispositon of the graph
    graph_pos=nx.shell_layout(G)

    #get weight data
    labels = [str(data[i].weight) for i in range(len(data))]
    edges_labels = dict(zip(graph, labels))

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color) #nodes formatting
    nx.draw_networkx_edges(G, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color) #edges formatting
    nx.draw_networkx_labels(G, graph_pos, font_size=node_text_size, font_family=text_font)#labels formatting
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edges_labels, font_size= edge_label_font_size,
                                                                        label_pos=edge_text_pos) #edges label (weight formatting)

    # if best_path and best_rate are not empty or null, change color of edges and nodes of best_path
    # Networkx needs edges information as list of couple (vertex_A, vertex_B) and nodes information as list of node
    if best_path and best_rate:
        nodes_best_path_in_G = [str(vertex) for vertex in best_path]
        edges_best_path_in_G = []
        for i in range(0, len(best_path)-1):
            edges_best_path_in_G.append( ( str(best_path[i]),str(best_path[i+1])))
        nodes_best_path_in_G.append(str(best_path[-1]))
        # change color of nodes of the best path
        nx.draw_networkx_nodes(G, graph_pos, nodelist=nodes_best_path_in_G, node_size=node_size,
                                                                            alpha=node_alpha, node_color='g')
        # change oolor of esges of the best path
        nx.draw_networkx_edges(G, graph_pos, edgelist= edges_best_path_in_G,  width=5,

                                                                            alpha=edge_alpha, edge_color='g')
        # add title
        plt.title("BEST RATE REQUEST "+str(best_path[0]).replace(',','') + " " +
                                       str(best_path[-1]).replace(',','') + ' ' +
                                       str(best_rate), fontsize=25, color = 'g')

    plt.axis('off') # don't show axis
    plt.show() # show the graph!

main()