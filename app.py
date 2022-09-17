from flask import Flask, render_template
import sqlite3
from datetime import datetime
import json
import copy
import datetime as DT

app = Flask(__name__)
@app.route('/')
def hello_world():
	sqliteConnection = sqlite3.connect('static/history.db')
	crsr = sqliteConnection.cursor()
	calc = "SELECT type_object FROM Stock"
	crsr.execute(calc)
	obj_lst = (crsr.fetchall())
	lst = []
	for i in obj_lst:
		lst.append(i[0])

	acc = "SELECT left FROM Stock"
	crsr.execute(acc)
	accumulate_list = (crsr.fetchall())
	lst2 = []
	for i in accumulate_list:
		lst2.append(i[0])

	left = "SELECT left FROM Stock"
	crsr.execute(left)
	left_list = (crsr.fetchall())
	lst3 = []
	for i in left_list:
		lst3.append(i[0])

	count_dict = {}
	today = DT.date.today() + DT.timedelta(days = 1)
	#items sold the most (weekly)
	week_ago = today - DT.timedelta(days=7)
	time_sales = "SELECT * FROM purchase WHERE time_stamp Between ? and ?"
	crsr.execute(time_sales, (week_ago,today))
	week_lst = crsr.fetchall()
	for i in week_lst:
		count = count_dict.get(i[1],0)+1
		count_dict [i[1]] = count

	top_lst = sorted(count_dict, key = count_dict.get, reverse = True)[:3]
	top1_week = top_lst[0]

	#items sold the most (monthly)
	month_ago = today - DT.timedelta(days=30)
	crsr.execute(time_sales, (month_ago,today))
	month_lst = crsr.fetchall()
	count_dict = {}
	for i in month_lst:
		count = count_dict.get(i[1],0)+1
		count_dict [i[1]] = count
	top_lst = sorted(count_dict, key = count_dict.get, reverse = True)[:3]
	top1_month = top_lst[0]

	#items sold the most (yearly)
	year_ago = today - DT.timedelta(days=365)
	crsr.execute(time_sales, (year_ago,today))
	year_lst = crsr.fetchall()
	count_dict = {}
	for i in year_lst:
		count = count_dict.get(i[1],0)+1
		count_dict [i[1]] = count
	top_lst = sorted(count_dict, key = count_dict.get, reverse = True)[:3]
	top1_year = top_lst[0]

	data_dict = {0: 'Chocopie', 1: 'Coke', 2: 'Eraser', 3: 'Fanta', 4: 'Haribo', 5: 'Homerun', 6: 'Pencil', 7: 'Pocachip',8: 'Ramen_chips', 9: 'Ramen_hot', 10: 'Ramen_mild', 11: 'Sprite', 12: 'White'}
	profit = "SELECT accumulate*profit as total_profit FROM Stock"
	crsr.execute(profit)
	profit_list = crsr.fetchall()
	lst4 = []
	t_profit = 0
	for i in profit_list:
		lst4.append(int(i[0]))
		t_profit = t_profit + int(i[0])

	temp_list = lst4.copy()
	largest = max(lst4)
	largest_index = lst4.index(largest)
	largest_item = data_dict[largest_index]
	temp_list.remove(largest)
	sec_largest = max(temp_list)
	sec_largest_index = lst4.index(sec_largest)
	sec_largest_item = data_dict[sec_largest_index]
	temp_list.remove(sec_largest)
	third_largest = max(temp_list)
	third_largest_index = lst4.index(third_largest)
	third_largest_item = data_dict[third_largest_index]
	temp_list.remove(third_largest)

	else_value = 0
	for i in temp_list:
		else_value = else_value + i

	top_margin = []
	top_margin.append(largest_item)
	top_margin.append(sec_largest_item)
	top_margin.append(third_largest_item)
	top_margin.append("Else")

	top_margin_value = []
	top_margin_value.append(largest)
	top_margin_value.append(sec_largest)
	top_margin_value.append(third_largest)
	top_margin_value.append(else_value)

	sqliteConnection.close()
	return render_template('index.html', lst = lst, lst2= lst2, lst3= lst3, top1_week = top1_week, top1_month = top1_month, top1_year = top1_year, t_profit = t_profit, top_margin = top_margin, top_margin_value = top_margin_value)

if __name__ == '__main__':
	app.run(debug = True)