### Creazione app skyscanner: https://www.youtube.com/watch?v=A5o-_sPIKos&list=WL&index=5&t=19s

Lui consiglia deepseek ma io uso altri tool.
* Perplexity: "Voglio creare una applicazione flightracker e sto cercando una api gratis che mi fornisca informazioni sui voli in tempo reale, cosa mi consigli?"
  * Ottengo Aviationstack, vado sul sito e ottengo una free api key
  * ChatGPT 2.5 pro: "Fammi un esempio di chiamata api che mi permette di ottenere informazioni su un volo partendo dal suo codice usando aviationstack.com"
      * Ottengo un esempio di call che mi salvo per utilizzarlo in seguito
      * Lancio il prompt.src e costruisco la mia app come indicato, funziona ma devo solo modificarla per zscaler
      * Ora vorrei anche aggiungere una mappa, uso prompt2.src e aggiorno i file come indicato. Funziona subito
      * Ora provo a migliorare la grafica con prompt3.src e lui fa al volo
      * Ora voglio creare una app android, mi consiglia sia la PWA che una WebView
      * A questo punto uso cloudrun per deployare la mia app
