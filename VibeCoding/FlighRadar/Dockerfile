# Dockerfile per l'applicazione Flight Tracker Node.js

# 1. Scegli un'immagine base Node.js ufficiale.
# Alpine Linux è una buona scelta per immagini più piccole.
# Scegli una versione LTS (Long Term Support) di Node.js che sia compatibile con il tuo codice.
# Ad esempio, Node.js 18.x o 20.x.
FROM node:18-alpine AS builder

# 2. Imposta la directory di lavoro all'interno del container.
WORKDIR /usr/src/app

# 3. Copia i file package.json e package-lock.json (se esiste).
# Copiare questi file per primi permette a Docker di mettere in cache lo strato delle dipendenze
# se questi file non cambiano, velocizzando le build successive.
COPY package*.json ./

# 4. Installa le dipendenze dell'applicazione.
# Usiamo --only=production per installare solo le dipendenze necessarie per l'esecuzione,
# escludendo le devDependencies, se l'obiettivo è un'immagine di produzione snella.
# Se hai devDependencies necessarie per una fase di build (es. transpiling),
# potresti aver bisogno di un approccio multi-stage o di installare tutte le dipendenze.
# Per questa app semplice, --only=production dovrebbe andare bene.
RUN npm install --only=production

# 5. Copia il resto del codice sorgente dell'applicazione.
# Questo include index.js, la cartella public, ecc.
COPY . .

# 6. Esponi la porta su cui l'applicazione è in ascolto.
# La tua app usa process.env.PORT || 3000.
# Esponiamo 3000 di default; puoi mappare a una porta diversa al runtime.
EXPOSE 3000

# 7. Definisci una variabile d'ambiente per la chiave API.
# Questa dovrà essere fornita al momento dell'esecuzione del container.
# Non inserire MAI la tua chiave API direttamente nel Dockerfile.
ENV AVIATIONSTACK_API_KEY=""
# È anche possibile non definirla qui e passarla interamente al runtime,
# ma definirla come vuota qui rende esplicito che è richiesta.

# 8. Il comando per avviare l'applicazione quando il container parte.
CMD [ "node", "index.js" ]

# --- Note aggiuntive ---
# Sicurezza: Considera di eseguire l'applicazione come utente non root.
# Per farlo, aggiungeresti:
# RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# USER appuser
# Questo andrebbe aggiunto prima del CMD. Per semplicità, l'ho omesso qui.

# Multi-stage build (per scenari più complessi):
# Se avessi una fase di build (es. TypeScript, SASS, minificazione JS/CSS),
# potresti usare un multi-stage build. La prima fase ("builder") conterrebbe
# tutte le devDependencies e gli strumenti di build. La seconda fase copierebbe
# solo gli artefatti buildati e le dipendenze di produzione in un'immagine base pulita.
# Per la tua attuale app JavaScript pura, non è strettamente necessario.
