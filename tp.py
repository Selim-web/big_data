
import csv, matplotlib.pyplot as mat, networkx as nx 

years = ['2022','2021','2020','2019','2018']
for year in years:
    file = 'data-'+year+'.csv'
    # Déclarer une liste qui va .append chaque tuple. 
    with open(file, 'r') as f:
        next(f)
        reader = f.readlines()[0:100]
        list = []
        for line in reader:
            authors = line.split('"')
            names = authors[11].split(';')
            for i in range(len(names)-1):
                for j in range(i+1,len(names)):
                    tuple= (names[i],names[j])
                    if tuple in list:
                        pass
                    else:
                        list.append(tuple)

    fieldnames = ['author1', 'author2']
    # create list of tuples and graph 
    G = nx.Graph()
    with open('liste_of_tuples_'+year+'.csv','w',encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        nodes = [] # List without double author 
        for author in list:
            rows = [{'author1': author[0], 'author2': author[1]}]
            writer.writerows(rows)
            if author[0] not in nodes:
                nodes.append(author[0])
                G.add_node(author[0])
            if author[1] not in nodes:
                nodes.append(author[1])
                G.add_node(author[1])
            G.add_edge(author[0],author[1])

    list_of_edge_betweness = []
    # on crée un liste des arrets present dans la list de tuple
    # on associe la valeur du plus petit cours chemin à 0 pour commencer.
    for edge in list:
        list_of_edge_betweness.append((edge,0))


    # Cette fonction nous permet de calculer le edge betweenness pour chaque arête déclarer dans la liste ci dessus
    def calculate_edge_betw(G,list_of_edge_betweness):
        for author in G:
            short = nx.shortest_path(G, source=author, target=None) # shortest_path de NetworkX nous permet de calculer le plus courts chemins et 
            # les longueurs des chemins entre les noeuds du graphe G.
            for k, v in short.items():
                if k != author:
                    for index in range(0,len(v)-1):
                        author1 = v[index]
                        author2 = v[index+1]
                        for index2 in range(0,len(list_of_edge_betweness)):
                            if (author1,author2) == list_of_edge_betweness[index2][0]:
                                update_edge = (list_of_edge_betweness[index2][0],list_of_edge_betweness[index2][1]+1)
                                list_of_edge_betweness[index2] = update_edge # ecrase l'ancien tuple pour avancer dans l'algo (boucle boucler) 



    # chercher le plus grand edge dans le liste créer par la fonction calculate_edge_betw
    def get_max_edge(list_of_edge_betweness):
        edge_max = list_of_edge_betweness[0][1]
        edge_tuple_with_max = list_of_edge_betweness[0][0]
        for edge in list_of_edge_betweness:
            if edge_max < edge[1]:
                edge_max = edge[1]
                edge_tuple_with_max = edge[0] # value of tuple
        return edge_max,edge_tuple_with_max


    ### GIRVAN NEWMANN BEGIN
    calculate_edge_betw(G, list_of_edge_betweness)
    edge_max, edge_tuple_with_max = get_max_edge(list_of_edge_betweness)
    list_of_edge_betweness.remove((edge_tuple_with_max,edge_max))

    while edge_max > 1 and len(list_of_edge_betweness) > 0:
        calculate_edge_betw(G, list_of_edge_betweness)
        edge_max, edge_tuple_with_max = get_max_edge(list_of_edge_betweness)
        list_of_edge_betweness.remove((edge_tuple_with_max,edge_max))
        try:
            G.remove_edge(*edge_tuple_with_max)
        except:
            tuple_t = (edge_tuple_with_max[1],edge_tuple_with_max[0])
            G.remove_edge(*tuple_t)
        print(edge_max,'-------',edge_tuple_with_max)
    ### GIRVAN NEWMANN END

    communities = [G.subgraph(c).copy() for c in nx.connected_components(G)] # list of communities of G
    c = 0
    for communitie in communities:
        n = 0
        for node in communitie:
            n+=1
        if n>1:
            nx.draw_circular(communitie,with_labels=True)
            path = '/Users/selimbouhassatine/big_data/community'+str(c)+'.png'
            mat.savefig(path)
            mat.clf()
            c+=1


    # Avant le 05 chercher les auteurs qui sont présent sur plusieurs années, list des auteurs présent sur au moins deux années, avec la list on va chercher la communauté année par année. 









    