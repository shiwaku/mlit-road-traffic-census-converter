/** インライン SVG アイコン（stroke=currentColor で配色はCSSに追従） */

const svg = (paths: string) =>
  `<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;

/** 調査年度（カレンダー） */
export const iconCalendar = svg(
  '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9h18M8 2.5v4M16 2.5v4"/>',
);

/** 主題（レイヤ） */
export const iconLayers = svg(
  '<path d="M12 3 2.5 8 12 13l9.5-5L12 3Z"/><path d="M2.5 12 12 17l9.5-5M2.5 16 12 21l9.5-5"/>',
);

/** 空中写真（画像） */
export const iconPhoto = svg(
  '<rect x="3" y="4.5" width="18" height="15" rx="2"/><circle cx="8.5" cy="9.5" r="1.6"/><path d="m4 18 5-5 4 4 3-3 4 4"/>',
);

/** 折りたたみトグル（シェブロン） */
export const iconChevron = svg('<path d="m6 9 6 6 6-6"/>');

/** 出典（情報） */
export const iconInfo = svg('<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>');
