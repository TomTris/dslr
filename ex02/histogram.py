import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib as mpl


def read_data(file_path):
	with open(file_path) as file:
		reader = pd.read_csv(file, delimiter=',')
		reader = np.array(reader)
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
		if len(sys.argv) != 2:
			raise Exception("Usage: python histogram.py [dataset]")
		data_table = read_data(sys.argv[1])
		
			


	except Exception as e:
		eprint(e)


if  __name__ == "__main__":
	main()
