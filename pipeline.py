from agents.guardrail_agent import run_guardrail_agent
from agents.judge_agent import run_judge_agent
from agents.rag_agent import run_rag_agent

def run_pipeline(query):
    # Etapa 1 - Verificação com o guardrail
    # Se o guardrail considerar a query inadequada, retorna uma resposta negativa
    guard_is_valid, guard_output = run_guardrail_agent(query)
    if not guard_is_valid:
        return guard_output
    
    # Etapa 2 - Geração da resposta com RAG
    # Recupera contexto e gera resposta
    rag_output, rag_context = run_rag_agent(query)

    # Etapa 3 - Validação da resposta com o juiz
    # Se o juiz aprova, a resposta original é enviada. Se rejeita, retorna a resposta ajustada
    judge_is_valid, judge_output = run_judge_agent(query, rag_output, rag_context)
    if judge_is_valid:
        return rag_output
    else:
        return judge_output
    
print(run_pipeline("Como fazer um bolo?"))