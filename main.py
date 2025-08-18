from fastapi import FastAPI
import uvicorn
from pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API do Chatbot Kronos está online!"}

@app.get("/chat")
def chat(query: str | None = None, session_id: str | None = None):
    if not query:
        return {"erro": "O parâmetro 'query' é obrigatório."}
    response = run_pipeline(query)
    return {"resposta": response}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8200, reload=True)
