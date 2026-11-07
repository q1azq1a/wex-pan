#!/usr/bin/env python3
"""Fetch the Wex TVBox source config, keep only the netdisk (pan) sites,
strip decorative emoji/icons from site names, drop the top-level `lives`
array, and write newwex-pan.json. Used by the daily GitHub Actions job
and for local runs. Fails (non-zero exit) if the result looks wrong, so a
broken source never gets committed."""
import json
import sys
import time
import unicodedata
import urllib.request

SOURCE = "https://9280.kstore.vip/newwex.json"
OUTPUT = "newwex-pan.json"

KEEP_KEYS = {
    "Douban", "Doubanaaaa", "Wexconfig", "MyPan",
    "花卷", "玩偶", "AiNewGuanYing", "AiQwMkv", "AiNewPianKu", "AiNewHuBan",
    "AiNewMuOu", "AiNewDuoDuo", "AiNewKuaiYing", "AiNewLaBi", "AiNewShanDian",
    "AiNewJuTou", "AiNewLibvio", "原盘", "蜗牛", "AiPan1Me", "AiNewYiDong4K",
    "FakeAi115Share", "AList", "webdav",
    "SoAiHaiYin", "SoAiPanSoo", "SoAiAiPanSo", "SoKaKa", "SoAiQuanPanGuard",
    "push_agent",
}


def clean_name(name: str) -> str:
    """Remove emoji/icon characters (and joiner/variation selectors) from a
    display name, keeping the text itself (incl. 【】 and ┃ separators)."""
    if not isinstance(name, str):
        return name
    out = []
    for ch in name:
        if ch in ("‍", "️", "​"):
            continue
        if "\u2500" <= ch <= "\u257f":
            out.append(ch)  # keep box-drawing separators such as ┃
            continue
        if unicodedata.category(ch) in ("So", "Sk"):
            continue
        out.append(ch)
    return "".join(out).strip()


def main() -> int:
    raw = None
    last_err = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(SOURCE, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
            break
        except Exception as e:  # source is occasionally flaky; retry with backoff
            last_err = e
            if attempt < 3:
                time.sleep(3 * (attempt + 1))
    if raw is None:
        print(f"ERROR: fetching source failed: {last_err}", file=sys.stderr)
        return 1
    cfg = json.loads(raw)

    sites = cfg.get("sites")
    if not isinstance(sites, list):
        print("ERROR: source has no sites list", file=sys.stderr)
        return 1

    kept = []
    for s in sites:
        if s.get("key") in KEEP_KEYS:
            s = dict(s)
            if "name" in s:
                s["name"] = clean_name(s["name"])
            kept.append(s)

    if len(kept) < 25:
        print(f"ERROR: only {len(kept)} sites kept, source structure may have changed",
              file=sys.stderr)
        return 1

    cfg["sites"] = kept
    cfg.pop("lives", None)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)
        f.write("\n")

    print(f"OK: kept {len(kept)} sites, dropped lives, names cleaned")
    for s in kept:
        print(" -", s.get("key"), "|", s.get("name"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
