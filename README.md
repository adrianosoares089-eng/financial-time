# Financial Time V6 — Terminal Profissional

## Instalação no GitHub Pages

Descomprime o ZIP e coloca os ficheiros e pastas **na raiz** do repositório `financial-time`, incluindo `.github/workflows/update-news.yml`, `scripts/update_news.py` e `news.json`.

**Atenção:** no iPad, a pasta `.github` é oculta em algumas aplicações Ficheiros. Ativa a visualização de ficheiros ocultos ou carrega-a pelo GitHub em modo desktop. Sem esta pasta, a aplicação funciona com as notícias verificadas incluídas, mas **não se atualiza automaticamente**.

A atualização das notícias é feita por GitHub Actions às 07:15, 13:15 e 19:15 UTC, quando o GitHub permitir. No repositório: Settings → Actions → General → Workflow permissions → Read and write permissions, se necessário. No separador Actions podes executar manualmente "Atualizar notícias financeiras".

As notícias mostram a **data da última recolha**, e não são apresentadas como notícias novas quando a atualização falha. Os preços e as empresas nos cartões inferiores continuam demonstrativos. Não há API de cotações reais nesta versão.

No iPad, para atualizar o ícone: remove o atalho antigo e adiciona novamente pelo Safari. O nome permanece Financial Time; o desenho do ícone tem apenas FT.


V7: gráficos imediatamente a seguir às cotações, rótulos regionais maiores, ícone FT restaurado da V5. Painel de notícias preservado. Se o painel não aparecer, confirmar que index.html V7 foi publicado e limpar dados do site/atalho antigo no Safari.
