# Apresentação institucional e das marcas — LG Representações

## Objetivo e escopo

Reorganizar o site público da LG Representações para que um visitante conheça rapidamente a empresa, encontre as nove indústrias representadas, entenda suas linhas de produtos e consiga falar com a equipe. O público principal inclui varejistas, atacadistas, distribuidores e fabricantes interessados em representação comercial. A atuação apresentada é em Pernambuco, com intenção de expansão para regiões vizinhas.

O site continuará como uma página única, com âncoras para as seções. A referência da Régis Representações orienta a clareza da navegação, o destaque dado às marcas e o movimento da apresentação. A composição, os textos e as imagens serão próprios da LG. Não entram páginas de promotores nem galeria de fotos e vídeos.

## Percurso do visitante

1. Um cabeçalho claro exibe logo LG, Início, Representadas, Sobre a LG e Contato. No desktop, uma faixa discreta oferece acesso ao contato e ao Instagram; no celular, esses destinos permanecem acessíveis no menu.
2. A capa abre com a LG, a foto da equipe comercial já aprovada e uma frase curta que descreve a ligação entre indústrias e compradores. O botão principal leva às representadas; o segundo leva ao contato.
3. Logo após a capa, uma faixa compacta de indicadores reúne os números fornecidos pela LG. Em seguida começa o bloco de marcas, para que o portfólio apareça antes do conteúdo institucional extenso.
4. As nove representadas aparecem em uma apresentação navegável. Cada painel contém logo íntegro, foto de produto ou linha, categoria, descrição curta, principais produtos, link para o site oficial e link para o catálogo correspondente. A ordem existente das nove marcas é preservada.
5. O bloco Sobre a LG apresenta história e fundador, área de atuação, propósito, missão, visão, os cinco valores e perspectivas futuras. Os textos serão editados para evitar repetições, sem alterar os compromissos fornecidos pelo usuário.
6. O encerramento reúne chamada para parceria, contatos dos times comercial e escritório, horários por dia, Instagram e rodapé.

## Direção visual

A identidade usa o azul e o amarelo da LG como cores principais, com fundos claros, contraste alto e mais espaço de leitura. A tipografia terá família sem serifa adequada a texto informativo; os títulos diferem por tamanho e peso, sem depender de condensação extrema. Elementos decorativos e números grandes não competirão com a informação principal.

O destaque das marcas terá uma composição editorial consistente, com fotografia de produto, logo e conteúdo legível. A interface não reproduzirá os banners, personagens ou arquivos gráficos da Régis. As fotos das linhas representadas serão selecionadas nos materiais e sites oficiais das próprias marcas, registrando a fonte de cada uma, baixadas para o projeto quando apropriado e otimizadas para web. Os logos e catálogos existentes no projeto permanecem vinculados às marcas corretas; a imagem jamais será ampliada por corte que elimine parte da marca.

## Comportamento e animação

O destaque de marcas permite avançar, voltar e selecionar uma representada diretamente. A troca usa uma transição curta de opacidade e deslocamento leve. A rolagem revela seções com movimento discreto uma única vez. Não haverá rolagem automática que retire o controle do visitante; caso haja reprodução automática de algum movimento decorativo, ele terá controle de pausa. Com `prefers-reduced-motion`, as transições e revelações são desativadas. Teclado, foco visível e rótulos acessíveis permitem navegar sem mouse.

No celular, o painel é compacto: texto e ações aparecem junto da imagem, sem exigir gestos ocultos. Botões de navegação são visíveis e não há rolagem horizontal da página.

## Conteúdo e links

As descrições de cada representada serão conferidas nos sites oficiais e nos catálogos já recebidos. A copy deve falar das linhas que a LG representa, sem prometer estoque, venda direta, preço ou cobertura geográfica que não tenham sido confirmados. Todos os painéis devem conter site oficial e catálogo. A ligação do Instagram será `https://www.instagram.com/lg.represen/`, identificada por ícone e texto acessível, aberta em nova aba. Os links de WhatsApp e e-mail já informados pela LG permanecem por integrante.

## Implementação e publicação

O projeto atual usa HTML, CSS e JavaScript estáticos, publicados pela raiz da branch `main` no GitHub Pages em `/lgrepresentacoes/`. A solução continuará estática. Recursos internos usarão caminhos relativos ao projeto, para funcionar nesse subdiretório. A página de compatibilidade `sobre/` continuará encaminhando para a âncora Sobre. O diretório `dist/`, usado pelo fluxo Sites, deverá refletir o mesmo conteúdo publicado; a implementação definirá uma cópia mecânica ou geração única para impedir divergência entre as duas saídas.

O layout prioriza imagens responsivas e comprimidas, carregamento adiado para painéis fora da vista e ausência de bibliotecas de animação pesadas. O HTML mantém títulos semânticos, metadados, link canônico para a URL pública e dados estruturados pertinentes. A implementação removerá o `noindex,nofollow` atual e a regra de bloqueio no `robots.txt`, pois o objetivo declarado é permitir indexação orgânica. Qualquer URL antiga conhecida será preservada ou redirecionada quando o mecanismo de hospedagem permitir.

## Verificação e critérios de aceite

- Na primeira tela, a LG e a proposta comercial ficam claras, com acesso imediato às marcas e ao contato.
- As nove marcas podem ser alcançadas por navegação direta e têm logo completo, descrição correta, site e catálogo funcionais.
- A apresentação funciona em desktop e celular, por toque e teclado, sem conteúdo cortado nem rolagem horizontal inesperada.
- O Instagram abre o perfil informado; WhatsApp, e-mail e PDFs levam aos destinos corretos.
- Movimento reduzido é respeitado; imagens não essenciais não atrasam a capa.
- A ordem visual é capa, indicadores, representadas, conteúdo institucional, contato.
- O build publicado no GitHub Pages carrega estilos, scripts, imagens e PDFs a partir de `/lgrepresentacoes/`, confirmado pela URL pública após a publicação.
- A página pública permite indexação e aponta seu endereço canônico para o GitHub Pages até que o domínio próprio seja configurado.

Antes da publicação, a LG revisará a copy e as imagens escolhidas para cada marca. A revisão visual será feita em desktop e celular, além de testes dos links e do comportamento de navegação.
