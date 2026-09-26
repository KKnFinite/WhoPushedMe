const CACHE_NAME = 'wpm-shell-v81';

const CRITICAL_FRONTEND_PATHS = new Set([
  '/static/app.css',
  '/static/audio.js',
  '/static/app.js',
]);

const APP_SHELL = [
  '/',
  '/static/app.css',
  '/static/audio.js',
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
  '/static/assets/icons/alternates/WPM_Icon_Mascot_Alt2.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_BrightDay.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_CreekBridge.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_GoldenHour.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_StormySunset.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_SunriseCourse.webp'
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

  // Critical CSS/JS must never be served stale against newer HTML.
  // This prevents a mixed-version shell during service-worker updates.
  if (CRITICAL_FRONTEND_PATHS.has(requestUrl.pathname)) {
    event.respondWith(
      fetch(event.request, { cache: 'no-store' })
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, copy);
            });
          }
          return response;
        })
        .catch(() =>
          caches.match(event.request).then(
            (cached) => cached || caches.match(requestUrl.pathname)
          )
        )
    );
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
