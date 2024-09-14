import numpy as np
import csv
import sys

def read_data(file_path):
	with open(file_path) as file:
		reader = csv.reader(file, delimiter=',')
		reader = list(reader)
		return reader

def eprint(*args, **kwargs):
	print('Error:', *args, file=sys.stderr, **kwargs)




def find_column_length_max(data_table:list):
	columns = []
	counter = 0
	for cnt in data_table[0]:
		columns += [0]
		columns[counter] = len(cnt)
		counter += 1


def extract_column_value(data_table:list, column):
	ret = []
	for row in data_table[1:]:
		if row[column] != '':
			ret.append(row[column])
	return ret


def calculate_mean(column_value):
	total_value = 0
	for value in column_value:
		total_value += value
	mean = total_value / len(column_value)
	return mean


def calculate_std(column_value, mean):
	deviation = 0
	for value in column_value:
		deviation += (value - mean) ** 2
	variance = deviation / (len(column_value) - 1)
	standard_deviation = variance ** 0.5
	return standard_deviation


def calculate_min(column_value):
	return column_value[0]
	

def calculate_25_percent(column_value):
	index_Q25 = (len(column_value) - 1) / 4
	int_index_Q25 = int(index_Q25)

	under_25 = column_value[int_index_Q25]
	if (index_Q25 % 4) == 0:
		return under_25

	upper_25 = column_value[int_index_Q25 + 1]
	real_module = index_Q25 - int_index_Q25
	real_value = under_25 + ((upper_25 - under_25) * real_module)
	return real_value


def calculate_50_percent(column_value):
	index_Q50 = (len(column_value) - 1) / 2
	int_index_Q50 = int(index_Q50)

	under_50 = column_value[int_index_Q50]
	if (index_Q50 % 4) == 0:
		return under_50

	upper_50 = column_value[int_index_Q50 + 1]
	real_module = index_Q50 - int_index_Q50
	real_value = under_50 + ((upper_50 - under_50) * real_module)
	return real_value


def calculate_75_percent(column_value):
	index_Q25 = (len(column_value) - 1) * 3 / 4
	int_index_Q25 = int(index_Q25)

	under_25 = column_value[int_index_Q25]
	if (index_Q25 % 4) == 0:
		return under_25

	upper_25 = column_value[int_index_Q25 + 1]
	real_module = index_Q25 - int_index_Q25
	real_value = under_25 + ((upper_25 - under_25) * real_module)
	return real_value


def calculate_max(column_value):
	return column_value[-1]




def add_to_table_to_print(return_table, column_value):
	Count = len(column_value)
	Mean = calculate_mean(column_value)
	Std = calculate_std(column_value, Mean)
	Min = calculate_min(column_value)
	Q1 = calculate_25_percent(column_value)
	Q2 = calculate_50_percent(column_value)
	Q3 = calculate_75_percent(column_value)
	Max = calculate_max(column_value)

	return_table[1].append("{:.6f}".format(Count))
	return_table[2].append("{:.6f}".format(Mean))
	return_table[3].append("{:.6f}".format(Std))
	return_table[4].append("{:.6f}".format(Min))
	return_table[5].append("{:.6f}".format(Q1))
	return_table[6].append("{:.6f}".format(Q2))
	return_table[7].append("{:.6f}".format(Q3))
	return_table[8].append("{:.6f}".format(Max))


def create_return_table(data_table):
	return_table = [[''], ['Count'],['Mean'], ['Std'], ['Min'], ['25%'], ['50%'], ['75%'], ['Max']]
	i = 0
	for column in range(len(data_table[0])):
		column_value = extract_column_value(data_table, column)
		try:
			a = 0
			column_value = [float(value) for value in column_value]
			a = 1
		except Exception:
			pass
		if a == 1:
			return_table[0].append(data_table[0][column])
			column_value.sort()
			add_to_table_to_print(return_table, column_value)
	return return_table

def decide_length_to_print(return_table):
	column_width = []
	for i in range(len(return_table[0])):
		column_width.append(0)
		for row in return_table:
			if len(row[i]) > column_width[i]:
				column_width[i] = len(row[i])
	for i in range(len(column_width)):
		if i != 0:
			column_width[i] += 2
	return column_width


def print_return_table(return_table):
	column_width = decide_length_to_print(return_table)	
	for row in return_table:
		i = 0
		for index in row:
			if i == 0:
				print(index, ' ' * (column_width[i] - len(index)), sep='', end='')
			else:
				print(' ' * (column_width[i] - len(index)), index, sep='', end='')
			i += 1
		print()


def main() -> None:
	try:
		if len(sys.argv) != 2:
			raise Exception("Usage: python3 describe.py [dataset]")
		data_table = read_data(sys.argv[1])
		return_table = create_return_table(data_table)
		# for row in return_table:
		# 	print(row)
		new = np.array(return_table)
		new = return_table[1:3, 2:4]
		for row in new:
			print(row)
		# print_return_table(return_table)

	except Exception as e:
		eprint(e)


if  __name__ == "__main__":
	main()
