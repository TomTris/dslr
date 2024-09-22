import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import csv 
import pandas as pd
import sys
import numpy as np

column = 20
houses = 0

def eprint(*args, **kwargs):
	print('Error:', *args, file=sys.stderr, **kwargs)


def generate_courses():
	with open(sys.argv[1]) as file:
		reader = csv.reader(file, delimiter=',')
		reader = list(reader)
		reader = np.array(reader[0])
		return reader[6:]


def normalize_score(data, courses):
	for course in courses:
		old_max = data[course].max()
		old_min = data[course].min()
		data[course] = (data[course] - old_min) / (old_max - old_min)
		for i in range(len(data[course])):
			column2 = column - 1
			value = data.at[i, course]
			while not np.isnan(value):
				if value >= column2 / column:
					data.at[i, course] = column2 / column + (0.1 / column)
					break
				column2 -= 1


def get_data_of_houses(data):
	global houses
	houses = []
	mix_houses = data['Hogwarts House']
	for house in mix_houses:
		if house not in houses:
			houses.append(house)
	
	data_of_houses = []
	for house in houses:
		data_of_houses.append(data[data[data.columns[1]] == house])
	return data_of_houses


def display_all(courses, data_of_houses, winner):
	num_courses = len(courses)
	ncols = int(num_courses ** 0.5) + 1
	nrows = (num_courses - 1 ) // ncols + 1
	fig, axs = plt.subplots(nrows, ncols, figsize=(15, 12))
	axs = axs.flatten() #convert 2D to 1D Axes
	colors = plt.cm.viridis(np.linspace(0, 1, len(data_of_houses)))

	for i, course in enumerate(courses):
		for cnt in range(len(data_of_houses)):
			axs[i].hist((data_of_houses[cnt])[course], bins=column, alpha=0.7, color=colors[cnt], range=(0.0, 1.0))
		if (course == winner):
			winner_title = 'WINNER: ' + course
			axs[i].set_title(winner_title)
		else:
			axs[i].set_title(course)
		axs[i].set_xlabel('Normalized Scores')
		axs[i].set_ylabel('Frequency')

	for j in range(len(courses), len(axs)):
		fig.delaxes(axs[j])
	
	custom_lines = []
	for i in range(len(colors)):
		custom_lines.append(Line2D([0], [1], color=colors[i], lw=16))
	
	fig.legend(custom_lines, houses,\
				fontsize='x-large', loc='lower right', ncol=1, bbox_to_anchor=(1, 0),\
				handlelength=4.5, handleheight=3.5, borderpad=1.0)

	plt.tight_layout()
	plt.show()


def find_winner(courses, data_of_houses):	
	interval_percentage = {}
	for course in courses:
		interval_percentage[course] = [100] * column
		for data_of_house in data_of_houses:
			interval = [0] * column
			student_total = 0
			for each_score in data_of_house[course]:
				if not np.isnan(each_score):
					interval[int(each_score * column)] += 1
					student_total += 1
			for cnt in range(column):
				if interval[cnt] / student_total * 100 < (interval_percentage[course])[cnt]:
					(interval_percentage[course])[cnt] = interval[cnt] / student_total * 100
	max_percentage = 0
	winner = ''
	for course in interval_percentage:
		sum_interval_percentage = sum(interval_percentage[course])
		if sum_interval_percentage > max_percentage:
			winner = course
			max_percentage = sum_interval_percentage
	print("Winner:", winner)
	print("Max_percentage:", max_percentage)
	print()
	return winner

def main() -> None:
	try:
		if len(sys.argv) > 3:
			raise Exception("Too many args")
		if len(sys.argv) == 1:
			raise Exception("Too little args")
		data = pd.read_csv(sys.argv[1])
		courses = generate_courses()
		normalize_score(data, courses)
		data_of_houses = get_data_of_houses(data)
		winner = find_winner(courses, data_of_houses)
		display_all(courses, data_of_houses, winner)

	except Exception as e:
		eprint(e)
		print('Usage: python3 histogram.py <dataset>', file=sys.stderr)
		print("For example:", file=sys.stderr)
		print("python3 histogram.py dataset_train.csv", file=sys.stderr)


if  __name__ == "__main__":
	main()

