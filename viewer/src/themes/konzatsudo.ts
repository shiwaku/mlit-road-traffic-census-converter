import type { ExpressionSpecification } from 'maplibre-gl';
import type { Theme } from './types.ts';
import { notNull } from '../map/roadStyle.ts';
import { hitLayers, lineLayer, labelLayer } from './helpers.ts';

const TRAFFIC_FIELD = '昼間１２時間自動車類交通量（上下合計）／合計（台）';

/** 混雑度（昼間12時間）を段階化する色式 */
const konzatsudoColor: ExpressionSpecification = [
  'step',
  ['to-number', ['get', '混雑度']],
  'rgb(0, 152, 0)',
  1.0, 'rgb(255, 210, 0)',
  1.25, 'rgb(255, 127, 0)',
  1.75, 'rgb(255, 0, 0)',
];

/** 混雑度 — 値で色分け、線幅は一定。ラベルは昼間12時間交通量 */
export const konzatsudo: Theme = {
  id: 'konzatsudo',
  label: '混雑度',
  legend: {
    title: '混雑度（昼間12時間）',
    items: [
      { color: 'rgb(0, 152, 0)', label: '1.0 未満' },
      { color: 'rgb(255, 210, 0)', label: '1.0 以上 〜 1.25 未満' },
      { color: 'rgb(255, 127, 0)', label: '1.25 以上 〜 1.75 未満' },
      { color: 'rgb(255, 0, 0)', label: '1.75 以上' },
    ],
    notes: ['図中の台数は昼間12時間交通量（全車上下計）'],
  },
  buildLayers: (year) => [
    ...hitLayers(year),
    lineLayer({ id: 'konz-ippando', year, color: konzatsudoColor, width: 4, extraFilter: notNull(TRAFFIC_FIELD), variant: 'ippando' }),
    lineLayer({ id: 'konz-kousoku', year, color: konzatsudoColor, width: 4, extraFilter: notNull(TRAFFIC_FIELD), variant: 'kousoku' }),
    labelLayer({ id: 'konz-ippando-label', year, field: TRAFFIC_FIELD, variant: 'ippando' }),
    labelLayer({ id: 'konz-kousoku-label', year, field: TRAFFIC_FIELD, variant: 'kousoku' }),
  ],
};
