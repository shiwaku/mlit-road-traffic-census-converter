import type { Theme } from '../themes/types.ts';
import { traffic24h } from '../themes/traffic24h.ts';
import { konzatsudo } from '../themes/konzatsudo.ts';
import { ogatasha } from '../themes/ogatasha.ts';
import { konzatsuji, hikonzatsuji } from '../themes/speed.ts';

/** テーマ登録（セレクタの並び順） */
export const THEMES: Theme[] = [traffic24h, konzatsudo, ogatasha, konzatsuji, hikonzatsuji];

export const THEME_BY_ID: Record<string, Theme> = Object.fromEntries(
  THEMES.map((t) => [t.id, t]),
);

export const DEFAULT_THEME_ID = traffic24h.id;
