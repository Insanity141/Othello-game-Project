nodes_searched = 0
pruned_nodes = 0
thinking_time = 0
evaluation_score = 0
algorithm = "-"


def reset():

    global nodes_searched
    global pruned_nodes
    global thinking_time
    global evaluation_score

    nodes_searched = 0
    pruned_nodes = 0
    thinking_time = 0
    evaluation_score = 0


def add_node():

    global nodes_searched

    nodes_searched += 1


def add_pruned():

    global pruned_nodes

    pruned_nodes += 1


def set_time(seconds):

    global thinking_time

    thinking_time = seconds


def set_score(score):

    global evaluation_score

    evaluation_score = score


def set_algorithm(name):

    global algorithm

    algorithm = name


def get_stats():

    return (nodes_searched, pruned_nodes, thinking_time, evaluation_score, algorithm)
