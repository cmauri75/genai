import os
from operator import add as add_messages
from typing import TypedDict, Annotated, Sequence

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END

load_dotenv(dotenv_path="../../.env_secret")
llm = ChatOpenAI(model="gpt-4.1-mini",
                 temperature=0)  # Tempreature set to 0 for deterministic output  and minimize hallucinations

# Very important to use an embedding model compatible to llm model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

pdf_pages = PyPDFLoader("11-Stock_Market_Performance_2024.pdf").load()
print("Loaded PDF pages:", len(pdf_pages))

# Chunker, embedder can't manage too large phrases, every chunk is a vector
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

pages_split = text_splitter.split_documents(pdf_pages)

persist_directory = "chromaDB"
collection_name = "stock_market"

chroma_db_path = os.path.join(persist_directory, "chroma.sqlite3")
if not os.path.exists(chroma_db_path):
    try:
        # Here, we actually create the chroma database using our embeddigns model
        vectorstore = Chroma.from_documents(
            documents=pages_split,
            embedding=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        print("Created ChromaDB vector store!")
        print(vectorstore.get().keys())
    except Exception as e:
        print(f"Error setting up ChromaDB: {str(e)}")
        raise
else:
    print("ChromaDB vector already exists")
    vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_directory, collection_name=collection_name)

# Retriver get most similar chunks
retriever = vectorstore.as_retriever(
    search_type="similarity",  # Use similarity search
    search_kwargs={"k": 5}  # K is the amount of chunks to return
)


@tool
def retriever_tool(query: str) -> str:
    """
    This tool searches and returns the information from the Stock Market Performance 2024 document.
    """
    docs = retriever.invoke(query)

    if not docs:
        return "I found no relevant information in the Stock Market Performance 2024 document."

    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i + 1}:\n{doc.page_content}")

    return "\n\n".join(results)


tools = [retriever_tool]
llm = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state: AgentState) -> bool:
    """Check if the last message contains tool calls."""
    result = state['messages'][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0


system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools}  # Creating a dictionary of our tools


# LLM Agent
def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state."""
    messages = list(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {'messages': [message]}


# Retriever Agent
def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""

    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")

        if not t['name'] in tools_dict:  # Checks if tool chosen by LLM is available
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}


graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {True: "retriever_agent", False: END}
)
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()


def running_agent():
    print("\n=== RAG AGENT===")

    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages = [HumanMessage(content=user_input)]  # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})

        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)


running_agent()
