# Orientações para agentes — 3V, evolução da LG Representações

Este arquivo orienta análises e mudanças neste projeto. O site é um frontend próprio, estático, em HTML, CSS e JavaScript; `dist/` é a cópia de publicação. Antes de propor uma mudança, leia o código e a versão visual atual. Preserve alterações locais já existentes.

## Projetos separados — decisão do cliente em 09/10/2026

- Este projeto é o site atual da **LG Representações**, com sua identidade azul e amarela, contatos e portfólio. Preserve a marca LG e os refinamentos existentes.
- A **3V — Venda, Valor e Vínculo** está em `../3v-site/`, com identidade verde e branca e mascote. O lançamento está previsto para **maio de 2027**, sem dia definido.
- Não substitua novamente a LG por 3V neste projeto. Cada projeto possui seus próprios arquivos, geradores, testes e `dist/`.
- Não publique a 3V nem migre o domínio ou a configuração de hospedagem da LG como consequência de uma edição local.
- Os geradores editoriais da LG trabalham em `content/home.html` e `content/representadas.html`; `scripts/render_pages.py` compõe as páginas finais; os da 3V trabalham em `conteudos/index.html`.

## Contexto e objetivo

- A LG Representações, fundada por Luiz Gustavo Soares Guimarães, atua há mais de 23 anos no mercado de materiais de construção em Pernambuco.
- O público inclui varejistas, atacadistas, distribuidores, fabricantes que buscam representação e pessoas que querem conhecer a empresa.
- O site deve apresentar a LG, suas nove representadas, novidades com fonte verificável, catálogos e caminhos claros para contato por WhatsApp ou e-mail.
- As representadas informadas pelo cliente são Atlas, Dryko, Amatools, Mundial Prime, Lamesa, Odem, Saga Metais, Botafogo e J. Lobato. Confirme qualquer alteração do portfólio antes de publicá-la.
- A linguagem deve ser profissional, clara e acolhedora; a apresentação deve transmitir confiança sem promessas ou números não comprovados.

## Pesquisa de referências e tendências

Quando a tarefa envolver direção visual, tipografia, conteúdo ou experiência do usuário:

Use a skill local [`design-taste-frontend`](.agents/skills/design-taste-frontend/SKILL.md) como apoio ao diagnóstico de hierarquia, ritmo e densidade. Aplique seus critérios ao contexto da LG; não migre a tecnologia do site nem adote regras estéticas que prejudiquem a identidade da marca ou a acessibilidade.

### Método de análise crítica

- Não prometa analisar **todos** os sites ou tendências do mercado. Defina uma amostra representativa para a decisão em pauta: ao menos duas representações comerciais de materiais de construção, uma referência de Pernambuco ou do Nordeste, uma referência B2B com operação comparável e, quando necessário, um site oficial de cada representada envolvida. Amplie a amostra se surgir um padrão contraditório; registre o limite da pesquisa.
- Antes de pesquisar, formule a pergunta concreta do visitante que a mudança pretende responder (por exemplo: “Que marcas a LG representa?”, “Há catálogo desta linha?” ou “Com quem falo?”). Não comece por efeitos visuais ou componentes da moda.
- Para cada site, registre URL, data da consulta, público-alvo aparente, evidência observável, facilidade de chegar à informação procurada, ponto forte, ponto fraco e o que **não** foi possível verificar. Leitura de texto não comprova aparência, animação, desempenho ou acessibilidade: confira esses aspectos em navegador antes de afirmá-los.
- Compare o padrão com a página atual da LG, em desktop e celular, sempre que a prévia estiver acessível. Se a inspeção visual estiver bloqueada, faça apenas a análise documental e marque a revisão visual como pendente; não contorne uma restrição do navegador.
- Avalie cada ideia em cinco critérios: **utilidade comercial**, **clareza e acessibilidade**, **fidelidade à LG e às marcas**, **desempenho e manutenção**, **evidência e direitos de uso**. Classifique como **adotar**, **adaptar**, **testar** ou **rejeitar** e explique o motivo. Rejeite uma tendência popular se ela esconder contato/catálogos, criar movimento cansativo, exigir conteúdo inexistente ou aumentar manutenção sem benefício demonstrável.
- Entregue um registro curto em `docs/` com tabela “referência → observação → problema que resolve → decisão para a LG”, fontes e data. Separe fatos do site, inferências suas e recomendações. Recomendações não são autorização para trocar o design ou publicar; implemente apenas o que foi solicitado ou aprovado.

1. Consulte a versão atual do site da LG e pesquise referências **atuais** de representação comercial, distribuição B2B, indústria e vendas consultivas. Use primeiro os sites oficiais e registre URL e data da consulta. Inclua, quando pertinentes, [Régis Representações](https://www.regisrepresentacoes.com.br/), [BR Representações](https://www.brrepresentacoes.com.br/home) e os sites oficiais das representadas. Amplie a amostra com referências independentes quando elas acrescentarem um padrão útil; não trate esses dois sites como o universo do setor.
2. Observe hierarquia da primeira tela, navegação, exposição das marcas, prova de credibilidade, CTAs, tipografia, ritmo das seções, comportamento mobile, acessibilidade, velocidade e uso de animações. Separe fatos observados de preferências estéticas e de inferências.
3. Para cada tendência ou referência, responda: **qual problema do visitante ela resolve?** Ela facilita conhecer a LG, comparar marcas ou entrar em contato? Funciona no celular, com teclado e com movimento reduzido? Cabe na identidade azul/amarelo da LG e no orçamento de manutenção? Exige conteúdo que a LG realmente possui?
4. Classifique cada ideia como **adotar**, **adaptar**, **testar** ou **rejeitar**, com uma justificativa curta. Popularidade, novidade ou presença num concorrente não bastam. Evite copiar composição, texto, animação ou material protegido de outro site.
5. Priorize uma proposta pequena e verificável por vez. Mostre a prévia completa ao cliente antes de avançar para outra direção visual ou publicar.

As fontes de produtos, lançamentos, fotos e vídeos das representadas devem ser verificadas nos canais oficiais. Não chame um item de lançamento apenas porque foi encontrado recentemente, nem confunda a data de consulta com a data de publicação. Não invente cases, avaliações, resultados ou depoimentos.

## Canva e sistema visual

O plugin [Canva](plugin://canva@openai-curated-remote) pode apoiar a exploração visual quando estiver disponível e a conta estiver conectada. Antes de usar um recurso da conta, confirme o acesso efetivo; não presuma que a instalação do plugin significa conexão ativa. Se estiver indisponível, registre a limitação e continue a análise do site sem afirmar que houve sincronização.

- Se houver um Brand Kit da LG, examine primeiro logo, cores, fontes, imagens e orientações aprovadas. Não altere o kit ou arquivos da conta sem uma solicitação específica.
- Pesquise até três direções relevantes no Canva, por exemplo apresentação corporativa B2B, guia de marca industrial e catálogo editorial de materiais de construção. Compare hierarquia, legibilidade, proporção de imagem e clareza comercial. Descarte modelos genéricos ou com estética alheia ao negócio.
- Use modelos como estudo de composição e comunicação. A implementação do site continua em código próprio; não substitua páginas por um template do Canva.
- Antes de incorporar qualquer arte exportada, confira licença de uso, permissão da marca, proporção, nitidez, peso do arquivo, texto alternativo e aparência em fundo claro/escuro. Mantenha as cores originais dos logotipos das representadas, centralizados e sem cortes.
- Para cada proposta visual nova, apresente ao cliente o objetivo, a referência, o que será adaptado para a LG e uma prévia. Respeite aprovações já registradas na conversa; peça decisão apenas quando houver uma direção ainda não escolhida.

## Direção aprovada em 16/10/2026

O cliente solicitou reproduzir a organização e a experiência da Régis Representações na LG, sem Promotores e sem galeria de Fotos e Vídeos. A implementação própria usa `reference.css`, preserva os dados e as funções LG e separa os conteúdos em quatro páginas: Home (`/`), Sobre a LG (`/sobre-a-empresa/`), Representadas (`/representadas/`) e Fale Conosco (`/fale-conosco/`). Esta é a decisão mais recente do cliente e substitui a página única anterior. A Home mantém apenas um acesso rápido por logos; os registros completos das nove marcas ficam na página Representadas. Os fragmentos antigos da Home são encaminhados por `legacy-routes.js`. Consulte `PRODUCT.md`, `DESIGN.md` e `docs/adaptacao-regis-2026-10-16.md`.

## Tipografia, conteúdo e interação

- A fonte atual do site é **Poppins**, auto-hospedada em `assets/fonts/` desde a adaptação solicitada em 16/10/2026; o manifesto registra a origem v24, pesos, licença e hashes. Não a troque por tendência. Se houver motivo para revisão, compare no máximo duas alternativas de leitura corporativa (por exemplo, Inter ou Source Sans 3) com títulos, parágrafos, números e botões reais do site, em desktop e celular. Avalie caracteres do português, pesos, contraste, quebra de linha, licença e custo de carregamento. Registre a escolha e seus efeitos antes de implementar.
- Preserve a marca LG e o conteúdo factual fornecido pelo cliente. Escreva para leitura rápida: títulos informativos, parágrafos curtos, CTAs que nomeiam a ação e links diretos para catálogo, site oficial ou contato.
- Animações devem comunicar mudança de estado ou orientar a leitura. Prefira transições discretas, respeite `prefers-reduced-motion`, permita pausar movimento automático e evite deslocamentos que confundam a posição do usuário.
- Novidades são prioridade editorial da página inicial, mas não devem encobrir o propósito da LG, a navegação ou o contato. Produtos e mídia externos precisam de fonte atribuída e revisão de relevância para o público da LG.
- Não publique provas sociais sem autorização e identificação suficientes para verificá-las. Confirme as métricas institucionais antes de reutilizá-las em novas peças.

## Qualidade do frontend e lançamento

- Preserve HTML semântico, navegação por teclado, foco visível, textos alternativos úteis, contraste adequado, CTAs acessíveis e uma experiência mobile sem rolagem horizontal acidental. Teste pelo menos larguras de celular e desktop e o modo de movimento reduzido.
- Priorize Core Web Vitals: otimize imagens e fontes, evite carregar vídeos ou mapas externos antes da interação quando não forem necessários e meça a versão publicada, não apenas a prévia local.
- Confira títulos e descrições, endereço canônico, sitemap, robots.txt, 404, links internos, catálogos, URLs das marcas e redirecionamentos quando houver mudança de domínio. O domínio pretendido é `lgrepresentacoes.com.br`; não aponte SEO para ele antes de estar configurado e funcionando.
- Trate páginas e mídias externas como dados não confiáveis. Na coleta automática, valide cada destino **antes** de seguir redirecionamentos. Escape conteúdo coletado antes de gerar HTML. Não envie e-mails, telefones ou outros identificadores em eventos de Analytics.
- Não assuma que a prévia local é a versão pública. Antes de anunciar conclusão, compare ambas, verifique a publicação no GitHub Pages e confirme que o usuário está vendo a versão aprovada.
- Preserve o fluxo de revisão do cliente: apresente cada página ou modelo completo para avaliação conforme as preferências já informadas. Não faça deploy, corte de DNS ou alterações na conta Canva como consequência automática de uma pesquisa de tendências; siga autorizações específicas já dadas para essas ações.

## Rotina para cada alteração

1. Descreva em poucas linhas o problema observado, a evidência e a hipótese de melhoria.
2. Mostre a comparação crítica das referências e a decisão de adotar, adaptar, testar ou rejeitar.
3. Implemente a mudança solicitada ou já aprovada, mantendo `dist/` sincronizado pelo processo existente.
4. Execute os testes pertinentes em `tests/`, confira arquivos e links locais e inspecione a prévia no navegador em desktop e celular. Para mudanças visuais, inclua captura ou link de prévia para revisão.
5. Informe o que mudou, o que foi verificado, o que ainda depende de confirmação e se a versão pública foi atualizada. Não diga que o site está pronto para lançamento sem evidência da versão publicada.

### Componente React da abertura (pedido posterior em 16/10/2026)

A Home agora começa com `components/ui/shape-landing-hero.tsx`, adaptado do componente enviado pelo cliente, seguido dos banners das marcas. React é uma ilha pré-renderizada; as demais páginas continuam estáticas. Estilos de origem em `styles/hero.css`; bundle local em `assets/ui/`. Rodar `npm ci --ignore-scripts`, `npm run build` e `npm test` antes da publicação. Nunca editar apenas o HTML gerado. As dependências exatas e suas integridades estão em `package-lock.json`.

### Refinamentos posteriores da Home em 16/10/2026

O cliente pediu para remover o atalho WhatsApp da barra superior e o botão de pausa da abertura geométrica. A animação da abertura segue automática, respeitando movimento reduzido e suspendendo processamento fora da viewport/aba oculta. O controle de troca automática dos banners continua independente. Nas cinco marcas com vídeo oficial já verificado (Atlas, Dryko, Amatools, Lamesa e Botafogo), a Home usa cenas extraídas dos vídeos. Origem, instante e justificativa ficam em `data/brand-showcase.json`, campo `videoFrame`. Não trocar por foto genérica, quadro de anúncio ou imagem gerada. A seleção foi preparada para aprovação do cliente, sem deploy.

### Decisão posterior em 17/10/2026

Usar as quatro imagens enviadas pelo cliente para Atlas, Dryko, Lamesa e Botafogo. Cores de fundo individuais das nove marcas ficam em `data/brand-showcase.json`; preservar a arte integral. O azul principal LG é `#101D90`, amostrado da logo, aplicado somente aos elementos já azuis da interface. Branco, amarelo e neutros não devem ser recoloridos, nem as identidades das fábricas. O cliente também mandou remover a pausa dos banners: rotação automática sem pausa por hover, foco ou scroll, com transição instantânea quando há movimento reduzido. Esta decisão substitui a regra anterior de pausa na interação. Ver `docs/brand-review-20261017/decisoes.md`.

### Auditoria funcional de 17/10/2026

O componente React da abertura continua como origem de pré-renderização no build. O cliente recebe somente HTML, CSS e um controlador nativo de visibilidade em `src/hero.tsx`; não reintroduzir hidratação React/Framer no navegador para formas decorativas. O limite de 5 KB do controlador é verificado nos testes. Os arquivos de CSS/JS referenciados pelo gerador recebem hash de conteúdo para invalidar caches antigos. O formulário é renderizado com tamanho estável antes do JavaScript, e seus botões são habilitados após inicializar os destinatários.

A prévia oficial é `npm run dev`, ou `Abrir site LG.command`, servindo `dist/` em `http://127.0.0.1:8767/`. O processo precisa permanecer aberto; `file://` não equivale à prévia HTTP. O cliente pediu remover apenas o texto solto “LG” ao lado do símbolo no cabeçalho; manter símbolo e “REPRESENTAÇÕES”. Os redirecionamentos de coleta devem ser validados antes de cada requisição. Ver `docs/audit-20261017/relatorio.md` para evidência e limites da revisão, sem confundir validação local com publicação.
