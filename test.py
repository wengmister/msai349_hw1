import math

def calculate_entropy(labels):
    """
    Calculate the entropy of a set of labels without using Counter.
    """
    # Total number of labels
    total_count = len(labels)
    
    # Get the unique labels
    unique_labels = set(labels)
    
    # Calculate the entropy
    entropy = 0.0
    for label in unique_labels:
        count = labels.count(label)
        p_i = count / total_count
        entropy -= p_i * math.log2(p_i)
    
    return entropy

# Example usage
labels = ['toxic', 'eatable', 'eatable', 'eatable', 'eatable']
print(f"Entropy: {calculate_entropy(labels):.4f}")

labels_R = ['toxic', 'eatable', 'eatable']
print(f"Red has entropy {calculate_entropy(labels_R)}")

print(0.92*3/5)