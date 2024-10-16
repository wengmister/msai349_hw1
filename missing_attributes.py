import parse
import copy


def get_average_value(data, attribute):
    """
    Get the most frequent value of the attribute.
    """
    appeared_values = []
    appeared_values_times = []
    for data_point in data:
        if data_point[attribute] != '?':
            if(data_point[attribute] not in appeared_values):
                appeared_values.append(data_point[attribute])
                appeared_values_times.append(1)
            else:
                appeared_values_times[appeared_values.index(data_point[attribute])] += 1
    most_frequnt_value = appeared_values[appeared_values_times.index(max(appeared_values_times))]
    return most_frequnt_value
    

def wash_data(data):
    """
    Replace missing attributes with the most frequent value of the attribute.
    """
    data = copy.deepcopy(data)
    for index, data_point in enumerate(data):
        for key, value in data_point.items():
            if value == '?':
                data_point[key] = get_average_value(data, key)
        data[index] = data_point
    return data


if __name__ == "__main__":
    # Print the data points with missing attributes
    data = parse.parse("house_votes_84.data")
    for data_point in data:
        flag_invalid_data = False
        for key, value in data_point.items():
            if value == '?':
                flag_invalid_data = True
                break
        if flag_invalid_data:
            print(data_point)
    
    # Segment data before and after washing
    print("=========================================")

    # Print the data points with missing attributes after washing
    washed_data = wash_data(data)
    for data_point in washed_data:
        flag_invalid_data = False
        for key, value in data_point.items():
            if value == '?':
                flag_invalid_data = True
                break
        if flag_invalid_data:
            print(data_point)
