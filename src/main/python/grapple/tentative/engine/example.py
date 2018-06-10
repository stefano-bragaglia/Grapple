from grapple.graph import Graph

if __name__ == '__main__':
    g = Graph()
    n1 = g.create_node()
    n2 = g.create_node()
    r = n1.create_relation_to(n2)
    r.add_types('starts_at')
    r.set_property('modified', True)

    n = n2
    for r in n.find_relations():
        if r.tail == r.other(n):
            print(n, '<' + str(r), r.other(n))
        elif r.head == r.other(n):
            print(n, str(r) + '>', r.other(n))
        else:
            print(n, r, r.other(n))
