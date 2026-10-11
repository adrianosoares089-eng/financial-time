# Financial Time V8

Substituir **todos os ficheiros na raiz do repositório**, especialmente `index.html`, `app.js` e `style.css`. Carregar também `news.json`, a pasta `scripts` e a pasta oculta `.github`.

A V8 aproxima o início dos gráficos da cotação (bloco de 108–116 px), reduz ligeiramente os rótulos EUA/EUROPA/ÁSIA-PACÍFICO e mantém o ícone da V5/V7. Inclui uma rotina de recuperação do painel de notícias caso o template anterior ainda esteja presente.

**Se o painel de notícias continuar completamente ausente**, abrir o código-fonte publicado e confirmar que aparece a expressão `Mercados hoje`; a ausência do título indica que `index.html` não foi atualizado ou está em cache. Testar no Safari numa aba privada e, se necessário, limpar os dados do site.

O `news.json` tem de estar publicado no mesmo diretório da página. As notícias têm data de recolha; as cotações e rankings inferiores continuam demonstrativos.
