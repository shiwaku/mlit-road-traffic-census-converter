import type { Theme } from './types.ts';
import { roadTypeColor, trafficWidth, notNull } from '../map/roadStyle.ts';
import { hitLayers, lineLayer, labelLayer } from './helpers.ts';

const FIELD = '２４時間自動車類交通量（上下合計）／合計（台）';

/** 24時間交通量（全車上下計） — 道路種別で色分け・交通量で線幅 */
export const traffic24h: Theme = {
  id: '24jikankotsuryo',
  label: '24時間交通量（全車上下計）',
  legend: {
    title: '２４時間交通量（全車上下計）',
    items: [
      { color: 'rgb(0, 0, 255)', label: '高速自動車国道' },
      { color: 'rgb(0, 0, 119)', label: '都市高速道路' },
      { color: 'rgb(255, 7, 7)', label: '一般国道 直轄' },
      { color: 'rgb(255, 0, 255)', label: '一般国道 補助国道' },
      { color: 'rgb(0, 116, 0)', label: '主要地方道（都道府県道・指定市市道）' },
      { color: 'rgb(116, 0, 0)', label: '一般都道府県道・指定市の一般市道' },
    ],
    widthScale: {
      heading: '線幅 = 24時間交通量',
      items: [
        { thickness: 1, label: '5千台 未満' },
        { thickness: 2, label: '5千 〜 1万台' },
        { thickness: 4, label: '1万 〜 2万台' },
        { thickness: 7, label: '2万 〜 4万台' },
        { thickness: 10, label: '4万 〜 8万台' },
        { thickness: 14, label: '8万台 以上' },
      ],
    },
    notes: ['図中の台数は24時間交通量（全車上下計）'],
  },
  buildLayers: (year) => [
    ...hitLayers(year),
    lineLayer({ id: '24h-ippando-line', year, color: roadTypeColor, width: trafficWidth, extraFilter: notNull(FIELD), variant: 'ippando' }),
    lineLayer({ id: '24h-kousoku-line', year, color: roadTypeColor, width: trafficWidth, extraFilter: notNull(FIELD), variant: 'kousoku' }),
    labelLayer({ id: '24h-ippando-label', year, field: FIELD, variant: 'ippando' }),
    labelLayer({ id: '24h-kousoku-label', year, field: FIELD, variant: 'kousoku' }),
  ],
};
