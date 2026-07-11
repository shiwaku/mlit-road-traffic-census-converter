import type {
  ExpressionSpecification,
  LineLayerSpecification,
  SymbolLayerSpecification,
} from 'maplibre-gl';
import type { YearDef } from '../config/years.ts';
import {
  ippandoFilter,
  kousokuFilter,
  labelLayout,
  labelPaint,
  notNull,
} from '../map/roadStyle.ts';

/** テーマレイヤ id を判定するための接頭辞（renderTheme が一括削除に使う） */
export const THEME_LAYER_PREFIX = 'theme:';

const tid = (id: string) => `${THEME_LAYER_PREFIX}${id}`;

/** 「上下」を組み合わせて null を大きな値に潰す（min を取るための前処理） */
const nullToBig = (field: string): ExpressionSpecification => [
  'case',
  ['==', ['get', field], null],
  999999,
  ['to-number', ['get', field]],
];

/**
 * 旅行速度の色分け式（上り・下りの遅い方＝min を段階化）。
 * 参照実装 konzatsuji/hikonzatsuji と同一の閾値・配色。
 */
export const speedColor = (up: string, down: string): ExpressionSpecification => [
  'step',
  ['min', nullToBig(up), nullToBig(down)],
  'rgb(255, 0, 0)',
  10, 'rgb(255, 127, 0)',
  20, 'rgb(255, 210, 0)',
  30, 'rgb(0, 152, 0)',
  40, 'rgb(0, 191, 255)',
  50, 'rgb(0, 63, 255)',
];

/** 速度テーマの表示対象フィルタ（上り or 下りいずれか計測あり） */
export const speedFilter = (up: string, down: string): ExpressionSpecification => [
  'any',
  notNull(up),
  notNull(down),
];

/** ライン系レイヤ（一般道 or 高速）を生成 */
export function lineLayer(opts: {
  id: string;
  year: YearDef;
  color: ExpressionSpecification | string;
  width: ExpressionSpecification | number;
  extraFilter: ExpressionSpecification;
  variant: 'ippando' | 'kousoku';
}): LineLayerSpecification {
  const roadFilter = opts.variant === 'ippando' ? ippandoFilter : kousokuFilter;
  return {
    id: tid(opts.id),
    type: 'line',
    source: opts.year.sourceId,
    'source-layer': opts.year.sourceLayer,
    minzoom: opts.variant === 'ippando' ? 10 : 4,
    layout: { 'line-join': 'round', 'line-cap': 'round' },
    paint: { 'line-color': opts.color, 'line-width': opts.width },
    filter: ['all', opts.extraFilter, roadFilter],
  };
}

/** ラベル（交通量など）レイヤを生成 */
export function labelLayer(opts: {
  id: string;
  year: YearDef;
  field: string;
  variant: 'ippando' | 'kousoku';
}): SymbolLayerSpecification {
  const roadFilter = opts.variant === 'ippando' ? ippandoFilter : kousokuFilter;
  return {
    id: tid(opts.id),
    type: 'symbol',
    source: opts.year.sourceId,
    'source-layer': opts.year.sourceLayer,
    minzoom: 10,
    layout: labelLayout(opts.field),
    paint: labelPaint(),
    filter: ['all', notNull(opts.field), roadFilter],
  };
}

/**
 * 透明なクリック判定用（幅広）ラインレイヤ。
 * 全テーマ共通でポップアップのヒット領域として使う（参照実装 zokusei-* 相当）。
 */
export function hitLayers(year: YearDef): LineLayerSpecification[] {
  const base = (variant: 'ippando' | 'kousoku'): LineLayerSpecification => ({
    id: tid(`hit-${variant}`),
    type: 'line',
    source: year.sourceId,
    'source-layer': year.sourceLayer,
    minzoom: variant === 'ippando' ? 10 : 4,
    layout: { 'line-join': 'round', 'line-cap': 'round' },
    paint: { 'line-color': 'rgba(255,255,255,0)', 'line-width': 10 },
    filter: ['all', variant === 'ippando' ? ippandoFilter : kousokuFilter],
  });
  return [base('ippando'), base('kousoku')];
}

/** ポップアップのクリック対象になるヒットレイヤ id */
export const HIT_LAYER_IDS = [tid('hit-ippando'), tid('hit-kousoku')];
