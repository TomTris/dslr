import csv
import sys

def main():
	if len(sys.argv) != 2:
		print("add name of csv")
		exit(0)
	with open(sys.argv[1]) as file:
		reader = csv.reader(file, delimiter=',')
		reader = list(reader)
		return reader


if  __name__ == "__main__":
	main()