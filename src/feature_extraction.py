import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_resume.csv")

print("Dataset loaded successfully")
print(df.head())

# Remove missing values
df.dropna(subset=["cleaned_resume"], inplace=True)

# convert all to string
df["cleaned_resume"] = df["cleaned_resume"].astype(str)

print("\nAfter removing null values:")
print("Shape:", df.shape)

# TF-IDF
tfidf = TfidfVectorizer(max_features=5000)

X = tfidf.fit_transform(df["cleaned_resume"])

print("\nTF-IDF completed successfully")
print("Matrix shape:", X.shape)

# create models folder
os.makedirs("models", exist_ok=True)

# save vectorizer
joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")

print("\nSaved successfully:")
print("models/tfidf_vectorizer.pkl")