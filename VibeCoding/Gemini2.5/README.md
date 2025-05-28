# Utilizzo coding via Gemini 2.5

## Prompt di utilizzo

### Carico il file csv e poi chiedo:

```
Analizza il file allegato e descrivine la struttura. Per ogni colonna, forniscimi:
- Nome della colonna
- Tipo di dato (string, int, float, boolean). In caso di date, specifica il formato. In caso di float,
  specifica i separatori.
- Descrizione del contenuto
- Range o set di valori possibili
  Formatta il risultato come elenco puntato, uno per colonna, nel seguente formato:
- nome_colonna (tipo_dato) [possibili_valori]: descrizione
```

non ce la fa, allora provo con:

```
ecco le prime righe:
Email,Numero Fattura,Importo,Data Fattura,Stato,Data Scadenza
beffamario@example.org,INV-2025-0001,1928.61,2024-12-12,Saldata,2025-02-10
qparri@example.net,INV-2025-0002,248.85,2023-08-27,Non saldata,2023-10-26
combonicecilia@example.org,INV-2025-0003,1397.23,2025-05-04,Non saldata,2025-07-03
```

Ora ritorna:

```
Basandomi su questi dati, ecco l'analisi della struttura del file:

Email (string) [es. beffamario@example.org, qparri@example.net]: Indirizzo email del contatto o cliente associato alla fattura.

Descrizione del contenuto: Contiene indirizzi email in formato standard.
Range o set di valori possibili: Stringhe rappresentanti indirizzi email validi.
Numero Fattura (string) [es. INV-2025-0001, INV-2025-0002]: Identificativo univoco della fattura.

Descrizione del contenuto: Codice alfanumerico che identifica la fattura, sembra seguire il pattern INV-AAAA-NNNN.
Range o set di valori possibili: Stringhe alfanumeriche univoche per ogni fattura.
Importo (float, separatore decimale '.', separatore migliaia non rilevato nei campioni) [es. 1928.61, 248.85, 1397.23]: Importo monetario della fattura.

Descrizione del contenuto: Valore numerico che rappresenta l'ammontare della fattura. Nei dati forniti, il range è da 248.85 a 1928.61.
Range o set di valori possibili: Valori numerici decimali positivi.
Data Fattura (data, formato AAAA-MM-GG) [es. 2024-12-12, 2023-08-27, 2025-05-04]: Data di emissione della fattura.

Descrizione del contenuto: Indica il giorno, mese e anno in cui la fattura è stata emessa.
Range o set di valori possibili: Date valide nel formato Anno-Mese-Giorno. Nei dati forniti, le date variano da 2023-08-27 a 2025-05-04.
Stato (string) [Set dai campioni: "Saldata", "Non saldata"]: Stato attuale del pagamento della fattura.

Descrizione del contenuto: Indica se la fattura è stata pagata o meno.
Range o set di valori possibili: Un insieme di stringhe predefinite. I valori osservati sono "Saldata" e "Non saldata"; il file completo potrebbe contenerne altri (es. "Scaduta", "Insoluta").
Data Scadenza (data, formato AAAA-MM-GG) [es. 2025-02-10, 2023-10-26, 2025-07-03]: Data entro cui la fattura deve essere pagata.

Descrizione del contenuto: Specifica il termine ultimo per il pagamento della fattura.
Range o set di valori possibili: Date valide nel formato Anno-Mese-Giorno. 
```

Ora scelgo "canvas" e chiedo:

```
Agisci come un software engineer esperto nella creazione di web app moderne e intuitive per l'analisi dati.
Progetta un'applicazione che permetta all'utente di caricare un file CSV con la seguente struttura:
1. Email (string) [es. beffamario@example.org, qparri@example.net]: Indirizzo email del contatto o cliente associato alla fattura.
2. Descrizione del contenuto: Contiene indirizzi email in formato standard.
Range o set di valori possibili: Stringhe rappresentanti indirizzi email validi.
Numero Fattura (string) [es. INV-2025-0001, INV-2025-0002]: Identificativo univoco della fattura.
3. Descrizione del contenuto: Codice alfanumerico che identifica la fattura, sembra seguire il pattern INV-AAAA-NNNN.
Range o set di valori possibili: Stringhe alfanumeriche univoche per ogni fattura.
Importo (float, separatore decimale '.', separatore migliaia non rilevato nei campioni) [es. 1928.61, 248.85, 1397.23]: Importo monetario della fattura.
4. Descrizione del contenuto: Valore numerico che rappresenta l'ammontare della fattura. Nei dati forniti, il range è da 248.85 a 1928.61.
Range o set di valori possibili: Valori numerici decimali positivi.
Data Fattura (data, formato AAAA-MM-GG) [es. 2024-12-12, 2023-08-27, 2025-05-04]: Data di emissione della fattura.
5. Descrizione del contenuto: Indica il giorno, mese e anno in cui la fattura è stata emessa.
Range o set di valori possibili: Date valide nel formato Anno-Mese-Giorno. Nei dati forniti, le date variano da 2023-08-27 a 2025-05-04.
Stato (string) [Set dai campioni: "Saldata", "Non saldata"]: Stato attuale del pagamento della fattura.
6. Descrizione del contenuto: Indica se la fattura è stata pagata o meno.
Range o set di valori possibili: Un insieme di stringhe predefinite. I valori osservati sono "Saldata" e "Non saldata"; il file completo potrebbe contenerne altri (es. "Scaduta", "Insoluta").
Data Scadenza (data, formato AAAA-MM-GG) [es. 2025-02-10, 2023-10-26, 2025-07-03]: Data entro cui la fattura deve essere pagata.
7. Descrizione del contenuto: Specifica il termine ultimo per il pagamento della fattura.
Range o set di valori possibili: Date valide nel formato Anno-Mese-Giorno.

   La web app deve includere una dashboard interattiva, chiara e adatta a un pubblico non tecnico, che permetta di applicare i seguenti filtri:
1. Filtro sullo stato di pagamento (SALDATA / NON SALDATA)
2. Filtro sulla data_fattura: prima, dopo, tra due date o uguale a una data
3. Filtro sulla data_limite_pagamento: prima, dopo, tra due date o uguale a una data
   I filtri devono essere combinabili tra loro.
   La dashboard deve anche mostrare informazioni aggregate calcolate dinamicamente a partire dai
   dati filtrati.
   Inoltre, l'utente deve poter scaricare un CSV contenente i dati filtrati tramite un pulsante
   "Download".
   L'interfaccia deve essere professionale, moderna e accattivante, con UX semplice e intuitiva.
```

Ottengo la descrizione dell'applicazione che mi piace com'è (potrei cambiarla) e poi clicco su "create --> webapp"

Quando ha finito posso fare "Preview" , quindi aggiungo: 
```
permetti di filtrare attraverso una tendina dove posso scegliere le possibili email e sistema l'errore che vedo in console: "[11:05:04] [GLOBAL] ReferenceError: updateTable is not defined
at applyAllFilters (blob:https://0f92nhpogr0bjldwj72ycz6tmh2n1lci2z18k9hrllu125bqf2-h761100114.scf.usercontent.goog/c80233c1-ff1b-40f9-a5d8-9052f8358588:910:17)
    at blob:https://0f92nhpogr0bjldwj72ycz6tmh2n1lci2z18k9hrllu125bqf2-h761100114.scf.usercontent.goog/c80233c1-ff1b-40f9-a5d8-9052f8358588:1276:9"
```

Ora ho l'app funzionante
