from ast import literal_eval
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Conecta com o Gemini para geração de respostas
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Lê o template do prompt
with open("prompts/guardrail_prompt.txt", "r", encoding="utf-8") as x:
    template = x.read()
prompt = PromptTemplate.from_template(template)

def run_guardrail_agent(query):
    try:
        # Invoca a LLM
        output = model.invoke(prompt.format(query=query))
        
        # Avalia o conteúdo do output como literal
        parsed_output = literal_eval(output.content.strip())

        if parsed_output == 0:
            return True, None
        elif isinstance(parsed_output, list) and parsed_output[0] == 1:
            return False, parsed_output[1]
        
    except Exception as e:
        print(f"Erro no guardrail: {e}")
    
    return False, "Não foi possível validar sua pergunta."
