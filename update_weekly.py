import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from io import StringIO

import pandas as pd
import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "weekly-performance.json"

SOURCES = [
    {
        "name": "S&P 500",
        "region": "EUA",
        "kind": "csv",
        "url": "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv",
        "symbol_col": "Symbol",
        "name_col": "Security",
    },
    {
        "name": "EURO STOXX 50",
        "region": "EUROPA",
        "kind": "euro",
        "url": "https://en.wikipedia.org/wiki/EURO_STOXX_50",
        "symbol_col": "Ticker",
        "name_col": "Name",
    },
    {
        "name": "ASIAN TITANS 50",
        "region": "ÁSIA-PACÍFICO",
        "kind": "local",
        "path": ROOT / "asian-titans-50.csv",
        "symbol_col": "Symbol",
        "name_col": "Name",
    },
]


def get_companies(source):
    if source["kind"] == "local":
        return pd.read_csv(source["path"])

    if source["kind"] == "csv":
        return pd.read_csv(source["url"])

    response = requests.get(
        source["url"],
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=25,
    )
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    matches = [
        table for table in tables
        if "Ticker" in table.columns and "Name" in table.columns
        and 45 <= len(table) <= 55
    ]
    if not matches:
        raise ValueError("Tabela EURO STOXX 50 não encontrada")
    return matches[0]


def calculate_market(source, base_date, end_date):
    companies = get_companies(source)

    symbol_col = source["symbol_col"]
    name_col = source["name_col"]

    companies = companies.dropna(subset=[symbol_col, name_col]).copy()
    companies[symbol_col] = companies[symbol_col].astype(str).str.replace(
        ".", "-", regex=False
    ) if source["kind"] == "csv" else companies[symbol_col].astype(str)

    symbols = companies[symbol_col].tolist()

    print(f'{source["name"]}: a consultar {len(symbols)} empresas...', flush=True)

    results = []

    for offset in range(0, len(symbols), 50):
        batch = symbols[offset:offset + 50]

        data = yf.download(
            batch,
            start=(base_date - timedelta(days=5)).isoformat(),
            end=(end_date + timedelta(days=1)).isoformat(),
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=True,
        )

        if data.empty:
            continue

        closes = data["Close"]

        for _, company in companies.iloc[offset:offset + 50].iterrows():
            symbol = company[symbol_col]

            try:
                series = closes[symbol].dropna()
                series.index = pd.to_datetime(series.index).tz_localize(None)

                baseline = series[series.index.date <= base_date]
                current = series[series.index.date <= end_date]

                if baseline.empty or current.empty:
                    continue

                base = float(baseline.iloc[-1])
                last = float(current.iloc[-1])

                if base <= 0:
                    continue

                results.append({
                    "name": str(company[name_col]),
                    "ticker": symbol,
                    "pct": round((last / base - 1) * 100, 2),
                })

            except (KeyError, ValueError, TypeError, IndexError):
                continue

    if len(results) < len(symbols) * 0.95:
        raise ValueError(
            f"Cobertura insuficiente: {len(results)}/{len(symbols)}"
        )

    ordered = sorted(results, key=lambda item: item["pct"], reverse=True)

    print(
        f'{source["name"]}: {len(results)}/{len(symbols)} | '
        f'+ {ordered[0]["name"]} {ordered[0]["pct"]}% | '
        f'- {ordered[-1]["name"]} {ordered[-1]["pct"]}%',
        flush=True,
    )

    return {
        "name": source["name"],
        "region": source["region"],
        "up": ordered[0],
        "down": ordered[-1],
        "coverage": len(results),
        "total": len(symbols),
    }


def main():
    today = datetime.now(timezone.utc).date()

    # Segunda-feira -> sexta-feira anterior.
    # Terça a sexta -> sexta-feira anterior.
    # Fim de semana -> sexta-feira anterior.
    days_since_friday = (today.weekday() - 4) % 7
    if days_since_friday == 0:
        days_since_friday = 7

    base_date = today - timedelta(days=days_since_friday)

    # Usar o último dia concluído, evitando misturar
    # cotações intradiárias com fechos históricos.
    end_date = today + timedelta(days=1)

    print(f"Período: {base_date} até {end_date}", flush=True)

    markets = [
        calculate_market(source, base_date, end_date)
        for source in SOURCES
    ]

    payload = {
        "calculation_date": today.isoformat(),
        "base_date": base_date.isoformat(),
        "end_date": end_date.isoformat(),
        "markets": markets,
    }

    temporary = OUT.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(OUT)

    print("Weekly Performance atualizada com sucesso.")


if __name__ == "__main__":
    main()
