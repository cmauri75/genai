from langchain.prompts import PromptTemplate, ChatPromptTemplate

# Simple prompt with placeholders
prompt_template = PromptTemplate.from_template(
    "Raccontami un {aggettivo} aneddoto riguardante {oggetto}."
)

# Filling placeholders to create a prompt
filled_prompt = prompt_template.format(aggettivo="divertente", oggetto="robots")
print(filled_prompt)

# Defining a chat prompt with various roles
chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Sei un alpinista esperto di materiale di montagna, il tuo nome è {name}."),
        ("human", "Ciao, come va?"),
        ("ai", "Va bene, grazie."),
        ("human", "{user_input}"),
    ]
)

# Formatting the chat prompt
formatted_messages = chat_template.format_messages(name="Planet Mountaing", user_input="Mi sai suggerire una buona scarpa da trail running?")
for message in formatted_messages:
    print(message)
