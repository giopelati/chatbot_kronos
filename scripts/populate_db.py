from pymongo import MongoClient

# Conecta com o Mongo
connection = MongoClient("mongodb://localhost:27017/")
database = connection["chatbot_kronos"]
docs_collection = database["docs"]

# Declara os docs 
docs = [
    {
        "title": "Introdução ao Kronos",
        "section": "Primeiros Passos",
        "content": "O Kronos é um aplicativo para controle de ponto e tarefas. Neste manual você aprenderá como usar as funcionalidades básicas para iniciar."
    },
    {
        "title": "Bater Ponto",
        "section": "Primeiros Passos",
        "content": "Para bater o ponto, abra o app e clique no botão 'Bater Ponto'. Escolha entrada ou saída e confirme."
    },
    {
        "title": "Registrar Tarefa",
        "section": "Tarefas",
        "content": "Para registrar uma tarefa, vá até a aba 'Tarefas', clique em 'Nova Tarefa', descreva e salve."
    },
    {
        "title": "Justificar Ausência",
        "section": "Dúvidas Frequentes",
        "content": "Justificar ausência significa explicar o motivo da falta em um dia de trabalho, como atestado médico ou outra razão."
    }
]

# Deleta qualquer documento antigo
docs_collection.delete_many({})

# Insere os novos
docs_collection.insert_many(docs)

print(f"{len(docs)} documentos inseridos.")