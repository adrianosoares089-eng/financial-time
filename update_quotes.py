#!/usr/bin/env python3
"""Intraday Yahoo chart snapshots: ETFs current/last exchange session, QNT Lisbon calendar day.
Data can be delayed or unavailable. Preserve last VERIFIED snapshot on transient errors.
"""
import datetime as dt
import json
import pathlib
import time
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'market-quotes.json'
SYMBOLS = ('IWDA.AS', 'SWRD.AS', 'SPYL.SW', 'QNT-USD')
LISBON = ZoneInfo('Europe/Lisbon')
UTC = dt.timezone.utc
now = dt.datetime.now(UTC)
try:
    previous = json.loads(OUT.read_text(encoding='utf-8'))
except (OSError, ValueError):
    previous = {}
quotes = dict(previous.get('quotes') or {})
errors = {}

def fetch(symbol, interval='5m', period='5d'):
    args = urllib.parse.urlencode({'range': period, 'interval': interval, 'includePrePost': 'false'})
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + urllib.parse.quote(symbol, safe='') + '?' + args
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=25) as response:
        payload = json.load(response)
    result = payload['chart']['result'][0]
    timestamps = result.get('timestamp') or []
    closes = result['indicators']['quote'][0]['close']
    points = [(dt.datetime.fromtimestamp(ts, UTC), float(v)) for ts, v in zip(timestamps, closes) if isinstance(v, (int, float)) and v > 0]
    return result['meta'], points

def date_key(t, timezone):
    return t.astimezone(timezone).date().isoformat()

for symbol in SYMBOLS:
    try:
        meta, points = fetch(symbol)
        if not points:
            raise ValueError('No intraday samples')
        crypto = symbol == 'QNT-USD'
        zone = LISBON if crypto else ZoneInfo(meta.get('exchangeTimezoneName') or 'Europe/Amsterdam')
        if crypto:
            # Lisbon midnight is the boundary, including DST changes; do not display yesterday's line.
            session = date_key(now, LISBON)
            day_points = [(t, v) for t, v in points if date_key(t, LISBON) == session]
            if not day_points:
                raise ValueError('No samples for current Lisbon day')
            # Previous day's last available 5-minute quote is a fallback only when no
            # sample at exactly midnight; compare to first sample of current day.
            baseline = day_points[0][1]
        else:
            # Outside trading hours retain the last available completed exchange session.
            session = date_key(points[-1][0], zone)
            day_points = [(t, v) for t, v in points if date_key(t, zone) == session]
            previous_points = [(t, v) for t, v in points if date_key(t, zone) < session]
            baseline = previous_points[-1][1] if previous_points else None
        if not day_points or baseline is None or baseline <= 0:
            raise ValueError('Insufficient reference data')
        price = day_points[-1][1]
        currency = meta.get('currency') or ('USD' if crypto else 'EUR')
        if currency not in ('EUR', 'USD', 'GBP', 'CHF'):
            raise ValueError('Unexpected currency: ' + str(currency))
        quotes[symbol] = {
            'price': round(price, 6),
            'change_percent': round((price / baseline - 1) * 100, 4),
            'currency': currency,
            'history': [round(v, 6) for _, v in day_points],
            'history_timestamps': [t.isoformat() for t, _ in day_points],
            'session_date': session,
            'session_timezone': str(zone),
            'period_label': '00H–24H · LISBOA' if crypto else 'SESSÃO',
            'as_of': day_points[-1][0].isoformat(),
            'source': 'Yahoo Finance chart (unofficial; may be delayed)',
        }
    except Exception as exc:
        errors[symbol] = str(exc)[:160]
    time.sleep(1)

# Never overwrite verified data with invented or empty observations.
if len(errors) < len(SYMBOLS):
    OUT.write_text(json.dumps({
        'updated_at': now.isoformat(), 'quotes': quotes, 'errors': errors,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Updated', len(SYMBOLS) - len(errors), 'symbols; errors:', errors)
