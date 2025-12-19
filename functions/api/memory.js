export async function onRequest(context) {
  const { results } = await context.env.KESTONE_D1.prepare("SELECT content FROM fragments ORDER BY created_at DESC LIMIT 1").all();
  return new Response(JSON.stringify(results[0] || {content: "Core Offline"}), {headers: {"Content-Type": "application/json"}});
}
