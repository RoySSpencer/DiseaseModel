import networkx as nx
import random
import matplotlib.pyplot as plt

def main():
    graphs = LoadFile()
    G = StartInfection(graphs[0])
    color_map = MakeColorMap(G)

    print("Day: 0")
    statuses = ListStatus(G)
    print(statuses)

    nx.draw_circular(G, node_color=color_map, with_labels=True, font_weight='bold')
    plt.show()

    for i in range(0, 5):
        G = SpreadInfection(G)
        # color_map = MakeColorMap(G)
        # nx.draw(G, node_color=color_map, with_labels=True, font_weight='bold')
        # plt.show()

        G = UpdateInfection(G)
        color_map = MakeColorMap(G)

        print("Day: " + str(i + 1))
        statuses = ListStatus(G)
        print(statuses)

        nx.draw_circular(G, node_color=color_map, with_labels=True, font_weight='bold')
        plt.show()



def SpreadInfection(G):
    for edges in G.edges:
        if (G.nodes[edges[0]]["status"] == "Healthy" and G.nodes[edges[1]]["status"] == "Infected") or (G.nodes[edges[0]]["status"] == "Infected" and G.nodes[edges[1]]["status"] == "Healthy"):
            node = edges[0]
            if G.nodes[edges[1]]["status"] == "Healthy":
                node = edges[1]

            if random.randint(0, 4) == 0:
                G.nodes[node]["status"] = "Newly Infected"

        # print(edges[0] + ":" + G.nodes[edges[0]]["status"])
        # print(edges[1] + ":" + G.nodes[edges[1]]["status"])
        # print()
    return G

def UpdateInfection(G):
    for node_data in G.nodes.data():
        node = G.nodes[node_data[0]]
        if node['status'] == "Infected":
            node['days_remaining'] -= 1
            if node['days_remaining'] == 0:
                node['status'] = "Recovered"
        elif node["status"] == "Newly Infected":
            node['status'] = "Infected"
            node['days_remaining'] = 2
    return G

def StartInfection(G):
    for node_data in G.nodes.data():
        node = G.nodes[node_data[0]]
        if random.randint(0, 3) == 0:
            node['status'] = "Infected"
            node['days_remaining'] = 2
        else:
            node['status'] = "Healthy"
    return G

def MakeColorMap(G):
    color_map = list()
    for node_data in G.nodes.data():
        node = G.nodes[node_data[0]]
        if node['status'] == "Infected":
            color_map.append("red")
        elif node['status'] == "Healthy":
            color_map.append("blue")
        elif node["status"] == "Newly Infected":
            color_map.append("yellow")
        elif node['status'] == "Recovered":
            color_map.append("green")
    return color_map

def ListStatus(G):
    statuses = dict()
    for node_data in G.nodes.data():
        node = G.nodes[node_data[0]]
        if node['status'] not in statuses:
            statuses[node['status']] = list()
        statuses[node['status']].append(node_data[0])
    return statuses

def LoadFile():
    graph_list = list()
    with open('12_3_3.txt') as f:
        isGraph = True
        count = 0
        entry = 0
        for x in f:
            if x.startswith("Graph"):
                isGraph = True
                graph_list.append(dict())
                entry = 1
            elif x.startswith("Taillenweite"):
                isGraph = False
                count += 1
            elif isGraph and x.strip() != "":
                graph_list[count][entry] = x.split(":")[1].strip().split(" ")
                entry += 1
    count = 0
    graphs = list()
    for graph in graph_list:
        count += 1
        G = nx.Graph()
        for key in graph:
            for edge in graph[key]:
                G.add_edge(str(key), edge)
        graphs.append(G)

    return graphs
