from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai.llms import OpenAI

# Create a JSON prompt
json_prompt = PromptTemplate.from_template(
    "Crea una risposta json coi seguenti valori \"data_nascita\" e \"luogo_nascita\" che risponde alla seguente domanda: {question}"
)

# Choose a model
model = OpenAI(temperature=0.0)

# Initialize the JSON parser
json_parser = SimpleJsonOutputParser()

# Create a chain with the prompt, model, and parser
json_chain = json_prompt | model | json_parser

# Stream through the results
result_list = list(json_chain.stream({"question": "Quando e dove è nato Alessandro Manzoni?"}))

# The result is a list of JSON-like dictionaries
print(result_list)
