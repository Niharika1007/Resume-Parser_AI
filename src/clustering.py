import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_resume.csv")

# remove null values
df.dropna(subset=["cleaned_resume"], inplace=True)
df["cleaned_resume"] = df["cleaned_resume"].astype(str)

print("Dataset loaded")
print("Shape:", df.shape)

# load saved tfidf
tfidf = joblib.load("models/tfidf_vectorizer.pkl")

# transform text
X = tfidf.transform(df["cleaned_resume"])

# KMeans clustering
kmeans = KMeans(
    n_clusters=10,
    random_state=42,
    n_init=10
)

kmeans.fit(X)

# assign clusters
df["Cluster"] = kmeans.labels_

print("\nClustering completed")
print(df[["Category", "Cluster"]].head())

# save model
os.makedirs("models", exist_ok=True)
joblib.dump(kmeans, "models/kmeans_model.pkl")

# save clustered data
df.to_csv("data/processed/clustered_resume.csv", index=False)

print("\nSaved:")
print("models/kmeans_model.pkl")
print("data/processed/clustered_resume.csv")