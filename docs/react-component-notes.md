# Componentes de referência

Este site é HTML, CSS e JavaScript estáticos, publicados no GitHub Pages. Os componentes React enviados como referência foram adaptados ao comportamento nativo do projeto: abas deslizantes da navegação e faixa contínua de logos. Criar `/components/ui` aqui não faria esses arquivos TSX funcionarem: faltam React, compilação TypeScript, Tailwind e a estrutura de projeto shadcn.

Em uma futura migração, inicie um projeto com `npx create-next-app@latest` selecionando TypeScript, Tailwind e App Router; execute `npx shadcn@latest init` na raiz. A pasta padrão será `components/ui` (ou `src/components/ui` se optar por `src/`), e o alias `@/components` precisa apontar para ela em `components.json` e `tsconfig.json`. Depois instale as dependências dos componentes escolhidos, como `framer-motion` e `react-icons`, e transpile os arquivos `.tsx`. Para este site não é necessária essa migração.
