import matplotlib.patches as mpatches
import os
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import sys
import numpy as np
import seaborn as sbn
from matplotlib.lines import Line2D

data_of_houses = 0
images = []
current_course = 0
ax = 0
fig = 0
courses = 0

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
				axs[i].set_xlabel(f"Score of {course}")
				axs[i].set_ylabel(f"Score of {current_course}")
			i += 1


def save_all(data_of_houses):
	global images

	num_courses = len(courses) - 1
	ncols = int(num_courses ** 0.5) + 1
	nrows = (num_courses - 1) // ncols + 1
	colors = plt.cm.viridis(np.linspace(0, 1, len(data_of_houses)))
	os.makedirs("images/", exist_ok=True)
	custom_lines = [Line2D([0], [1], color=colors[0], lw=16	),
					Line2D([0], [1], color=colors[1], lw=16	),
					Line2D([0], [1], color=colors[2], lw=16	),
					Line2D([0], [1], color=colors[3], lw=16	)]
	for i, course in enumerate(courses):
		fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15,12))
		axs = axs.flatten()
		fig.suptitle(f"{course} with:", fontsize=25)
		display_course(fig, axs, colors, course, courses)
		fig.legend(custom_lines, ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff'],\
				fontsize='x-large', loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.01),\
				handlelength=4.5, handleheight=3.5, borderpad=1.0)
		plt.tight_layout(rect=[0, 0.1, 1, 1])
		fig.savefig(f"images/img{i}")
		images.append(mpimg.imread(f"images/img{i}.png"))
		plt.close()


def display_with_widget():
	global ax
	global current_course

	current_course %= (len(courses) - 1)

	ax.clear()
	ax.imshow(images[current_course])
	ax.axis('off')
	plt.draw()


def on_key(event):
	global current_course
	global fig

	if event.key == 'left':
		current_course -= 1
		display_with_widget()
	elif event.key == 'right':
		current_course += 1
		display_with_widget()
	elif event.key == 'escape':
		plt.close(fig)


def main():
	data = pd.read_csv("dataset_train.csv")
	global courses
	global data_of_houses
	global ax
	global fig

	courses = data.columns[6:]
	data_of_houses = get_data_of_houses(data)
	save_all(data_of_houses)
	fig, ax = plt.subplots(figsize=(15,12))
	fig.canvas.mpl_connect('key_press_event', on_key)
	display_with_widget()
	plt.show()
	

if __name__ == "__main__":
	main()