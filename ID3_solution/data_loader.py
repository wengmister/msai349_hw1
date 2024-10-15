import csv
from collections import Counter


class DataLoader:
    '''
    Class to load and
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.data = []
        self.data_archive = []
        self.data_loaded = False
        self.data_size = 0
        
    
    def get_most_frequent_label(self, data):
        # Extract the 'Class' values from each dictionary in the list
        labels = [item['Class'] for item in data]
        
        # Count the occurrences of each label
        label_count = Counter(labels)
        
        # Find the label with the highest count
        most_frequent_label = label_count.most_common(1)[0][0]
        
        return most_frequent_label


    def get_attribute_names(self):
        '''
        Returns the attribute names
        
        Args:
        None
        
        Returns:
        list, the attribute names
        '''
        if(self.data_loaded == False):
            print("Data not loaded, no attribute names.")
            
        return list(self.data[0].keys())
    
    
    def get_data_size(self):
        '''
        Returns the size of the data
        
        Args:
        None
        
        Returns:
        int, the size of the data
        '''
        if(self.data_loaded == False):
            print("Data not loaded, size is 0.")
            
        return self.data_size
    
    
    def load_data(self, filename):
        '''
        Takes a filename and returns attribute information and all the data in array of dictionaries
        Credit: This function derived from parer.py in the homework folder.
        
        Args:
        filename - string, the name of the file
        
        Returns:
        data - list of dictionaries, the dataset
        '''
        
        # initialize variables
        data = []  
        
        # note: you may need to add encoding="utf-8" as a parameter
        csvfile = open(filename,'r')
        fileToRead = csv.reader(csvfile)
        headers = next(fileToRead)

        # iterate through rows of actual data
        for row in fileToRead:
            data.append(dict(zip(headers, row)))
            self.data_archive.append(dict(zip(headers, row)))
        
        # Set the data and data_loaded variables
        self.data = data
        self.data_loaded = True
        
        # Set the data size
        self.data_size = len(data)
        
        return data
    
    
    def split_data_by_attribute(self, attribute):
        '''
        Split the data by the attribute.
        
        Credit: This function is derived from split_data_by_attribute(data,seperator_attribute) 
                in separate.py, originally written by Kris Weng and Ben Benyamin.
        
        Args:
        data - list of dictionaries, the dataset
        attribute - string, the attribute to split the data by
        
        Returns:
        splited_data - dictionary, the data split by the attribute, where the key is
                       the attribute value
        '''
        splited_data = {}
        
        # Split the data by the attribute
        for data_point in self.data:
            # If the attribute value is not in the dictionary, add it
            if (not data_point[attribute] in splited_data.keys()):
                splited_data[data_point[attribute]] = []
                
            # Add the row to the dictionary
            splited_data[data_point[attribute]].append(data_point)
            
        return splited_data
    
    
    def delete_attribute(self, attribute):
        '''
        Delete the attribute from the data
        
        Args:
        attribute - string, the attribute to delete
        
        Returns:
        None
        '''
        for data_point in self.data:
            if (attribute in data_point.keys()):
                del data_point[attribute]
                
                
    def print_data(self):
        '''
        Print the data
        
        Args:
        None
        
        Returns:
        None
        '''
        if(self.data_loaded == False):
            print("Data not loaded.")
        else:
            for row in self.data:
                print(row)