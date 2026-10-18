"""Build an allowlisted, inspected public artifact; never preserve stale dist entries."""
from pathlib import Path
import os
import base64
import json
import re
import shutil
import tempfile
from security_policy import protect_html

SECRET = re.compile(rb'(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|sb_secret_[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|"role"\s*:\s*"service_role")')
ALLOWED = {'.html','.css','.js','.svg','.png','.jpg','.jpeg','.webp','.gif','.pdf','.woff','.woff2','.json','.xml','.ico','.map'}

def inspect(path, base=None):
    if path.is_symlink(): raise ValueError('Symlink in public source: ' + str(path))
    names = path.relative_to(base).parts if base else (path.name,)
    if any(name.startswith('.') for name in names) and not (names == ('.nojekyll',) and path.is_file() and path.stat().st_size == 0):
        raise ValueError('Hidden public path: ' + str(path))
    if path.is_dir(): return
    if path.suffix.lower() not in ALLOWED and path.name not in {'.nojekyll','robots.txt','CNAME','LICENSE.txt','OFL.txt','Poppins-OFL.txt','hero.js.LEGAL.txt'}:
        raise ValueError('Unexpected public file: ' + str(path))
    if path.suffix.lower() == '.json' and path.name not in {'manifest.json','whatsapp-source.json'}:
        raise ValueError('Unapproved JSON in public assets: ' + str(path))
    content = path.read_bytes()
    for match in re.finditer(rb'[A-Za-z0-9_-]{8,}\.([A-Za-z0-9_-]{8,})\.[A-Za-z0-9_-]{8,}', content):
        try:
            payload = match[1] + b'=' * (-len(match[1]) % 4)
            claims = json.loads(base64.urlsafe_b64decode(payload))
        except (ValueError, UnicodeError): continue
        if isinstance(claims, dict) and claims.get('role') == 'service_role':
            raise ValueError('Privileged JWT in public artifact: ' + str(path))
    if SECRET.search(content): raise ValueError('Possible secret in public artifact: ' + str(path))

def publish(root, files, directories):
    root = Path(root)
    staging = Path(tempfile.mkdtemp(prefix='.public-stage-', dir=root))
    backup = root/'.dist-previous'
    try:
        for name in files + directories:
            source = root/name
            inspect(source, root)
            if source.is_dir():
                for child in source.rglob('*'): inspect(child, root)
                shutil.copytree(source, staging/name)
            else:
                (staging/name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, staging/name)
        for page in staging.rglob('*.html'):
            page.write_text(protect_html(page.read_text()))
        # Source HTML and dist share security metadata: tests compare their bytes.
        for page in staging.rglob('*.html'):
            (root/page.relative_to(staging)).write_bytes(page.read_bytes())
        if backup.exists(): shutil.rmtree(backup)
        if (root/'dist').exists(): os.replace(root/'dist', backup)
        try: os.replace(staging, root/'dist')
        except BaseException:
            if backup.exists(): os.replace(backup, root/'dist')
            raise
        if backup.exists(): shutil.rmtree(backup)
    finally:
        if staging.exists(): shutil.rmtree(staging)
