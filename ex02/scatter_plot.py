import time
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import sys
import numpy as np
import seaborn as sbn

current_course = 0
num_courses = 0
ncols = 0
nrows = 0
fig = 0
axs = 0
axs = 0
colors = 0
courses = 0
data_of_houses = 0

def get_data_of_houses(data):
	houses = []
	for each_house in data.iloc[:, 1]:
		if each_house not in houses:
			houses.append(each_house)
	
	data_of_houses = []
	for house in houses:
		data_of_houses.append(data[data[data.columns[1]] == house])
	return data_of_houses


def display_course(event=0):
	global axs
	# global current_course

	# if (event == 'left'):
	# 	current_course -= 1
	# if (event == 'right'):
	# 	current_course += 1
	# print(1)
	# current_course = current_course % len(courses)
	i = 0
	for ax in axs:
		ax.cla()

	for course in courses:
		if course != current_course:
			for cnt, data_of_house in enumerate(data_of_houses):
				# mask = ~np.isnan(data_of_house[course]) & ~np.isnan(data_of_house[current_course])
				# print(len(mask))
				axs[i].scatter(x=data_of_house[course], y=data_of_house[current_course],\
					alpha=0.5, color=[colors[cnt]], s=10)
			i += 1
	plt.draw()


def display_all(data_of_houses, data):
	global num_courses
	global ncols
	global nrows
	global fig
	global axs
	global colors
	global current_course

	num_courses = len(courses) - 1
	ncols = int(num_courses ** 0.5) + 1
	nrows = (num_courses - 1) // ncols + 1
	fig, axs = plt.subplots(nrows, ncols, figsize=(15,12))
	axs = axs.flatten()
	colors = plt.cm.viridis(np.linspace(0, 1, len(data_of_houses)))
	for i, course in enumerate(courses):
		current_course = course
		display_course()
		fig.savefig(f"img{i}")
		i += 1


def main():
	data = pd.read_csv("dataset_train.csv")
	global courses
	global data_of_houses

	courses = data.columns[6:]
	data_of_houses = get_data_of_houses(data)
	display_all(data_of_houses, data)
	

if __name__ == "__main__":
	main()