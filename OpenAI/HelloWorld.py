from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-nano",
    input="Scrivi una storia della buonanotte in una frase su un unicorno."
)

print(response.output_text)
