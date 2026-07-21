/**
 * 時間帯別交通量の折れ線グラフ（依存ライブラリ無し・インラインSVG）。
 * 上り/下りの全車（小型+大型）を 0–23 時で描く。ポップアップ内に収まる小型サイズ。
 */
import type { UnitData } from '../data/jikantai.ts';
import { totalByHour } from '../data/jikantai.ts';

const UP_COLOR = '#4fc3f7'; // 上り
const DOWN_COLOR = '#ffb74d'; // 下り

const W = 328;
const H = 168;
const PAD = { top: 10, right: 10, bottom: 20, left: 34 };
const PLOT_W = W - PAD.left - PAD.right;
const PLOT_H = H - PAD.top - PAD.bottom;

const esc = (v: unknown): string =>
  String(v ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const xAt = (h: number): number => PAD.left + (h / 23) * PLOT_W;
const yAt = (v: number, max: number): number =>
  PAD.top + PLOT_H - (max > 0 ? (v / max) * PLOT_H : 0);

/** null を切れ目にして複数の <polyline> を生成（線が欠測でつながらないように）。 */
function polylines(vals: (number | null)[], max: number, color: string): string {
  const segs: string[][] = [];
  let cur: string[] = [];
  vals.forEach((v, h) => {
    if (v === null) {
      if (cur.length) segs.push(cur);
      cur = [];
    } else {
      cur.push(`${xAt(h).toFixed(1)},${yAt(v, max).toFixed(1)}`);
    }
  });
  if (cur.length) segs.push(cur);
  return segs
    .map((pts) =>
      pts.length === 1
        ? `<circle cx="${pts[0].split(',')[0]}" cy="${pts[0].split(',')[1]}" r="1.6" fill="${color}"/>`
        : `<polyline points="${pts.join(' ')}" fill="none" stroke="${color}" stroke-width="1.6" stroke-linejoin="round"/>`,
    )
    .join('');
}

/** 24時間交通量（台）を桁区切り。null は — */
const fmt = (v: number | null): string =>
  v === null || v === undefined ? '—' : v.toLocaleString();

/** 1区間分の時間帯別データからグラフ HTML を組み立てる。 */
export function buildChartHtml(unit: UnitData): string {
  const up = totalByHour(unit.up);
  const down = totalByHour(unit.down);
  const values = [...up, ...down].filter((v): v is number => v !== null);
  if (values.length === 0) {
    return '<div class="popup-chart-empty">時間帯別交通量データなし</div>';
  }
  const rawMax = Math.max(...values);
  // Y軸の上端を「見やすい丸め」に（1/2/5 × 10^n）
  const niceMax = niceCeil(rawMax);

  // Y軸グリッド（0, 中間, 上端の3本）
  const yTicks = [0, niceMax / 2, niceMax];
  const grid = yTicks
    .map((t) => {
      const y = yAt(t, niceMax).toFixed(1);
      return (
        `<line x1="${PAD.left}" y1="${y}" x2="${W - PAD.right}" y2="${y}" ` +
        `stroke="currentColor" stroke-opacity="0.15"/>` +
        `<text x="${PAD.left - 4}" y="${y}" text-anchor="end" dominant-baseline="middle" ` +
        `font-size="8" fill="currentColor" fill-opacity="0.6">${shortNum(t)}</text>`
      );
    })
    .join('');

  // X軸ラベル（0,6,12,18,23時）
  const xLabels = [0, 6, 12, 18, 23]
    .map(
      (h) =>
        `<text x="${xAt(h).toFixed(1)}" y="${H - 6}" text-anchor="middle" ` +
        `font-size="8" fill="currentColor" fill-opacity="0.6">${h}</text>`,
    )
    .join('');

  // 小型+大型（各々すでに上下合算済み）。多くの区間は12時間観測で24時間集計は空。
  const combine = (t: { s: number | null; l: number | null }): number | null =>
    t.s === null && t.l === null ? null : (t.s ?? 0) + (t.l ?? 0);
  const day12 = combine(unit.t12);
  const day24 = combine(unit.t24);

  const svg =
    `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" ` +
    `aria-label="時間帯別交通量グラフ" class="popup-chart-svg">` +
    grid +
    `<line x1="${PAD.left}" y1="${PAD.top}" x2="${PAD.left}" y2="${PAD.top + PLOT_H}" ` +
    `stroke="currentColor" stroke-opacity="0.3"/>` +
    xLabels +
    polylines(down, niceMax, DOWN_COLOR) +
    polylines(up, niceMax, UP_COLOR) +
    `</svg>`;

  return (
    `<div class="popup-chart">` +
    `<div class="popup-chart-head">時間帯別交通量（台/時・全車）` +
    `<span class="popup-chart-legend">` +
    `<i style="background:${UP_COLOR}"></i>上り` +
    `<i style="background:${DOWN_COLOR}"></i>下り` +
    `</span></div>` +
    svg +
    `<div class="popup-chart-note">昼間12時間 ${esc(fmt(day12))} 台` +
    (day24 !== null ? ` ／ 24時間 ${esc(fmt(day24))} 台` : '') +
    `（上下計/全車）</div>` +
    `</div>`
  );
}

/** 端数を 1/2/5×10^n に切り上げ。 */
function niceCeil(v: number): number {
  if (v <= 0) return 1;
  const exp = Math.floor(Math.log10(v));
  const base = Math.pow(10, exp);
  const f = v / base;
  const nice = f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10;
  return nice * base;
}

/** 軸ラベル用の短縮。1万以上は「万」表記、未満は桁区切りの通常数値。 */
function shortNum(v: number): string {
  if (v >= 10000) {
    return `${(v / 10000).toLocaleString(undefined, { maximumFractionDigits: 1 })}万`;
  }
  return v.toLocaleString();
}
