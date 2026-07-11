import type { ExpressionSpecification, SymbolLayerSpecification } from 'maplibre-gl';

/**
 * 道路種別で色分けする共通式。
 * 「3：一般国道」かつ「管理区分 != 国土交通大臣」（＝補助国道）はマゼンタ、
 * それ以外は道路種別で match。参照実装 (24jikankotsuryo-*-line) と同一。
 */
export const roadTypeColor: ExpressionSpecification = [
  'case',
  [
    'all',
    ['==', ['get', '道路種別'], '3：一般国道'],
    ['!=', ['get', '管理区分'], '1：国土交通大臣'],
  ],
  'rgba(255,0,255)',
  [
    'match',
    ['get', '道路種別'],
    '1：高速自動車国道', 'rgba(0,0,255)',
    '2：都市高速道路', 'rgba(0,0,119)',
    '3：一般国道', 'rgba(255,7,7)',
    '4：主要地方道（都道府県道）', 'rgba(0,116,0)',
    '5：主要地方道（指定市市道）', 'rgba(0,116,0)',
    '6：一般都道府県道', 'rgba(116,0,0)',
    '7：指定市の一般市道', 'rgba(116,0,0)',
    'rgba(0,0,0)',
  ],
];

/**
 * ２４時間交通量（上下計）で線幅を段階化する共通式。
 * 参照実装の step 閾値（5000/10000/20000/40000/80000 → 1/2/4/8/12/16）を踏襲。
 */
export const trafficWidth: ExpressionSpecification = [
  'step',
  ['to-number', ['get', '２４時間自動車類交通量（上下合計）／合計（台）']],
  1,
  5000, 2,
  10000, 4,
  20000, 8,
  40000, 12,
  80000, 16,
];

/** 一般道フィルタ（高速・都市高速を除外） */
export const ippandoFilter: ExpressionSpecification = [
  'all',
  ['!=', ['get', '道路種別'], '1：高速自動車国道'],
  ['!=', ['get', '道路種別'], '2：都市高速道路'],
];

/** 高速道路フィルタ（高速・都市高速のみ） */
export const kousokuFilter: ExpressionSpecification = [
  'any',
  ['==', ['get', '道路種別'], '1：高速自動車国道'],
  ['==', ['get', '道路種別'], '2：都市高速道路'],
];

/** 指定キーが null でない条件 */
export const notNull = (key: string): ExpressionSpecification => ['!=', ['get', key], null];

/** ラベル（線中央・全車/大型交通量）レイヤの共通 layout */
export const labelLayout = (field: string): SymbolLayerSpecification['layout'] => ({
  'symbol-placement': 'line-center',
  'text-rotation-alignment': 'map',
  'text-field': ['concat', ['get', field], '台'],
  // GSI 最適化ベクトルタイルの glyphs に存在するフォント（Open Sans 系は 404 のため使用不可）
  'text-font': ['NotoSansJP-Regular'],
  'text-size': 11,
  'text-offset': [0, -0.5],
});

/** ラベルの共通 paint */
export const labelPaint = (): SymbolLayerSpecification['paint'] => ({
  'text-color': 'rgba(255, 255, 255, 1)',
  'text-halo-blur': 0.8,
  'text-halo-color': 'rgba(0, 0, 0, 1)',
  'text-halo-width': 1,
});
