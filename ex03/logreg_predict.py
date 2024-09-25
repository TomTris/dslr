import json
import numpy as np
import pandas as pd

houses = []
weights = []

def normalize_score(data, max_min):
	for cnt in range(len(max_min)):
		old_max = max_min[cnt][0]
		old_min = max_min[cnt][1]
		for i in range(len(data[:, 6  + cnt])):
			if np.isnan(data[:, 6  + cnt][i]):
				data[:, 6  + cnt][i] = (old_max + old_min) / 2
		data[:, 6  + cnt] = (data[:, 6  + cnt] - old_min) / (old_max - old_min)



def sigmoid(weight, xs):
	ret = weight[0]
	for cnt, x in enumerate(xs):
		ret = ret + (x * weight[cnt + 1])
	return (1 / (1 + np.exp(-ret)))


def highest(results):
	cnt = 0
	current = results[0]
	for i, result in enumerate(results):
		if result > current:
			cnt = i
			current = result
	return cnt


def main():
	data = pd.read_csv("dataset_test.csv")
	index_name = data.columns[0]
	house_name = data.columns[1]
	data = np.array(data)
	with open('weights', 'r') as file:
		parsing = json.load(file)
	weights = parsing['values']
	max_min = parsing['max_min']
	houses = parsing['houses']
	normalize_score(data, max_min)
	with open("houses.csv", 'w') as file:
		print(index_name, house_name, sep=',', file=file)
		for i, each_row in enumerate(data):
			print(i, end=',', file=file)
			results = []
			for j, weight in enumerate(weights):
				results.append(sigmoid(weight, each_row[6:]))
			print(houses[highest(results)], file=file)

	


if __name__ == '__main__':
	main()