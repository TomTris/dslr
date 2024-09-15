from matplotlib.lines import Line2D
import csv 
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt


def eprint(*args, **kwargs):
	print('Error:', *args, file=sys.stderr, **kwargs)


def generate_courses():
	with open(sys.argv[1]) as file:
		reader = csv.reader(file, delimiter=',')
		reader = list(reader)
		for i, row in enumerate(reader):
			if i > 0:
				break
			reader = np.array(row)
			return reader[6:]


def normalize_score(data, courses):
	for course in courses:
		old_max = data[course].max()
		old_min = data[course].min()
		data[course] = (data[course] - old_min) / (old_max - old_min)


def get_data_of_houses(data):
	houses = []
	mix_houses = data['Hogwarts House']
	for house in mix_houses:
		if house not in houses:
			houses.append(house)
	
	data_of_houses = []
	for house in houses:
		data_of_houses.append(data[data['Hogwarts House'] == house])
	return data_of_houses


def display_all(courses, data_of_houses):
	plt.figure(figsize=(12, 8))

	num_courses = len(courses)
	ncols = int(num_courses ** 0.5) + 1
	nrows = (num_courses - 1 ) // ncols + 1
	fig, axs = plt.subplots(nrows, ncols, figsize=(15, 12))
	axs = axs.flatten()
	colors = plt.cm.viridis(np.linspace(0, 1, len(data_of_houses)))

	for i, course in enumerate(courses):
		for cnt, data_of_a_house in enumerate(data_of_houses):
			axs[i].hist(data_of_a_house[course], bins=20, alpha=0.55, color=colors[cnt])
		axs[i].set_title(course)
		axs[i].set_xlabel('Normalized Scores')
		axs[i].set_ylabel('Frequency')

	for j in range(len(courses), len(axs)):
		fig.delaxes(axs[j])
	
	custom_lines = [Line2D([0], [1], color=colors[0], lw=16	),
					Line2D([0], [1], color=colors[1], lw=16	),
					Line2D([0], [1], color=colors[2], lw=16	),
					Line2D([0], [1], color=colors[3], lw=16	)]
	
	fig.legend(custom_lines, ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff'],\
				fontsize='large', loc='lower right', ncol=20, bbox_to_anchor=(1, 0),\
				handlelength=4.5, handleheight=3.5)

	plt.tight_layout()
	plt.title('Overlapping Histograms of Hogwarts Courses')
	plt.savefig('/app/ex02/histograms.png')


def display_winner(courses, data_of_houses):		
	
	interval_percentage = {}
	
	for course in courses:
		interval_percentage[course] = [100] * 21
		for data_of_house in data_of_houses:
			interval = [0] * 21
			student_total = 0
			for cnt, each_score in enumerate(data_of_house[course]):
				if not np.isnan(each_score):
					interval[int(each_score * 20)] += 1
					student_total += 1
			for cnt in range(21):
				if interval[cnt] / student_total * 100 < (interval_percentage[course])[cnt]:
					(interval_percentage[course])[cnt] = interval[cnt] / student_total * 100
	max_percentage = 0
	winner = ''
	for course in interval_percentage:
		print(sum(interval_percentage[course]))
		print(course)
		print()
		if sum(interval_percentage[course]) > max_percentage:
			winner = course
			max_percentage = sum(interval_percentage[course])
	print("Winner:", winner)
	print("Max_percentage:", max_percentage)
	

def main() -> None:
	try:
		data = pd.read_csv(sys.argv[1])
		courses = generate_courses()
		normalize_score(data, courses)
		data_of_houses = get_data_of_houses(data)
		display_all(courses, data_of_houses)
		display_winner(courses, data_of_houses)


	except Exception as e:
		eprint(e)


if  __name__ == "__main__":
	main()

