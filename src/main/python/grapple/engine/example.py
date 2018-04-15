from grapple.bom.graph import Graph

if __name__ == '__main__':
    g = Graph()
    n1 = g.create_node()
    n2 = g.create_node()
    n1.create_relation_to(n2)

    for r in n1.find_relations():
        print(r)