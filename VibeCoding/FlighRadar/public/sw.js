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
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Se la risorsa è in cache, restituiscila
                if (response) {
                    return response;
                }
                // Altrimenti, effettua la richiesta di rete
                return fetch(event.request);
            })
    );
});

self.addEventListener('activate', event => {
    console.log('Service Worker: Attivazione...');
    // Rimuovi vecchie cache se necessario (non implementato qui per semplicità)
});
