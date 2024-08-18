# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:45:02 2024

@author: huhua
"""

import numpy as np
import pandas as pd

lower = 70
upper = 90
test_number = 81

def conditional_formatting(number: float, upper: float, lower: float, reverse = False, numerical_formatting = None):
    if not (isinstance(number, (int, float)) and isinstance(upper, (int, float)) and isinstance(lower, (int, float))):
        raise ValueError("Input to format, upper bound, and lower bound must be numbers.")
    
    #define the color, reverse if necessary
    color_list = ["green", "yellow","orange","red"]    #four colors definded so far
    if reverse:
        color_list = color_list[::-1]
    top_color = color_list.pop()

    def generate_output(color):
        return f":{color}[{number}]"

    #find the color for the input number
    boundaries = np.linspace(lower, upper, len(color_list)).tolist()
    print(boundaries)
    for (boundary, color) in zip(boundaries, color_list):
        if boundary > number:
            print(number)
            print(boundary)
            print(color)
            return generate_output(color)
    return generate_output(top_color)

print(conditional_formatting(test_number, upper, lower))

df_data = pd.DataFrame({"level":["A5-A10","A1-A4","M","A0","S","BP","D","Partner"],
					    "sales":[0.65,0.17,0.14,0.01,0,0,0,0],
						"salary":[0.58,0.11,0.16,0.03,0.03,0.03,0,0.06]})

df_data.set_index(["level"],inplace = True, drop = True)

data_sales = []
data_salary = []

for name, value in df_data.iterrows():
    data_sales.append({"name":name, "value": value["sales"]})
    data_salary.append({"name":name, "value": value["salary"]})
    
