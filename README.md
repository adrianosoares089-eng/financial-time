# Financial Time — primeira versão

Dashboard estático para iPad horizontal, sem bibliotecas ou serviços pagos.

## Publicar no GitHub Pages

1. Criar um repositório público no GitHub (por exemplo, `financial-time`).
2. Carregar os ficheiros **dentro** desta pasta para a raiz do repositório (index.html, style.css, app.js, etc.).
3. Ir a **Settings → Pages → Build and deployment → Deploy from a branch**.
4. Escolher a branch `main`, pasta `/(root)` e guardar.
5. Abrir o endereço publicado no Safari do iPad. Usar **Partilhar → Adicionar ao ecrã principal**.

## Estado atual

- Quatro ativos, gráficos ilustrativos e três painéis de índices.
- Três relógios mundiais em tempo real.
- Indicadores de sessão: indisponíveis até integrar calendários bolsistas fiáveis.
- Dados de mercado, empresas e percentagens são **fictícios** e servem apenas para validar a interface.
- Não existem ainda cotações reais, rankings de constituintes ou notícias.
- O painel principal é desenhado para iPad horizontal; as janelas de detalhe podem abrir por cima.

## Alterações futuras

Integrar API de mercado e backend para guardar credenciais e obter calendários, constituintes oficiais e notícias verificáveis.
