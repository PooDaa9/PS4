// sw.js
const CACHE_NAME = 'ps4-tool-v2';

// كل الملفات بدون هاش (المتصفح هيتعامل معاها عادي)
const FILES = [
  '/',
  '/index.html',
  '/run_lapse.html',
  '/PS4_13.00_Webkit.html',
  '/chain_lapse.js',
  '/chain_poops.js',
  '/sysctl.html',
  '/sysctl.js',
  '/core.js',
  '/mem.js',
  '/int64.js',
  '/ps4_offsets.js',
  '/rpc_worker.js',
  '/payload.bin',
  '/patches/1100.bin',
  '/patches/1150.bin',
  '/patches/1200.bin',
  '/patches/1300.bin'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        // تحميل الملفات بالتدريج عشان متقفش عند 43%
        return cache.addAll(FILES);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});