#!/usr/bin/env python3
import datetime
import email.utils
import json
import pathlib
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OUT = pathlib.Path(__file__).resolve().parent / "news.json"
NOW = datetime.datetime.now(datetime.timezone.utc)

QUERIES = [
    "stock markets economy when:2d",
    "financial markets earnings stocks when:2d",
    "mercados financeiros bolsas economia when:2d",
]

items = []
seen = set()

for query in QUERIES:
    params = urllib.parse.urlencode({
        "q": query,
        "hl": "pt-PT",
        "gl": "PT",
        "ceid": "PT:pt"
    })
    url = "https://news.google.com/rss/search?" + params

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            root = ET.fromstring(response.read())

        for entry in root.findall("./channel/item"):
            title = (entry.findtext("title") or "").strip()
            link = (entry.findtext("link") or "").strip()
            source = (entry.findtext("source") or "Google News").strip()
            published = (entry.findtext("pubDate") or "").strip()

            if not title or not link.startswith("https://"):
                continue

            try:
                date = email.utils.parsedate_to_datetime(
                    published
                ).astimezone(datetime.timezone.utc)
            except (TypeError, ValueError):
                continue

            if not (
                NOW - datetime.timedelta(days=3)
                <= date
                <= NOW + datetime.timedelta(minutes=15)
            ):
                continue

            title = re.sub(
                r"\s+-\s+" + re.escape(source) + r"$",
                "",
                title,
                flags=re.I
            ).strip()

            key = title.casefold()[:75]
            if key in seen:
                continue

            seen.add(key)

            items.append({
                "title": title,
                "source": source,
                "url": link,
                "published_at": date.isoformat().replace("+00:00", "Z")
            })

    except Exception as exc:
        print("Erro na pesquisa:", query, exc)

items.sort(key=lambda n: n["published_at"], reverse=True)

if items:
    data = {
        "updated_at": NOW.isoformat().replace("+00:00", "Z"),
        "items": items[:5]
    }
    OUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print("Notícias atualizadas:", len(data["items"]))
    for item in data["items"]:
        print("-", item["source"], "|", item["title"])
else:
    print("Nenhuma notícia recente; ficheiro anterior preservado.")
