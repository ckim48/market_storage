from keras.models import load_model
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from keras.preprocessing import image
import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import os.path
import time
import sqlite3
from datetime import datetime

model = load_model('myModel.h5')
data_dict = {0: 'Chocopie', 1: 'Coke', 2: 'Eraser', 3: 'Fanta', 4: 'Haribo', 5: 'Homerun', 6: 'Pencil', 7: 'Pocachip',8: 'Ramen_chips', 9: 'Ramen_hot', 10: 'Ramen_mild', 11: 'Sprite', 12: 'White'}
parent_dir = "data_image/"

def calc_profits():
	sqliteConnection = sqlite3.connect('static/history.db')
	crsr = sqliteConnection.cursor()
	calc = "SELECT type_object, profit * accumulate AS total_profit FROM Stock"
	crsr.execute(calc)
	profit_lst = (crsr.fetchall())
	sqliteConnection.close()

def update_DB(parent_dir):
	sqliteConnection = sqlite3.connect('static/history.db',timeout = 10)
	crsr = sqliteConnection.cursor()
	for subdir, dirs, files in os.walk(parent_dir):
		for file in files:
			if not file.startswith('.'):
				path = os.path.join(subdir, file)
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
				sqliteConnection.commit()
	sqliteConnection.close()
	print("Finished")
update_DB(parent_dir)
#calc_profits()