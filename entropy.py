import math
import parse

def calculate_node_entropy(data, target_attribute='Class'):
    """
    Calculate the entropy of a node based on the target attribute (Class).
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


if __name__ == "__main__":
    test_data = parse.parse("tennis.data")
    print(calculate_node_entropy(test_data))