import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
execFileSync(process.env.PYTHON || 'python3', [join(root, 'scripts/render_pages.py')], { cwd: root, stdio: 'inherit' });
const files = ['index.html', '404.html', 'legacy-routes.js', 'reference.css', 'contact-form.js', 'style.css', 'editorial.css', 'showcase.css', 'showcase-editorial.css', 'main.js', 'marcas.js', 'logo-cloud.js', 'novidades.js', 'showcase.js', 'analytics.js', 'pernambuco-map.js', 'robots.txt', 'sitemap.xml', '.nojekyll'];
execFileSync(process.env.PYTHON || 'python3', ['-c', `
import sys
sys.path.insert(0, 'scripts')
from public_artifact import publish
publish('.', ${JSON.stringify(files)}, ['assets','sobre','sobre-a-empresa','representadas','fale-conosco'])
`], { cwd: root, stdio: 'inherit' });
console.log('Distribuição limpa, validada e com política de conteúdo.');
