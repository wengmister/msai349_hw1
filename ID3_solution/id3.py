from data_loader import DataLoader
from tree import Tree, TreeNode, LeafNode
from config import CONFIG

import math        



class ID3Solution:
    def __init__(self, data_file_name='mushroom.data'):
        # Initialize the data and data_loaded variables
        self.data_loader = DataLoader()
        self.data_loader.load_data(data_file_name)
        
        # Initialize the H variable (entropy of the dataset)
        self.H = self._calculate_entropy(self.data_loader.data, target_attribute='Class')
        
         # Initialize the tree
        self.tree = self.init_tree()
    
    
    def run(self):
        continue_running = True
        while(self.tree.tree_depth < CONFIG['max_tree_depth']
              and self.tree.get_num_nodes() < CONFIG['max_tree_nodes']
              and continue_running):
            continue_running = self.add_tree_layer()
        print("The tree:")
        self.tree.print_tree()
        print("")
        print(f"Tree depth: {self.tree.tree_depth}")
        print(f"Tree nodes: {self.tree.get_num_nodes()}")
    
    
    def init_tree(self):
        """
        Initialize the decision tree.
        
        Args:
        - None
        
        Returns:
        - Tree: The initialized decision tree.
        """
        # Initialize the tree
        best_attr = self.get_the_best_attribute_with_highest_ig(self.data_loader.data)
        best_attr_values = list(self.data_loader.split_data_by_attribute(best_attr).keys())
        self.tree = Tree(root_attribute=best_attr, root_attribute_values=best_attr_values)
        # self.data_loader.delete_attribute(best_attr)
        
        return self.tree
    
    
    def add_tree_layer(self):
        # Record nodes to be added
        leaf_information = []
        child_information = []
        
        # If there are only 2 attributes left, they're the attribute just added with nodes
        # and the target attribute 'Class'
        if(len(self.data_loader.get_attribute_names()) == 1):
            return False
        # Only build the tree when there are unexplored attributes
        elif(len(self.data_loader.get_attribute_names()) == 2):
            # Visit each node in the tree
            for tree_node in self.tree.tree_nodes.values():
                # Find the child node at specified depth
                if (tree_node.is_leaf == False) and (tree_node.depth == self.tree.tree_depth):
                    attr_value_to_subset_dict = self.data_loader.split_data_by_attribute(tree_node.attribute)
                    for attribute_value in tree_node.attribute_values:
                        subset_data = attr_value_to_subset_dict[attribute_value]
                        # add a leaf node
                        approximated_label = self.data_loader.get_most_frequent_label(subset_data)
                        leaf_node_information = [tree_node.index, attribute_value, 
                                                approximated_label, tree_node.attribute]
                        leaf_information.append(leaf_node_information)
                        # self.tree.add_leaf(tree_node.index, attribute_value, subset_data[0]['Class'])
            # Add leaf nodes
            for leaf_node_info in leaf_information:
                self.tree.add_leaf(leaf_node_info[0], leaf_node_info[1], leaf_node_info[2])
                # Delete the attribute used to split the data
                self.data_loader.delete_attribute(leaf_node_information[3])
            
            return True
        else:
            # Visit each node in the tree
            for tree_node in self.tree.tree_nodes.values():
                # Find the child node at specified depth
                if (tree_node.is_leaf == False) and (tree_node.depth == self.tree.tree_depth):
                    attr_value_to_subset_dict = self.data_loader.split_data_by_attribute(tree_node.attribute)
                    for attribute_value in tree_node.attribute_values:
                        subset_data = attr_value_to_subset_dict[attribute_value]
                        subset_entropy = self._calculate_entropy(subset_data, target_attribute='Class')
                        # print(subset_entropy)
                        # If the subset entropy is 0, add a leaf node
                        if(subset_entropy == 0):
                            leaf_node_information = [tree_node.index, attribute_value, 
                                                    subset_data[0]['Class'], tree_node.attribute]
                            leaf_information.append(leaf_node_information)
                            # self.tree.add_leaf(tree_node.index, attribute_value, subset_data[0]['Class'])
                        # If the subset entropy is not 0, add a child node
                        else:
                            best_attr = self.get_the_best_attribute_with_highest_ig(subset_data, ignore_attribute=tree_node.attribute) 
                            best_attr_values = list(self.data_loader.split_data_by_attribute(best_attr).keys())
                            approximated_label = self.data_loader.get_most_frequent_label(subset_data)
                            print(approximated_label)
                            child_node_information = [tree_node.index, attribute_value, 
                                                      best_attr, best_attr_values,
                                                      approximated_label, tree_node.attribute]
                            child_information.append(child_node_information)
            # Add leaf nodes
            for leaf_node_info in leaf_information:
                self.tree.add_leaf(leaf_node_info[0], leaf_node_info[1], leaf_node_info[2])
            # Add child nodes
            for child_node_info in child_information:
                self.tree.add_node(child_node_info[0], child_node_info[1], child_node_info[2], child_node_info[3], child_node_info[4])
            # Delete the attribute used to split the data
            for child_node_info in child_information:
                self.data_loader.delete_attribute(child_node_info[5])
            
            return True
        
        
    def calc_ig(self, attribute):
        '''
        Calculate the information gain of a dataset for a given attribute
        
        Credit: This function is written by Zhengxiao Han.
        
        Args:
        data - list of dictionaries, the dataset
        attribute - string, the attribute to calculate the information gain for
        
        Returns:
        ig - float, the information gain
        '''
        # Initialize the information gain
        ig = 0
        
        # Split the data by the attribute
        splited_attribute_dict = self.data_loader.split_data_by_attribute(attribute)
        H_i = 0
        for attribute_value in splited_attribute_dict.keys():
            # The data list for this attribute value
            data_list = splited_attribute_dict[attribute_value]
            # The probability of this attribute value
            p_i = len(data_list) / self.data_loader.get_data_size() 
            # Calculate the entropy of this attribute value
            H_i += self._calculate_entropy(data_list, target_attribute='Class') * p_i
            
        # Calculate the information gain
        ig = self.H + H_i
        
        return ig
    
    
    def get_the_best_attribute_with_highest_ig(self, dataset=None, ignore_attribute=None):
        """
        Identifies the attribute that maximizes information gain for data splitting.
        
        Credit: This function is derived from find_best_attribute_to_split_on(data) in
                separate.py, originally written by Kris Weng and Ben Benyamin.
                Zhengxiao Han modified this function and incorporated the use of 
                calc_ig(attribute) function to make it easier to understand.
        
        Args:
        data (list or DataFrame): The dataset to analyze, consisting of multiple data points.
        
        Returns:
        str: The attribute that maximizes information gain
        """
        
        if(len(dataset) == 0):
            print("get_the_best_attribute_with_highest_ig: no data.")
            return None
        else:
            # Extract the attribute list except the last one, which is the target attribute 'Class'
            attribute_list = list(dataset[0].keys())[:-1]
            # If there is no attribute, return None
            if len(attribute_list) == 0:
                print("No attribute in the dataset.")
                return None
            else:
                # Initialize the best attribute. The default is the first attribute
                best_attribute = attribute_list[0]
                # Initialize the highest information gain
                highest_ig = 0
                # Visit each attribute
                for attribute in attribute_list:
                    if attribute != ignore_attribute:
                        # Calculate the information gain for this attribute
                        ig = self.calc_ig(attribute)
                        # Update the highest information gain and the best attribute
                        if ig > highest_ig:
                            highest_ig = ig
                            best_attribute = attribute
                        
                return best_attribute
    

    def _calculate_entropy(self, data, target_attribute='Class'):
        """
        Calculate the entropy of a node based on the target attribute. Defaults to the Class attribute.
        
        Args:
        data (dict): The dataset to analyze, consisting of multiple data points.
        target_attribute (str): The attribute to calculate the entropy for.
        
        Returns:
        float: The entropy of the dataset.
        """
        # Total number of instances in the dataset
        total_count = len(data)
        
        # If there's no data, entropy is 0
        if total_count == 0:
            return 0

        # Get the unique classes and their frequencies
        class_counts = {}
        for row in data:
            label = row[target_attribute]
            if label not in class_counts:
                class_counts[label] = 0
            class_counts[label] += 1
        
        # Calculate entropy
        entropy = 0.0
        for count in class_counts.values():
            p_i = count / total_count
            entropy -= p_i * math.log2(p_i)
        
        return entropy
