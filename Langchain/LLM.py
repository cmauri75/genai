from langchain_openai.llms import OpenAI

llm = OpenAI()
response = llm.invoke("Dimmi quali sono le 7 meraviglie del mondo")
print(response)

# Potrei anche leggere lo stream token per token:
for chunk in llm.stream("Dove si sono tenute le olimpiadi 2024?"):
    print(chunk+"-", end="", flush=True)
