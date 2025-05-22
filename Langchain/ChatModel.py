from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Tu sei Micheal Jordan."),
    HumanMessage(content="Qual'è il miglior produttore di scarpe?"),
]
response = ChatOpenAI().invoke(input=messages)
print(response.content)
