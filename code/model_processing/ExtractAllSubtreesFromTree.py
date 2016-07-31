# The code generating all possible subtrees of a given tree
#
# Author: John Kugelman on 'http://stackoverflow.com/questions/1160160/generating-all-possible-trees-of-depth-n'


def all_combos(choices):
    """
    Given a list of items (a,b,c,...), generates all possible combinations of
    items where one item is taken from a, one from b, one from c, and so on.

    For example, all_combos([[1, 2], ["a", "b", "c"]]) yields:

        [1, "a"]
        [1, "b"]
        [1, "c"]
        [2, "a"]
        [2, "b"]
        [2, "c"]
    """
    if not choices:
        yield []
        return

    for left_choice in choices[0]:
        for right_choices in all_combos(choices[1:]):
            yield [left_choice] + right_choices

class Node:
    def __init__(self, value, children=[]):
        self.value    = value
        self.children = children

    def all_subtrees(self, max_depth):
        yield Node(self.value)

        if max_depth > 0:
            # For each child, get all of its possible sub-trees.
            child_subtrees = [list(self.children[i].all_subtrees(max_depth - 1)) for i in range(len(self.children))]

            # Now for the n children iterate through the 2^n possibilities where
            # each child's subtree is independently present or not present. The
            # i-th child is present if the i-th bit in "bits" is a 1.
            for bits in range(1, 2 ** len(self.children)):
                for combos in all_combos([child_subtrees[i] for i in range(len(self.children)) if bits & (1 << i) != 0]):
                    yield Node(self.value, combos)

    def __str__(self):
        """
        Display the node's value, and then its children in brackets if it has any.
        """
        if self.children:
            return "%s,%s" % (self.value, self.children)
        else:
            return str(self.value)+',[]'

    def __repr__(self):
        return str(self)

def generate_all_possible_tree(height):
    """

    :param height: maximum height of the trees
    :return:       list of generated subtrees
    """
    if height > 4:
        raise("The maximum permissible height of generated trees is 4\n")

    Mother_tree = Node(1,
    [
        Node(1,
        [
            Node(1,
            [
                Node(1),
                Node(1)
            ]),
            Node(1,
            [
                Node(1),
                Node(1)
            ])
        ]),
        Node(1,
        [
            Node(1,
            [
                Node(1),
                Node(1)
            ]),
            Node(1,
            [
                Node(1),
                Node(1)
            ])
        ])
    ])
    s = [str('['+repr(q)+']').replace(" ", "") for q in Mother_tree.all_subtrees(2)]
    s = list(set(s))
    return s

