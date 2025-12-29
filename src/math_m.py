class Math_m():
    ### Calculates the moving average at datapoint i for n values. The moving average at datapoint i is calculated with the datapoints between i - n + offset and i + offset.###
    ### If there's not enough datapoints within the given range it will shorten the length of n to fit the data.                                                         ###
    def calculate_moving_average(data, n, offset=0):
        result = []
        for i in range(len(data)):
            lower_boundary = max(0, i - n + offset + 1)
            upper_boundary = min(len(data), i + offset + 1) 

            moving_average = sum(data[lower_boundary:upper_boundary])/(upper_boundary - lower_boundary)

            result.append(moving_average)  
        return result
