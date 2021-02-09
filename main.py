import networkx as nx
import random
import matplotlib.pyplot as plt

def main(plot=False, load=False, prnt_list=False, start_percent=5, infect_percent=15,
        days_infected=3, nodes=100, type="watts", draw="circular", vaccinate_percent=0, vaccine_affectiveness=0):
    num_days = list()
    num_healthy = list()
    for i in range(0, 10):
        if load:
            graphs = LoadFile()
        else:
            graphs = GetRandomGraph(nodes, type)
        print("Clustering Coefficient: " + str(nx.clustering(graphs[0])))
        G = StartInfection(graphs[0], start_percent, days_infected)
        G = Vaccinate(graphs[0], vaccinate_percent)
        color_map = MakeColorMap(G)


        statuses = ListStatus(G)
        if prnt_list:
            print("Day: 0")
            print(statuses)

        if plot:
            if draw == "circular":
                nx.draw_circular(G, node_color=color_map, with_labels=True, font_weight='bold')
            else:
                nx.draw(G, node_color=color_map, with_labels=True, font_weight='bold')
            plt.show()

        # for i in range(0, 10):
        i = 0
        while "Infected" in statuses:
            G = SpreadInfection(G, infect_percent,vaccine_affectiveness)
            # color_map = MakeColorMap(G)
            # nx.draw(G, node_color=color_map, with_labels=True, font_weight='bold')
            # plt.show()

            G = UpdateInfection(G, days_infected)
            color_map = MakeColorMap(G)

            i += 1
            statuses = ListStatus(G)
            if prnt_list:
                print("Day: " + str(i))
                print(statuses)

            if plot:
                if draw == "circular":
                    nx.draw_circular(G, node_color=color_map, with_labels=True, font_weight='bold')
                else:
                    nx.draw(G, node_color=color_map, with_labels=True, font_weight='bold')
                plt.show()
        num_days.append(i)
        num_healthy.append(len(statuses['Healthy']))
    print(num_days)
    print(num_healthy)


def Vaccinate(G, vaccinate_percent):
    for node_data in G.nodes.data():
        node = G.nodes[node_data[0]]
        if random.randint(0, 100) < vaccinate_percent:
            node['vaccinated'] = True
        else:
            node['vaccinated'] = False
    return G

def SpreadInfection(G, infect_percent, vaccine_affectiveness):
    for edges in G.edges:
        if (G.nodes[edges[0]]["status"] == "Healthy" and G.nodes[edges[1]]["status"] == "Infected") or (G.nodes[edges[0]]["status"] == "Infected" and G.nodes[edges[1]]["status"] == "Healthy"):
            node = edges[0]
            if G.nodes[edges[1]]["status"] == "Healthy":
                node = edges[1]

            if random.randint(0, 100) < infect_percent:
                if not G.nodes[node]["vaccinated"] or random.randint(0, 100) > vaccine_affectiveness:
                    G.nodes[node]["status"] = "Newly Infected"

        # print(edges[0] + ":" + G.nodes[edges[0]]["status"])
        # print(edges[1] + ":" + G.nodes[edges[1]]["status"])
        # print()
    return G

def UpdateInfection(G, days_infected):
    for node_data in G.nodes.data():
        node = G.nodes[node_data[0]]
        if node['status'] == "Infected":
            node['days_remaining'] -= 1
            if node['days_remaining'] == 0:
                node['status'] = "Recovered"
        elif node["status"] == "Newly Infected":
            node['status'] = "Infected"
            node['days_remaining'] = days_infected
    return G

def StartInfection(G, start_percent, days_infected):
    for node_data in G.nodes.data():
        node = G.nodes[node_data[0]]
        if random.randint(0, 100) < start_percent:
            node['status'] = "Infected"
            node['days_remaining'] = days_infected
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

def GetRandomGraph(nodes, type):
    if (type == "random"):
        return [nx.gnm_random_graph(nodes, 350)]
    elif (type == "watts"):
        return [nx.connected_watts_strogatz_graph(nodes, 10, .3)]
    return [nx.connected_watts_strogatz_graph(nodes, 5, .3)]

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
