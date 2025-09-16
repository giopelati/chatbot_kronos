from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

# Conecta com o Mongo
connection = MongoClient("mongodb://localhost:27017/")
database = connection["chatbot_kronos"]
docs_collection = database["docs"]

# Conecta o Gemini para embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Seleciona os documentos sem embeddings
docs = list(docs_collection.find({"embedding": {"$exists": False}}))

for doc in docs:
    # Gera os embeddings do campo "content"
    content = doc["content"]
    vector = embeddings.embed_query(content)

    # Atualiza os documentos incluindo o novo campo "embedding"
    docs_collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {"embedding": vector}}
    )

print(f"Embeddings atualizados para {len(docs)} documentos.")
