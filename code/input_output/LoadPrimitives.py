# Extract information about primitives available for construction of superpositions
#
# Author: Kulunchakov Andrei
import os
from code.structures.Primitive import Primitive
def load():
    DATA_LOCAL_PATH = "/primitives/Primitives.txt"
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH

    file = open(DATA_FULL_PATH, 'r')
    list_primitives = []
    for line in file.readlines():
        if not line.startswith('#'):
            pieces = line.split()
            list_primitives.append(Primitive(pieces[0], int(pieces[1]),int(pieces[2])))


    return list_primitives