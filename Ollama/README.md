# Ollama

Info on: https://github.com/ollama/ollama

Usage via docker:
```bash
docker rm ollama
docker run -d --mount src=`pwd`/model,target=/root/model,type=bind -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Run model locally:
```bash
docker exec -it ollama ollama run gemma3:1b
```

Import finetuned model and run it
```bash
docker exec -oit ollama bash
cd /root/model
ollama create myModel -f Modelfile 
ollama run myModel
```

