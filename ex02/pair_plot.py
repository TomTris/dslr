import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import screeninfo
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

houses = 0
data_of_houses = 0
data = 0
courses = 0
colors = 0

def get_data_of_houses(data):
	global houses
	global data_of_houses
	houses = []
	data_of_houses = []
	for each_house in data.iloc[:, 1]:
		if each_house not in houses:
			houses.append(each_house)
			data_of_houses.append(data[data[data.columns[1]] == each_house])
	return data_of_houses
	


def creat_frame(num_courses, axs):
	for i in range(num_courses):
		if len(courses[i]) > 15:
			shortened_course_name = (courses[i][:12] + '...')
		else:
			shortened_course_name = courses[i]
		axs[i * num_courses].set_ylabel(shortened_course_name)
		axs[i].set_title(shortened_course_name)


def format_ticks(x, pos):
    if x >= 1000 or x <= -1000:
        return f'{int(x/1000)}k' 
    return str(int(x))


def display_inside_axs(num_courses, axs):
	col = -1
	row = 0

	for ax in axs:
		col += 1
		if col == len(courses):
			col = 0
			row += 1
		if col == row:
			max = data[courses[col]].max()
			min = data[courses[col]].min()
			for cnt in range(len(data_of_houses)):
				ax.hist((data_of_houses[cnt])[courses[col]], \
					bins=20, alpha=0.7, color=colors[cnt], range=(min, max))
			
		else:
			for cnt, data_of_house in enumerate(data_of_houses):
				ax.scatter(x=data_of_house[courses[col]], y=data_of_house[courses[row]],\
					alpha=0.5, color=[colors[cnt]], s=3)
		ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_ticks))
		ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_ticks))

def on_key(event):
	if event.key == 'escape':
		plt.close()

def display_all():
	num_courses = len(courses)
	custom_lines = []
	for i in range(len(colors)):
		custom_lines.append(Line2D([0], [1], color=colors[i], lw=16))	

	screen = screeninfo.get_monitors()[0]
	fig, axs = plt.subplots(ncols=num_courses, nrows=num_courses, \
						 figsize=(screen.width / 130, screen.height / 113))
	axs = axs.flatten()
	creat_frame(num_courses, axs)
	display_inside_axs(num_courses, axs)

	
	fig.legend(custom_lines, houses,\
				fontsize='x-large', loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.005),\
				handlelength=4.5, handleheight=3.5, borderpad=1.0)
	plt.tight_layout(rect=[0, 0.05, 1, 1])
	fig.canvas.mpl_connect('key_press_event', on_key)
	plt.show()

def main():
	try:
		if len(sys.argv) != 2:
			raise Exception("Error: Wrong amount of args")
		global data
		global courses
		global colors
		data = pd.read_csv(sys.argv[1])
		get_data_of_houses(data)
		colors = plt.cm.viridis(np.linspace(0, 1, len(data_of_houses)))
		courses = data.columns[6:]
		display_all()
	except Exception as e:
		print(e, file=sys.stderr)
		print("Usage: python3 pair_plot.py <dataset>\nExample:", file=sys.stderr)
		print("python3 pair_plot.py dataset_train.csv", file=sys.stderr)

if __name__ == "__main__":
	main()