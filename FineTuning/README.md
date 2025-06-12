# Finetuning

Utilizzo colab (così da avere GPU gratuite) per fare il fine tuning di un modello LLM. Mi baso su un pdf che racconta la storia della Ducati, lo trasformo in una serie di domande e risposte e lo uso per fare il fine tuning di un modello LLM.

Lo trovi: https://colab.research.google.com/drive/1yG8x1SyewVDOEdxagVBPXbb5GrioV1y9?hl=en#scrollTo=PMlLZAcKayn5

In questo caso ho utilizzato un pdf con dati tutto sommato pubblici, ma se fosse interno con informazioni riservate avrei avuto il caso d'uso ottimale.

1. Mi serve il dataset di domande e risposte: 
   Uso chatgpt o gemini col seguente prompt: "Dato il documento fornito, genera 200 domande possibili da fare sul documento formattate in una tabella senza categorizzazione, quindi aggiungi una colonna con le relative risposte. Non elencarle a video ma fornisci un link per il download"
2. Addestro il modello LLM con il dataset ottenuto al punto 1.
   
3. Esporto il modello così da poterlo poi usare in ollama
