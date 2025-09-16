import os, json
from typing import Union
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain.chains import LLMChain
from services.memory_service import get_memory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate

class GuardrailOutput(BaseModel):
    flag: int = Field(
        description='0 se a entrada for válida, 1 se for ofensiva'
    )
    message: Union[str, None] = Field(
        description='Mensagem educada para fugir do assunto caso flag=1, ou None se flag=0'
    )
    
# Conecta com o Gemini para geração de respostas
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
).with_structured_output(GuardrailOutput)

# Lê o template do prompt
with open("prompts/guardrail/system_prompt.txt", "r", encoding="utf-8") as x:
    system_text = x.read()
system_prompt = ("system", system_text)

# Lê exemplos few-shot
with open("prompts/guardrail/fewshots.json", "r", encoding="utf-8") as x:
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
guardrail_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    fewshots,
    MessagesPlaceholder("memory"),   # opcional: histórico/memória
    ("human", "{query}"),
])

# Declara a pipeline
pipeline = guardrail_prompt | model 

def run_guardrail_agent(query, session_id):
    try: 
        memory = get_memory(session_id)

        output: GuardrailOutput = pipeline.invoke({"query": query, "memory": memory.messages})

        print('Guardrail:', output)

        if output.flag == 0:
            return True, None
        else:
            return False, output.message
        
    except Exception as e:
        print(f"Erro no guardrail: {e}")
    
    return False, "Não foi possível validar sua pergunta."
