# Coding

```shell
# Riuso il virtualenv creato per openai
source ../.venv/bin/activate
## questi sono deprecati
# pip install langchain
# pip install langchain_community
pip install langchain_openai
#cli per lavorare coi template e con langserve
pip install langchain-cli
#uso openai come backend
pip install openai
source ../OpenAI/.env_secret
```

```
python LLM.py
python ChatModel.py
python Template.py

python Parser-PydanticOutputParser.py
python Parser-SimpleJsonOutputParser.py
python Parser-CommaSeparatedListOutputParser.py
python Parser-DocumentLoader.py

python Embeddings.py

python Chroma.py
```

