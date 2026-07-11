import type { Theme, Legend } from './types.ts';
import { hitLayers, lineLayer, speedColor, speedFilter } from './helpers.ts';

const speedLegend = (title: string, note: string): Legend => ({
  title,
  items: [
    { color: 'rgb(255, 0, 0)', label: '10km/h 未満' },
    { color: 'rgb(255, 127, 0)', label: '10 〜 20km/h 未満' },
    { color: 'rgb(255, 210, 0)', label: '20 〜 30km/h 未満' },
    { color: 'rgb(0, 152, 0)', label: '30 〜 40km/h 未満' },
    { color: 'rgb(0, 191, 255)', label: '40 〜 50km/h 未満' },
    { color: 'rgb(0, 63, 255)', label: '50km/h 以上' },
  ],
  notes: ['上り・下りで速度の低いほうを表示', note],
});

/** 旅行速度テーマ（混雑時/非混雑時）を生成するファクトリ。列名は年度定義から注入 */
function makeSpeedTheme(opts: {
  id: string;
  label: string;
  legend: Legend;
  pick: (y: import('../config/years.ts').YearDef) => { up: string; down: string };
}): Theme {
  return {
    id: opts.id,
    label: opts.label,
    legend: opts.legend,
    buildLayers: (year) => {
      const { up, down } = opts.pick(year);
      const color = speedColor(up, down);
      const filter = speedFilter(up, down);
      return [
        ...hitLayers(year),
        lineLayer({ id: `${opts.id}-ippando`, year, color, width: 4, extraFilter: filter, variant: 'ippando' }),
        lineLayer({ id: `${opts.id}-kousoku`, year, color, width: 4, extraFilter: filter, variant: 'kousoku' }),
      ];
    },
  };
}

/** 混雑時旅行速度（朝7-9時 / 夕17-19時） */
export const konzatsuji = makeSpeedTheme({
  id: 'konzatsuji',
  label: '混雑時旅行速度',
  legend: speedLegend('混雑時旅行速度', '午前7〜9時または午後5〜7時'),
  pick: (y) => ({ up: y.speed.congestedUp, down: y.speed.congestedDown }),
});

/** 昼間非混雑時旅行速度 */
export const hikonzatsuji = makeSpeedTheme({
  id: 'hikonzatsuji',
  label: '昼間非混雑時旅行速度',
  legend: speedLegend('昼間非混雑時旅行速度', '昼間の非混雑時間帯'),
  pick: (y) => ({ up: y.speed.uncongestedUp, down: y.speed.uncongestedDown }),
});
