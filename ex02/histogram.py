
import csv 
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def eprint(*args, **kwargs):
	print('Error:', *args, file=sys.stderr, **kwargs)


def print_number_of_student_in_each_house(data_table):
	data_table = np.array(data_table)
	houses = data_table[:, 1:2]
	cnt1 = 0
	cnt2 = 0
	cnt3 = 0
	cnt4 = 0
	for house in houses:
		if house == 'Ravenclaw':
			cnt1 += 1
		elif house == 'Slytherin':
			cnt2 += 1
		elif house == 'Hufflepuff':
			cnt3 += 1
		elif house == 'Gryffindor':
			cnt4 += 1
		else:
			raise Exception("Data base has unexpected house")
	print("Number of students in each house is:")
	print("Ravenclaw:", cnt1)
	print("Slytherin:", cnt2)
	print("Hufflepuff", cnt3)
	print("Gryffindor", cnt4)
	print()

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

def main() -> None:
	try:
		data = pd.read_csv(sys.argv[1])
		print_number_of_student_in_each_house(data)
		courses = generate_courses()
		normalize_score(data, courses)
		data_1 = data[data['Hogwarts House'] == 'Ravenclaw']
		data_2 = data[data['Hogwarts House'] == 'Slytherin']
		data_3 = data[data['Hogwarts House'] == 'Gryffindor']
		data_4 = data[data['Hogwarts House'] == 'Hufflepuff']
		

		plt.figure(figsize=(12, 8))

		num_courses = len(courses)
		ncols = 4
		nrows = (num_courses - 1 ) // ncols + 1
		fig, axs = plt.subplots(nrows, ncols, figsize=(15, 12))
		axs = axs.flatten()
		colors = plt.cm.viridis(np.linspace(0, 1, 4))

		for i, course in enumerate(courses):
			axs[i].hist(data_1[course], bins=20, alpha=0.55, color=colors[0])
			axs[i].hist(data_2[course], bins=20, alpha=0.55, color=colors[1])
			axs[i].hist(data_3[course], bins=20, alpha=0.55, color=colors[2])
			axs[i].hist(data_4[course], bins=20, alpha=0.55, color=colors[3])

			axs[i].set_title(course)
			axs[i].set_xlabel('Normalized Scores')
			axs[i].set_ylabel('Frequency')

		for j in range(len(courses), len(axs)):
			fig.delaxes(axs[j])

		plt.tight_layout()
		plt.savefig('/app/ex02/histograms.png')

	except Exception as e:
		eprint(e)


if  __name__ == "__main__":
	main()
