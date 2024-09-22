import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create the plot
fig, ax = plt.subplots()
line, = ax.plot(x, y)

# Key event handler
def on_key(event):
    if event.key == 'up':
        # Example action: increase line width
        line.set_linewidth(line.get_linewidth() + 1)
        plt.draw()  # Redraw the figure
    elif event.key == 'down':
        # Example action: decrease line width
        line.set_linewidth(max(line.get_linewidth() - 1, 1))
        plt.draw()
    elif event.key == 'escape':
        plt.close(fig)  # Close the plot window

# Connect the key event
fig.canvas.mpl_connect('key_press_event', on_key)

# Show the plot
plt.title('Press Up/Down to Change Line Width, Escape to Close')
plt.show()