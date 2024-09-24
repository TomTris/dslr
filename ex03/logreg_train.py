import numpy as np
import pandas as pd

houses = []
courses = []
data = None
learning_rate = 0.01

def calculate_number_of_houses():
	global houses
	global data

	for each_house in data.iloc[:, 1]:
		if each_house not in houses:
			houses.append(each_house)
	return len(houses)


def find_avarage(column):
	summe = 0
	total = 0
	for each_value in column:
		if not np.isnan(each_value):
			summe += each_value
			total += 1
	avarage = total / summe
	for i in range(len(column)):
		if np.isnan(each_value):
			column[i] = avarage
	return avarage


def normalize_score():
	global data

	value_data = data[:, 6:]
	for i in range(len(value_data[0])):
		old_max = value_data[:, i].max()
		old_min = value_data[:, i].min()
		value_data[:, i] = (value_data[:, i] - old_min) / (old_max - old_min)
		avarage = find_avarage(value_data[:, i])
		for j in range(len(value_data[:, i])):
			if np.isnan(value_data[j][i]):
				value_data[j][i] = avarage


def sigmoid(z):
	return (1 / (1 + np.exp(-z)))


def calculate_z(weight, xs):
	ret = weight[0]
	for cnt, x in enumerate(xs):
		ret += x * weight[cnt + 1]
	return ret
	
# loc[1:4, 5:6], iloc ['Hogwards']
# loc -> to change on copy
# data[data[data.columns[1]] == house][data.columns[1]] = 0
# => create a new one and change in the new one => be careful
def calculate_weight2(weight, datal, total, iterations=0):
	global learning_rate
	
	summes = np.zeros_like(weight)
	for i in range(total):
		row = datal[i]
		actual = row[1]
		xs = row[6:]
		z = calculate_z(weight, xs)
		predicted = sigmoid(z)
		summes[0] += (predicted - actual)
		for j in range(len(xs)):
			summes[j + 1] += (predicted - actual) * xs[j]

	for i in range(len(summes)):
		summes[i] /= total
		weight[i] = weight[i] - learning_rate * summes[i]

	if iterations == 10:
		return weight
	return calculate_weight2(weight, datal, total, iterations + 1)

# def calculate_weight2(weight, datal, y_val, x_val, total, iterations=0):
# 	global learning_rate

# 	sigmoids = sigmoid(np.dot(weight, x_val.T))
# 	summes = np.dot(sigmoids - y_val, x_val)
# 	print(summes)
# 	gradients = summes / x_val.shape[1] * learning_rate
# 	for i in range(14):
# 		weight[i] = weight[i] - gradients[i]


# 	if iterations == 10:
# 		return weight
# 	return calculate_weight2(weight, datal,y_val, x_val, total, iterations + 1)


# dono why must have weight copy, if not all of them will be change, somehow?
def calculate_weight(house_find, lenth):
	global data
	datal = data.copy()
	weight = np.zeros([lenth])
	
	for i in range(len(datal)):
		if datal[i][1] == house_find:
			datal[i][1] = 1
		else:
			datal[i][1] = 0
	total = datal.shape[0]
	y_val = datal[:, 1]
	x_val = np.ones([len(datal), len(weight)])
	x_val[:, 1:] = datal[:, 6:]
	return calculate_weight2(weight, datal, total)


def main():
	global data
	global houses
	global courses

	data = pd.read_csv("dataset_train.csv")
	courses = data.columns[6:]
	number_of_houses = calculate_number_of_houses()
	data = np.array(data)
	normalize_score()
	weights = np.zeros([number_of_houses, len(courses) + 1])
	for i in range(len(weights)):
		weights[i] = calculate_weight(houses[i], len(courses) + 1)
	with open("weights", 'w') as file:
		for i, weight in enumerate(weights):
			print(houses[i], file=file, end=';')
			for cnt in range(len(weight)):
				if cnt != len(weight) - 1:
					print(weight[cnt], end=',', file=file) 
				else:
					print(weight[cnt], end='', file=file) 
			print(file=file)


if __name__ == "__main__":
	main()