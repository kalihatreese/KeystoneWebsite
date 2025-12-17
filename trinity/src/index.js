import { getAssetFromKV, mapRequestToAsset } from '@cloudflare/kv-asset-handler';

const ASSET_MANIFEST = globalThis.__ASSET_MANIFEST || {};

const requestMapper = (request) => {
  let url = new URL(request.url);
  if (url.pathname === '/') {
    url.pathname = '/index.html';
  }
  return mapRequestToAsset(new Request(url.toString(), request));
};


export default {
  async fetch(request, env, ctx) {
    try {
      if (env.NODE_ENV !== 'production') {
        getAssetFromKV.defaultOptions = { cacheControl: { bypassCache: true } };
      }

      return await getAssetFromKV(
        { request, waitUntil: ctx.waitUntil.bind(ctx) },
        {
          ASSET_NAMESPACE: env.__FINAL_ASSETS, // <-- FIXED TO USE NEW BINDING NAME
          ASSET_MANIFEST,
          mapRequestToAsset: requestMapper,
        }
      );
    } catch (e) {
      const pathname = new URL(request.url).pathname;
      return new Response(`"${pathname}" not found.`, {
        status: 404,
        statusText: 'Not Found',
      });
    }
  },
};
