import csv 
import pandas as pd
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
column = 4
size_frame = 1250
colors = None
data = None
img = None

def blend_images(img1, img2, width_change1, width_change2, height_change1, height_change2):
    img1 = img1.convert('RGBA')
    img2 = img2.convert('RGBA')
    
    if img1.size != img2.size:
        raise ValueError("Images must have the same size")
    
    width, height = img1.size
    # blended_image = Image.new('RGBA', (width, height))

    pixels1 = img1.load()
    pixels2 = img2.load()
    blended_pixels = img1.load()
    for x in range(width_change1, width_change2):
        for y in range(height_change1, height_change2):
            r1, g1, b1, a1 = pixels1[x, y]
            r2, g2, b2, a2 = pixels2[x, y]
            a1 /= 255.0
            a2 /= 255.0
            new_alpha = min(a1 + a2, 1.0)

            if new_alpha == 0:
                new_color = (0, 0, 0, 0)
            else:
                blend_ratio = a1 / (a1 + a2)
                r = int((r1 * blend_ratio + r2 * (1 - blend_ratio)) * 255)
                g = int((g1 * blend_ratio + g2 * (1 - blend_ratio)) * 255)
                b = int((b1 * blend_ratio + b2 * (1 - blend_ratio)) * 255)
                new_color = (r, g, b, int(new_alpha * 255))
            blended_pixels[x, y] = new_color
    # img1.show()
    return img1



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


def find_highest_frequency(data_of_houses, course):
    max_ret = 0
    for i, data_of_house in enumerate(data_of_houses):
        interval = [0] * column
        for each_score in data_of_house[course]:
            if not np.isnan(each_score):
                interval[int(each_score * column)] += 1
        max = 0
        for ite in interval:
            if ite > max:
                max = ite
        if max > max_ret:
            max_ret = max
    
    return max_ret


# def normalize_to_rgba(values, alpha=1):
# 	"""
# 	Interpolate colors based on the input values and add transparency.

# 	Parameters:
# 	- values: Array of values to interpolate colors for.
# 	- alpha: Transparency level (0.0 is fully transparent, 1.0 is fully opaque).

# 	Returns:
# 	- List of RGBA tuples with colors and transparency.
# 	"""
# 	# Define base colors (in RGB format with values in the range [0, 1])
# 	yellow = np.array([1, 1, 0])
# 	red = np.array([1, 0, 0])
# 	blue = np.array([0, 0, 1])
    
# 	# Create an array to hold the interpolated colors
# 	colors = np.zeros((len(values), 4))
    
# 	# Interpolate between yellow, red, and blue
# 	for i, value in enumerate(values):
# 		if value <= 0.5:
# 			# Interpolating between yellow and red
# 			t = value * 2  # Scale value to be between 0 and 1
# 			colors[i, :3] = (1 - t) * yellow + t * red
# 		else:
# 			# Interpolating between red and blue
# 			t = (value - 0.5) * 2  # Scale value to be between 0 and 1
# 			colors[i, :3] = (1 - t) * red + t * blue
        
# 		# Set alpha channel
# 		colors[i, 3] = alpha
    
# 	# Convert colors to integers in range [0, 255]
# 	colors = (colors * 255).astype(int)
    
# 	# Convert to list of tuples for PIL compatibility
# 	colors = [tuple(color) for color in colors]
    
# 	return colors

def interpolate_color(t, color_start, color_end):
    """ Interpolate between two colors with transparency. """
    r = int(color_start[0] * (1 - t) + color_end[0] * t)
    g = int(color_start[1] * (1 - t) + color_end[1] * t)
    b = int(color_start[2] * (1 - t) + color_end[2] * t)
    a = int(color_start[3] * (1 - t) + color_end[3] * t)
    return (r, g, b, a)

def normalize_to_rgba(values):
    """ Get a color from the gradient defined by color1, color2, and color3. """
    color1 = (255, 0, 0, 100)   # Red with 100 alpha (semi-transparent)
    color2 = (255, 255, 0, 150) # Yellow with 150 alpha (more opaque)
    color3 = (0, 0, 255, 200)   # Blue with 200 alpha (opaque)

    colors = []
    for value in values:
        if value < 0.5:
            # Interpolate between color1 and color2
            t = value * 2  # Normalize the value to [0, 1] within the first segment
            colors.append(interpolate_color(t, color1, color2))
        else:
            # Interpolate between color2 and color3
            t = (value - 0.5) * 2  # Normalize the value to [0, 1] within the second segment
            colors.append(interpolate_color(t, color2, color3))
    return colors

def draw_each_house(horizon_start, horizon_end, vertical, color, data, highest_frequency):
    size_side = horizon_end - horizon_start
    interval = [0] * column
    highest_frequency = (highest_frequency * 1.1) // 1
    for each_score in data:
        if not np.isnan(each_score):
            interval[int(each_score * column)] += 1
    for cnt in range(len(interval)):
        interval[cnt] = interval[cnt] / highest_frequency * (horizon_end - horizon_start)

    global img
    for cnt, each_frequency in enumerate(interval):
        hori_start = horizon_start + (cnt / column * size_side)
        hori_end = horizon_start + ((cnt + 1) / column * size_side)
        verti_end = vertical
        verti_start = verti_end - interval[cnt]
        img_new = Image.new('RGBA', (size_frame, size_frame))
        draw = ImageDraw.Draw(img_new)
        draw.rectangle([(hori_start, verti_start), (hori_end, verti_end)], outline='blue', fill=color)
        img = blend_images(img, img_new, int(hori_start) - 1, int(hori_end) + 1, int(verti_start) - 1, int(verti_end) + 1)

def display_each_course(course, col, row, data_of_houses, winner, margin_each, size_each):
    horizon_start = margin_each + (col * (margin_each + size_each))
    vertical_start = margin_each + (row * (margin_each + size_each))
    horizon_end = horizon_start + size_each
    vertical_end = vertical_start + size_each

    font = ImageFont.load_default(size=20)
    img_new = Image.new('RGBA', (size_frame, size_frame))
    draw = ImageDraw.Draw(img_new)
    width, height = draw.textbbox((0, 0), course, font=font)[2:4]
    global img
    text_width_end = horizon_start + width
    if text_width_end >= 1249:
        text_width_end = 1249
    draw.text((horizon_start, vertical_start - margin_each / 4), course, font=font, fill='black')
    img = blend_images(img, img_new, int(horizon_start) - 1, int(text_width_end) + 1, int(vertical_start) - 1, int(vertical_start + height ) + 1)
    draw.rectangle([(horizon_start, vertical_start), (horizon_end, vertical_end)], outline='black', fill=(0,0,0,0))
    img = blend_images(img, img_new, int(horizon_start) - 1, int(horizon_end) + 1, int(vertical_start) - 1, int(vertical_end) + 1)
    highest_frequency = find_highest_frequency(data_of_houses, course)
    for i, data_of_house in enumerate(data_of_houses):
        draw_each_house(horizon_start, horizon_end, vertical_end, colors[i], data_of_house[course], highest_frequency)


def display_all(courses, data_of_houses, winner):
    total = len(courses)
    cols = ((total - 1) ** 0.5) // 1 + 1 
    # rows = ((total - 1) // cols) + 1
    margin_each = size_frame / (1 + 6 * cols) * 2
    size_each = size_frame / (1 + 6 * cols) * 4
    current_col = 0
    current_row = 0
    global img
    for course in courses:
        display_each_course(course, current_col, current_row, data_of_houses, winner, margin_each, size_each)
        current_col += 1
        if current_col == cols:
            current_col = 0
            current_row += 1
    draw = ImageDraw.Draw(img)
    draw.rectangle([(1000, 1100 - 300), (1100, 1200 - 300)], outline='blue', fill=colors[0])
    draw.rectangle([(1000, 1200 - 300), (1100, 1300 - 300)], outline='blue', fill=colors[1])
    draw.rectangle([(1000, 1300 - 300), (1100, 1400 - 300)], outline='blue', fill=colors[2])
    draw.rectangle([(1000, 1400 - 300), (1100, 1500 - 300)], outline='blue', fill=colors[3])

    img.show()


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

        global img
        global colors
        # colors = np.linspace(0, 1, len(data_of_houses))
        colors = np.linspace(0, 1, 4)
        colors = normalize_to_rgba(colors)
        print(colors)
        img = Image.new('RGBA', (size_frame, size_frame))
        display_all(courses, data_of_houses, winner)

    except Exception as e:
        eprint(e)


if  __name__ == "__main__":
    main()

