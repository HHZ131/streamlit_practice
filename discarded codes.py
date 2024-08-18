#treemap using 
from pyecharts.charts import TreeMap
from pyecharts import options as opts

df_data = pd.DataFrame({"level":["A5-A10","A1-A4","M","A0","S","BP","D","Partner"],
					    "sales":[0.65,0.17,0.14,0.01,0.0,0.0,0.0,0.0],
						"salary":[0.58,0.11,0.16,0.03,0.03,0.03,0.0,0.06]})

df_data.set_index(["level"],inplace = True, drop = True)

data_sales = []
data_salary = []

for name, value in df_data.iterrows():
    data_sales.append({"name":name, "value": value["sales"] * 100})  #shown as percentage
    data_salary.append({"name":name, "value": value["salary"] * 100})  #shown as percentage

#sales part
# color setting function, all squares will use the same color and be differentiated by opacity
def set_opacity(value, max_value, color = (0,0,255)):
	(r, g, b) = color
	alpha = value / max_value
	return f'rgba({r}, {g}, {b}, {alpha})'

max_value = max(item['value'] for item in data_sales)
for item in data_sales:
    item['itemStyle'] = {"color": set_opacity(item['value'], max_value, color = (37, 93, 143))}

#generate treemap
treemap_sales = (
    TreeMap()
    .add(
        series_name="Sales Structure",
        data=data_sales,
        label_opts=opts.LabelOpts(formatter="{b}: {c}%"),
    )
)