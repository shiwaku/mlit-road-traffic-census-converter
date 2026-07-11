import type { LayerSpecification } from 'maplibre-gl';
import type { YearDef } from '../config/years.ts';

export interface LegendItem {
  /** 凡例スウォッチ色（省略時はラベルのみ） */
  color?: string;
  label: string;
}

/** 線幅スケール（交通量→太さ）を凡例に表示するための項目 */
export interface WidthScaleItem {
  /** 表示上の線の太さ(px) */
  thickness: number;
  label: string;
}

export interface Legend {
  title: string;
  items: LegendItem[];
  /** 線幅スケール（省略可。24時間交通量テーマ等で使用） */
  widthScale?: { heading: string; items: WidthScaleItem[] };
  /** 補足（※〜）行 */
  notes?: string[];
}

export interface Theme {
  id: string;
  /** UI（テーマセレクタ）表示名 */
  label: string;
  legend: Legend;
  /** 指定年度の source に対するテーマレイヤ群を生成（追加順＝描画順、後=前面） */
  buildLayers(year: YearDef): LayerSpecification[];
}
