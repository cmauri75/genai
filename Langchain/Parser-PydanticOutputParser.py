from typing import List

from langchain_openai.llms import OpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator, field_validator
from langchain.output_parsers import PydanticOutputParser

# Initialize the language model
model = OpenAI(temperature=0.0)

# Define your desired data structure using Pydantic
class Joke(BaseModel):
    setup: str = Field(description="Domanda la cui risposta è una barzelletta")
    punchline: str = Field(description="Risposta per la barzelletta")

    @field_validator("setup")
    def question_ends_with_question_mark(cls, field):
        if field[-1] != "?":
            raise ValueError("Domanda mal formattata, manca il '?' finale!")
        return field

# Set up a PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=Joke)

# Create a prompt with format instructions
prompt = PromptTemplate(
    template="Rispondi alla domanda dell'utente.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Define a query to prompt the language model
query = "Raccontami una barzelletta."


# Combine prompt, model, and parser to get structured output
prompt_and_model = prompt | model
output = prompt_and_model.invoke({"query": query})
# Parse the output using the parser
parsed_result = parser.invoke(output)

# The result is a structured object
print(parsed_result)


### Altro esempio
class CryptoCurrencySummary(BaseModel):
    name: str
    high: float
    low: float

class Summary(BaseModel):
    date: str
    crypto_currencies: List[CryptoCurrencySummary]

parser = PydanticOutputParser(pydantic_object=Summary)

prompt_template = """
        Sei un esperto di criptovaluta.
        Il tuo ruolo è quello di estrarre il valore massimo e minimo in euro delle 10 migliori criptovalute.
        Il formato della data deve essere nel formato AAAA-MM-GG
                                
        {format_instructions}
    """

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model
json = chain.invoke({})
print(json)
