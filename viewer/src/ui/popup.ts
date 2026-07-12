import maplibregl from 'maplibre-gl';
import type { YearDef } from '../config/years.ts';
import { HIT_LAYER_IDS } from '../themes/helpers.ts';
import type { Highlight } from '../map/highlight.ts';

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
 * クリック→区間ハイライト＋属性ポップアップを接続。
 *
 * ヒットレイヤ（全テーマ共通・透明）を queryRenderedFeatures で判定する単一の
 * map クリックハンドラにまとめることで、空地クリック（＝選択解除）も同じ経路で
 * 扱え、ポップアップの多重表示も避けられる。表示中の年度定義で項目を整形する。
 * getYear は年度切替に追従するためのゲッター。
 */
export function initPopup(
  map: maplibregl.Map,
  getYear: () => YearDef,
  highlight: Highlight,
): void {
  let popup: maplibregl.Popup | null = null;

  // ユーザーが × で閉じたときのハンドラ。
  // 差し替え・空地クリックで閉じる際は closePopup が事前に off するので呼ばれない
  // ＝ close の発火タイミング（同期/非同期）に依存せず選択を打ち消さない。
  const onUserClose = () => {
    popup = null;
    highlight.clear(map);
  };

  const closePopup = () => {
    if (!popup) return;
    popup.off('close', onUserClose);
    popup.remove();
    popup = null;
  };

  map.on('click', (e) => {
    const layers = HIT_LAYER_IDS.filter((id) => map.getLayer(id));
    const feature = layers.length
      ? map.queryRenderedFeatures(e.point, { layers })[0]
      : undefined;

    // まず既存ポップアップを閉じる（この時点では選択に触れない）
    closePopup();

    if (!feature) {
      // 空地クリック → ハイライト解除
      highlight.clear(map);
      return;
    }

    // 閉じ終えた後に選択を更新するので、close ハンドラに打ち消される余地がない
    highlight.select(map, feature);
    popup = new maplibregl.Popup({
      className: 'census-popup',
      maxWidth: '360px',
      closeOnClick: false,
    })
      .setLngLat(e.lngLat)
      .setHTML(buildTable(feature.properties as Record<string, unknown>, getYear()))
      .addTo(map);
    popup.on('close', onUserClose);
  });

  for (const id of HIT_LAYER_IDS) {
    map.on('mouseenter', id, () => {
      map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', id, () => {
      map.getCanvas().style.cursor = '';
    });
  }
}
