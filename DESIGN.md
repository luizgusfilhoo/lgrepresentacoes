# Design — LG Representações

Direção solicitada em 16/10/2026: adaptar a estrutura completa da Régis Representações à identidade e aos conteúdos LG, excluindo Promotores e Fotos e Vídeos. A entrevista e as aprovações do cliente já constam da conversa e de AGENTS.md; não reiniciar a descoberta do negócio.

## Mundo visual
Institucional comercial claro: contato em faixa superior, menu branco, banners oficiais largos, faixa azul de contato, logos com cores originais, superfícies brancas/cinza-claro e rodapé grafite em quatro colunas. Amarelo LG reservado a chamadas e detalhes de seleção. Tipografia Poppins auto-hospedada, aproximando o caráter da referência; texto corrido com bom contraste e entrelinha.

## Página e navegação
Quatro páginas: Home com abertura geométrica enviada pelo cliente, banners oficiais, acesso rápido às marcas, indicadores, resumo institucional e serviços; Sobre a LG com história, propósito, missão, visão e valores; Representadas com as nove marcas, catálogos e produtos em uma área expansível; Fale Conosco com equipe, formulário, horários, mapa e FAQ. Cabeçalho e rodapé são compartilhados. Cada página tem título, descrição, canonical e navegação próprios. Os fragmentos antigos encaminham para os novos destinos. Esta decisão substitui a página única anterior.

## Movimento
Banners avançam automaticamente a cada 10 s quando visíveis; pausar com interação, foco, aba inativa e movimento reduzido. Setas, indicadores e gesto horizontal. Entradas discretas em blocos selecionados, 240 ms, sem esconder conteúdo antes da inicialização. Logos não recebem outra animação contínua; uma linha clara de marcas evita disputa com o banner.

## Adaptação crítica
Recriar os padrões visuais com código próprio. Não incorporar scripts de terceiros, analytics da referência, formulário sem destino validado, texto ou contatos da Régis. Preservar os recursos funcionais da LG, os geradores editoriais e o mapa local. Não inventar automações de Instagram, estoque, prova social ou envio de formulários.

## Verificação
Uma rodada conjunta desktop/celular com Playwright, revisão de mídia, navegação, banner, catálogos, mapa, foco, movimento reduzido e erros de console; corrigir achados e confirmar. Sincronizar dist e mostrar a prévia. Publicação é uma etapa separada.

Abertura geométrica: fundo azul-marinho, formas translúcidas azuis e amarelas, tipografia Poppins e duas ações claras. Movimento de fundo de 12 segundos, deslocamento de 15 px, sem botão de pausa por pedido expresso do cliente, pausa fora da área visível/aba inativa e alternativa sem movimento. Nenhum título fica invisível aguardando JavaScript. Atalho de WhatsApp removido do topo por pedido posterior do cliente; botão flutuante preservado; sem setas diagonais decorativas nos links; legenda da imagem ilustrativa com asterisco e 10 px.

Ajuste de 17/10/2026: azul principal `#101D90`, correspondente à amostra predominante da logo LG. Substitui o azul anterior apenas onde já havia azul. Fundos específicos para cada fábrica, arte integral sem cortes. Novas artes do cliente em Atlas, Dryko, Lamesa e Botafogo. Banners automáticos a cada 10 s sem controle de pausa e sem pausa por interação; movimento reduzido mantém a rotação com troca instantânea.
