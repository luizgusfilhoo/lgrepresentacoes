# Atualização do time comercial — 26/10/2026

Solicitação: retirar Allyson da equipe e ajustar o site ao quadro atual.

## Alterações

- Removidos nome, WhatsApp e e-mail do contato público e do seletor estático.
- Time comercial: Luiz Filho e Luiz Gustavo, em duas colunas no desktop e uma no celular. Escritório: Manoel e Felipe.
- O controlador do formulário continua derivando seus destinatários dos cartões, evitando listas de encaminhamento divergentes.
- Testes validam o quadro atual, opções, índices e ausência do contato retirado no conteúdo e nas duas cópias de publicação. Os testes de encaminhamento percorrem os contatos existentes e rejeitam índices fora do quadro.
- Build sincronizou dist, referências CSS com hash, metadados e links para o domínio atual.

## Verificação local

Build concluído; 56 testes Python e 20 testes Node aprovados. Quatro rotas verificadas via Playwright em 1440px e 390px: HTTP 200, navegação ativa correta, nenhuma rolagem horizontal, imagem quebrada carregada ou erro JavaScript observado. Formulário conferido para os quatro contatos com abertura de WhatsApp interceptada; nenhum envio foi realizado. Os testes automatizados conferem também e-mail, validação e codificação dos dados. Menu mobile e resposta 404 verificados. Capturas desktop/mobile salvas junto a este relatório local.

Impeccable e Design Taste foram usados para o ajuste limitado ao layout existente. O detector apontou uma borda de destaque preexistente fora da alteração; a identidade aprovada foi preservada.

## Limites

A alteração cobre o site estático publicado. Não comprova revogação de contas externas, caixas de e-mail ou acessos de equipe em outros sistemas; não foram alterados registros históricos nem o projeto separado 3V. A verificação pública posterior deve constar da evidência de publicação.
