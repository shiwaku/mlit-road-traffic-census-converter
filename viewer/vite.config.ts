import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';
import { createReadStream, statSync } from 'node:fs';
import { resolve } from 'node:path';
import type { IncomingMessage, ServerResponse } from 'node:http';

/**
 * 開発時のみ有効な PMTiles 配信ミドルウェア。
 * リポジトリの data/{year}/output/*.pmtiles（数百MB）を public/ にコピーせず、
 * HTTP Range（206 Partial Content）対応でストリーム配信する。
 * pmtiles プロトコルは Range リクエストでヘッダ・ディレクトリ・タイルを取得するため必須。
 */
const REPO_ROOT = resolve(__dirname, '..');

const LOCAL_PMTILES: Record<string, string> = {
  '/pmtiles/r03.pmtiles': 'data/r03/output/traffic_census_2021_converted.pmtiles',
  '/pmtiles/h27.pmtiles': 'data/h27/output/traffic_census_2015_converted.pmtiles',
};

function servePmtiles(req: IncomingMessage, res: ServerResponse): boolean {
  const url = (req.url ?? '').split('?')[0];
  const rel = LOCAL_PMTILES[url];
  if (!rel) return false;

  const filePath = resolve(REPO_ROOT, rel);
  let size: number;
  try {
    size = statSync(filePath).size;
  } catch {
    res.statusCode = 404;
    res.end(`PMTiles not found: ${rel}`);
    return true;
  }

  res.setHeader('Content-Type', 'application/octet-stream');
  res.setHeader('Accept-Ranges', 'bytes');
  res.setHeader('Cache-Control', 'no-cache');

  const range = req.headers.range;
  if (range) {
    const m = /bytes=(\d*)-(\d*)/.exec(range);
    const start = m && m[1] ? parseInt(m[1], 10) : 0;
    const end = m && m[2] ? parseInt(m[2], 10) : size - 1;
    if (start > end || start >= size) {
      res.statusCode = 416;
      res.setHeader('Content-Range', `bytes */${size}`);
      res.end();
      return true;
    }
    res.statusCode = 206;
    res.setHeader('Content-Range', `bytes ${start}-${end}/${size}`);
    res.setHeader('Content-Length', String(end - start + 1));
    createReadStream(filePath, { start, end }).pipe(res);
  } else {
    res.statusCode = 200;
    res.setHeader('Content-Length', String(size));
    createReadStream(filePath).pipe(res);
  }
  return true;
}

export default defineConfig({
  // GitHub Pages のサブパス配信に対応。PWA(SW) は相対 base 非推奨のため絶対パスを注入する。
  // 開発は既定の '/'、Pages ビルドはワークフローが VITE_BASE=/<repo>/ を設定する。
  base: process.env.VITE_BASE ?? '/',
  server: {
    // WSL の /mnt/c（Windows マウント）では inotify が効かず HMR が発火しないため、
    // ポーリング監視に切り替えて変更を確実に検知する。
    watch: { usePolling: true, interval: 300 },
  },
  plugins: [
    {
      name: 'serve-local-pmtiles',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          if (!servePmtiles(req, res)) next();
        });
      },
      // preview（ビルド後の確認）でも同じ配信を有効化
      configurePreviewServer(server) {
        server.middlewares.use((req, res, next) => {
          if (!servePmtiles(req, res)) next();
        });
      },
    },
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/apple-touch-icon.png', 'icons/favicon-32.png'],
      manifest: {
        name: '道路交通センサスマップ',
        short_name: 'センサスマップ',
        description:
          '道路交通センサス（R03/H27）の交通量・混雑度・旅行速度をMapLibreで可視化するビューワ',
        lang: 'ja',
        theme_color: '#12141b',
        background_color: '#12141b',
        display: 'standalone',
        orientation: 'any',
        start_url: './',
        scope: './',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' },
          { src: 'icons/maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
      workbox: {
        // アプリシェル（HTML/JS/CSS/アイコン）のみプリキャッシュ。
        // 巨大な PMTiles（数百MB）やタイルは対象外＝ネットワーク経由のまま。
        globPatterns: ['**/*.{js,css,html,png,svg,woff2}'],
        // バンドルJS（maplibre 込み）が大きいため上限を引き上げ
        maximumFileSizeToCacheInBytes: 4 * 1024 * 1024,
        navigateFallback: 'index.html',
        // PMTiles/タイルのリクエストは SW のナビゲーション処理から除外
        navigateFallbackDenylist: [/\/pmtiles\//, /\.pmtiles/],
        runtimeCaching: [
          {
            // GSI のグリフ・スプライト（小さく静的）はキャッシュしてラベル表示を高速化
            urlPattern: /^https:\/\/gsi-cyberjapan\.github\.io\/optimal_bvmap\/(glyphs|sprite)\//,
            handler: 'StaleWhileRevalidate',
            options: {
              cacheName: 'gsi-glyphs-sprite',
              expiration: { maxEntries: 300, maxAgeSeconds: 60 * 60 * 24 * 30 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
        ],
      },
      devOptions: { enabled: false },
    }),
  ],
});
