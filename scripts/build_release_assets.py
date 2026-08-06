# -*- coding: utf-8 -*-
"""GitHub Releases に添付する成果物一式と SHA256SUMS.txt をまとめて用意する。

`run.py --step all` で `data/{r03,h27}/output/` に成果物が揃っている状態から実行する。
リリース作業（アセットの組み立て・ハッシュ計算・アップロードコマンド）を手作業から外すのが目的。

生成するもの（`--dest`、既定 `dist/release/`）:

  <prefix>_qgis.zip          GeoParquet同梱のQGIS一式（generate_qgis_bundle.pack を呼ぶ）
  <prefix>_jikantai.tar.gz   時間帯別交通量JSON。展開すると jikantai/<year>/{01..47,index}.json
  SHA256SUMS.txt             全アセット（下記の「参照するもの」も含む）のハッシュ

参照するもの（巨大なのでコピーせず、置いてある場所のまま `gh release upload` に渡す）:

  data/<year>/output/<prefix>_converted.parquet     GeoParquet 単体
  data/<year>/output/<prefix>_converted.pmtiles     PMTiles
  configs/qgis_styles/bundle/<prefix>_converted.qml サイドカーQML

**SHA256SUMS.txt は「全アセットを一括でアップロードする」前提で全件を書く。**
一部だけ差し替える運用では、公開中の他アセットのハッシュと食い違うので使わないこと
（その場合は公開中の SHA256SUMS.txt の該当行だけを差し替える）。

tar.gz は mtime/uid/gid/gzipヘッダを固定して再現ビルドにしてある（zipは ZIP_EPOCH で同様）。
そのため同じ入力からは毎回同じハッシュになる。ただし **data-v1 で公開中の
`*_jikantai.tar.gz` は本スクリプト導入前に手作業で作ったものなので、
中身は同じでもバイト列（＝ハッシュ）は一致しない。**

使い方:
    python scripts/build_release_assets.py
    python scripts/build_release_assets.py --dest /tmp/dist --tag data-v2
"""
import argparse
import gzip
import hashlib
import os
import sys
import tarfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QGIS_STYLES_DIR = os.path.join(REPO_ROOT, "configs", "qgis_styles")
sys.path.insert(0, QGIS_STYLES_DIR)

import generate_qgis_bundle as qb  # noqa: E402  (sys.path を通したあとに読む)
from generate_qml import YEARS  # noqa: E402

# 同じ入力から同じバイト列を出すための固定値（zip側は generate_qgis_bundle.ZIP_EPOCH）。
TAR_EPOCH = 0


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_jikantai_tar(dest_dir: str, year: str, prefix: str) -> str:
    """時間帯別JSONを tar.gz にまとめる。展開後の構造は jikantai/<year>/<file>。

    自前ホストするときにWebルートへそのまま展開できるよう、年度フォルダを1段挟む
    （リリースの2年度分を同じ場所に展開しても衝突しない）。
    """
    src = os.path.join(REPO_ROOT, "data", year, "output", "jikantai")
    names = sorted(os.listdir(src))
    out = os.path.join(dest_dir, f"{prefix}_jikantai.tar.gz")
    # gzip の mtime も固定する（GzipFile 既定は現在時刻で、中身が同じでもハッシュが変わる）
    with open(out, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", compresslevel=9,
                           fileobj=raw, mtime=TAR_EPOCH) as gz:
            with tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as t:
                for name in names:
                    path = os.path.join(src, name)
                    ti = tarfile.TarInfo(f"jikantai/{year}/{name}")
                    ti.size = os.path.getsize(path)
                    ti.mtime = TAR_EPOCH
                    ti.mode = 0o644
                    ti.uid = ti.gid = 0
                    ti.uname = ti.gname = ""
                    with open(path, "rb") as f:
                        t.addfile(ti, f)
    print(f"生成: {out} ({os.path.getsize(out):,} bytes / {len(names)} files)")
    return out


def collect(dest_dir: str) -> list:
    """アップロード対象を「リリースノートに載せる順」で返す: [(表示名, 実パス), ...]"""
    assets = []
    for kind in ("qgis.zip", "jikantai.tar.gz", "parquet", "pmtiles", "qml"):
        for year, ycfg in YEARS.items():
            pre = ycfg["prefix"]
            out = os.path.join(REPO_ROOT, "data", year, "output")
            if kind == "qgis.zip":
                assets.append((f"{pre}_qgis.zip", os.path.join(dest_dir, f"{pre}_qgis.zip")))
            elif kind == "jikantai.tar.gz":
                assets.append((f"{pre}_jikantai.tar.gz",
                               os.path.join(dest_dir, f"{pre}_jikantai.tar.gz")))
            elif kind == "qml":
                assets.append((f"{pre}_converted.qml",
                               os.path.join(qb.BUNDLE_DIR, f"{pre}_converted.qml")))
            else:
                assets.append((f"{pre}_converted.{kind}",
                               os.path.join(out, f"{pre}_converted.{kind}")))
    return assets


def require_inputs() -> None:
    """成果物が揃っているか先に確かめる（途中まで作って失敗するのを避ける）。"""
    missing = []
    for year, ycfg in YEARS.items():
        pre = ycfg["prefix"]
        out = os.path.join(REPO_ROOT, "data", year, "output")
        for rel in (f"{pre}_converted.parquet", f"{pre}_converted.pmtiles", "jikantai"):
            p = os.path.join(out, rel)
            if not os.path.exists(p):
                missing.append((year, p))
        qml = os.path.join(qb.BUNDLE_DIR, f"{pre}_converted.qml")
        if not os.path.isfile(qml):
            missing.append((year, qml))
    if missing:
        raise SystemExit(
            "リリースに必要な成果物が足りません:\n"
            + "\n".join(f"  {p}" for _y, p in missing)
            + "\n\n先に生成してください:\n"
            + "".join(f"  python run.py --year {y} --step all\n" for y in sorted(YEARS))
            + "  python configs/qgis_styles/generate_qgis_bundle.py\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="リリース添付用の成果物一式とSHA256SUMS.txtを用意する")
    ap.add_argument("--dest", default=os.path.join(REPO_ROOT, "dist", "release"),
                    help="生成物の出力先（既定: dist/release）")
    ap.add_argument("--tag", default="data-v1", help="表示する gh release upload のタグ名")
    args = ap.parse_args()

    require_inputs()
    os.makedirs(args.dest, exist_ok=True)

    # 1) QGIS一式（GeoParquet同梱）。pack() 側で parquet の存在チェックも走る
    qb.pack(args.dest, qb.build_all())
    # 2) 時間帯別JSON
    for year, ycfg in YEARS.items():
        build_jikantai_tar(args.dest, year, ycfg["prefix"])

    # 3) SHA256SUMS.txt（全アセット）
    assets = collect(args.dest)
    lines = []
    print()
    for name, path in assets:
        digest = sha256_of(path)
        lines.append(f"{digest}  {name}")
        print(f"{digest}  {name}  ({os.path.getsize(path):,} bytes)")
    sums = os.path.join(args.dest, "SHA256SUMS.txt")
    with open(sums, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n生成: {sums}")

    print("\n--- アップロード（内容を確認してから実行してください）---")
    paths = " \\\n  ".join(f'"{p}"' for _n, p in assets) + f' \\\n  "{sums}"'
    print(f"gh release upload {args.tag} --clobber \\\n  {paths}")
    print("\n注意: SHA256SUMS.txt は全アセットを一括アップロードする前提で全件を書いています。"
          "\n      一部だけ差し替える場合は、公開中の SHA256SUMS.txt の該当行のみを直してください。")


if __name__ == "__main__":
    main()
