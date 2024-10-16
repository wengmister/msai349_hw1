class Node:
    def __init__(self, node_info_gain, attribute=None, value=None, label=None, is_leaf=False):
        """
        Initialize a node in the decision tree.

        Args:
        - attribute (str): The feature/attribute to split on at this node.
        - value (str): The value of the feature (only relevant for child nodes).
        - label (str/int): The class label (for leaf nodes).
        - is_leaf (bool): True if the node is a leaf node (i.e., no further splitting).
        """
        self.label = label
        self.children = []
        self.attribute = attribute    # The feature to split on
        self.value = value            # The value of the parent node's attribute (for children)
        self.is_leaf = is_leaf        # Whether the node is a leaf node
        self.node_info_gain = node_info_gain

    def add_child(self, child_node):
        """
        Add a child node to the current node.

        Args:
        - child_node (Node): The child node to add.
        """
        self.children.append(child_node)

    def __repr__(self):
      """
      String representation for easier visualization.
      """
      if self.is_leaf:
          return f"Leaf(label={self.label},value = {self.value}, info_gain={self.node_info_gain})"
      else:
          return f"Node(attribute={self.attribute}, value={self.value}, children={len(self.children)}, info_gain={self.node_info_gain})"
      
    def print_tree(self, depth=0):
        """
        (Recursively) print the whole ID3.

        - node - The root node of the decision tree.
        - depth - The current depth.
        """
        indent = "  " * depth
        
        if (self.children):
            connector = "├── "
        else:
            connector = "└── "
        print(f"{indent}{connector}{self.__repr__()}")
        if (self.is_leaf): return      
        for child in self.children:
            child.print_tree(depth + 1)

