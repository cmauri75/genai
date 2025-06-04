from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_openai.llms import OpenAI

# Initialize the language model
model = OpenAI(temperature=0.0)

# Initialize the parser
output_parser = CommaSeparatedListOutputParser()

# Create format instructions
format_instructions = output_parser.get_format_instructions()

# Create a prompt to request a list
prompt = PromptTemplate(
    template="Elenca dieci {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)

# Define a query to prompt the model
query = "Squadre di calcio italiane di serie A"

# Generate the output
output = model(prompt.format(subject=query))

# Parse the output using the parser
parsed_result = output_parser.parse(output)

# The result is a list of items
print(parsed_result)
