import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from services.memory_service import get_memory
from services.rag_service import retrieve_similar_docs

# Conecta com o Gemini para geração de respostas
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Lê o template do prompt
with open("prompts/rag_prompt.txt", "r", encoding="utf-8") as x:
    template = x.read()
prompt = PromptTemplate.from_template(template)

def run_rag_agent(query, session_id):
    try:
        # Recupera os documentos mais relevantes como contexto
        context = retrieve_similar_docs(query)

    except Exception as e:
        print(f"Erro na recuperação de contexto: {e}")
        return "Desculpe, houve um problema ao processar sua pergunta. Tente novamente mais tarde.", ""

    try:
        memory = get_memory(session_id)
        # Invoca a LLM
        output = model.invoke(prompt.format(context=context, query=query, memory=memory))
        return output.content, context
    
    except Exception as e:
        print(f"Erro na geração da resposta: {e}")
        return "Desculpe, houve um problema ao processar sua pergunta. Tente novamente mais tarde.", ""