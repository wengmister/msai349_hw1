from collections import Counter

class Tree:
    def __init__(self, root_attribute=None, root_attribute_values=None):
        # Initialize the tree
        self.tree_index = 0
        self.tree_depth = 0
        self.tree_nodes = {}
        self.tree = self._init_tree_root(root_attribute, root_attribute_values)
    
    
    def get_num_nodes(self):
        """
        Get the number of nodes in the decision tree.

        Args:
        - None
        
        Returns:
        - int: The number of nodes in the decision tree.
        """
        return len(self.tree_nodes)


    def _init_tree_root(self, attribute=None, attribute_values=None):
        """
        Initialize a root node in the decision tree.

        Args:
        - attribute (str): The feature/attribute to split on at this node.
        - attribute_values (list): The values of the attribute.
        
        Returns:
        - TreeNode: The root node created.
        """
        self.tree = TreeNode(attribute=attribute, 
                             attribute_values=attribute_values, 
                             is_leaf=False, 
                             depth=1,
                             index=self.tree_index)
        self.tree_nodes[str(self.tree_index)] = self.tree
        self.tree_index += 1
        self.tree_depth += 1
        return self.tree
    
    
    def print_tree(self):
        """
        Print the whole ID3.

        Args:
        - None
        
        Returns:
        - None
        """
        for depth in range(self.tree_depth):
            depth += 1
            indent = "  " * depth
            for tree_node in self.tree_nodes.values():
                if(tree_node.depth == depth):
                    connector = "└── "
                    if(tree_node.is_leaf):
                        print(f"{indent}{connector}Leaf(ParentValue={tree_node.parent_value}, Label={tree_node.label}, Depth={tree_node.depth})")
                    elif(not tree_node.is_leaf):
                        print(f"{indent}{connector}Node(ParentValue={tree_node.parent_value}, Label={tree_node.label}, Attribute={tree_node.attribute}, AttributeValues={tree_node.attribute_values}, Depth={tree_node.depth})")
    
    
    def add_leaf(self, parent_index, parent_value, label):
        """
        Add a leaf node to the decision tree.

        Args:
        - parent_index (int): The index of the parent node.
        - label (str/int): The class label.
        - value (str): The value of the parent node's attribute.
        
        Returns:
        - None
        """
        leaf = LeafNode(depth=self.tree_nodes[str(parent_index)].depth+1, 
                        parent_value=parent_value,
                        index=self.tree_index, 
                        label=label)
        self.tree_nodes[str(parent_index)].add_child_index(parent_value, self.tree_index)
        self.tree_nodes[str(self.tree_index)] = leaf
        self.tree_index += 1
        self.update_tree_depth(self.tree_nodes[str(parent_index)].depth+1)
        
    
    def add_node(self, parent_index, parent_value, attribute, attribute_values, label):
        """
        
        """        
        node = TreeNode(attribute=attribute,
                        attribute_values=attribute_values,
                        is_leaf=False,
                        depth=self.tree_nodes[str(parent_index)].depth+1,
                        parent_value=parent_value,
                        index=self.tree_index,
                        label=label)
        self.tree_nodes[str(parent_index)].add_child_index(parent_value, self.tree_index)
        self.tree_nodes[str(self.tree_index)] = node
        self.tree_index += 1
        self.update_tree_depth(self.tree_nodes[str(parent_index)].depth+1)
        
    
    def update_tree_depth(self, depth):
        """
        Update the depth of the decision tree.

        Args:
        - None
        
        Returns:
        - None
        """
        if(depth > self.tree_depth):
            self.tree_depth = depth
        
        
class TreeNode:
    def __init__(self, attribute=None, attribute_values = None, is_leaf=False, depth=0, parent_value=None, index=0, label=None):
        """
        Initialize a node in the decision tree.

        Args:
        - attribute (str): The feature/attribute to split on at this node.
        - attribute_values (list): The values of the attribute.
        - is_leaf (bool): True if the node is a leaf node (i.e., no further splitting).
        - depth (int): The depth of the node in the tree.
        - index (int): The index of the node in the tree.
        """
        self.attribute = attribute # The feature to split on
        self.attribute_values = attribute_values # The values of the attribute
        self.is_leaf = is_leaf # Whether the node is a leaf node
        self.depth = depth # The depth of the node in the tree
        self.parent_value = parent_value # The parent node index
        self.index = index # The index of the node in the tree
        self.label = label # The class label (for leaf nodes)

        self.children = {} # The children node indices corresponding to the attribute values
        
    
    def add_child_index(self, attribute_value, child_node_index):
        """
        Add a child node to the current node.

        Args:
        - child_node (Node): The child node to add.
        
        Returns:
        - None
        """
        self.children[attribute_value] = child_node_index
        
        
    def get_child_index_according_to_attribute_value(self, attribute_value):
        """
        Get the child node according to the attribute value.

        Args:
        - attribute_value (str): The value of the attribute.
        
        Returns:
        - TreeNode: The child node corresponding to the attribute value.
        """
        return self.children[attribute_value]
      
      
    def print_tree(self, depth=0):
        """
        Recursively print the whole ID3.

        Args:
        - depth (int): The current depth.
        
        Returns:
        - None
        """
        indent = "  " * depth
        
        if (self.children):
            connector = "├── "
        else:
            connector = "└── "
        print(f"{indent}{connector}{self.as_str()}")
        if (self.is_leaf): return      
        for child_index in self.children.keys():
            child = self.children[child_index]
            child.print_tree(depth + 1)
            
            
    def get_label(self):
        """
        Get the label of the leaf node.

        Args:
        - None
        
        Returns:
        - str: The label of the leaf node.
        """
        # Extract the 'Class' values from each dictionary in the list
        labels = [labels for label in self.attribute_values]
        
        # Count the occurrences of each label
        label_count = Counter(labels)
        
        # Find the label with the highest count
        most_frequent_label = label_count.most_common(1)[0][0]
        
        return most_frequent_label


class LeafNode(TreeNode):
    def __init__(self, depth=0, parent_value=None, index=0, label=None):
        """
        Initialize a node in the decision tree.

        Args:
        - depth (int): The depth of the node in the tree.
        - index (int): The index of the node in the tree.
        - label (str/int): The class label (for leaf nodes).
        """
        self.is_leaf = True
        self.depth = depth
        self.parent_value = parent_value
        self.index = index
        self.label = label
    
    
    def get_label(self):
        """
        Get the label of the leaf node.

        Args:
        - None
        
        Returns:
        - str: The label of the leaf node.
        """
        return self.label
    