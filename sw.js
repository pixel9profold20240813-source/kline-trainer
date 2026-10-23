const V='kt-v1',SH=['./','index.html','manifest.json','icon-192.png','icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SH)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!=V).map(x=>caches.delete(x)))));self.clients.claim()});
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!='GET'||u.origin!=location.origin)return;
const put=r=>{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r};
const cacheFirst=u.pathname.includes('/data/')&&!u.pathname.endsWith('index.json');
e.respondWith(cacheFirst?caches.match(e.request).then(m=>m||fetch(e.request).then(put)):fetch(e.request).then(put).catch(()=>caches.match(e.request)))});
