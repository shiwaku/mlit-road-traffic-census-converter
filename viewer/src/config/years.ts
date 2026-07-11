/**
 * 年度定義。
 * 参照実装は生の日本語列から paint 式を組む。列名・値は両年度でほぼ共通だが、
 * 「旅行速度」列名とポップアップ観測区分の表記に年度差があるため、ここで吸収する。
 */

export type YearId = 'r03' | 'h27';

/** 混雑時・非混雑時それぞれの上り/下り速度列名 */
export interface SpeedFields {
  congestedUp: string;
  congestedDown: string;
  uncongestedUp: string;
  uncongestedDown: string;
}

/** ポップアップに表示する属性（存在する列のみ描画する） */
export interface PopupField {
  label: string;
  key: string;
  /** 数値を桁区切り + 単位付きで整形するか */
  unit?: string;
}

export interface YearDef {
  id: YearId;
  /** UI 表示名 */
  label: string;
  /** 元号・調査名（凡例やポップアップ見出し用） */
  fullLabel: string;
  /** MapLibre source id */
  sourceId: string;
  /** PMTiles の source-layer 名（tippecanoe -l で付与した名前） */
  sourceLayer: string;
  /** PMTiles URL（開発時はローカル配信、本番は外部URL。env で上書き可能） */
  pmtilesUrl: string;
  /** 速度テーマ用の列名 */
  speed: SpeedFields;
  /** ポップアップ表示フィールド（順序どおり、存在する列のみ描画） */
  popupFields: PopupField[];
}

/** 交通量・区間の共通フィールド（両年度で列名一致） */
const commonTrafficFields = (): PopupField[] => [
  { label: '２４時間交通量（上下計/全車）', key: '２４時間自動車類交通量（上下合計）／合計（台）', unit: '台' },
  { label: '２４時間交通量（上下計/大型）', key: '２４時間自動車類交通量（上下合計）／大型車（台）', unit: '台' },
  { label: '昼間１２時間交通量（上下計/全車）', key: '昼間１２時間自動車類交通量（上下合計）／合計（台）', unit: '台' },
  { label: '昼間１２時間交通量（上下計/大型）', key: '昼間１２時間自動車類交通量（上下合計）／大型車（台）', unit: '台' },
  { label: '昼間１２時間大型車混入率', key: '昼間１２時間大型車混入率（％）', unit: '％' },
  { label: '混雑度', key: '混雑度' },
];

const R03_ENV = import.meta.env.VITE_PMTILES_R03_URL as string | undefined;
const H27_ENV = import.meta.env.VITE_PMTILES_H27_URL as string | undefined;

/** 本番ホスト（レンタルサーバ, HTTP Range 対応）の既定 URL */
const PROD_URL: Record<YearId, string> = {
  r03: 'https://shiworks2.xsrv.jp/mlit-road-traffic-census/traffic_census_2021_converted.pmtiles',
  h27: 'https://shiworks2.xsrv.jp/mlit-road-traffic-census/traffic_census_2015_converted.pmtiles',
};

/**
 * PMTiles URL の解決順:
 *   1) 環境変数 VITE_PMTILES_*_URL（あれば最優先）
 *   2) 開発サーバ（vite dev）はローカル Range 配信 /pmtiles/{id}.pmtiles
 *   3) 本番ビルドは PROD_URL（外部ホスト）
 */
const resolveUrl = (id: YearId, env: string | undefined): string => {
  if (env) return env;
  return import.meta.env.DEV ? `/pmtiles/${id}.pmtiles` : PROD_URL[id];
};

export const YEARS: Record<YearId, YearDef> = {
  r03: {
    id: 'r03',
    label: '令和3年度 (2021)',
    fullLabel: '令和3年度 全国道路・街路交通情勢調査（2021）',
    sourceId: 'census-r03',
    sourceLayer: 'traffic_census_2021',
    pmtilesUrl: resolveUrl('r03', R03_ENV),
    speed: {
      congestedUp: '朝夕（混雑時）／上り／旅行速度／合計（ｋｍ／ｈ）',
      congestedDown: '朝夕（混雑時）／下り／旅行速度／合計（ｋｍ／ｈ）',
      uncongestedUp: '昼間（非混雑時）／上り／旅行速度／合計（ｋｍ／ｈ）',
      uncongestedDown: '昼間（非混雑時）／下り／旅行速度／合計（ｋｍ／ｈ）',
    },
    popupFields: [
      { label: '交通調査基本区間番号', key: '交通調査基本区間番号' },
      { label: '道路種別', key: '道路種別' },
      { label: '路線名', key: '路線名' },
      { label: '管理区分', key: '管理区分' },
      { label: '区間延長', key: '区間延長（ｋｍ）', unit: 'km' },
      { label: '車線数', key: '車線数' },
      { label: '代表沿道状況', key: '代表沿道状況' },
      ...commonTrafficFields(),
      { label: '混雑時旅行速度（上り）', key: '朝夕（混雑時）／上り／旅行速度／合計（ｋｍ／ｈ）', unit: 'km/h' },
      { label: '混雑時旅行速度（下り）', key: '朝夕（混雑時）／下り／旅行速度／合計（ｋｍ／ｈ）', unit: 'km/h' },
      { label: '昼間非混雑時旅行速度（上り）', key: '昼間（非混雑時）／上り／旅行速度／合計（ｋｍ／ｈ）', unit: 'km/h' },
      { label: '昼間非混雑時旅行速度（下り）', key: '昼間（非混雑時）／下り／旅行速度／合計（ｋｍ／ｈ）', unit: 'km/h' },
    ],
  },
  h27: {
    id: 'h27',
    label: '平成27年度 (2015)',
    fullLabel: '平成27年度 全国道路・街路交通情勢調査（2015）',
    sourceId: 'census-h27',
    sourceLayer: 'traffic_census_2015',
    pmtilesUrl: resolveUrl('h27', H27_ENV),
    speed: {
      congestedUp: '混雑時／上り／旅行速度（ｋｍ／ｈ）',
      congestedDown: '混雑時／下り／旅行速度（ｋｍ／ｈ）',
      uncongestedUp: '昼間非混雑時／上り／旅行速度（ｋｍ／ｈ）',
      uncongestedDown: '昼間非混雑時／下り／旅行速度（ｋｍ／ｈ）',
    },
    popupFields: [
      { label: '交通調査基本区間番号', key: '交通調査基本区間番号' },
      { label: '道路種別', key: '道路種別' },
      { label: '路線名', key: '路線／路線名' },
      { label: '管理区分', key: '管理区分' },
      { label: '区間延長', key: '区間延長（ｋｍ）', unit: 'km' },
      { label: '車線数', key: '車線数' },
      { label: '代表沿道状況', key: '代表沿道状況' },
      ...commonTrafficFields(),
      { label: '混雑時旅行速度（上り）', key: '混雑時／上り／旅行速度（ｋｍ／ｈ）', unit: 'km/h' },
      { label: '混雑時旅行速度（下り）', key: '混雑時／下り／旅行速度（ｋｍ／ｈ）', unit: 'km/h' },
      { label: '昼間非混雑時旅行速度（上り）', key: '昼間非混雑時／上り／旅行速度（ｋｍ／ｈ）', unit: 'km/h' },
      { label: '昼間非混雑時旅行速度（下り）', key: '昼間非混雑時／下り／旅行速度（ｋｍ／ｈ）', unit: 'km/h' },
    ],
  },
};

export const YEAR_ORDER: YearId[] = ['r03', 'h27'];
export const DEFAULT_YEAR: YearId = 'r03';
