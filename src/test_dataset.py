import pandas as pd

df = pd.read_csv("data/raw/Resume.csv")

print(df.head())
print("\nColumns:", df.columns)
print("Shape:", df.shape)
print("\nNull values:")
print(df.isnull().sum())