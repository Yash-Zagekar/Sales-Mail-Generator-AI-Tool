import pandas as pd
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.vectorizer = TfidfVectorizer()
        self.index = None
        self.vectors = None

    def load_portfolio(self):
        # Convert the tech stack (text) to vectors using TF-IDF
        tech_stacks = self.data["Techstack"].values
        self.vectors = self.vectorizer.fit_transform(tech_stacks).toarray()

        # Create a FAISS index for similarity search
        dim = self.vectors.shape[1]  # dimension of the vectors
        self.index = faiss.IndexFlatL2(dim)  # L2 distance index
        self.index.add(np.array(self.vectors).astype('float32'))  # Add vectors to the index

    def query_links(self, skills):
        # Ensure skills is a string; you may want to handle a list of skills differently.
        if isinstance(skills, list):
            skills = " ".join(skills)  # Join list into a single string

        # Transform the input query (skills) into the same vector space
        query_vector = self.vectorizer.transform([skills]).toarray().astype('float32')

        # Perform the similarity search
        _, indices = self.index.search(query_vector, k=2)  # Search for 2 closest vectors

        # Retrieve metadata (links) for the closest tech stacks
        results = []
        for idx in indices[0]:
            results.append({"links": self.data.iloc[idx]["Links"]})
        return results
