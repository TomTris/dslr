import os
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import sys
import numpy as np
import seaborn as sbn

data_of_houses = 0
images = []

def get_data_of_houses(data):
	houses = []
	for each_house in data.iloc[:, 1]:
		if each_house not in houses:
			houses.append(each_house)
	
	data_of_houses = []
	for house in houses:
		data_of_houses.append(data[data[data.columns[1]] == house])
	return data_of_houses


def display_course(fig, axs, colors, current_course, courses):

	# for ax in axs:
	# 	ax.cla()

	i = 0
	for course in courses:
		if course != current_course:
			for cnt, data_of_house in enumerate(data_of_houses):
				axs[i].scatter(x=data_of_house[course], y=data_of_house[current_course],\
					alpha=0.5, color=[colors[cnt]], s=10)
				axs[i].set_title(course)
			i += 1


def save_all(data_of_houses, data):
	num_courses = len(courses) - 1
	ncols = int(num_courses ** 0.5) + 1
	nrows = (num_courses - 1) // ncols + 1
	colors = plt.cm.viridis(np.linspace(0, 1, len(data_of_houses)))
	os.makedirs("images/", exist_ok=True)
	global images
	for i, course in enumerate(courses):
		fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15,12))
		axs = axs.flatten()
		fig.suptitle(f"{course} with:", fontsize=25)
		display_course(fig, axs, colors, course, courses)
		fig.savefig(f"images/img{i}")
		images.append(mpimg.imread(f"images/img{i}.png"))
		plt.close()


# def display_with_widget():
# 	global current_course
# 	global axs

# 	current_course += 1
# 	axs.clear()
# 	fig.imgshow(images[current_course])



def main():
	data = pd.read_csv("dataset_train.csv")
	global courses
	global data_of_houses

	courses = data.columns[6:]
	data_of_houses = get_data_of_houses(data)
	save_all(data_of_houses, data)
	# display_with_widget()
	

if __name__ == "__main__":
	main()