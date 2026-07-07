from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:

    def calculate(self, resume_text, jd_text):

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            [resume_text, jd_text]
        )

        similarity = cosine_similarity(vectors)[0][1]

        return round(similarity * 100, 2)