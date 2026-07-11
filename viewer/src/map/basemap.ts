import type maplibregl from 'maplibre-gl';

export const SEAMLESSPHOTO_LAYER = 'seamlessphoto';
const DEFAULT_OPACITY = 0.3;

/**
 * 全国最新写真（シームレス, 地理院）を raster レイヤとして追加。
 * 初期不透明度 30%。ズーム12以上で表示（広域では非表示）。
 */
export function addAerialPhoto(map: maplibregl.Map): void {
  map.addSource('seamlessphoto', {
    type: 'raster',
    tiles: ['https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg'],
    tileSize: 256,
    attribution:
      '<a href="https://maps.gsi.go.jp/development/ichiran.html#seamlessphoto" target="_blank" rel="noopener">全国最新写真（シームレス）</a>',
  });
  map.addLayer({
    id: SEAMLESSPHOTO_LAYER,
    type: 'raster',
    source: 'seamlessphoto',
    minzoom: 12,
    maxzoom: 23,
    paint: { 'raster-opacity': DEFAULT_OPACITY },
  });
}

export const DEFAULT_AERIAL_OPACITY = DEFAULT_OPACITY;
