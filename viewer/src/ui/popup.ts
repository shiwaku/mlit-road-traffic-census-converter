import maplibregl from 'maplibre-gl';
import type { YearDef } from '../config/years.ts';
import { HIT_LAYER_IDS } from '../themes/helpers.ts';

const esc = (v: unknown): string =>
  String(v ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

/** 値を整形（数値は桁区切り + 単位、非数値はそのまま） */
function formatValue(raw: unknown, unit?: string): string {
  if (raw === null || raw === undefined || raw === '') return '—';
  const num = typeof raw === 'number' ? raw : Number(raw);
  if (unit && Number.isFinite(num) && String(raw).trim() !== '') {
    return `${num.toLocaleString()} ${unit}`;
  }
  return esc(raw);
}

/** 属性から年度定義に沿ったテーブル HTML を組み立て（存在する列のみ） */
function buildTable(props: Record<string, unknown>, year: YearDef): string {
  const rows: string[] = [];
  for (const f of year.popupFields) {
    const raw = props[f.key];
    if (raw === null || raw === undefined || raw === '') continue;
    rows.push(
      `<tr><th>${esc(f.label)}</th><td>${formatValue(raw, f.unit)}</td></tr>`,
    );
  }
  return (
    `<div class="popup-title">${esc(year.label)}</div>` +
    `<table>${rows.join('')}</table>`
  );
}

/**
 * クリック→属性ポップアップを接続。
 * ヒットレイヤ（全テーマ共通・透明）を対象にし、表示中の年度定義で項目を整形する。
 * getYear は年度切替に追従するためのゲッター。
 */
export function initPopup(map: maplibregl.Map, getYear: () => YearDef): void {
  const onClick = (e: maplibregl.MapLayerMouseEvent) => {
    const feature = e.features?.[0];
    if (!feature) return;
    new maplibregl.Popup({ className: 'census-popup', maxWidth: '360px' })
      .setLngLat(e.lngLat)
      .setHTML(buildTable(feature.properties as Record<string, unknown>, getYear()))
      .addTo(map);
  };

  for (const id of HIT_LAYER_IDS) {
    map.on('click', id, onClick);
    map.on('mouseenter', id, () => {
      map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', id, () => {
      map.getCanvas().style.cursor = '';
    });
  }
}
