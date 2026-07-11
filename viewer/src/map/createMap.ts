import maplibregl from 'maplibre-gl';
import type { StyleSpecification } from 'maplibre-gl';
import paleStyle from '../basemap/pale.json';

/** 地図の初期表示（首都圏北部あたり） */
const INITIAL_CENTER: [number, number] = [139.483113, 35.925003];
const INITIAL_ZOOM = 12;

/**
 * MapLibre 地図を生成し、各種コントロールを追加して返す。
 * ベースマップは国土地理院「最適化ベクトルタイル（淡色）」（pale.json をバンドル）。
 * コントロール（ナビ/全画面/現在地/スケール）は左下、出典は右下。
 * 左上＝操作パネル（不透明度スライダー統合）/ 右上＝凡例 と重ならない配置。
 */
export function createMap(container: string): maplibregl.Map {
  const map = new maplibregl.Map({
    container,
    style: paleStyle as unknown as StyleSpecification,
    hash: true,
    center: INITIAL_CENTER,
    zoom: INITIAL_ZOOM,
    minZoom: 4,
    maxZoom: 23,
    attributionControl: false,
  });

  // 出典は各ソース（pale.json のベースマップ / センサス / 空中写真）の attribution に一本化。
  // customAttribution を足すと重複するため付けない。
  map.addControl(new maplibregl.AttributionControl({ compact: true }), 'bottom-right');
  // 左下スタックは「最初に追加＝最下段、最後に追加＝最上段」。
  // 表示（上→下）: ナビ → 現在地 → 全面表示 → スケール（最下）にするため、
  // 追加はその逆順（スケール → 全面表示 → 現在地 → ナビ）で行う。
  map.addControl(new maplibregl.ScaleControl({ maxWidth: 200, unit: 'metric' }), 'bottom-left');
  map.addControl(new maplibregl.FullscreenControl(), 'bottom-left');
  map.addControl(
    new maplibregl.GeolocateControl({
      positionOptions: { enableHighAccuracy: false },
      fitBoundsOptions: { maxZoom: 18 },
      trackUserLocation: true,
      showUserLocation: true,
    }),
    'bottom-left',
  );
  map.addControl(new maplibregl.NavigationControl(), 'bottom-left');

  return map;
}
