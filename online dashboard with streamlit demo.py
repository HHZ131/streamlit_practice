# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:51:11 2024

@author: huhua
"""

import streamlit as st
import plotly.express as px
from pyecharts.charts import Bar, Grid
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
import numpy as np
import pandas as pd

#global functions
def label_format(label: str, formatting_dict = None):
	#extract formatting information
	if formatting_dict is None:
		font_size = ""
		opacity = ""
		line_height = ""
	else:
		font_size = formatting_dict["size"]
		opacity = formatting_dict["opacity"]
		line_height = formatting_dict["line-height"]

	return f"<p style='font-size: {font_size}px; opacity: {opacity}; line-height: {line_height}px;'>{label}</p>"

def find_color_from_cmap(value, vmin, vmax, color_list = ["green", "yellow","orange","red"], reverse = False):
	#reverse color if necessary
	color_list_copy = color_list.copy()
	if reverse:
		color_list_copy = color_list_copy[::-1]
	top_color = color_list_copy.pop()

	#find the color for the input value
	boundaries = np.linspace(vmin, vmax, len(color_list_copy)).tolist()
	for (boundary, color) in zip(boundaries, color_list_copy):
	    if boundary > value:
	        return color
	return top_color

def conditional_formatting(value: float, vmin = None, vmax = None, color_list = ["green", "yellow","orange","red"], reverse = False, numerical_formatting = ".2f", formatting_dict = None):
	#extract formatting information
	if formatting_dict is None:
		font_size = ""
		opacity = ""
		line_height = ""
	else:
		font_size = formatting_dict["size"]
		opacity = formatting_dict["opacity"]
		line_height = formatting_dict["line-height"]

	#a tool to combine all formatting together to generate final results
	def generate_output(color):
		return f"<p style='font-size: {font_size}px; color: {color}; opacity: {opacity}; line-height: {line_height}px'>{value: {numerical_formatting}}</p>"

	if not isinstance(value, (int, float)):
		raise ValueError("Input must be a number.")

	if not(isinstance(vmin, (int, float)) and isinstance(vmax, (int, float))):
		return generate_output("")
	
	#find color and return
	color = find_color_from_cmap(value, vmin, vmax, color_list, reverse)
	
	return generate_output(color)

#Company level main matrics
#set formatting
label_format_dict = {"size": 18,
					 "opacity": "",
					 "line-height": 30}
value_format_dict = {"size": 40,
					 "opacity": 0.9,
					 "line-height": 20}

#values    #to be replaced by analytical process
salary_to_sales = 0.75
fixed_salary = 68149
sales = 495738
commision_to_sales = 0.61
fixed_salary_per_person = 1410
sales_per_person = 11850

#deploy
#set params
height = 90

#row 1
st.markdown("### Company Level")
r1c1, r1c2, r1c3 = st.columns(3)
#column 1
cell = r1c1.container(height = height, border = False)
cell.write(label_format("Total Salary / Sales", label_format_dict), unsafe_allow_html=True)
cell.write(conditional_formatting(salary_to_sales, 0.7, 0.9, numerical_formatting = ".0%", formatting_dict = value_format_dict), unsafe_allow_html=True)
#column 2
cell = r1c2.container(height = height, border = False)
cell.write(label_format("Fixed Salary", label_format_dict), unsafe_allow_html=True)
cell.write(conditional_formatting(fixed_salary, numerical_formatting = ",", formatting_dict = value_format_dict), unsafe_allow_html=True)
#column 3
cell = r1c3.container(height = height, border = False)
cell.write(label_format("Sales", label_format_dict), unsafe_allow_html=True)
cell.write(conditional_formatting(sales, numerical_formatting = ",", formatting_dict = value_format_dict), unsafe_allow_html=True)

#row 2
r2c1, r2c2, r2c3 = st.columns(3)
#column 1
cell = r2c1.container(height = height, border = False)
cell.write(label_format("Commission / Sales", label_format_dict), unsafe_allow_html=True)
cell.write(conditional_formatting(commision_to_sales, 0.5, 0.7, numerical_formatting = ".0%", formatting_dict = value_format_dict), unsafe_allow_html=True)

#column 2
cell = r2c2.container(height = height, border = False)
cell.write(label_format("Fixed Salary Per Person", label_format_dict), unsafe_allow_html=True)
cell.write(conditional_formatting(fixed_salary_per_person, numerical_formatting = ",", formatting_dict = value_format_dict), unsafe_allow_html=True)

#column 3
cell = r2c3.container(height = height, border = False)
cell.write(label_format("Sales Per Person", label_format_dict), unsafe_allow_html=True)
cell.write(conditional_formatting(sales_per_person, numerical_formatting = ",", formatting_dict = value_format_dict), unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------
# Structure-by-Structure Comparison
#Deploy Treemap
#initial container
ax2 = st.container(border = False)
ax2.markdown("### Structure-by-Structure Comparison")
c1, c2 = ax2.columns(2)

#data    #can be replaced by further analysis processes
df_data = pd.DataFrame({"level":["A5-A10","A1-A4","M","A0","S","BP","D","Partner"],
					    "sales":[0.65,0.17,0.14,0.01,0.0,0.0,0.0,0.0],
						"salary":[0.58,0.11,0.16,0.03,0.03,0.03,0.0,0.06]})

#sales part
df_sales = df_data.loc[df_data["sales"] != 0, ["level", "sales"]]
treemap_sales = px.treemap(df_sales, path=[px.Constant("Sales Contribution Structure"),'level'], values='sales', color = 'sales', color_continuous_scale="Blues")
treemap_sales.update_layout(margin=dict(t=0, b=0), 
							font=dict(size=17), 
							height = 300)
treemap_sales.update(layout_coloraxis_showscale=False)
treemap_sales.update_traces(root_color="rgba(0,0,0,0)")
treemap_sales.update_traces(
							texttemplate='%{label}<br>%{value:.0%}',  # Show values as percentiles in the label
    						hovertemplate='<b>%{label}</b><br>Sales: %{value:.0%}<extra></extra>',  # Customize hover info
    						)

c1.plotly_chart(treemap_sales, use_container_width = True)

#salary part
df_salary = df_data.loc[df_data["salary"] != 0, ["level", "salary"]]
treemap_salary = px.treemap(df_salary, path=[px.Constant("Salary Distribution Structure"),'level'], values='salary', color = 'salary', color_continuous_scale="Oranges")
treemap_salary.update_layout(margin=dict(t=0, b=0), 
							font=dict(size=17), 
							height = 300)
treemap_salary.update(layout_coloraxis_showscale=False)
treemap_salary.update_traces(root_color="rgba(0,0,0,0)")
treemap_salary.update_traces(
							texttemplate='%{label}<br>%{value:.0%}',  # Show values as percentiles in the label
    						hovertemplate='<b>%{label}</b><br>Salary: %{value:.0%}<extra></extra>',  # Customize hover info
    						)

#c1.markdown("##### Sales Contribution Structure")
c2.plotly_chart(treemap_salary, use_container_width = True)

#----------------------------------------------------------------------------------------------------
#Operational level and management level matrics
#data     #to be replaced by analytical process later
df_operation = pd.DataFrame({"Level":["A0","A1-A4","A5-A10","M"],
							 "Head Counts": [4,9,25,5],
							 "Avg Sales":[907,9733,13087,15084],
							 "Salary to Sales":[2.69,0.46,0.67,0.83],
							 "Commission Ratio":[0.25,0.45,0.63,0.73]})
df_operation.set_index(["Level"], inplace = True, drop = True)

df_management = pd.DataFrame({"Level":["S","D","BP","Partner"],
							 "Head Counts": [2,1,3,1],
							 "Avg Fixed Salary":[10000,15000,4183,16000],
							 "Management Commission Ratio":[0.01,0.01,0,0.02],
							 "Management Bandwidth":[21,44,14,47]})
df_management.set_index(["Level"], inplace = True, drop = True)

#conditional formatting setup
def background_color_map(row, min_max_bound = None, index_mapping_dict = None, color_list = ["green", "yellow","orange","red"], reverse = False):
	#extract value
	value = row.values[0]

	#decide vmin, vmax
	if index_mapping_dict is not None:
		level = row.name
		if level in index_mapping_dict.keys():
			(vmin, vmax) = index_mapping_dict[level]
		else:
			return [""]     #if not specified, don't format anything
	else:
		(vmin, vmax) = min_max_bound
	#find color
	color = find_color_from_cmap(value, vmin, vmax, color_list, reverse)
	
	return [f'background-color: {color}; opacity: 0.9']

#define formatting logic
#avg sales
sales_cmap_vmin_vmax = {"A0": (500,2500),
					    "A1-A4": (5000, 15000),
					    "A5-A10": (10000, 20000),
					    "M": (10000, 20000)}

salary_to_sales_vmin_vmax = (0.7, 0.9)
commission_ratio_vmin_vmax = (0.5, 0.7)

color_list = ["", "yellow","orange","red"]

#Other formatting params
font_size = 10  #px
df_height = 300

#format operational
df_operation_formatted = df_operation.style.apply(background_color_map, index_mapping_dict = sales_cmap_vmin_vmax, color_list = color_list, reverse = True, subset = ["Avg Sales"], axis = 1) \
								 		   .apply(background_color_map, min_max_bound = salary_to_sales_vmin_vmax, color_list = color_list, reverse = False, subset = ["Salary to Sales"], axis = 1) \
								 		   .apply(background_color_map, min_max_bound = commission_ratio_vmin_vmax, color_list = color_list, reverse = False, subset = ["Commission Ratio"], axis = 1) \
								 		   .set_table_styles([{'selector': 'td:hover',
      											   			   'props': f'font-size: {font_size}px'}]) \
							     		   .format({"Avg Sales": "{:,}",
							     	      		    "Salary to Sales": "{:.0%}",
							     	      			"Commission Ratio": "{:.0%}"})

ax0 = st.container(border = False)
ax0.markdown("### Operational Level")
ax0.dataframe(df_operation_formatted, use_container_width = True)

#--------------------------------------------------------------------------------------------------
# bar in bar chart
# Provided data
data = pd.DataFrame({
    'level': ['M', 'A5-A10', 'A1-A4', 'A0'],
    'Avg Sales': [15083.70, 13086.53, 9732.78, 907.33],
    'Avg Fixed Salary': [1428.57, 510.20, 157.07, 2210.47],
    'Avg Commission': [10959.07, 8245.20, 4336.23, 231.30],
    'Avg Management Commission': [3500, 0, 0, 0]
})

# Define RGB values for outer and inner bars
outer_r, outer_g, outer_b = 65, 114, 196  # Blue for outer bars
inner_r, inner_g, inner_b = 255, 165, 0  # Orange for inner bars

# Set text color
text_color = "#A6A6A6"

# Create the bar chart
bar_outer = Bar()
bar_inner = Bar()

# Add x-axis data
bar_outer.add_xaxis(data["level"].tolist())
bar_inner.add_xaxis(data["level"].tolist())

# Add y-axis data with adjusted bar width and hidden labels
bar_outer.add_yaxis(
    "Avg Sales", data['Avg Sales'].tolist(), category_gap="50%", bar_width=20, label_opts=opts.LabelOpts(is_show=False),
    itemstyle_opts=opts.ItemStyleOpts(color=f"rgba({outer_r}, {outer_g}, {outer_b}, 1)")
)

# Add inner stacked bars with adjusted bar width, hidden labels, and custom colors
bar_inner.add_yaxis(
    "Avg Commission", data['Avg Commission'].tolist(), stack="stack1", category_gap="50%", bar_width=10, label_opts=opts.LabelOpts(is_show=False),
    itemstyle_opts=opts.ItemStyleOpts(color=f"rgba({inner_r}, {inner_g}, {inner_b}, 1)")
)
bar_inner.add_yaxis(
    "Avg Fixed Salary", data['Avg Fixed Salary'].tolist(), stack="stack1", category_gap="50%", bar_width=10, label_opts=opts.LabelOpts(is_show=False),
    itemstyle_opts=opts.ItemStyleOpts(color=f"rgba({inner_r}, {inner_g}, {inner_b}, 0.7)")
)
bar_inner.add_yaxis(
    "Avg Management Commission", data['Avg Management Commission'].tolist(), stack="stack1", category_gap="50%", bar_width=10, label_opts=opts.LabelOpts(is_show=False),
    itemstyle_opts=opts.ItemStyleOpts(color="rgba(255, 140, 0, 1)")
)

# Make it horizontal
bar_outer.reversal_axis()
bar_inner.reversal_axis()

# Configure to hide grid lines and x-axis ticks
bar_outer.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        splitline_opts=opts.SplitLineOpts(is_show=False),
        axisline_opts=opts.AxisLineOpts(is_show=False),
        axistick_opts=opts.AxisTickOpts(is_show=False),
        axislabel_opts=opts.LabelOpts(color=text_color)
    ),
    yaxis_opts=opts.AxisOpts(
        splitline_opts=opts.SplitLineOpts(is_show=False),
        axistick_opts=opts.AxisTickOpts(is_show=False),
        axislabel_opts=opts.LabelOpts(color=text_color)
    ),
    legend_opts=opts.LegendOpts(pos_top="5%", pos_right="32%", orient="vertical",textstyle_opts=opts.TextStyleOpts(color=text_color))
)
bar_inner.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        splitline_opts=opts.SplitLineOpts(is_show=False),
        axisline_opts=opts.AxisLineOpts(is_show=False),
        axistick_opts=opts.AxisTickOpts(is_show=False),
        axislabel_opts=opts.LabelOpts(color=text_color)
    ),
    yaxis_opts=opts.AxisOpts(
        splitline_opts=opts.SplitLineOpts(is_show=False),
        axistick_opts=opts.AxisTickOpts(is_show=False),
        axislabel_opts=opts.LabelOpts(color=text_color)
    ),
    legend_opts=opts.LegendOpts(pos_top="5%", pos_right="0%", orient="vertical",textstyle_opts=opts.TextStyleOpts(color=text_color))
)

# Combine the charts using Grid
grid = Grid(init_opts=opts.InitOpts(height="200px"))   #doesn't work so far
grid.add(bar_outer, grid_opts=opts.GridOpts(pos_left="8%", pos_right="5%", pos_top="5%", pos_bottom="0%", height="180px"))
grid.add(bar_inner, grid_opts=opts.GridOpts(pos_left="8%", pos_right="5%", pos_top="5%", pos_bottom="0%", height="180px"))

# Render the chart in Streamlit container
ax = st.container(height = 280, border = False)
ax.markdown("### Operational Level - A Closer Look")
with ax:
    st_pyecharts(grid)

#------------------------------------
#format management
#define formatting logic
#avg sales
avg_fixed_salary_cmap_vmin_vmax = {"S": (5000,12000),     #For this part, the formatting rules can be replaced by more 
					    		   "D": (10000, 20000),   #sophisticated settings, for example, the warning zone for S level
					    		   "BP": (5000, 10000)}   #can be determined by management bandwidth and company-level profits jointly

commission_ratio_vmin_vmax = (0.02, 0.1)

color_list = ["", "yellow","orange","red"]

bandwidth_vmin_vmax = {"S": (10, 30),     #formatting rules for management bandwidth are generally reversely "U-curved"
					   "D": (50, 80),     #the settings between vmin and vmax can be treated as "comfort zones"
					   "BP": (10, 30)}

bandwidth_color_list = ["yellow", "","yellow"]

#Other formatting params
font_size = 10  #px
df_height = 300

df_management_formatted = df_management.style.apply(background_color_map, index_mapping_dict = avg_fixed_salary_cmap_vmin_vmax, color_list = color_list, reverse = False, subset = ["Avg Fixed Salary"], axis = 1) \
								 		     .apply(background_color_map, min_max_bound = commission_ratio_vmin_vmax, color_list = color_list, reverse = False, subset = ["Management Commission Ratio"], axis = 1) \
								 		     .apply(background_color_map, index_mapping_dict = bandwidth_vmin_vmax, color_list = bandwidth_color_list, reverse = False, subset = ["Management Bandwidth"], axis = 1) \
								 		     .set_table_styles([{'selector': 'td:hover',
      											   			     'props': f'font-size: {font_size}px'}]) \
							     		     .format({"Avg Fixed Salary": "{:,}",
							     	      		      "Management Commission Ratio": "{:.0%}",
							     	      			  "Management Bandwidth": "{:.0f}"})

ax1 = st.container(border = False)
ax1.markdown("### Mangement Level")
ax1.dataframe(df_management_formatted, use_container_width = True)

