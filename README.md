# AI Resume Parser & Intelligent Resume Screening System

Live Demo: https://your-app.streamlit.app  
GitHub: https://github.com/YOUR_USERNAME/Resume-Parser-AI

---

## Project Overview

AI-based Resume Screening and Suggestion System built using Python, NLP, and Machine Learning.

This application analyzes **one candidate resume at a time** against a given job description and provides:
- Resume match score (0–10)
- Missing skills analysis
- Experience gap detection
- Personalized recommendations for resume improvement

---

## Features

✅ Upload Resume (PDF / DOCX / TXT)

✅ Enter Job Description

✅ Resume Match Score (/10)

✅ Missing Skills Detection

✅ Experience Gap Analysis

✅ Personalized Recommendations

---

## Example Output

Resume Match Score: 6.02/10

Average Match

Your Strengths:
- Python
- SQL

Missing Skills:
- Machine Learning
- Data Analysis

Recommendations:
- Learn or add project on Machine Learning
- Learn or add project on Data Analysis
- Add certifications
- Update resume summary

---

## Tech Stack

- Python
- NLTK
- Scikit-learn
- Streamlit
- PyPDF2
- python-docx

---

## Machine Learning Models Used

1. TF-IDF Vectorizer
   - converts resume text into vectors

2. KMeans Clustering
   - groups similar resumes

3. Cosine Similarity
   - calculates job-resume match score

---

## Project Workflow

Resume Upload
↓
Text Extraction
↓
NLTK Preprocessing
↓
TF-IDF Feature Extraction
↓
Resume Scoring
↓
Skill Gap Detection
↓
Suggestions Output

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run src/app.py
