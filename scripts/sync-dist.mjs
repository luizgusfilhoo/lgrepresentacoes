import { execFileSync } from 'node:child_process';
import { cp, mkdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
execFileSync(process.env.PYTHON || 'python3', [join(root, 'scripts/render_pages.py')], { cwd: root, stdio: 'inherit' });
const files = ['index.html', '404.html', 'legacy-routes.js', 'reference.css', 'contact-form.js', 'style.css', 'editorial.css', 'showcase.css', 'showcase-editorial.css', 'main.js', 'marcas.js', 'logo-cloud.js', 'novidades.js', 'showcase.js', 'analytics.js', 'pernambuco-map.js', 'robots.txt', 'sitemap.xml', '.nojekyll'];
for (const file of files) {
  await mkdir(join(root, 'dist', dirname(file)), { recursive: true });
  await cp(join(root, file), join(root, 'dist', file));
}
for (const directory of ['assets', 'sobre', 'sobre-a-empresa', 'representadas', 'fale-conosco']) {
  await cp(join(root, directory), join(root, 'dist', directory), { recursive: true, force: true });
}
console.log('Dist sincronizado sem remover outros arquivos.');
