from parse import *
from entropy import *
import random

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

def find_best_attribute_to_split_on(data, number_of_classes = 2, random_ratio = 1.0):
    """
    Identifies the attribute that minimizes entropy for data splitting.

    Parameters:
    data (list or DataFrame): The dataset to analyze, consisting of multiple data points.
    attribute_list (list): A list of attributes to evaluate for potential splits.
    """

    smallest_H = 1
    chosen_att = ""

    #Assume the all of the examples has all of the attributes (even if unkown)
    attribute_list = list(data[0].keys())
    attribute_list.remove("Class")

    # Randomly select a subset of attributes to consider
    if(random_ratio != 1.0):
        subset_size = max(1, int((len(attribute_list) * random_ratio)))
        attribute_list = random.sample(attribute_list, subset_size)

    if (len(attribute_list) == 1): return attribute_list[0], 0

    current_entropy = calculate_entropy(data, number_of_classes)

    for att in attribute_list:
        
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