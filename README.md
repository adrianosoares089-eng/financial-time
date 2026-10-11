# Financial Time V20 — gráficos intradiários

Mantém o design da V19. **IWDA.AS, SWRD.AS, SPYL.SW**: gráfico de 5 minutos da última sessão de bolsa (incluindo a sessão em curso); percentagem relativa ao último preço disponível da sessão anterior. **QNT-USD**: gráfico de 5 minutos do dia civil corrente, das 00:00 às 24:00 em **Europe/Lisbon**, incluindo mudanças de horário de verão; percentagem desde a primeira amostra disponível após as 00:00.

## Instalação

Substitui todos os ficheiros no repositório GitHub Pages, **incluindo** `.github/workflows/update-quotes.yml` e `scripts/update_quotes.py`. Ativa as permissões de escrita para GitHub Actions (Settings → Actions → General → Workflow permissions → Read and write permissions) e executa **Actions → Atualizar cotações de mercado → Run workflow**. Verifica `market-quotes.json`. Abre o site com `?v=20`.

## Limitações

Fonte Yahoo Finance não oficial, sujeita a falhas, limitações e atrasos. O GitHub Actions é solicitado a cada 15 minutos, **não garante pontualidade**. Gráficos de 5 minutos dependem da disponibilidade dos dados na fonte. O valor do QNT às 00:00 é aproximado pela primeira amostra disponível depois da meia-noite; não é uma cotação oficial de abertura. Na ausência de amostras do novo dia, QNT mostra indisponível até nova recolha; se a fonte falhar, os ETFs podem mostrar dados antigos, identificáveis pela hora de recolha. Sem streaming nem atualização ao minuto. Outros painéis continuam com dados demonstrativos ou aguardam dados reais.
