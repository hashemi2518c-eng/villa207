// نسخه را با هر تغییر صفحه یک واحد بالا ببرید تا گوشی‌ها نسخه تازه را بگیرند.
const CACHE = 'att207-v2';
const FILES = ['./', 'index.html', 'manifest.webmanifest', 'icons/logo.svg', 'icons/icon-192.png', 'icons/icon-180.png',
  'fonts/vazirmatn-arabic-400-normal.woff2', 'fonts/vazirmatn-arabic-700-normal.woff2', 'fonts/vazirmatn-arabic-800-normal.woff2',
  'fonts/poppins-latin-400-normal.woff2', 'fonts/poppins-latin-600-normal.woff2'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return; // گوگل شیت از کش رد نمی‌شود
  // اول شبکه (برای گرفتن نسخه تازه)، اگر اینترنت نبود از کش
  e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put(e.request, c)); return r; })
    .catch(() => caches.match(e.request, {ignoreSearch: true})));
});
