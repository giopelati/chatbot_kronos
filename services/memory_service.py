from langchain_mongodb import MongoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory

def get_memory(session_id):
    return MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://localhost:27017/",
        database_name="chatbot_kronos",
        collection_name="conversations",
    )