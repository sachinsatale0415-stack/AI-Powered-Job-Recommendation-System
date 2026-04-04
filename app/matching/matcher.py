from sklearn.metrics.pairwise import cosine_similarity
from app.matching.embedder import get_embedding

def calculate_match(resume_text, job_text):
    r_vec = get_embedding(resume_text)
    j_vec = get_embedding(job_text)

    score = cosine_similarity([r_vec], [j_vec])[0][0]
    return score * 100