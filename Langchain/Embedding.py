# Initialize the language model
from langchain_openai import OpenAIEmbeddings
from scipy.spatial.distance import cosine

# Initialize the model
embeddings_model = OpenAIEmbeddings()

# Embed a list of texts
embeddings = embeddings_model.embed_documents(
    ["Hi there!", "Oh, hello!", "What's your name?", "My friends call me World", "Hello World!"]
)
print("Number of documents embedded:", len(embeddings))
for( i, embedding) in enumerate(embeddings):
    print(f"Embedding {i}: {embedding[:5]}...")  # Print first 5 elements of each embedding for brevity

embedded_query = embeddings_model.embed_query("What was the name mentioned in the conversation?")
print("First five dimensions of the embedded query:", embedded_query[:5])

#Questa l'ho ideata io
for i, embedding in enumerate(embeddings):
    distance = cosine(embedding, embedded_query)
    print(f"Cosine distance between embedding {i} and embedded_query: {distance:.4f}")
