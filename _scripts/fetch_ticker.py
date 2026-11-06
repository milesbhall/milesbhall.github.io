#!/usr/bin/env python3
"""Fetch commodity prices from FRED (Federal Reserve Bank of St. Louis) into _data/ticker.json.

The GitHub Action runs this before every build. With FRED_API_KEY set it uses the
official FRED API; without a key (e.g. on your own computer) it falls back to FRED's
public CSV download. If anything fails, the existing _data/ticker.json is left alone,
so the site still builds with the last prices it had.

To change what the ticker shows, edit SERIES below. Find series IDs on
https://fred.stlouisfed.org (the ID is the code in parentheses after a series title).
"""
import csv
import io
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone

# (label shown on the ticker, FRED series ID, format, unit text)
#   format "$2"  -> $99.64    "$3" -> $2.728    "$0" -> $14,473    "c1" -> 330.1¢
SERIES = [
    ("WTI CRUDE",   "DCOILWTICO",   "$2", "/bbl"),
    ("BRENT",       "DCOILBRENTEU", "$2", "/bbl"),
    ("NAT GAS",     "DHHNGSP",      "$2", "/MMBtu"),
    ("GASOLINE",    "DGASNYH",      "$3", "/gal"),
    ("HEATING OIL", "DHOILNYH",     "$3", "/gal"),
    ("COPPER",      "PCOPPUSDM",    "$0", "/t"),
    ("ALUMINUM",    "PALUMUSDM",    "$0", "/t"),
    ("NICKEL",      "PNICKUSDM",    "$0", "/t"),
    ("IRON ORE",    "PIORECRUSDM",  "$2", "/t"),
    ("WHEAT",       "PWHEAMTUSDM",  "$2", "/t"),
    ("CORN",        "PMAIZMTUSDM",  "$2", "/t"),
    ("SOYBEANS",    "PSOYBUSDM",    "$2", "/t"),
    ("COFFEE",      "PCOFFOTMUSDM", "c1", "/lb"),
    ("SUGAR",       "PSUGAISAUSDM", "c2", "/lb"),
    ("COTTON",      "PCOTTINDUSDM", "c2", "/lb"),
]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_data", "ticker.json")
USER_AGENT = "mileshall.com ticker (GitHub Actions)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def observations(series_id, key):
    """Return the two most recent (date, value) pairs, newest first."""
    if key:
        q = urllib.parse.urlencode({
            "series_id": series_id, "api_key": key, "file_type": "json",
            "sort_order": "desc", "limit": 20,
        })
        data = json.loads(get("https://api.stlouisfed.org/fred/series/observations?" + q))
        rows = [(o["date"], o["value"]) for o in data["observations"]]
    else:
        text = get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + series_id)
        rows = list(csv.reader(io.StringIO(text)))[1:][::-1]
    rows = [(d, float(v)) for d, v in rows if v not in (".", "")]
    if len(rows) < 2:
        raise ValueError(f"not enough observations for {series_id}")
    return rows[0], rows[1]


def fmt_price(value, style):
    kind, places = style[0], int(style[1])
    number = f"{value:,.{places}f}"
    return f"${number}" if kind == "$" else f"{number}¢"


def fmt_date(iso, monthly):
    d = date.fromisoformat(iso)
    return d.strftime("%b %Y") if monthly else f"{d.strftime('%b')} {d.day}"


def main():
    key = os.environ.get("FRED_API_KEY", "").strip()
    items = []
    for label, sid, style, unit in SERIES:
        (d_now, v_now), (d_prev, v_prev) = observations(sid, key)
        monthly = d_now.endswith("-01") and d_prev.endswith("-01")
        pct = (v_now - v_prev) / v_prev * 100 if v_prev else 0.0
        direction = "up" if pct > 0.005 else "down" if pct < -0.005 else "flat"
        sign = "+" if direction == "up" else "−" if direction == "down" else "±"
        items.append({
            "label": label,
            "series": sid,
            "price": fmt_price(v_now, style) + unit,
            "change": f"{sign}{abs(pct):.1f}%",
            "direction": direction,
            "as_of": fmt_date(d_now, monthly),
            "date": d_now,
        })
    out = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "via": "api" if key else "csv",
        "items": items,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {len(items)} prices to _data/ticker.json via {out['via']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # keep the old file so the site still builds
        print(f"ticker fetch failed, keeping existing _data/ticker.json: {e}", file=sys.stderr)
        sys.exit(1)
