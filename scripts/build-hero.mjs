import { build } from 'esbuild';
import { execFileSync } from 'node:child_process';
import { mkdir, writeFile, rm } from 'node:fs/promises';
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
execFileSync(resolve(root, 'node_modules/.bin/tailwindcss'), ['-i', 'styles/hero.css', '-o', 'assets/ui/hero.css', '--minify'], { cwd: root, stdio: 'inherit' });
await rm(resolve(root, '.build'), { recursive: true, force: true });
console.log('Hero React pré-renderizado e empacotado localmente.');
