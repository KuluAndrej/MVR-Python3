# Generates all possible models of given height (maximum of 4).
# The 'number_of_variables' signify the number of variables, which can be stored in terminal nodes
# Author: Kulunchakov Andrei

import itertools, re
import code.input_output.SavePopulationToFile as SavePopulationToFile
from code.modules.model_reconstructer import model_reconstruct
import code.model_processing.ExtractAllSubtreesFromTree as ExtractAllSubtreesFromTree
import code.input_output.LoadPrimitives as LoadPrimitives

def generate(filename, height = 4, number_of_variables = 1):
    """
    Generate all possible models which syntax tree's height is equal to 'height'
    Be aware of burst of the number of models in case of large 'number_of_variables'

    Author: Kulunchakov Andrei
    """

    print("Start generation of all possible models with height", height, "and num_vars", number_of_variables)
    created_models = []
    primitives = LoadPrimitives.load()
    grouped_primitives = divide_primitives_according_arities(primitives, number_of_variables)

    list_of_str_trees = ExtractAllSubtreesFromTree.generate_all_possible_tree(height)
    print(len(list_of_str_trees),"trees are being processed...")
    for tree in list_of_str_trees:
        print("Process the tree:", tree)
        degrees = get_degrees_of_nodes(eval(tree)[1])
        variants_of_tokens = create_tokens_for_all_matching_trees(grouped_primitives, degrees)
        for tokens in variants_of_tokens:
            model = create_model(eval(tree)[1], tokens, current_root = [0])
            model = re.sub(r'X\[(\d+)\]', r'x\1', model)
            model = model_reconstruct(model)
            model = re.sub(r'x(\d+)', r'X[\1]', model)
            created_models.append(model)

    created_models = list(set(created_models))
    print(len(created_models),'models are generated')
    SavePopulationToFile.save_population_to_file(created_models, None, None, None, filename=filename)


def create_tokens_for_all_matching_trees(grouped_primitives, degrees):
    """
    Return all possible arrays of tokens of models, which trees have array of node's degrees equal to
    the 'degrees'

    :param grouped_primitives: list of tokens available for use to construct models
    :param degrees:            list of degrees, which acts like a template for models
    :return:                   list of lists of tokens
    """

    # lists of list of tokens
    # i-th list contains those tokens, which can be placed at the i-th node
    positions_vs_possible_tokens = [[] for i in range(len(degrees))]
    for ind, position in enumerate(positions_vs_possible_tokens):
        position.extend(grouped_primitives[degrees[ind]])


    return list(itertools.product(*positions_vs_possible_tokens))

def get_degrees_of_nodes(str_tree):
    degrees = [0]
    for elem in str_tree:
        if type(elem) == type(1):
            degrees[0] += 1
        if type(elem) == type([]):
            degrees.extend(get_degrees_of_nodes(elem))

    return degrees

def divide_primitives_according_arities(primitives, number_of_variables):
    """
    If we have a list primitives, say 'x+y, x*y, sin(x)', then we are to return a list [[sin(x)], [x+y, x*y]],
    as the first two functions have arity equal to 2, and the last one - 1

    If the 'number_of_variables' = 5, then the list of functions of zero arity consists of X[0],X[1],...X[4]

    We suppose, that all arities up to the maximum one are presented among the primitives
    """
    arities = [primitive.number_args for primitive in primitives]
    set_divided_primitives = [[] for i in range(0, max(arities) + 1)]
    for primitive in primitives:
        set_divided_primitives[primitive.number_args].append(primitive)

    # process the functions with zero arity
    set_divided_primitives[0].extend(['X['+str(i)+']' for i in range(number_of_variables)])
    print(set_divided_primitives[0])
    return set_divided_primitives



def create_model(str_tree, tokens, current_root = [0]):
    if str_tree:
        handle = tokens[current_root[0]] + '('
    else:
        if type(tokens[current_root[0]]) == type(''):
            return tokens[current_root[0]]
        else:
            return tokens[current_root[0]] + '()'

    is_first_subling = True

    for elem in str_tree:
        if type(elem) == type(1):
            current_root[0] += 1
        if type(elem) == type([]):
            if not is_first_subling:
                handle += ','
            else:
                is_first_subling = False

            handle = handle + create_model(elem, tokens, current_root)

    return handle + ')'

"""
l = [1,[1,[1,[],1,[]],1,[]]]
d = get_degrees_of_nodes(l)
p = LoadPrimitives.load()
print(l,d)
t = divide_primitives_according_arities(p,1)
print(t)

s = create_tokens_for_all_matching_trees(t, d)
print(create_model(l, s[0]))
"""

#generate('data/Rules creation files/init_patterns.txt', height = 4, number_of_variables = 1)
#s = ExtractAllSubtreesFromTree.generate_all_possible_tree(4)
#print(s)
"""
primitives = LoadPrimitives.load()
grouped_primitives = divide_primitives_according_arities(primitives, 1)
tree = '[1,[1,[1,[]]]]'
degrees = get_degrees_of_nodes(eval(tree)[1])
variants_of_tokens = create_tokens_for_all_matching_trees(grouped_primitives, degrees)
print(create_model([1, [1, []]], variants_of_tokens[3], current_root = [0]))
"""