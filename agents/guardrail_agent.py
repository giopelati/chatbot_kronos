import os
from typing import Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.chains import LLMChain
from services.memory_service import get_memory
from langchain_core.runnables.history import RunnableWithMessageHistory

class GuardrailOutput(BaseModel):
    flag: int = Field(
        description='0 se a entrada for válida, 1 se for ofensiva'
    )
    message: Union[str, None] = Field(
        description='Mensagem educada para fugir do assunto caso flag=1, ou None se flag=0'
    )
    
# Conecta com o Gemini para geração de respostas
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
).with_structured_output(GuardrailOutput)

# Lê o template do prompt
with open("prompts/guardrail_prompt.txt", "r", encoding="utf-8") as x:
    template = x.read()
prompt = PromptTemplate.from_template(template)

# Declara a pipeline
pipeline = prompt | model 

def run_guardrail_agent(query, session_id):
    try:
        # Recupera a memória
        memory = get_memory(session_id)

        output: GuardrailOutput = pipeline.invoke({"query": query, "memory": memory})

        if output.flag == 0:
            return True, None
        else:
            return False, output.message
        
    except Exception as e:
        print(f"Erro no guardrail: {e}")
    
    return False, "Não foi possível validar sua pergunta."
