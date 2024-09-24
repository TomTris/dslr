import numpy as np
import pandas as pd

data_of_houses = []
houses = []
courses = []
data = None
learning_rate = 0.1

def get_data_of_houses():
	global houses
	global data
	global data_of_houses

	for each_house in data.iloc[:, 1]:
		if each_house not in houses:
			houses.append(each_house)
			data_of_houses.append(data[data[data.columns[1]] == each_house])


def create_weight_array():
	global data_of_houses
	global houses

	weight = list(courses)
	weight.append(0)
	weights = []
	for i in range(len(houses)):
		weights.append(weight)
		for j in range(len(weights[i])):
			weights[i][j] = 0
	return weights


def normalize_score():
	global data

	for course in courses:
		old_max = data[course].max()
		old_min = data[course].min()
		data[course] = (data[course] - old_min) / (old_max - old_min)
	


def sigmoid(z):
	return (1 / (1 + np.exp(z)))


def check_nan(xs):
	i = 0
	while 1:
		if i < len(xs):
			if np.isnan(xs[i]):
				return "yes"
			else:
				i += 1
		else:
			break 
	return "no"



def calculate_z(weight, xs):
	ret = weight[0]
	for cnt, x in enumerate(xs):
		ret += x * weight[cnt + 1]
	return ret
	
# loc[1:4, 5:6], iloc ['Hogwards']
# loc -> to change on copy
# data[data[data.columns[1]] == house][data.columns[1]] = 0
# => create a new one and change in the new one => be careful
def calculate_weight2(house, weight, datal, num_of_rows, iterations=0, abc=[]):
	global learning_rate
	abc = []
	summes = weight
	for i in range(len(summes)):
		summes[i] = 0

	m = 0
	for i in range(num_of_rows):
		row = datal.loc[i:i]
		row = np.array(row)
		if (check_nan(row[0, 6:]) == "no"):
			m += 1
			actual = row[0][1]
			abc.append(actual)
			xs = row[0, 6:]
			z = calculate_z(weight, xs)
			predicted = sigmoid(z)
			summes[0] += (predicted - actual)
			for i in range(len(summes) - 1):
				summes[i + 1] += (predicted - actual) * xs[i]

				
	for i in range(len(summes)):
		summes[i] /= m
	for i in range(len(summes)):
		weight[i] = weight[i] - learning_rate * summes[i]
	if iterations == 10:
		return weight
	return calculate_weight2(house, weight, datal, num_of_rows, iterations + 1, abc)



# dono why must have weight copy, if not all of them will be change, somehow?
def calculate_weight(house, weight):
	global data
	datal = data.copy()

	datal.loc[datal[datal.columns[1]] != house, datal.columns[1]] = 0
	datal.loc[datal[datal.columns[1]] == house, datal.columns[1]] = 1
	num_of_rows = datal.shape[0]

	weight_copy = weight.copy()
	return calculate_weight2(house, weight_copy, datal, num_of_rows)


def main():
	global data
	global data_of_houses
	global houses
	global courses

	data = pd.read_csv("dataset_train.csv")
	courses = data.columns[6:]
	normalize_score()
	data_of_houses = get_data_of_houses()
	weights = create_weight_array()
	for i in range(len(weights)):
		weights[i] = calculate_weight(houses[i], weights[i])
	with open("weights", 'w') as file:
		for i, weight in enumerate(weights):
			print(houses[i], file=file, end=';')
			for cnt in range(len(weight)):
				if cnt != len(weight) - 1:
					print(weight[cnt], end=';', file=file) 
				else:
					print(weight[cnt], end='', file=file) 
			print(file=file)


if __name__ == "__main__":
	main()