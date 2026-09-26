# Componentes de referência

Este site é HTML, CSS e JavaScript estáticos, publicados no GitHub Pages. Os componentes React enviados como referência foram adaptados ao comportamento nativo do projeto: abas deslizantes da navegação e faixa contínua de logos. Criar `/components/ui` aqui não faria esses arquivos TSX funcionarem: faltam React, compilação TypeScript, Tailwind e a estrutura de projeto shadcn.

Em uma futura migração, inicie um projeto com `npx create-next-app@latest` selecionando TypeScript, Tailwind e App Router; execute `npx shadcn@latest init` na raiz. A pasta padrão será `components/ui` (ou `src/components/ui` se optar por `src/`), e o alias `@/components` precisa apontar para ela em `components.json` e `tsconfig.json`. Depois instale as dependências dos componentes escolhidos, como `framer-motion` e `react-icons`, e transpile os arquivos `.tsx`. Para este site não é necessária essa migração.

## Logo Cloud

O exemplo `logo-cloud-3.tsx` foi traduzido para a faixa de representadas já existente. Ela usa os nove arquivos locais da LG, sem logos externas nem filtro monocromático; `logo-cloud.js` mantém o movimento inverso contínuo, acelera de um ciclo de 80 s para 25 s no hover sem reiniciar a posição e respeita pausa, foco por teclado, visibilidade da seção e preferência por movimento reduzido. O exemplo React enviado usa `speed` e `speedOnHover`, enquanto o código da dependência declara `duration` e `durationOnHover`; copiar literalmente não entregaria a velocidade especificada.
