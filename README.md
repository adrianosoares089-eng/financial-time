# Financial Time V17

Carrega todos os ficheiros e pastas na raiz do repositório GitHub Pages.

## Novas secções
- NEWS DESK alinhado com MARKET, com moldura própria abaixo da barra dourada.
- WEEKLY PERFORMANCE mais compacta, sem «DESEMPENHO SEMANAL», com setas verdes e vermelhas.
- GLOBAL MARKET CAP: gráfico circular preparado para dados reais verificados por continente.
- EARNINGS THIS WEEK: agenda preparada para empresas com resultados nesta semana.

**Importante:** os novos painéis mostram «A aguardar dados verificados» e «Agenda por atualizar» enquanto não houver informação real validada. Não são inventadas percentagens ou datas de resultados. Para alimentar os painéis, preencher `market-data.json` com `verified: true`, `regions: [{"name":"América do Norte","percent": ...}]`, `source`, `as_of`, e `earnings.companies: [{"name":"...","date":"..."}]`. A atualização automática existente aplica-se apenas às notícias, não a estes novos dados.

As cotações e desempenhos existentes continuam demonstrativos.
