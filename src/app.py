import streamlit as st
import joblib
import re
import nltk
import PyPDF2
from docx import Document
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from skills_db import SKILLS_DB

# download resources
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# load model
tfidf = joblib.load("models/tfidf_vectorizer.pkl")


# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = str(text).lower()

    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))

    words = [w for w in words if w not in stop_words]

    return " ".join(words)


# ---------------- SCORE ----------------
def score_resume(job_description, resume_text):
    job_clean = clean_text(job_description)
    resume_clean = clean_text(resume_text)

    job_vector = tfidf.transform([job_clean])
    resume_vector = tfidf.transform([resume_clean])

    score = cosine_similarity(job_vector, resume_vector)[0][0]

    return round(score * 10, 2)


# ---------------- EXPERIENCE ----------------
def extract_years(text):
    years = re.findall(r'(\d+)\+?\s+years', text.lower())

    if years:
        return max(map(int, years))

    return 0


# ---------------- SUGGESTIONS ----------------
def suggest_improvements(job_description, resume_text):

    job_clean = clean_text(job_description)
    resume_clean = clean_text(resume_text)

    job_words = set(job_clean.split())
    resume_words = set(resume_clean.split())

    missing_skills = []
    matched_skills = []

    for category, skills in SKILLS_DB.items():

        for skill in skills:

            skill_words = set(skill.lower().split())

            # skill required in job
            if skill_words.issubset(job_words):

                # skill exists in resume
                if skill_words.issubset(resume_words):
                    matched_skills.append(skill)

                else:
                    missing_skills.append(skill)

    # experience comparison
    job_exp = extract_years(job_description)
    resume_exp = extract_years(resume_text)

    exp_gap = None

    if job_exp > resume_exp:
        exp_gap = f"Need {job_exp} years, resume shows {resume_exp}"

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "experience_gap": exp_gap
    }


# ---------------- PDF READER ----------------
def read_pdf(file):
    text = ""

    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


# ---------------- DOCX READER ----------------
def read_docx(file):
    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# ---------------- UI ----------------
st.title("Resume Parser AI")
st.subheader("AI Resume Screening & Suggestions")

job = st.text_area("Enter Job Description")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

resume_text = ""

if uploaded_file:

    ext = uploaded_file.name.split(".")[-1].lower()

    if ext == "pdf":
        resume_text = read_pdf(uploaded_file)

    elif ext == "docx":
        resume_text = read_docx(uploaded_file)

    elif ext == "txt":
        resume_text = str(uploaded_file.read(), "utf-8")

    st.success("Resume uploaded successfully")


if st.button("Analyze Resume"):

    if job and resume_text:

        score = score_resume(job, resume_text)

        st.success(f"Resume Match Score: {score}/10")

        if score >= 8:
            st.write("Excellent Match")
        elif score >= 5:
            st.write("Average Match")
        else:
            st.write("Low Match")

        suggestions = suggest_improvements(job, resume_text)

        st.subheader("Analysis & Suggestions")

        # strengths
        if suggestions["matched_skills"]:
            st.write("Your Strengths:")
            for skill in suggestions["matched_skills"]:
                st.write(f"✅ {skill}")

        # missing skills
        if suggestions["missing_skills"]:
            st.write("Missing Skills:")
            for skill in suggestions["missing_skills"]:
                st.write(f"❌ {skill}")

        # experience gap
        if suggestions["experience_gap"]:
            st.write("Experience Gap:")
            st.write(f"⚠ {suggestions['experience_gap']}")

        # recommendations
        st.write("Recommendations:")

        if suggestions["missing_skills"]:
            for skill in suggestions["missing_skills"]:
                st.write(f"✔ Learn or add project on {skill}")

        st.write("✔ Add certifications")
        st.write("✔ Update resume summary")
        st.write("✔ Quantify achievements")

    else:
        st.warning("Upload resume and enter job description")