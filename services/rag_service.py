from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Conecta com o Mongo
connection = MongoClient("mongodb://localhost:27017/")
database = connection["chatbot_kronos"]
docs_collection = database["docs"]

# Conecta o Gemini para embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def retrieve_similar_docs(query, top_k=3):
    # Gera o embedding da query
    query_emb = embeddings.embed_query(query)
    query_vec = np.array(query_emb).reshape(1, -1)
    
    # Seleciona os documentos que possuem embedding
    docs = list(docs_collection.find({"embedding": {"$exists": True}}))

    score_docs = []
    for doc in docs:
        # Calcula o cosine similarity entre a query e o embedding do documento
        score = cosine_similarity(query_vec, np.array(doc["embedding"]).reshape(1, -1))
        score_docs.append((score, doc))

    # Ordena os documentos da maior para a menor similaridade
    score_docs.sort(key=lambda x: x[0], reverse=True)

    # Retorna apenas os top_ks maiores
    return [doc["content"] for x, doc in score_docs[:top_k]]
