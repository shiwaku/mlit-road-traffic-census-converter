import type { ExpressionSpecification } from 'maplibre-gl';
import type { Theme } from './types.ts';
import { notNull } from '../map/roadStyle.ts';
import { hitLayers, lineLayer, labelLayer } from './helpers.ts';

const OGATA_FIELD = '昼間１２時間自動車類交通量（上下合計）／大型車（台）';

/** 大型車混入率（昼間12時間, ％）を段階化する色式 */
const ogatashaColor: ExpressionSpecification = [
  'step',
  ['to-number', ['get', '昼間１２時間大型車混入率（％）']],
  'rgb(0, 152, 0)',
  10, 'rgb(255, 210, 0)',
  15, 'rgb(255, 127, 0)',
  20, 'rgb(255, 0, 0)',
];

/** 大型車混入率 — 値で色分け。ラベルは昼間12時間大型車交通量 */
export const ogatasha: Theme = {
  id: 'ogatashakonnyuritsu',
  label: '大型車混入率',
  legend: {
    title: '大型車混入率（昼間12時間）',
    items: [
      { color: 'rgb(0, 152, 0)', label: '10% 未満' },
      { color: 'rgb(255, 210, 0)', label: '10% 以上 〜 15% 未満' },
      { color: 'rgb(255, 127, 0)', label: '15% 以上 〜 20% 未満' },
      { color: 'rgb(255, 0, 0)', label: '20% 以上' },
    ],
    notes: ['図中の台数は昼間12時間交通量（大型車上下計）'],
  },
  buildLayers: (year) => [
    ...hitLayers(year),
    lineLayer({ id: 'ogata-ippando', year, color: ogatashaColor, width: 4, extraFilter: notNull(OGATA_FIELD), variant: 'ippando' }),
    lineLayer({ id: 'ogata-kousoku', year, color: ogatashaColor, width: 4, extraFilter: notNull(OGATA_FIELD), variant: 'kousoku' }),
    labelLayer({ id: 'ogata-ippando-label', year, field: OGATA_FIELD, variant: 'ippando' }),
    labelLayer({ id: 'ogata-kousoku-label', year, field: OGATA_FIELD, variant: 'kousoku' }),
  ],
};
