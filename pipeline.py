import uuid
from langchain_mongodb import MongoDBChatMessageHistory
from agents.guardrail_agent import run_guardrail_agent
from agents.judge_agent import run_judge_agent
from agents.rag_agent import run_rag_agent

def run_pipeline(query, session_id):
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    # Inicializa o histórico do MongoDB para essa sessão
    chat_message_history = MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://localhost:27017/",
        database_name="chatbot_kronos",
        collection_name="conversations",
    )

    # Salva a mensagem do usuário
    chat_message_history.add_user_message(query)

    # Etapa 1 - Verificação com o guardrail
    # Se o guardrail considerar a query inadequada, retorna uma resposta negativa
    guard_is_valid, guard_output = run_guardrail_agent(query, session_id)
    if not guard_is_valid:
        chat_message_history.add_ai_message(guard_output)
        return guard_output
    
    # Etapa 2 - Geração da resposta com RAG
    # Recupera contexto e gera resposta
    rag_output, rag_context = run_rag_agent(query, session_id)

    # Etapa 3 - Validação da resposta com o juiz
    # Se o juiz aprova, a resposta original é enviada. Se rejeita, retorna a resposta ajustada
    judge_is_valid, judge_output = run_judge_agent(query, rag_output, rag_context, session_id)
    if judge_is_valid:
        chat_message_history.add_ai_message(rag_output)
        return rag_output
    else:
        chat_message_history.add_ai_message(judge_output)
        return judge_output