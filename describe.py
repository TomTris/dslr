import csv
import sys

def read_data(file_path):
	with open(sys.argv[1]) as file:
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

def main() -> None:
	try:
		if len(sys.argv) != 2:
			raise Exception("Usage: python3 describe.py [dataset]")
		data_table = read_data(sys.argv[1])
		column = 18
		# column_length_max = find_column_length_max(datatable)
		column_value = extract_column_value(data_table, column)
		column_value = [float(value) for value in column_value]
		column_value.sort()
		count = len(column_value)
		print(count)

		Mean = calculate_mean(column_value)
		print("{:.6f}".format(Mean))

		Std = calculate_std(column_value, Mean)
		print("{:.6f}".format(Std))

		Min = calculate_min(column_value)
		print("{:.6f}".format(Min))
		
		Q1 = calculate_25_percent(column_value)
		print("{:.6f}".format(Q1))
		Q2 = calculate_50_percent(column_value)
		print("{:.6f}".format(Q2))
		Q3 = calculate_75_percent(column_value)
		print("{:.6f}".format(Q3))

		Max = calculate_max(column_value)
		print("{:.6f}".format(Max))













	except Exception as e:
		eprint(e)


if  __name__ == "__main__":
	main()