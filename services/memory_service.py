from langchain_mongodb import MongoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory

def get_memory(session_id):
    chat_message_history = MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://localhost:27017/",
        database_name="chatbot_kronos",
        collection_name="conversations",
    )
    memory = ConversationBufferMemory(chat_memory=chat_message_history, return_messages=True)
    return memory