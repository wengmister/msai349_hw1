class Node:
    def __init__(self, attribute=None, value=None, label=None, is_leaf=False):
        """
        Initialize a node in the decision tree.

        Args:
        - attribute (str): The feature/attribute to split on at this node.
        - value (str): The value of the feature (only relevant for child nodes).
        - label (str/int): The class label (for leaf nodes).
        - is_leaf (bool): True if the node is a leaf node (i.e., no further splitting).
        """
        self.label = None
        self.children = []
        self.attribute = attribute    # The feature to split on
        self.value = value            # The value of the parent node's attribute (for children)
        self.is_leaf = is_leaf        # Whether the node is a leaf node

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
          return f"Leaf(label={self.label})"
      else:
          return f"Node(attribute={self.attribute}, value={self.value}, children={len(self.children)})"

