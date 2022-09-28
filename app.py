from flask import Flask, render_template, redirect, url_for, flash
import sqlite3
from datetime import datetime
import json
import copy
import datetime as DT
from flask import request
import os
from keras.models import load_model
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from keras.preprocessing import image
import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import shutil
import sys
#123
app = Flask(__name__)
app.secret_key = b'_5#y2L'

def update_DB(parent_dir):
	model = load_model('static/myModel.h5')
	data_dict = {0: 'Chocopie', 1: 'Coke', 2: 'Eraser', 3: 'Fanta', 4: 'Haribo', 5: 'Homerun', 6: 'Pencil', 7: 'Pocachip',8: 'Ramen_chips', 9: 'Ramen_hot', 10: 'Ramen_mild', 11: 'Sprite', 12: 'White'}
	sqliteConnection = sqlite3.connect('static/history.db',timeout = 10)
	crsr = sqliteConnection.cursor()
	for subdir, dirs, files in os.walk(parent_dir):
		for file in files:
			if not file.startswith('.'):
				path = os.path.join(subdir, file)
				if datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d %H:%M:%S"):
					img = Image.open(path)
					now = datetime.now()
					date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					# print(date)

					test_image = tf.keras.utils.load_img(path, target_size=(224,224))
					test_image = tf.keras.utils.img_to_array(test_image)
					test_image = np.expand_dims(test_image, axis = 0) #change image into array

					result = model.predict(test_image)

					# print(result)
					# print(result[0].argmax(axis=0)) #selects greatest number (which is 1)
					# print(data_dict[result[0].argmax(axis=0)])
					item = data_dict[result[0].argmax(axis=0)]

					insert = " INSERT INTO purchase VALUES(?,?)" #(?,?) --> (current, kind_object) from line below
					update_left = "UPDATE Stock SET left = left -1 WHERE type_object = (?)"
					update_accumulate = "UPDATE Stock SET accumulate = accumulate + 1 WHERE type_object = (?)"

					crsr.execute(insert,(date,item))
					crsr.execute(update_left,(item,))
					crsr.execute(update_accumulate,(item,))
					img.close()
					shutil.move(path, "static/old_images")
					sqliteConnection.commit()

@app.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == "POST":
		update_DB("static/images")
		flash('Successfully Updated')
		return redirect(url_for('index'))
	else: 

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

		initial = "SELECT initial FROM Stock"
		crsr.execute(initial)
		initial_list = (crsr.fetchall())
		lst_initial = []
		for i in initial_list:
			lst_initial.append(i[0])

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
		if 
		top_lst = sorted(count_dict, key = count_dict.get, reverse = True)[:3]
		if len(top_lst) == 0:
			top1_week="No purchase in this week"
		else:
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

		data_dict2 = {0: 'Chocopie', 1: 'Ramen_hot', 2: 'Ramen_mild', 3: 'Ramen_chips', 4: 'Pocachip', 5: 'Haribo', 6: 'Coke', 7: 'Sprite',8: 'Fanta', 9: 'White', 10: 'Eraser', 11: 'Pencil', 12: 'Homerun'}
		profit = "SELECT accumulate*profit,type_object as total_profit FROM Stock"
		crsr.execute(profit)
		profit_list = crsr.fetchall()
		lst4 = []
		t_profit = 0
		for i in profit_list:
			lst4.append(int(i[0]))
			t_profit = t_profit + int(i[0])

		temp_list = lst4.copy()
		print(profit_list, file=sys.stderr)
		largest = max(lst4)
		largest_index = lst4.index(largest)
		largest_item = data_dict2[largest_index]
		temp_list.remove(largest)
		sec_largest = max(temp_list)
		sec_largest_index = lst4.index(sec_largest)
		sec_largest_item = data_dict2[sec_largest_index]
		temp_list.remove(sec_largest)
		third_largest = max(temp_list)
		third_largest_index = lst4.index(third_largest)
		third_largest_item = data_dict2[third_largest_index]
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
		return render_template('index.html', lst = lst, lst2= lst2, lst3= lst3,lst_initial=lst_initial, top1_week = top1_week, top1_month = top1_month, top1_year = top1_year, t_profit = t_profit, top_margin = top_margin, top_margin_value = top_margin_value)

if __name__ == '__main__':
	app.run(debug = True)