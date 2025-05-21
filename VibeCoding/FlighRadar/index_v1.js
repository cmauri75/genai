// index.js
const express = require('express');
const https = require('https')
const fs = require('fs')
const axios = require('axios');

const httpsAgent = new https.Agent({
    rejectUnauthorized: false, // (NOTE: this will disable client verification)
    cert: fs.readFileSync("./merged.pem")
})

const path = require('path');


const app = express();
const PORT = process.env.PORT || 3000;

// Middleware per parsare i dati del form URL-encoded
app.use(express.urlencoded({extended: true}));
// Middleware per servire file statici (come il nostro HTML)
app.use(express.static('public'));

// La tua chiave API di AviationStack
// IMPORTANTE: Memorizza la tua chiave API in modo sicuro.
// Su Replit, puoi usare la sezione "Secrets" (Environment Variables).
// Clicca sull'icona del lucchetto (Secrets) nella barra laterale sinistra.
// Aggiungi una nuova variabile chiamata AVIATIONSTACK_API_KEY e incolla la tua chiave.
const AVIATIONSTACK_API_KEY = process.env.AVIATIONSTACK_API_KEY;

if (!AVIATIONSTACK_API_KEY) {
    console.error("ERRORE CRITICO: La variabile d'ambiente AVIATIONSTACK_API_KEY non è impostata.");
    console.log("Per favore, imposta la tua chiave API nella sezione 'Secrets' di Replit.");
}

// Route principale per servire la pagina HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route per la ricerca del volo (definiremo questa più tardi)
app.post('/search-flight', async (req, res) => {
    // La logica di ricerca del volo andrà qui
    const flightIata = req.body.flightIata;
    console.log(`Richiesta di ricerca per il volo IATA: ${flightIata}`);

    if (!flightIata) {
        console.error("Errore: Codice IATA del volo non fornito.");
        return res.status(400).send("Per favore, inserisci un codice IATA del volo.");
    }

    if (!AVIATIONSTACK_API_KEY) {
        console.error("Errore: Chiave API AviationStack non configurata sul server.");
        return res.status(500).send("Errore del server: Configurazione API mancante.");
    }

    const params = {
        access_key: AVIATIONSTACK_API_KEY,
        flight_iata: flightIata,
    };

    try {
        console.log(`Chiamata API a AviationStack con IATA: ${flightIata}`);
        const response = await axios.get('https://api.aviationstack.com/v1/flights', {params:params,httpsAgent});

        console.log("Risposta API ricevuta. Status:", response.status);

        if (response.data && response.data.data && response.data.data.length > 0) {
            const flightInfo = response.data.data[0]; // Prendiamo il primo risultato
            console.log("Dati del volo estratti:", flightInfo);

            // Estrai le informazioni richieste basandoti sull'esempio di risposta fornito
            const displayData = {
                flight_date: flightInfo.flight_date, //
                flight_status: flightInfo.flight_status, //
                departure_airport: flightInfo.departure.airport, //
                arrival_airport: flightInfo.arrival.airport, //
                airline_name: flightInfo.airline.name, //
                arrival_scheduled: flightInfo.arrival.scheduled, //
                arrival_estimated: flightInfo.arrival.estimated //
            };
            res.json(displayData); // Invia i dati come JSON al client
        } else {
            console.warn("Nessun dato trovato per il volo:", flightIata, "Risposta API:", response.data);
            res.status(404).json({message: "Nessun dato trovato per il codice IATA fornito o la risposta dell'API era vuota/inattesa."});
        }
    } catch (error) {
        console.error("Errore durante la chiamata API a AviationStack:", error.message);
        if (error.response) {
            // La richiesta è stata fatta e il server ha risposto con uno status code
            // che non rientra nel range di 2xx
            console.error("Dati dell'errore API:", error.response.data);
            console.error("Stato dell'errore API:", error.response.status);
            console.error("Header dell'errore API:", error.response.headers);
            let errorMessage = "Errore durante la ricerca del volo.";
            if (error.response.data && error.response.data.error && error.response.data.error.message) {
                errorMessage = `Errore dall'API: ${error.response.data.error.message}`;
            } else if (error.response.status === 429) {
                errorMessage = "Hai superato il limite di richieste API. Riprova più tardi.";
            } else if (error.response.status === 401 || error.response.status === 403) {
                errorMessage = "Autenticazione fallita. Controlla la tua chiave API.";
            }
            res.status(error.response.status).json({message: errorMessage, details: error.response.data});
        } else if (error.request) {
            // La richiesta è stata fatta ma non è stata ricevuta nessuna risposta
            console.error("Nessuna risposta ricevuta dall'API:", error.request);
            res.status(500).json({message: "Nessuna risposta dal servizio AviationStack. Controlla la tua connessione o lo stato del servizio."});
        } else {
            // Qualcosa è successo durante la configurazione della richiesta che ha generato un Errore
            console.error("Errore nella configurazione della richiesta API:", error.message);
            res.status(500).json({message: "Errore interno del server durante la preparazione della richiesta API."});
        }
    }
});


app.listen(PORT, () => {
    console.log(`Server in ascolto sulla porta ${PORT}`);
    if (!AVIATIONSTACK_API_KEY) {
        console.warn("ATTENZIONE: La chiave API di AviationStack non è configurata. Le ricerche dei voli falliranno.");
    } else {
        console.log("Chiave API AviationStack caricata correttamente.");
    }
});
