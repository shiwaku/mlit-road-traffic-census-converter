/**
 * 時間帯別交通量の県別JSONを遅延ロードし、地物のキーで引くローダ。
 *
 * zkntrf 由来の県別JSON（コンバーターの jikantai ステップ生成物）を
 * 都道府県指定市コードごとに1ファイル取得してキャッシュし、
 * 複合キー `<都道府県指定市コード>_<交通量調査単位区間番号>` で1区間分を返す。
 */
import type { JikantaiDef, YearId } from '../config/years.ts';

/** 1方向・車種別の時間帯配列（index=0..23時、null=欠測） */
export interface DirSeries {
  s: (number | null)[]; // 小型
  l: (number | null)[]; // 大型
}

export interface UnitData {
  up: DirSeries;
  down: DirSeries;
  t12: { s: number | null; l: number | null };
  t24: { s: number | null; l: number | null };
}

interface PrefFile {
  year: string;
  hours: number[];
  units: Record<string, UnitData>;
}

// 県別ファイル取得結果のキャッシュ（year:NN -> Promise）。null=取得失敗。
const cache = new Map<string, Promise<PrefFile | null>>();

/** '13100.0' / 13100 / '13100' -> '13100'（canonical int-string）。不正は null。 */
function normKey(v: unknown): string | null {
  if (v === null || v === undefined) return null;
  const s = String(v).trim();
  if (s === '') return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return String(Math.round(n));
}

/** 都道府県指定市コード -> 県別ファイル番号 NN（コード // 1000、2桁ゼロ埋め） */
function fileNo(prefCode: string): string {
  return String(Math.floor(Number(prefCode) / 1000)).padStart(2, '0');
}

function loadPref(year: YearId, base: string, nn: string): Promise<PrefFile | null> {
  const cacheKey = `${year}:${nn}`;
  const hit = cache.get(cacheKey);
  if (hit) return hit;
  const p = fetch(`${base}${nn}.json`)
    .then((r) => (r.ok ? (r.json() as Promise<PrefFile>) : null))
    .catch(() => null);
  cache.set(cacheKey, p);
  return p;
}

/**
 * 地物プロパティから時間帯別データを引く。
 * 見つからない/未観測区間は null（呼び出し側で「データなし」を表示）。
 */
export async function lookupUnit(
  props: Record<string, unknown>,
  def: JikantaiDef,
  year: YearId,
): Promise<UnitData | null> {
  const pref = normKey(props[def.prefKey]);
  const unit = normKey(props[def.unitKey]);
  if (pref === null || unit === null) return null;
  const file = await loadPref(year, def.baseUrl, fileNo(pref));
  if (!file) return null;
  return file.units[`${pref}_${unit}`] ?? null;
}

/** 上り/下りの全車（小型+大型）合計を index=時刻(0..23) で返す。 */
export function totalByHour(series: DirSeries): (number | null)[] {
  return series.s.map((s, i) => {
    const l = series.l[i];
    if (s === null && l === null) return null;
    return (s ?? 0) + (l ?? 0);
  });
}
