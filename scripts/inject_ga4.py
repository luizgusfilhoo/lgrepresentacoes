"""Add the Google tag to publish output only when a real GA4 ID is configured."""
import os
import re
from pathlib import Path
try:
    from .security_policy import protect_html
except ImportError:
    from security_policy import protect_html

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- GA4 START -->', '<!-- GA4 END -->'


def inject(page, measurement_id):
    if measurement_id and not re.fullmatch(r'G-[A-Z0-9]{5,20}', measurement_id):
        raise ValueError('GA4_MEASUREMENT_ID must be a valid G- measurement ID')
    text = page.read_text()
    if START in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        text = before + after
    if measurement_id:
        snippet = f'''{START}
  <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{measurement_id}');</script>
  {END}
  '''
        text = text.replace('</head>', snippet + '</head>', 1)
    # Refresh exact script hashes when the build already has a CSP.
    if 'http-equiv="Content-Security-Policy"' in text:
        text = protect_html(text)
    page.write_text(text)


if __name__ == '__main__':
    identifier = os.environ.get('GA4_MEASUREMENT_ID', '').strip().upper()
    for page in (ROOT / 'dist').rglob('*.html'):
        inject(page, identifier)
    print('GA4 ativado na distribuição.' if identifier else 'GA4 aguardando ID real; nenhum rastreador adicionado.')
