import os
from operator import add as add_messages
from typing import TypedDict, Annotated, Sequence

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END

def init():
    """Initialize the agent."""
    print("Initializing the agent...")
    file_path = "./content/Reviews-Export-2025-February-05-1008.csv"

    loader = CSVLoader(
        file_path=file_path,
        csv_args={
            "delimiter": ",",
            "quotechar": '"',
            "fieldnames": ["ID", "Title", "Content"],
        },
        source_column="Title",
    )

    reviews = loader.load()
    print(f"Loaded {len(reviews)} rows from reviews CSV file.")

    load_dotenv()
    llm = ChatOpenAI(model="gpt-4.1-mini",
                     temperature=0)  # Tempreature set to 0 for deterministic output  and minimize hallucinations

    # Very important to use an embedding model compatible to llm model
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    pages_split = text_splitter.split_documents(reviews)

    print(f"Created {len(pages_split)} chunks from reviews.")

    persist_directory = "chromaDB"
    collection_name = "reviews"

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
        vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_directory,
                             collection_name=collection_name)

    # Retriver get 5 most similar chunks
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )


    @tool
    def retriever_tool(query: str) -> str:
        """
        This tool searches and returns the information from MountainReview reviews.
        """
        docs = retriever.invoke(query)

        if not docs:
            return "Mi spiace, ma non ho trovato informazioni rilevanti alla tua richiesta tra le recensioni di MountainReview."

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
    Sei un assistente AI intelligente esperto di materiale per l'outdoor in montagna che risponde a domande su consigli per il miglior materiale per la montagna, basandoti sulle informazioni caricate nella tua base di conoscenza.
    Usa lo strumento di recupero disponibile per rispondere alle domande che ti sono poste. Puoi effettuare più chiamate se necessario.
    Se hai bisogno di cercare alcune informazioni prima di fare una domanda di follow-up, sei autorizzato a farlo.
    ```
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
            if t['name'] not in tools_dict:  # Checks if tool chosen by LLM is available
                print(f"\nTool: {t['name']} does not exist.")
                result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
            else:
                result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
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

    return graph.compile()

def running_agent():
    rag_agent = init()
    print("\nCiao, sono l'assistente AI di MountainReview, come posso aiutarti?")

    while True:
        user_input = input("\n>  ")
        if user_input.lower() in ['exit', 'quit', 'esci', 'stop', 'termina', 'ferma',  'bye', 'arrivederci',
                                  'addio', 'fine']:
            break

        messages = [HumanMessage(content=user_input)]  # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})

        print("\n=== RISPOSTA ===")
        print(result['messages'][-1].content)

agent = init()
history_messages = {}
def one_shot_agent(user_input: str, session_id: str) -> str:
    if session_id not in history_messages:
        print(f"Creating messages cache for session {session_id}")
        history_messages[session_id] = []

    history_messages[session_id].append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": history_messages[session_id]})
    history_messages[session_id] = result['messages']
    
    return result['messages'][-1].content
