import { YEARS, YEAR_ORDER, type YearId } from '../config/years.ts';
import { THEMES } from '../config/themes.ts';
import { iconCalendar, iconLayers, iconChevron, iconInfo, iconPhoto } from './icons.ts';

export interface ControlPanelOptions {
  el: HTMLElement;
  currentYear: YearId;
  currentThemeId: string;
  onYearChange: (id: YearId) => void;
  onThemeChange: (id: string) => void;
  /** 空中写真の不透明度（%）— パネルに統合したスライダー */
  opacity: { initialPct: number; onChange: (pct: number) => void };
}

/** パネル共通のヘッダ（タイトル・クレジット・折りたたみボタン）を生成 */
function buildHeader(panel: HTMLElement): HTMLElement {
  const header = document.createElement('div');
  header.className = 'panel-header';
  header.innerHTML = `
    <div class="title-group">
      <h1>道路交通センサスマップ</h1>
      <span class="credit">${iconInfo} 国土交通省 / PDL1.0</span>
    </div>
    <button class="collapse-btn" type="button" aria-label="パネルを折りたたむ">${iconChevron}</button>
  `;
  header.querySelector('.collapse-btn')!.addEventListener('click', () => {
    panel.classList.toggle('collapsed');
  });
  return header;
}

/** 年度セグメント + テーマセレクタ + 空中写真不透明度のコントロールパネルを描画 */
export function initControlPanel(opts: ControlPanelOptions): void {
  const { el } = opts;
  el.innerHTML = '';
  el.appendChild(buildHeader(el));

  const body = document.createElement('div');
  body.className = 'panel-body';

  // --- 年度セグメント ---
  const yearField = document.createElement('div');
  yearField.className = 'field';
  yearField.innerHTML = `<div class="field-label">${iconCalendar} 調査年度</div>`;

  const seg = document.createElement('div');
  seg.className = 'segmented';
  for (const id of YEAR_ORDER) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = YEARS[id].label;
    if (id === opts.currentYear) btn.classList.add('active');
    btn.addEventListener('click', () => {
      if (btn.classList.contains('active')) return;
      seg.querySelectorAll('button').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      opts.onYearChange(id);
    });
    seg.appendChild(btn);
  }
  yearField.appendChild(seg);
  body.appendChild(yearField);

  // --- テーマセレクタ ---
  const themeField = document.createElement('div');
  themeField.className = 'field';
  themeField.innerHTML = `<div class="field-label">${iconLayers} 表示する主題</div>`;

  const selectWrap = document.createElement('div');
  selectWrap.className = 'select-wrap';
  const select = document.createElement('select');
  for (const theme of THEMES) {
    const opt = document.createElement('option');
    opt.value = theme.id;
    opt.textContent = theme.label;
    if (theme.id === opts.currentThemeId) opt.selected = true;
    select.appendChild(opt);
  }
  select.addEventListener('change', () => opts.onThemeChange(select.value));
  selectWrap.appendChild(select);
  themeField.appendChild(selectWrap);
  body.appendChild(themeField);

  // --- 空中写真 不透明度（統合） ---
  const opField = document.createElement('div');
  opField.className = 'field';
  opField.innerHTML = `
    <div class="field-label">${iconPhoto} 空中写真<span class="op-value">${opts.opacity.initialPct}%</span></div>
  `;
  const slider = document.createElement('input');
  slider.type = 'range';
  slider.min = '0';
  slider.max = '100';
  slider.step = '1';
  slider.value = String(opts.opacity.initialPct);
  slider.setAttribute('aria-label', '空中写真の不透明度');
  const opValue = opField.querySelector('.op-value') as HTMLElement;
  slider.addEventListener('input', () => {
    const pct = parseInt(slider.value, 10);
    opValue.textContent = `${pct}%`;
    opts.opacity.onChange(pct);
  });
  opField.appendChild(slider);
  body.appendChild(opField);

  el.appendChild(body);
}
