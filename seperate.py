from parse import parse

<<<<<<< HEAD
def seperate(data,seperator_attribute):
=======

def split_data_by_attribute(data,seperator_attribute):
>>>>>>> ea86119 (more small changes)
    '''
    data - list of dictionaries, a row in the data file
    seperator_attribute - the name of the attribute to seperate the data with
    '''
    sep_att = {}
    
    for row in data:
        if (not row[seperator_attribute] in sep_att.keys()):
            sep_att[row[seperator_attribute]] = []
        
        sep_att[row[seperator_attribute]].append(row)
    return sep_att
<<<<<<< HEAD
=======

def find_best_attribute_to_split_on(data,attribue_list):
    """
    Identifies the attribute that minimizes entropy for data splitting.

    Parameters:
    
    data (list): The dataset to analyze, consisting of multiple data points.
    attribute_list (list): A list of attributes to evaluate for potential splits.
    """
    smallest_H = -1
    chosen_att = ""

    for att in attribue_list:
        
        seg_data = split_data_by_attribute(data,att)

        this_H = 0.0
        for att_type in seg_data.keys():
            this_H += 1.0*calculate_node_entropy(seg_data[att_type]) * len(seg_data[att_type])/len(data)

        print(f"{att}: {this_H}")

        if(this_H < smallest_H):
            smallest_H = this_H
            chosen_att = att
>>>>>>> ea86119 (more small changes)
    
data = parse("mushroom.data")
print(seperate(data,"Color")["red"])
        

