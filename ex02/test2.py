import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
dataset_train = pd.read_csv('dataset_train.csv')

# Check the first few rows
print(dataset_train.head())

# Create a pair plot
sns.pairplot(dataset_train, hue='target')  # Replace 'target' with your categorical column
plt.show()
