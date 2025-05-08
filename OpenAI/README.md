# OpenAI

Simple calls direct to OpenAI API service

## setup
* Add to .env_secret OPENAI_API_KEY. 
* Install requirements
```shell
# create virtual env
python3 -m venv openaiEnv
# activate virtual env
source ./.venv/bin/activate
# install openai requirements
pip install openai
# add cacert to avoid zscaler ssl problems
cp cacert.pem .venv/lib/python3.13/site-packages/certifi/cacert.pem
```
* Run poc
```shell
source .env_secret
python3 HelloWorld.py
```
