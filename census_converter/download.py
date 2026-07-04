"""ステップ1: GeoJSONタイルと箇所別基本表CSVのダウンロード（方式A）。

- GeoJSON: road_types × tileindex(z/x/y) を可視化ツールから取得。404はスキップ。
- 箇所別基本表CSV: 都道府県コードごとに取得。
サーバ負荷に配慮し、単一スレッド + request_sleep 間隔で取得する。
"""
from __future__ import annotations
import csv
import os
import time

import requests
from requests.exceptions import RequestException

from .config import Config, ensure_dirs


def _read_tileindex(path: str) -> list[tuple[str, str, str]]:
    """tileindex CSV（列順 x,y,z / ヘッダなし）を (z, x, y) で返す。"""
    tiles = []
    with open(path, newline="") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and row[0].strip().isdigit():
                tiles.append((row[2], row[0], row[1]))  # z, x, y
    return tiles


def _read_ken_codes(path: str) -> list[str]:
    codes = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r, None)  # ヘッダ
        for row in r:
            if row and row[0].strip():
                codes.append(row[0].strip())
    return codes


def download_geojson(cfg: Config, skip_existing: bool = True) -> dict[str, int]:
    """GeoJSONタイルを取得。返り値は集計（saved/skip/notfound/error）。"""
    ensure_dirs(cfg)
    tiles = _read_tileindex(cfg.tileindex)
    sess = requests.Session()
    stat = {"saved": 0, "skip": 0, "notfound": 0, "error": 0}
    total = len(cfg.road_types) * len(tiles)
    done = 0
    for rt in cfg.road_types:
        for (z, x, y) in tiles:
            done += 1
            fname = f"{rt}_{z}_{x}_{y}.geojson"
            dest = os.path.join(cfg.tiles_dir, fname)
            if skip_existing and os.path.exists(dest):
                stat["skip"] += 1
                continue
            url = f"{cfg.geojson_url_base}/{rt}/{z}/{x}/{y}.geojson"
            try:
                r = sess.get(url, timeout=cfg.request_timeout)
                time.sleep(cfg.request_sleep)
                if r.status_code == 200:
                    with open(dest, "wb") as w:
                        w.write(r.content)
                    stat["saved"] += 1
                elif r.status_code == 404:
                    stat["notfound"] += 1
                else:
                    stat["error"] += 1
            except RequestException:
                stat["error"] += 1
            if done % 2000 == 0:
                print(f"  geojson {done:,}/{total:,}  saved={stat['saved']:,} "
                      f"skip={stat['skip']:,} 404={stat['notfound']:,}", flush=True)
    print(f"[download_geojson] {stat}", flush=True)
    return stat


def download_kasho_csv(cfg: Config, skip_existing: bool = True) -> dict[str, int]:
    """箇所別基本表CSVを都道府県コードごとに取得。"""
    ensure_dirs(cfg)
    codes = _read_ken_codes(cfg.ken_code_list)
    sess = requests.Session()
    stat = {"saved": 0, "skip": 0, "error": 0}
    for code in codes:
        dest = os.path.join(cfg.kasho_dir, f"kasyo{code}.csv")
        if skip_existing and os.path.exists(dest):
            stat["skip"] += 1
            continue
        url = cfg.kasho_csv_url_template.format(ken=code)
        try:
            r = sess.get(url, timeout=cfg.request_timeout)
            time.sleep(cfg.request_sleep)
            if r.status_code == 200:
                with open(dest, "wb") as w:
                    w.write(r.content)
                stat["saved"] += 1
            else:
                stat["error"] += 1
                print(f"  警告: kasyo{code}.csv -> HTTP {r.status_code}", flush=True)
        except RequestException as e:
            stat["error"] += 1
            print(f"  警告: kasyo{code}.csv -> {e}", flush=True)
    print(f"[download_kasho_csv] {stat}", flush=True)
    return stat


def download_jikantai_csv(cfg: Config, skip_existing: bool = True) -> dict[str, int]:
    """時間帯別交通量表CSVを都道府県コードごとに取得（拡張・任意）。

    config に jikantai_csv_url_template が無ければ何もしない。DESIGN.md §8 参照。
    箇所別基本表(csv/)とはスキーマが異なるため、別ディレクトリ jikantai/ に保存する。
    """
    if not cfg.jikantai_csv_url_template:
        return {"saved": 0, "skip": 0, "error": 0}
    ensure_dirs(cfg)
    codes = _read_ken_codes(cfg.ken_code_list)
    sess = requests.Session()
    stat = {"saved": 0, "skip": 0, "error": 0}
    for code in codes:
        dest = os.path.join(cfg.jikantai_dir, f"zkntrf{code}.csv")
        if skip_existing and os.path.exists(dest) and os.path.getsize(dest) > 0:
            stat["skip"] += 1
            continue
        url = cfg.jikantai_csv_url_template.format(ken=code)
        try:
            r = sess.get(url, timeout=cfg.request_timeout)
            time.sleep(cfg.request_sleep)
            if r.status_code == 200:
                with open(dest, "wb") as w:
                    w.write(r.content)
                stat["saved"] += 1
            else:
                stat["error"] += 1
                print(f"  警告: zkntrf{code}.csv -> HTTP {r.status_code}", flush=True)
        except RequestException as e:
            stat["error"] += 1
            print(f"  警告: zkntrf{code}.csv -> {e}", flush=True)
    print(f"[download_jikantai_csv] {stat}", flush=True)
    return stat


def run(cfg: Config) -> None:
    download_geojson(cfg)
    download_kasho_csv(cfg)
    download_jikantai_csv(cfg)
