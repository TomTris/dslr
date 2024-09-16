import csv 
import pandas as pd
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

column = 4
size_frame = 1250
colors = None
data = None

def eprint(*args, **kwargs):
	print('Error:', *args, file=sys.stderr, **kwargs)


def generate_courses():
	with open(sys.argv[1]) as file:
		reader = csv.reader(file, delimiter=',')
		reader = list(reader)
		reader = np.array(reader[0])
		return reader[6:]


def normalize_score(data, courses):
	for course in courses:
		old_max = data[course].max()
		old_min = data[course].min()
		data[course] = (data[course] - old_min) / (old_max - old_min)
		for i in range(len(data[course])):
			column2 = column - 1
			value = data.at[i, course]
			while not np.isnan(value):
				if value >= column2 / column:
					data.at[i, course] = column2 / column
					break
				column2 -= 1


def get_data_of_houses(data):
	houses = []
	mix_houses = data['Hogwarts House']
	for house in mix_houses:
		if house not in houses:
			houses.append(house)
	
	data_of_houses = []
	for house in houses:
		data_of_houses.append(data[data['Hogwarts House'] == house])
	return data_of_houses


def find_highest_frequency(data):
	interval = [0] * column
	for each_score in data:
		if not np.isnan(each_score):
			interval[int(each_score * column)] += 1
	max = interval[0]
	for ite in interval:
		if ite > max:
			max = ite
	return max

def interpolate_color(t, color_start, color_end):
	""" Interpolate between two colors with transparency. """
	r = int(color_start[0] * (1 - t) + color_end[0] * t)
	g = int(color_start[1] * (1 - t) + color_end[1] * t)
	b = int(color_start[2] * (1 - t) + color_end[2] * t)
	a = int(color_start[3] * (1 - t) + color_end[3] * t)
	return (r, g, b, a)

def normalize_to_rgba(value):
	""" Get a color from the gradient defined by color1, color2, and color3. """
	color1 = (255, 0, 0, 100)   # Red with 100 alpha (semi-transparent)
	color2 = (255, 255, 0, 150) # Yellow with 150 alpha (more opaque)
	color3 = (0, 0, 255, 200)
	# Determine which segment of the gradient we are in
	if value < 0.5:
		# Interpolate between color1 and color2
		t = value * 2  # Normalize the value to [0, 1] within the first segment
		return interpolate_color(t, color1, color2)
	else:
		# Interpolate between color2 and color3
		t = (value - 0.5) * 2  # Normalize the value to [0, 1] within the second segment
		return interpolate_color(t, color2, color3)

# def normalize_to_rgba(value):
#	 """ Convert a normalized value (0 to 1) to an RGBA color. """
#	 blue = (0, 0, 255, 100)  # 100 is the alpha value for transparency
#	 red = (255, 0, 0, 100)   # 100 is the alpha value for transparency
		
#	 # Interpolate between blue and red
#	 r = int(blue[0] * (1 - value) + red[0] * value)
#	 g = int(blue[1] * (1 - value) + red[1] * value)
#	 b = int(blue[2] * (1 - value) + red[2] * value)
#	 a = int(blue[3] * (1 - value) + red[3] * value)
		
#	return (r, g, b, a)

def draw_each_house(horizon_start, horizon_end, vertical, color, data, draw, highest_frequency):
	size_side = horizon_end - horizon_start
	interval = [0] * column
	color = normalize_to_rgba(color)
	# highest_frequency = (highest_frequency * 1.1) // 1
	for each_score in data:
		if not np.isnan(each_score):
			interval[int(each_score * column)] += 1
	for cnt in range(len(interval)):
		interval[cnt] = interval[cnt] / highest_frequency * (horizon_end - horizon_start)
	print(interval)
	for cnt, each_frequency in enumerate(interval):
		hori_start = horizon_start + (cnt / column * size_side)
		hori_end = horizon_start + ((cnt + 1) / column * size_side)
		verti_end = vertical
		verti_start = verti_end - interval[cnt]
		draw.rectangle([(hori_start, verti_start), (hori_end, verti_end)], outline='blue', fill=color)

def display_each_course(course, col, row, draw, data_of_houses, winner, margin_each, size_each):
	horizon_start = margin_each + (col * (margin_each + size_each))
	vertical_start = margin_each + (row * (margin_each + size_each))
	horizon_end = horizon_start + size_each
	vertical_end = vertical_start + size_each

	font = ImageFont.load_default(size=20)
	draw.text((horizon_start, vertical_start - margin_each / 4), course, font=font, fill='black')
	draw.rectangle([(horizon_start, vertical_start), (horizon_end, vertical_end)], outline='black', fill='white')
	highest_frequency = find_highest_frequency(data[course])
	for i, data_of_house in enumerate(data_of_houses):
		draw_each_house(horizon_start, horizon_end, vertical_end, colors[i], data_of_house[course], draw, highest_frequency)
	
	
	# draw.rectangle([(100, 60), (350, 350)], outline='blue', fill='white')


def display_all(courses, data_of_houses, winner):
	global colors
	colors = np.linspace(0, 1, len(data_of_houses))
	
	total = len(courses)
	cols = ((total - 1) ** 0.5) // 1 + 1 
	
	rows = ((total - 1) // cols) + 1

	img = Image.new('RGBA', (size_frame, size_frame), (255, 255, 255, 255))
	margin_each = size_frame / (1 + 6 * cols) * 2
	size_each = size_frame / (1 + 6 * cols) * 4
	current_col = 0
	current_row = 0
	draw = ImageDraw.Draw(img)
	for course in courses:
		display_each_course(course, current_col, current_row, draw, data_of_houses, winner, margin_each, size_each)
		current_col += 1
		if current_col == cols:
			current_col = 0
			current_row += 1
	draw.rectangle([(1000, 1100 - 300), (1100, 1200 - 300)], outline='blue', fill=normalize_to_rgba(colors[0]))
	draw.rectangle([(1000, 1200 - 300), (1100, 1300 - 300)], outline='blue', fill=normalize_to_rgba(colors[1]))
	draw.rectangle([(1000, 1300 - 300), (1100, 1400 - 300)], outline='blue', fill=normalize_to_rgba(colors[2]))
	draw.rectangle([(1000, 1400 - 300), (1100, 1500 - 300)], outline='blue', fill=normalize_to_rgba(colors[3]))

	img.show()
	# img.save('blank_image.jpg')


def find_winner(courses, data_of_houses):		
	interval_percentage = {}
	for course in courses:
		interval_percentage[course] = [100] * column
		for data_of_house in data_of_houses:
			interval = [0] * column
			student_total = 0
			for each_score in data_of_house[course]:
				if not np.isnan(each_score):
					interval[int(each_score * column)] += 1
					student_total += 1
			for cnt in range(column):
				if interval[cnt] / student_total * 100 < (interval_percentage[course])[cnt]:
					(interval_percentage[course])[cnt] = interval[cnt] / student_total * 100
	max_percentage = 0
	winner = ''
	for course in interval_percentage:
		sum_interval_percentage = sum(interval_percentage[course])
		if sum_interval_percentage > max_percentage:
			winner = course
			max_percentage = sum_interval_percentage
	return winner

def main() -> None:
	try:
		if len(sys.argv) == 1 or len(sys.argv) >= 4:
			raise Exception("python histogram.py <dataset> [optional <number of column>]")
		if len(sys.argv) == 3:
			global column
			column = int(sys.argv[2])
			if column < 2 or column > 50:
				raise Exception("column should be: 2 <= column <= 50")
		global data
		data = pd.read_csv(sys.argv[1])
		courses = generate_courses()
		normalize_score(data, courses)
		data_of_houses = get_data_of_houses(data)
		winner = find_winner(courses, data_of_houses)
		display_all(courses, data_of_houses, winner)

	except Exception as e:
		eprint(e)


if  __name__ == "__main__":
	main()

