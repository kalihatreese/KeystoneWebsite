addEventListener("fetch", event => {
  event.respondWith(
    new Response("🧠 Keystone Overlord Console Active", {
      headers: { "Content-Type": "text/plain" }
    })
  )
})
