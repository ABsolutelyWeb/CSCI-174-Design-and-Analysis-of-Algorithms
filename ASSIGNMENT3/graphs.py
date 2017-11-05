# We are using "default dictionaries":
# - they allow adding new values to non-initialized keys
# - by default, values of these keys are defined as empty
from collections import defaultdict

def read_graph(filename):
    """Read the graph from the input file.

    The graph is defined as a list of edges:
    - each line in the text files contains two numbers
    - these two numbers define an edge in a directed graph
    """

    # Initialize the graph an an empty dictionary of sets
    graph = defaultdict(set)

    # Open the file
    with open(filename) as input_data:
        # Read each line from the file
        for line in input_data:
            # Extract two values separated by whitespace; ignore newline character
            a, b = line.rstrip().split(' ')
            # Convert extracted values into integers
            a, b = int(a), int(b)
            # Add the extracted edge into the graph
            graph[a].add(b)

    # Review all nodes: 
    # if the node doesn't have an incoming connection,
    # then initialize it as an empty set
    for i in range(1, len(graph.keys()) + 1):
        if i not in set(graph.keys()):
            graph[i] = set()

    # Return as a normal dictionary
    return dict(graph)


def bfs(graph, start):
    """Breadth-first search in a graph starting from the node 'start'.
    """
    # Initialize the set of visited nodes + queue of the nodes to visit
    visited, queue = set(), [start]
    # While queue is not empty = we still have nodes to visit:
    while queue:
        # Return and remove the first element of the queue
        node = queue.pop(0)
        # If node was not visited yet
        if node not in visited:
            # Mark it as visited
            visited.add(node)
            # Add outgoing connections from this node to the queue (except visited)
            queue.extend(graph[node] - visited)
    # Return the list of visited nodes in the right order
    return visited

def bfs_paths(graph, start, end):
    """Find shortest paths in the graph from node 'start' to node 'finish'.
    """
    # Initialize the queue as a tuple: starting node, starting path
    queue = [(start, [start])]
    # While queue is not empty
    while queue:
        # Return and remove the first element of the queue
        (node, path) = queue.pop(0)
        # For each outgoing connection which wasn't visited yet
        for next in graph[node] - set(path):
            # If we reached our destination node
            if next == end:
                # Return the resulting path
                return path + [next]
            else:
                # Add the current node to the path, and continue search
                queue.append((next, path + [next]))
    # If the queue is empty, return the starting node only
    return [start]


def dfs_times(graph, starting_vertex):
    visited = set()
    counter = [0]
    traversal_times = defaultdict(dict)

    def traverse(vertex):
        visited.add(vertex)
        counter[0] += 1
        traversal_times[vertex]['discovery'] = counter[0]

        for next_vertex in graph[vertex]:
            if next_vertex not in visited:
                traverse(next_vertex)

        counter[0] += 1
        traversal_times[vertex]['finish'] = counter[0]

    # in this case start with just one vertex, but we could equally
    # dfs from all_vertices to product a dfs forest
    traverse(starting_vertex)
    return traversal_times

def dfs_tree(graph, starting_vertex):
    visited = set()
    tree = []

    def compute_tree(vertex):
        visited.add(vertex)
        for next_vertex in graph[vertex]:
            if next_vertex not in visited:
                tree.append((vertex, next_vertex))
                compute_tree(next_vertex)

    # in this case start with just one vertex, but we could equally
    # dfs from all_vertices to product a dfs forest
    compute_tree(starting_vertex)
    return tree

def dfs_edges(tree, graph, order):
    tree_graph = defaultdict(set)
    for (u, v) in tree:
        tree_graph[u].add(v)

    def get_children(node):
        for child in tree_graph[node]:
            yield child
            for grandchild in get_children(child):
                yield grandchild

    back = []
    forward = []
    cross = []

    descents_ok = defaultdict(set)
    for u in graph.keys():
        descents = get_children(u)
        for i in descents:
            descents_ok[u].add(i)
        for v in descents_ok[u]:
            if u in graph[v]:
                back.append((v, u))
            if v in graph[u] and (u, v) not in tree:
                forward.append((u, v))
                        

    for u in graph.keys():
        for v in graph[u]:
            if u not in descents_ok[v] and v not in descents_ok[u]:
                cross.append((u, v))                
        
    return back, forward, cross

def dfs_order(graph, starting_vertex):
    visited = set()
    order = [starting_vertex]

    def compute_order(vertex):
        visited.add(vertex)
        for next_vertex in graph[vertex]:
            if next_vertex not in visited:
                order.append(next_vertex)
                compute_order(next_vertex)

    # in this case start with just one vertex, but we could equally
    # dfs from all_vertices to product a dfs forest
    compute_order(starting_vertex)
    return order


def write_bfs_output(input_filename, output_filename):
    """Create an output file with BFS data for the given input file."""
    # Read the graph
    graph = read_graph(input_filename)
    # Write the output file
    with open(output_filename, 'w') as output_file:
        # Write the header
        output_file.write('Vertex: Distance [Path]\n')
        # For each node in the graph
        for node in range(1, len(graph.keys()) + 1):
            # Seach for shortest paths from node #1 to this node
            paths = bfs_paths(graph, 1, node)
            # If paths exist
            if paths:
                # Write the node number
                output_file.write(str(node) + ' : ')
                # Write the number of edges in the path (which is the number of nodes - 1)
                output_file.write(str(len(paths) - 1) + ' ')
                # Write the shortest path itself
                output_file.write(str(paths) + '\n')

def write_dfs_output(input_filename, output_filename):
    """Create an output file with DFS data for the given input file."""
    # Read the graph
    graph = read_graph(input_filename)
    # Write the output file
    with open(output_filename, 'w') as output_file:
        # For each node in the graph
        for node in range(1, len(graph.keys()) + 1):
            # Seach for shortest paths from node #1 to this node
            times = dfs_times(graph, 1)
            output_file.write("Discover/Finish: "+str(node)+" : ")
            if 'discovery' not in times[node]:
                output_file.write('None None\n')
            else:
                output_file.write(str(times[node]['discovery'])+' '+str(times[node]['finish'])+'\n')
        tree = dfs_tree(graph, 1)
        output_file.write("Tree: "+str(tree)+'\n')

        order = dfs_order(graph, 1)        
        back, forward, cross = dfs_edges(tree, graph, order)
        output_file.write("Back: "+str(back)+'\n')
        output_file.write("Forward: "+str(forward)+'\n')
        output_file.write("Cross: "+str(cross)+'\n')
        output_file.write("Vertices in topological order: "+str(order)+'\n')


# If we call this script from the command line
if __name__ == "__main__":

    # Process each input file and write output files
    # Here, all files are located in the script folder
    write_bfs_output("input_1.txt", "bfs_1.txt")
    write_bfs_output("input_2.txt", "bfs_2.txt")
    write_bfs_output("input_3.txt", "bfs_3.txt")

    write_dfs_output("input_1.txt", "dfs_1.txt")
    write_dfs_output("input_2.txt", "dfs_2.txt")
    write_dfs_output("input_3.txt", "dfs_3.txt")
