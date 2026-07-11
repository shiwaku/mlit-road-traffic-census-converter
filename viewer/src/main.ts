import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { Protocol } from 'pmtiles';
import './style.css';

import { createMap } from './map/createMap.ts';
import { addAerialPhoto, SEAMLESSPHOTO_LAYER, DEFAULT_AERIAL_OPACITY } from './map/basemap.ts';
import { addCensusSources } from './map/sources.ts';
import { renderTheme } from './map/renderTheme.ts';
import { initControlPanel } from './ui/controlPanel.ts';
import { renderLegend } from './ui/legend.ts';
import { initPopup } from './ui/popup.ts';
import { YEARS, DEFAULT_YEAR, type YearId } from './config/years.ts';
import { THEME_BY_ID, DEFAULT_THEME_ID } from './config/themes.ts';

// PMTiles プロトコルを登録（map 生成前）
const protocol = new Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

// アプリ状態
let currentYear: YearId = DEFAULT_YEAR;
let currentThemeId = DEFAULT_THEME_ID;

const map = createMap('map');

function apply(): void {
  renderTheme(map, YEARS[currentYear], THEME_BY_ID[currentThemeId]);
  renderLegend(document.getElementById('legend')!, THEME_BY_ID[currentThemeId]);
}

map.on('load', () => {
  addAerialPhoto(map);
  addCensusSources(map);
  apply();

  initControlPanel({
    el: document.getElementById('control-panel')!,
    currentYear,
    currentThemeId,
    onYearChange: (id) => {
      currentYear = id;
      apply();
    },
    onThemeChange: (id) => {
      currentThemeId = id;
      apply();
    },
    opacity: {
      initialPct: Math.round(DEFAULT_AERIAL_OPACITY * 100),
      onChange: (pct) => {
        if (map.getLayer(SEAMLESSPHOTO_LAYER)) {
          map.setPaintProperty(SEAMLESSPHOTO_LAYER, 'raster-opacity', pct / 100);
        }
      },
    },
  });

  initPopup(map, () => YEARS[currentYear]);
});
