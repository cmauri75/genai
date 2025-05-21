// public/sw.js
const CACHE_NAME = 'flight-tracker-pro-v1';
const urlsToCache = [
    '/',
    '/index.html',
    // Aggiungi qui i percorsi ai tuoi file CSS e JS principali se li hai separati
    // Esempio: '/style.css', '/script.js'
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
    // Aggiungi anche le icone del manifest se vuoi che siano disponibili offline
    // '/images/icon-192x192.png',
    // '/images/icon-512x512.png'
];

self.addEventListener('install', event => {
    console.log('Service Worker: Installazione...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Caching delle risorse statiche');
                return cache.addAll(urlsToCache);
            })
            .catch(err => {
                console.error('Service Worker: Fallimento caching durante installazione:', err);
            })
    );
});

self.addEventListener('fetch', event => {
    console.log(`Service Worker: Intercettata richiesta per: ${event.request.url}, Mode: ${event.request.mode}, Destination: ${event.request.destination}`);

    // Non tentare di gestire richieste non-GET o richieste per estensioni Chrome, ecc.
    if (event.request.method !== 'GET' || event.request.url.startsWith('chrome-extension://')) {
        // Lascia che il browser gestisca queste richieste normalmente
        return;
    }

    event.respondWith(
        caches.match(event.request)
            .then(cachedResponse => {
                if (cachedResponse) {
                    console.log(`Service Worker: Risorsa TROVATA in cache: ${event.request.url}`);
                    return cachedResponse;
                }

                console.log(`Service Worker: Risorsa NON in cache, fetching da rete: ${event.request.url}`);
                return fetch(event.request)
                    .then(networkResponse => {
                        console.log(`Service Worker: Risposta OTTENUTA da rete per: ${event.request.url}, Status: ${networkResponse.status}`);

                        // Opzionale: Metti in cache la nuova risorsa per usi futuri
                        // Assicurati che la risposta sia valida prima di metterla in cache
                        if (networkResponse && networkResponse.ok && event.request.destination !== 'video' && event.request.destination !== 'audio') { // networkResponse.ok controlla status 200-299
                            const responseToCache = networkResponse.clone(); // Cloniamo perché la response può essere letta una sola volta
                            caches.open(CACHE_NAME)
                                .then(cache => {
                                    console.log(`Service Worker: Messa in cache nuova risorsa: ${event.request.url}`);
                                    cache.put(event.request, responseToCache);
                                })
                                .catch(cacheError => {
                                    console.error(`Service Worker: Fallimento messa in cache per ${event.request.url}`, cacheError);
                                });
                        }
                        return networkResponse;
                    })
                    .catch(networkError => {
                        // Questo .catch() è specifico per il fallimento della chiamata fetch()
                        console.error(`Service Worker: Fallimento FETCH da rete per ${event.request.url}`, networkError);
                        // È importante restituire qualcosa qui, anche se è un errore o una pagina di fallback.
                        // Se non si restituisce nulla, la richiesta originale del browser potrebbe bloccarsi o fallire in modo anomalo.
                        // Esempio di pagina di fallback:
                        // if (event.request.destination === 'document') { // Se è una richiesta di navigazione
                        //   return caches.match('/offline.html'); // Assicurati di avere un offline.html cachato
                        // }
                        // Per ora, per il debug, restituiamo una risposta di errore semplice.
                        return new Response(`Network error: Impossibile recuperare ${event.request.url}. Errore: ${networkError.message}`, {
                            status: 503, // Service Unavailable (o un altro codice di errore appropriato)
                            statusText: `Network error: ${networkError.message}`,
                            headers: { 'Content-Type': 'text/plain' }
                        });
                    });
            })
            .catch(error => {
                // Questo .catch() è per errori nel caches.match()
                console.error(`Service Worker: Errore nel gestore fetch (probabilmente caches.match) per ${event.request.url}:`, error);
                return new Response(`Errore nel service worker per ${event.request.url}. Dettagli: ${error.message}`, {
                    status: 500,
                    headers: { 'Content-Type': 'text/plain' }
                });
            })
    );
});

self.addEventListener('activate', event => {
    console.log('Service Worker: Attivazione...');
    // Rimuovi vecchie cache se necessario (non implementato qui per semplicità)
});
