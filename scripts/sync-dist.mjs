import { cp, mkdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const files = ['index.html', 'style.css', 'main.js', 'marcas.js', 'logo-cloud.js', 'pernambuco-map.js', 'robots.txt', 'sitemap.xml', '.nojekyll'];
for (const file of files) {
  await mkdir(join(root, 'dist', dirname(file)), { recursive: true });
  await cp(join(root, file), join(root, 'dist', file));
}
for (const directory of ['assets', 'sobre']) {
  await cp(join(root, directory), join(root, 'dist', directory), { recursive: true, force: true });
}
console.log('Dist sincronizado sem remover outros arquivos.');
