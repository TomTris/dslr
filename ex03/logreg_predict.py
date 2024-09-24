import numpy as np
import pandas as pd

houses = []
weights = []
with open("weights", 'r') as file:
	while 1:
		weight = []
		line = file.readline()
		if (not line):
			break
		line = line.split(';')
		weight = [float(num) for num in line[1:]]
		houses.append(line[0])
		weights.append(weight)


def normalize_score(data, courses):
	for course in courses:
		old_max = data[course].max()
		old_min = data[course].min()
		data[course] = (data[course] - old_min) / (old_max - old_min)



def sigmoid(weight, xs):
	ret = weight[0]
	for cnt, x in enumerate(xs):
		ret += x * weight[cnt + 1]
	return (1 / (1 + np.exp(-ret)))


def highest(results):
	cnt = 0
	current = results[0]
	print(results)
	for i, result in enumerate(results):
		if result > current:
			i = cnt
			current = result
	return cnt


def main():
	data = pd.read_csv("dataset_test.csv")
	courses = data.columns[6:]
	normalize_score(data, courses)
	with open("houses.csv", 'w') as file:
		print(data.columns[0],data.columns[1], sep=',', file=file)
		data = np.array(data)
		for i, each_row in enumerate(data):
			print(i, end=',', file=file)
			results = []
			for j, weight in enumerate(weights):
				results.append(sigmoid(weight, each_row[6:]))
			print(houses[highest(results)], file=file)

	


if __name__ == '__main__':
	main()