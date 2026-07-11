import type maplibregl from 'maplibre-gl';
import type { Theme } from '../themes/types.ts';
import type { YearDef } from '../config/years.ts';
import { THEME_LAYER_PREFIX } from '../themes/helpers.ts';

/** 現在追加されているテーマレイヤ（接頭辞一致）をすべて削除 */
function clearThemeLayers(map: maplibregl.Map): void {
  const ids = map
    .getStyle()
    .layers.filter((l) => l.id.startsWith(THEME_LAYER_PREFIX))
    .map((l) => l.id);
  for (const id of ids) map.removeLayer(id);
}

/**
 * 指定年度・テーマのレイヤに差し替える。
 * 既存テーマレイヤを消してから buildLayers を追加順（=描画順、後が前面）で追加。
 * seamlessphoto より後に追加されるため常に空中写真の上に描画される。
 */
export function renderTheme(map: maplibregl.Map, year: YearDef, theme: Theme): void {
  clearThemeLayers(map);
  for (const spec of theme.buildLayers(year)) {
    map.addLayer(spec);
  }
}
