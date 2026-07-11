import type { Theme } from '../themes/types.ts';
import { iconChevron } from './icons.ts';

/** 凡例パネル（テーマ連動・線スタイル風スウォッチ）を描画 */
export function renderLegend(panel: HTMLElement, theme: Theme): void {
  const { legend } = theme;
  panel.innerHTML = '';

  // ヘッダ（タイトル + 折りたたみ）
  const header = document.createElement('div');
  header.className = 'panel-header';
  header.innerHTML = `
    <div class="title-group"><h1>凡例</h1></div>
    <button class="collapse-btn" type="button" aria-label="凡例を折りたたむ">${iconChevron}</button>
  `;
  header.querySelector('.collapse-btn')!.addEventListener('click', () => {
    panel.classList.toggle('collapsed');
  });
  panel.appendChild(header);

  const body = document.createElement('div');
  body.className = 'panel-body';

  const title = document.createElement('div');
  title.className = 'legend-title';
  title.textContent = legend.title;
  body.appendChild(title);

  // 色分け（線スタイル風）
  for (const item of legend.items) {
    const row = document.createElement('div');
    row.className = 'legend-row';
    if (item.color) {
      const line = document.createElement('span');
      line.className = 'legend-line';
      line.style.backgroundColor = item.color;
      row.appendChild(line);
    }
    const label = document.createElement('span');
    label.className = 'legend-label';
    label.textContent = item.label;
    row.appendChild(label);
    body.appendChild(row);
  }

  // 線幅スケール（交通量→太さ）
  if (legend.widthScale) {
    const sub = document.createElement('div');
    sub.className = 'legend-subheading';
    sub.textContent = legend.widthScale.heading;
    body.appendChild(sub);
    for (const w of legend.widthScale.items) {
      const row = document.createElement('div');
      row.className = 'legend-row';
      const line = document.createElement('span');
      line.className = 'legend-width-line';
      line.style.height = `${w.thickness}px`;
      row.appendChild(line);
      const label = document.createElement('span');
      label.className = 'legend-label';
      label.textContent = w.label;
      row.appendChild(label);
      body.appendChild(row);
    }
  }

  for (const note of legend.notes ?? []) {
    const n = document.createElement('div');
    n.className = 'legend-note';
    n.textContent = `※ ${note}`;
    body.appendChild(n);
  }

  panel.appendChild(body);
}
