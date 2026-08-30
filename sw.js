// sw.js - Service Worker للتخزين المؤقت
const CACHE_NAME = 'ps4-tool-v2';

// الملفات الأساسية (خفيفة - تتحمل أولاً)
const CORE_FILES = [
  '/',
  '/index.html',
  '/run_lapse.html',
  '/PS4_13.00_Webkit.html',
  '/sysctl.html',
  '/preview.png'
];

// الملفات الإضافية (تتحمل بعد كده)
const EXTRA_FILES = [
  '/chain_lapse.js',
  '/chain_poops.js',
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

// تركيب الـ Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('📦 تحميل الملفات الأساسية...');
        return cache.addAll(CORE_FILES);
      })
      .then(() => {
        console.log('✅ تم تحميل الملفات الأساسية');
        // تحميل الملفات الإضافية في الخلفية
        caches.open(CACHE_NAME).then(cache => {
          cache.addAll(EXTRA_FILES).catch(() => {
            console.log('⚠️ بعض الملفات الإضافية مش موجودة');
          });
        });
      })
  );
  self.skipWaiting();
});

// تفعيل الـ Service Worker
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ حذف الكاش القديم:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// التعامل مع الطلبات
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response; // من الكاش
        }
        return fetch(event.request);
      })
  );
});