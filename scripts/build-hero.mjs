import { build } from 'esbuild';
import { compile, optimize } from '@tailwindcss/node';
import { Scanner } from '@tailwindcss/oxide';
import { mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const temporary = resolve(root, '.build/hero-static.mjs');
await mkdir(resolve(root, 'assets/ui'), { recursive: true });
const settings = { bundle: true, minify: true, jsx: 'automatic', absWorkingDir: root,
  define: { 'process.env.NODE_ENV': '"production"' }, tsconfig: 'tsconfig.json', legalComments: 'linked' };
await build({ ...settings, entryPoints: ['src/hero.tsx'], outfile: 'assets/ui/hero.js', format: 'esm', target: ['es2022'] });
await build({ ...settings, entryPoints: ['src/hero-static.tsx'], outfile: temporary, platform: 'node', format: 'esm', packages: 'external' });
const { renderHero } = await import(pathToFileURL(temporary));
await writeFile(resolve(root, 'content/hero.html'), `<div id="lg-hero-root">${renderHero()}</div>`);
// This build is one-shot; the CLI's filesystem watcher is not needed.
const input = resolve(root, 'styles/hero.css');
const compiler = await compile(await readFile(input, 'utf8'), {
  from: input, base: dirname(input), onDependency() {},
});
const sources = (compiler.root === 'none' ? [] : compiler.root === null
  ? [{ base: root, pattern: '**/*', negated: false }]
  : [{ ...compiler.root, negated: false }]).concat(compiler.sources);
const scanner = new Scanner({ sources });
const css = compiler.build(scanner.scan());
await writeFile(resolve(root, 'assets/ui/hero.css'), optimize(css, { file: input, minify: true }).code);
await rm(resolve(root, '.build'), { recursive: true, force: true });
console.log('Hero React pré-renderizado e empacotado localmente.');
