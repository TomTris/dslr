import matplotlib.pyplot as plt

ncols = 2
nrows = 2

# Create subplots and flatten the axes array
fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15, 12))
axs = axs.flatten()

# Set individual titles for each subplot
for i, ax in enumerate(axs):
    ax.plot([1, 2, 3], [4, 5, 6])  # Plot example data
    ax.set_title(f"Plot {i+1}")  # Set title for each subplot

# Set a super title for the entire figure (can also be done after subplot titles)
fig.suptitle("Main Title for the Whole Figure", fontsize=16)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
