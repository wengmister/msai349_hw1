from parse import *
from entropy import *

def split_data_by_attribute(data,seperator_attribute):
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

def find_best_attribute_to_split_on(data, number_of_classes = 2):
    """
    Identifies the attribute that minimizes entropy for data splitting.

    Parameters:
    data (list or DataFrame): The dataset to analyze, consisting of multiple data points.
    attribute_list (list): A list of attributes to evaluate for potential splits.
    """

    smallest_H = 1
    chosen_att = ""

    #Assume the all of the examples has all of the attributes (even if unkown)
    attribue_list = list(data[0].keys())
    attribue_list.remove("Class")

    if (len(attribue_list) == 1): return attribue_list[0], 0

    current_entropy = calculate_entropy(data, number_of_classes)

    for att in attribue_list:
        
        seg_data = split_data_by_attribute(data,att)

        this_H = 0.0
        for att_type in seg_data.keys():
            this_H += 1.0*calculate_entropy(seg_data[att_type], number_of_classes) * len(seg_data[att_type])/len(data)

        if(this_H < smallest_H):
            smallest_H = this_H
            chosen_att = att
    
    info_gain = current_entropy - smallest_H
    # print(f"Chosen attribute: {chosen_att}, Info Gain: {info_gain}")

    return chosen_att, info_gain

def remove_best_att_from_data(data,best_att):

    new_data = []
    for row in data:
        new_row = {}
        for att in row.keys():
            if (att == best_att):
                continue
            new_row[att] = row[att]
        new_data.append(new_row)
    
    return new_data

def get_most_common_label(node):

    # Get a list of labels and their occurrence
    labels_count = {}
    for child in node.children:
        if (child.label not in labels_count):
            labels_count[child.label] = 0
            
        labels_count[child.label] += 1 

    # Find the most common one
    
    most_common = list(labels_count.keys())[0]
    occ = labels_count[most_common]

    for label in labels_count.keys():
        if (labels_count[label] > occ):
            most_common = label
    return most_common


  