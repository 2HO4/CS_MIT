# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: data = line.split(' ')
#         Nodes: Node(data[0]), Node(data[1])
#         Edges: WeightedEdge(Node(data[0]), Node(data[1]), data[2], data[3])
#         Total distances: data[2]
#        Outdoor distances: data[3]
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
    print("Loading map from file...")

    mit_map = Digraph()
    with open(map_filename, 'r') as map_data:
        data_list = map_data.read().split('\n')
        if data_list[-1] == '':
            data_list = data_list[:-1]
        for line in data_list:
            data = line.split(' ')
            if not mit_map.has_node(Node(data[0])):
                mit_map.add_node(Node(data[0]))
            if not mit_map.has_node(Node(data[1])):
                mit_map.add_node(Node(data[1]))
            mit_map.add_edge(WeightedEdge(Node(data[0]), Node(data[1]),
                                          data[2], data[3]))
        return mit_map


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# print(load_map('test_load_map.txt'), '\n')
# print(load_map('mit_map.txt'))


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#         Objective function: find shortest path
#         Constraints: smallest total distance, limit on outdoor distance
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_total_dist, max_dist_outdoors,
                   best_dist, best_dist_o, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO


    # Check if nodes are valid
    start_node, end_node = None, None
    for node in digraph.nodes:
        if node == Node(start):
            start_node = node
        if node == Node(end):
            end_node = node
    if start_node is None or end_node is None:
        raise ValueError('Starting or ending point does not exist')

    path = path + [start]

    # If start and end are the same, this means path only adds [end] of length 0,
    #  which means we've reached the end
    if start == end:
        return path, 0, 0
        
    # Else if start and end are different, we begin from start, add it to the path,
    # and find the best remaining path with another start node connected to {start}:
    else:
        for edge in digraph.get_edges_for_node(start_node):
            new_start = str(edge.get_destination())
            if new_start not in path:
                if best_path is None or len(path) < len(best_path):
                    data = get_best_path(digraph, new_start, end, path,
                                         max_total_dist, max_dist_outdoors,
                                         best_dist, best_dist_o, best_path)
                    if data[0] is not None:
                        dist = float(edge.get_total_distance()) + data[1]
                        dist_o = float(edge.get_outdoor_distance()) + data[2]
                        if dist <= max_total_dist and dist_o <= max_dist_outdoors:
                            best_path = data[0]
                            best_dist = dist
                            best_dist_o = dist_o
        return best_path, best_dist, best_dist_o


a = Node('A')
b = Node('B')
c = Node('C')
d = Node('D')
e = Node('E')
ab = WeightedEdge(a, b, 3, 4)
bd = WeightedEdge(b, d, 2, 1)
ad = WeightedEdge(a, d, 3, 2)
eb = WeightedEdge(e, b, 5, 3)
de = WeightedEdge(d, e, 2, 2)
ec = WeightedEdge(e, c, 4, 3)
cd = WeightedEdge(c, d, 1, 1)
dg = Digraph()
dg.add_node(a)
dg.add_node(b)
dg.add_node(c)
dg.add_node(d)
dg.add_node(e)
dg.add_edge(ab)
dg.add_edge(bd)
dg.add_edge(ad)
dg.add_edge(eb)
dg.add_edge(de)
dg.add_edge(ec)
dg.add_edge(cd)
print(get_best_path(load_map('mit_map.txt'), '23', '14', [], 8, 0, 0, 0, None))
mit_map = load_map('mit_map.txt')
print(mit_map.nodes)


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO

    path = get_best_path(digraph, start, end, [], max_total_dist, max_dist_outdoors,
                         0, 0, None)[0]
    if path is None:
        raise ValueError
    else:
        return path


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


# if __name__ == "__main__":
#     unittest.main()
