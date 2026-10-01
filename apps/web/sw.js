const CACHE_PREFIX = "veilbound-shell-";
const CACHE = `${CACHE_PREFIX}v4`;
const SHELL = ["./", "./index.html", "./app.css", "./app.js", "./manifest.webmanifest"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    Promise.all([
      caches.keys().then((keys) =>
        Promise.all(
          keys
            .filter((key) => key.startsWith(CACHE_PREFIX) && key !== CACHE)
            .map((key) => caches.delete(key))
        )
      ),
      self.clients.claim()
    ])
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  const requestUrl = new URL(event.request.url);
  const shellUrl = new URL(self.registration.scope);

  if (requestUrl.origin !== shellUrl.origin) return;

  event.respondWith(
    (async () => {
      let response;

      try {
        response = await fetch(event.request);
      } catch {
        const cached = await caches.match(event.request);
        return cached || Response.error();
      }

      if (response.ok) {
        try {
          const cache = await caches.open(CACHE);
          await cache.put(event.request, response.clone());
        } catch (error) {
          console.warn("Veilbound cache update failed; serving network response.", error);
        }
      }

      return response;
    })()
  );
});
