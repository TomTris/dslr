import sys
import json
import numpy as np
import pandas as pd
# import time

learning_rate = 0.1
interations = 800

def find_houses(data):
	houses = []
	for each_house in data.iloc[:, 1]:
		if each_house not in houses:
			houses.append(each_house)
	return houses


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


def normalize_score(data):
	value_data = data[:, 6:]
	max_min = []
	for i in range(len(value_data[0])):
		old_max = value_data[:, i].max()
		old_min = value_data[:, i].min()
		max_min.append([old_max, old_min])
		value_data[:, i] = (value_data[:, i] - old_min) / (old_max - old_min)
		avarage = find_avarage(value_data[:, i])
		for j in range(len(value_data[:, i])):
			if np.isnan(value_data[j][i]):
				value_data[j][i] = avarage
	return max_min

def sigmoid(z):
	return 1 / (1 + np.exp(list(-z)))
	
def calculate_weight2(weight, datal, actuals, total):

	for l in range(interations):
		predictions = sigmoid(np.dot(datal, weight))
		error_calculated = predictions - actuals
		summes = np.dot(error_calculated, datal) / total
		weight = weight - learning_rate * summes
	return weight



def calculate_weight(house_find, lenth, datal):
	weight = np.zeros([lenth])
	total = len(datal)
	for i in range(total):
		if datal[i][1] == house_find:
			datal[i][0] = 1
		else:
			datal[i][0] = 0
	datal[:, 5] = 1
	actuals = datal[:, 0]
	return calculate_weight2(weight, datal[:, 5:], actuals, total)


def main():
	try:
		if len(sys.argv) != 2:
			raise Exception("Usage: python3 logreg_train.py <dataset>\nFor Example: python3 logreg_train.py dataset_train.csv")
		data = pd.read_csv(sys.argv[1])
		courses = data.columns[6:]
		houses = find_houses(data)
		data = np.array(data)
		max_min = normalize_score(data)
		weights = np.zeros([len(houses), len(courses) + 1])
		for i in range(len(weights)):
			weights[i] = calculate_weight(houses[i], len(courses) + 1, data)
		to_print = {
			'values': weights.tolist(),
			'max_min': max_min,
			'houses': houses
		}
		with open("weights.json", 'w') as file:
			json.dump(to_print, file, indent=4)
	except Exception as e:
		print(e, file=sys.stderr)
		


if __name__ == "__main__":
	main()