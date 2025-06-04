from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever

full_text = open("Chroma-Stati.txt", "r").read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_text(full_text)

embeddings = OpenAIEmbeddings()
db = Chroma.from_texts(texts, embeddings)
retriever = db.as_retriever()

retrieved_docs = retriever.invoke("Cosa pensa il presidente riguardo Ketanji Brown Jackson?")
print(retrieved_docs[0].page_content)

print("----------")
question = "Quali sono gli approcci alla Task Decomposition?"
llm = ChatOpenAI(temperature=0)
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(), llm=llm
)

unique_docs = retriever_from_llm.get_relevant_documents(query=question)
print("Number of unique documents:", len(unique_docs))
