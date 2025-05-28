# Prova di utilizzo di vibecoding

## Start
Uso https://claude.ai

Prompt: vedi il file prompt.src

## Prototipo

### ChatGCP:
Dopo la generazione del codice chiedo:

* "genera il file package.json per l'esecuzione locale"
* "come devo chiamare il file generato per poterlo eseguire in locale con npm run dev?"

### Copilot 
Crea in automatico i file principali divisi in 5 Jsx

Aggiungo:
* "crea gli altri file necessari per l'esecuzione del codice in locale con npm"
* "l'applicazione non funziona per via di problemi di CORS, risolvili"
* "L'applicazione non è molto bella da vedere, puoi creare un css per abbellirla?"

Ora ho l'app funzionante

### Gemini
Crea un solo file js vanilla contenente tutto

* "Rifattorizza l'applicazione per utilizzare un backend esterno REST da cui ottenere i dati e salvare le nuove ricette"

### Cloud run via Gemini
"Crea una applicazione spring boot che espone un servizio rest /api/log che riceve un parametro di nome param nella request, quindi crea un file json nella directory /mnt/logs contenente la data e ora della richiesta e il contenuto di tale parametro. Crea inoltre un file docker per generare una macchina eseguibile e uno script per pubblicare su dockerhub tale macchina. Crea anche uno script per deployare la macchina su cloudrun"

## Casi d'uso
* Posso specificare un repo con un'app e chiedergli di trasformarla, ad esempio crearmi una UI


## Gemini 2.5
Creo un'app per lavorare su file excel e lo trasforma in un'app
