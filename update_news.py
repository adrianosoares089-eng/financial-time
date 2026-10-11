#!/usr/bin/env python3
"""Recolhe títulos do Google News RSS, com fonte, data e link. Sem inventar conteúdo."""
import datetime,email.utils,json,pathlib,re,urllib.parse,urllib.request,xml.etree.ElementTree as ET
OUT=pathlib.Path('news.json')
queries=['mercados financeiros ações obrigações petróleo quando:2d','financial markets stocks bonds central banks when:2d']
items=[];seen=set();now=datetime.datetime.now(datetime.timezone.utc)
for query in queries:
    params=urllib.parse.urlencode({'q':query,'hl':'pt-PT','gl':'PT','ceid':'PT:pt-150'})
    url='https://news.google.com/rss/search?'+params
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 FinancialTimeNews/1.0'})
        with urllib.request.urlopen(req,timeout=20) as response: root=ET.fromstring(response.read())
        for entry in root.findall('./channel/item'):
            title=(entry.findtext('title') or '').strip();link=(entry.findtext('link') or '').strip()
            source_el=entry.find('source');source=(source_el.text or '').strip() if source_el is not None else 'Google News'
            pub=(entry.findtext('pubDate') or '').strip()
            try: date=email.utils.parsedate_to_datetime(pub).astimezone(datetime.timezone.utc)
            except (TypeError,ValueError):continue
            if not title or not link.startswith('https://') or now-date>datetime.timedelta(days=3):continue
            title=re.sub(r'\s+-\s+'+re.escape(source)+r'$', '', title, flags=re.I).strip()
            key=title.casefold()[:75]
            if key in seen:continue
            seen.add(key);items.append({'title':title,'source':source,'url':link,'published_at':date.isoformat().replace('+00:00','Z')})
    except Exception as exc: print('Feed indisponível:',exc)
items.sort(key=lambda n:n['published_at'],reverse=True)
if items:
    OUT.write_text(json.dumps({'updated_at':now.isoformat().replace('+00:00','Z'),'items':items[:8]},ensure_ascii=False,indent=2)+'\n')
    print('Notícias atualizadas:',len(items))
else:print('Nenhuma notícia recente; preservado o ficheiro anterior')
