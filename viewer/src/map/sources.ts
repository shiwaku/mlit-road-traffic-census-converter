import type maplibregl from 'maplibre-gl';
import { YEARS, YEAR_ORDER } from '../config/years.ts';

/**
 * 両年度のセンサス PMTiles を vector source として登録。
 * タイルは参照（レイヤ追加）されるまで取得されないため、二重登録のコストは低い。
 */
export function addCensusSources(map: maplibregl.Map): void {
  for (const id of YEAR_ORDER) {
    const y = YEARS[id];
    if (map.getSource(y.sourceId)) continue;
    map.addSource(y.sourceId, {
      type: 'vector',
      url: `pmtiles://${y.pmtilesUrl}`,
      // リンク先が 404 のためハイパーリンクは付けずプレーンテキストにする
      attribution: '道路交通センサス（国土交通省, PDL1.0）',
    });
  }
}
