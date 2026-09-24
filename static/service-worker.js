const CACHE_NAME = 'wpm-shell-v45';

const APP_SHELL = [
  '/',
  '/static/app.css',
  '/static/app.js',
  '/static/manifest.webmanifest',
  '/static/assets/_meta/asset-manifest.json',
  '/static/icons/icon-32.png',
  '/static/icons/apple-touch-icon-180.png',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/static/assets/icons/WPM_DesktopIcon_Official.webp',
  '/static/assets/brand/WPM_Splash_Login.webp',
  '/static/assets/brand/WPM_Wordmark.webp',
  '/static/assets/home/WPM_Home_Mascot.png',
  '/static/assets/home/backgrounds/WPM_Home_Background_SunriseBridge.webp',
  '/static/assets/home/backgrounds/WPM_Home_Background_BrightFairway.webp',
  '/static/assets/home/backgrounds/WPM_Home_Background_CreekBridge.webp',
  '/static/assets/home/backgrounds/WPM_Home_Background_IslandGreenGoldenHour.webp',
  '/static/assets/home/backgrounds/WPM_Home_Background_StormySunset.webp'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );

  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const requestUrl = new URL(event.request.url);

  if (requestUrl.origin !== self.location.origin) return;

  // Never cache live/shared round API data.
  if (requestUrl.pathname.startsWith('/api/')) {
    event.respondWith(fetch(event.request));
    return;
  }

  // Navigation stays network-first with an offline shell fallback.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const copy = response.clone();

          caches.open(CACHE_NAME).then((cache) => {
            cache.put('/', copy);
          });

          return response;
        })
        .catch(() => caches.match('/'))
    );

    return;
  }

  // Static assets are cache-first.
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;

      return fetch(event.request).then((response) => {
        if (response.ok) {
          const copy = response.clone();

          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, copy);
          });
        }

        return response;
      });
    })
  );
});
