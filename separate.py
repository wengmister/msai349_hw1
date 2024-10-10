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

def find_best_attribute_to_split_on(data):
    """
    Identifies the attribute that minimizes entropy for data splitting.

    Parameters:
    data (list or DataFrame): The dataset to analyze, consisting of multiple data points.
    attribute_list (list): A list of attributes to evaluate for potential splits.
    """

    smallest_H = 1
    chosen_att = ""

    #Assume the all of the examples has all of the attributes (even if unkown)
    attribue_list = list(data[0].keys())[:-1]

    for att in attribue_list:
        
        seg_data = split_data_by_attribute(data,att)

        this_H = 0.0
        for att_type in seg_data.keys():
            this_H += 1.0*calculate_entropy(seg_data[att_type]) * len(seg_data[att_type])/len(data)

        print(f"{att}: {this_H}")

        if(this_H < smallest_H):
            smallest_H = this_H
            chosen_att = att
    
    return chosen_att

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