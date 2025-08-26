import os
from typing import Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from services.memory_service import get_memory

class JudgeOutput(BaseModel):
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
).with_structured_output(JudgeOutput)

# Lê o template do prompt
with open("prompts/judge_prompt.txt", "r", encoding="utf-8") as x:
    template = x.read()
prompt = PromptTemplate.from_template(template)

# Declara a pipeline
pipeline = prompt | model 

def run_judge_agent(query, rag_output, context, session_id):
    try:
        # Recupera a memória
        memory = get_memory(session_id)
        
        output: JudgeOutput = pipeline.invoke({"query": query, "rag_output": rag_output, "context": context, "memory": memory})

        if output.flag == 0:
            return True, None
        else:
            return False, output.message
        
    except Exception as e:
        print(f"Erro no juiz: {e}")
    
    return False, "Não foi possível validar a resposta."
