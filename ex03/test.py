import numpy as np
import matplotlib.pyplot as plt

# Define the sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Generate data for visualization
z = np.linspace(-10, 10, 2)  # Values from -10 to 10
sig = sigmoid(z)
print(sig)
# Plot the sigmoid function
plt.plot(z, sig, label="Sigmoid Function")
plt.title("Sigmoid Function")
plt.xlabel("z")
plt.ylabel("sigmoid(z)")
plt.grid(True)
plt.show()
