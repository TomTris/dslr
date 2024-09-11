import sys
import pandas as pd

def main() -> None:
	df = pd.read_csv(sys.argv[1])
	print(df.describe())

if  __name__ == "__main__":
    main()