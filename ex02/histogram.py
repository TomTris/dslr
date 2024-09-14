import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def read_data(file_path):
	with open(file_path) as file:
		reader = pd.read_csv(file, delimiter=',')
		print(reader)
		reader = np.array(reader)
		print(reader)
		return reader


def eprint(*args, **kwargs):
	print('Error:', *args, file=sys.stderr, **kwargs)



def print_number_of_student_in_each_house(data_table):
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
			print(house)
	print(cnt1)
	print(cnt2)
	print(cnt3)
	print(cnt4)

def main() -> None:
	try:
		import matplotlib.pyplot as plt
		import numpy as np

		np.random.seed(0)  # For reproducibility

				# Data for four groups
		data = pd.read_csv(sys.argv[1])
		data.loc[:, 'Flying'] = data.loc[:, 'Arithmancy'] - 4000
		# data = pd(data)
		# data = 
		# print(data1[1:, 7:9])
		# Create histogram
		plt.figure(figsize=(12, 8))

		# List of courses to plot
		courses = [
			'Arithmancy',
			'Astronomy',
			'Herbology',
			'Defense Against the Dark Arts',
			'Divination',
			'Muggle Studies',
			'Ancient Runes',
			'History of Magic',
			'Transfiguration',
			'Potions',
			'Care of Magical Creatures',
			'Charms',
			'Flying'
		]

		# Colors for histograms
		colors = plt.cm.viridis(np.linspace(0, 1, len(courses)))

		# Plot histograms for each course
		for i, course in enumerate(courses):
			plt.hist(data[course], bins=20, alpha=0.5, label=course, color=colors[i])

		# Add titles and labels
		plt.title('Overlapping Histograms of Hogwarts Courses')
		plt.xlabel('Scores')
		plt.ylabel('Frequency')

		# Add legend
		plt.legend(loc='upper right')

		# Display plot
		plt.savefig('/app/ex02/histogram.png')


	except Exception as e:
		eprint(e)


if  __name__ == "__main__":
	main()
