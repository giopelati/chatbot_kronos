import os, json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from services.memory_service import get_memory
from services.rag_service import retrieve_similar_docs

# Conecta com o Gemini para geração de respostas
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

# Lê o template do prompt
with open("prompts/rag/system_prompt.txt", "r", encoding="utf-8") as x:
    system_text = x.read()
system_prompt = ("system", system_text)

# Lê exemplos few-shot
with open("prompts/rag/fewshots.json", "r", encoding="utf-8") as x:
    shots = json.load(x)

example_prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("{human}"),
    AIMessagePromptTemplate.from_template("{ai}")
])

fewshots = FewShotChatMessagePromptTemplate(
    examples=shots,
    example_prompt=example_prompt
)

# Monta prompt final (inclui histórico opcional e query)
rag_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    fewshots,
    MessagesPlaceholder("memory"),   
    ("human", 
     "Contexto:\n{context}\n\nPergunta:\n{query}")
])

def run_rag_agent(query, session_id):
    try:
        # Recupera contexto do RAG
        context = retrieve_similar_docs(query)

    except Exception as e:
        print(f"Erro na recuperação de contexto: {e}")
        return "Desculpe, houve um problema ao processar sua pergunta. Tente novamente mais tarde.", ""

    try:
        memory = get_memory(session_id)

        output = model.invoke(rag_prompt.format(context=context, query=query, memory=memory.messages))

        return output.content, context

    except Exception as e:
        print(f"Erro na geração da resposta: {e}")

    return "Desculpe, houve um problema ao processar sua pergunta. Tente novamente mais tarde.", ""