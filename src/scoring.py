import joblib
from sklearn.metrics.pairwise import cosine_similarity

# load trained tfidf
tfidf = joblib.load("models/tfidf_vectorizer.pkl")


def score_resume(job_description, resume_text):
    # convert both into vectors
    job_vector = tfidf.transform([job_description])
    resume_vector = tfidf.transform([resume_text])

    # similarity
    score = cosine_similarity(job_vector, resume_vector)[0][0]

    # convert to 0-10
    final_score = round(score * 10, 2)

    return final_score


# test example
if __name__ == "__main__":
    job = "Python SQL Machine Learning Data Analysis"

    resume = """
    Experienced in Python, SQL, Machine Learning,
    Data Analysis and Deep Learning
    """

    result = score_resume(job, resume)

    print("Resume Match Score:", result, "/10")