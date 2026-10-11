# Financial Time V9

Versão baseada na V8 que já mostrou o painel «Mercados hoje» no iPad.

## Alterações
- Gráficos 180–205 px (dependendo do tamanho do ecrã), mantendo o início imediatamente a seguir à cotação.
- EUA, EUROPA e ÁSIA-PACÍFICO ligeiramente menores.
- Ícone FT anterior mantido.
- Painel de notícias mantido. As notícias são recolhidas de feeds externos, não inventadas; a atualização automática depende da configuração abaixo.

## Instalação no GitHub
Substitui os ficheiros na raiz do repositório `financial-time`. As pastas `scripts` e **`.github/workflows`** também têm de estar no repositório. O GitHub no iPad pode não mostrar pastas ocultas ao carregar ficheiros em massa. Se não aparecer `.github/workflows/update-news.yml`, cria esse caminho manualmente no GitHub através de **Add file → Create new file** com o nome `.github/workflows/update-news.yml` e cola o conteúdo fornecido no ZIP.

Para confirmar a atualização: no repositório, abre **Actions → Atualizar notícias financeiras → Run workflow**. Se o workflow não surgir, o ficheiro `.github/workflows/update-news.yml` não foi publicado. Se surgir mas falhar ao gravar, em **Settings → Actions → General → Workflow permissions** seleciona **Read and write permissions** (se permitido). A atualização está agendada três vezes por dia (UTC), mas os horários do GitHub Actions podem sofrer atrasos.

O `news.json` inicial é apenas um conjunto de notícias guardadas; sem workflow ativo não se atualiza automaticamente. As cotações e os rankings inferiores continuam **demonstrativos**.
