# class DisplayTree:
#
#     @staticmethod
#     def display_node(node):
#         print(node)
#         print('type', node.type)
#         print('action', node.action)
#         print('pot', node.pot)
#         print('to call', node.to_call)
#         print('human stack', node.human_stack)
#         print('bot stack', node.bot_stack)
#         print('children', node.children)
#
#     def display_subtree(self, node):
#         if node.children:
#             for child in node.children:
#                 self.display_subtree(child)
#         self.display_node(node)
#
#     @staticmethod
#     def display_subtree2(root):
#         def count_children(node, depth):
#             for child in node.children:
#                 try:
#                     nodes_children[str(depth-1)+'_'+str(levels_count[str(depth - 1)])].append(child)
#                     try:
#                         levels_count[str(depth)] += 1
#                     except KeyError:
#                         levels_count[str(depth)] = 1
#                 except KeyError:
#                     nodes_children[str(depth-1)+'_'+str(levels_count[str(depth - 1)])] = [child]
#                     try:
#                         levels_count[str(depth)] += 1
#                     except KeyError:
#                         levels_count[str(depth)] = 1
#
#         def recurse_level(level):
#             for count in range(1, levels_count[str(level-1)] + 1):
#                 for node in nodes_children[str(level-1)+'_'+str(count)]:
#                     count_children(node, level+1)
#             recurse_level(level+1)
#
#         def width_node(node):  #WRONG width can be higher than max number of nodes due to gaps between nodes
#             def count_width(current_node, level, current):
#                 if current_node.children:
#                     all_leaves = True
#                     for child in current_node.children:
#                         level_count += 1
#                         count_width(child, level, current+1)
#                         if child.children:
#                             all_leaves = False
#                     if not all_leaves:
#                         level_count -= 1
#
#             width_levels = [1]
#             level = 1
#             while width_levels[-1] != 0:
#                 level_count = 0
#                 count_width(node, level, 0)
#                 width_levels.append(level_count)
#                 level += 1
#             return max(width_levels)  #TODO sum number of nodes from widest level to root
#
#         def print_level(level):
#             string = ' ' * max_width
#             substring = ''
#             for parent in range(1, levels_count[level-1] + 1):
#                 for i in range(nodes_children[str(level-1)+'_'+str(parent)]):
#                     node = nodes_children[str(level-1)+'_'+str(parent)][i]
#                     if node.type == 'bot':  #equivalently, level%2 == 0
#                         s = 'B'  #TODO print action
#                     else:
#                         s = 'H'
#                     width = width_node(node)
#                     nodes_positions[str(level)+'_'+str(i)] = nodes_positions[str(level-1)+'_'+str(parent)] + len(substring)
#                     substring += '-' * (width//2) + s + '-' * ((width - 1)//2)
#                 string[nodes_positions[str(level-1)+'_'+str(parent)]:len(substring)] = substring
#
#             print(string)
#
#         nodes_children = {}
#         nodes_positions = {}
#         levels_count = {'0': 1}
#         count_children(root, 1)
#         recurse_level(1)
#         max_width = width_node(root)
#         print('_' * (max_width//2) + 'B' + '_' * ((max_width - 1)//2))
#         nodes_positions['0_1'] = 0
#         for level in range(1, len(levels_count.keys()) + 1):
#             print_level(level)

class TestNode:
    def __init__(self, parent, depth):
        self.parent = parent
        self.children = []
        self.depth = depth
        self.width = 0
        self.right_most_leave = False
        self.position = None

def display_tree(old_root):
    def build_tree(old_node, new_node):
        if old_node.children == None:
            return
        for _ in old_node.children:
            new_node.children.append(TestNode(new_node, new_node.depth + 1))
        for old_child, new_child in zip(old_node.children, new_node.children):
            build_tree(old_child, new_child)

    def assing_widths(root):
        width = 0
        if root.children:
            width += len(root.children) - 1
            for child in root.children:
                child.width = assing_widths(child)
                width += child.width
            return width
        else:
            root.width = 1
            return 1

    def assign_positions(root):
        pos = root.position
        for child in root.children:
            child.position = pos
            pos += child.width + 1
            assign_positions(child)
        if root.children:
            if not child.children:
                child.right_most_leave = True  # So that we can add spaces between leave nodes

    def build_print_dict(top_root, root, print_dict):
        width = root.width
        extra = 0
        if root.depth % 2 == 0:
            s = 'B'
        else:
            s = 'H'
        if (not root.children) and (not root.right_most_leave):
            s += ' '
            extra = 1
        try:
            print_dict[str(root.depth)][root.position:root.width + extra] = list('-' * (width//2) + s + '-' * ((width-1) // 2))
        except KeyError:
            print_dict[str(root.depth)] = list(' ' * top_root.width)
            print_dict[str(root.depth)][root.position:root.width + extra] = list('-'*(width//2) + s + '-' * ((width-1) // 2))
        for child in root.children:
            build_print_dict(top_root, child, print_dict)

    new_root = TestNode(None, 0)
    build_tree(old_root, new_root)
    new_root.width = assing_widths(new_root)
    new_root.position = 0
    assign_positions(new_root)
    print_dictionary = {}
    build_print_dict(new_root, new_root, print_dictionary)

    depth = 0
    while True:
        try:
            print(''.join(print_dictionary[str(depth)]))
            depth += 1
        except KeyError:
            break

# class OldNode:
#     children = []
#
# old_root = OldNode()
# second_node1 = OldNode()
# second_node2 = OldNode()
# second_node4 = OldNode()
# third_node1 = OldNode()
# second_node1.children = [OldNode(), OldNode(), OldNode()]
# second_node2.children = [OldNode(), third_node1, OldNode()]
# second_node4.children = [OldNode(), OldNode()]
# third_node1.children = [OldNode(), OldNode(), OldNode(), OldNode(), OldNode(), OldNode(), OldNode()]
# old_root.children = [second_node1, second_node2, OldNode(),second_node4, OldNode()]
# display_tree(old_root)
