import pandas as pd
import nltk
import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources (only first time)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


# Function to clean text
def clean_text(text):
    # convert to lowercase
    text = str(text).lower()

    # remove numbers and special characters
    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    # tokenize
    words = word_tokenize(text)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # join words back
    return " ".join(words)


# Load dataset
df = pd.read_csv("data/raw/Resume.csv")

print("Original Columns:", df.columns)

# Rename Resume_str to Resume
df.rename(columns={"Resume_str": "Resume"}, inplace=True)

# Apply cleaning
df["cleaned_resume"] = df["Resume"].apply(clean_text)

# Keep only needed columns
df = df[["Category", "cleaned_resume"]]

# Create processed folder automatically
os.makedirs("data/processed", exist_ok=True)

# Save cleaned file
df.to_csv("data/processed/cleaned_resume.csv", index=False)

print("\nPreprocessing completed successfully")
print("Saved file: data/processed/cleaned_resume.csv")
print("\nPreview:")
print(df.head())
print("\nShape:", df.shape)