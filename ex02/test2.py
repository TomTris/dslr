import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

class CourseImageViewer:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.courses = [f"img{i}.png" for i in range(13)]  # Example course names
        self.current_course = 0
        self.num_courses = len(self.courses)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.images = 0
        self.load_images()
        self.display_course()

    def load_images(self):
        self.images = {}
        for course in self.courses:
            print(course)
            course_path = os.path.join(self.image_folder, '')
            print(course_path)
            self.images[course] = [mpimg.imread(os.path.join(course_path, course))]
        

    def display_course(self):
        # images = self.load_images()  # Load images for all courses
        self.ax.clear()  # Clear previous images

        # Display the first image for the current course
        print(1)
        print(self.images)
        print(1)
        print(self.courses)
        if self.images[self.courses[self.current_course]]:
            self.ax.imshow(self.images[self.courses[self.current_course]][0])  # Show the first image
            self.ax.set_title(self.courses[self.current_course])
            self.ax.axis('off')  # Hide axes
        plt.draw()

    def on_key(self, event):
        if event.key == 'left':
            self.current_course = (self.current_course - 1) % self.num_courses
            self.display_course()
        elif event.key == 'right':
            self.current_course = (self.current_course + 1) % self.num_courses
            self.display_course()
        elif event.key == 'escape':
            plt.close(self.fig)

def main():
    image_folder = "bla"  # Specify the path to your image folders
    viewer = CourseImageViewer(image_folder)
    plt.show()

if __name__ == "__main__":
    main()
