"""Content policy shared by build and HTTP preview; no security claim for ignored host files."""
import base64
from hashlib import sha256
from html import escape
import re

POLICY_RE = re.compile(r'<meta\s+http-equiv="Content-Security-Policy"\s+content="[^"]*"\s*/?>', re.I)

def policy(markup, *, header=False):
    hashes = []
    for attrs, body in re.findall(r'<script\b([^>]*)>([\s\S]*?)</script>', markup, re.I):
        if not re.search(r'\bsrc\s*=', attrs, re.I):
            hashes.append("'sha256-" + base64.b64encode(sha256(body.encode()).digest()).decode() + "'")
    directives = [
        "default-src 'self'", "base-uri 'none'", "object-src 'none'",
        "script-src 'self' https://www.googletagmanager.com " + ' '.join(sorted(set(hashes))),
        "style-src 'self' 'unsafe-inline'", # Leaflet positions map layers with style attributes.
        "font-src 'self'", "img-src 'self' data: https://tile.openstreetmap.org https://gibs.earthdata.nasa.gov https://www.google-analytics.com",
        "connect-src 'self' https://nominatim.openstreetmap.org https://www.google-analytics.com https://region1.google-analytics.com https://ruepjyxtenhwnfdahqxb.supabase.co",
        "frame-src https://www.youtube-nocookie.com", "form-action 'self'", "upgrade-insecure-requests",
    ]
    if header: directives.append("frame-ancestors 'none'")
    return '; '.join(item.strip() for item in directives)

def protect_html(markup):
    markup = POLICY_RE.sub('', markup)
    markup = re.sub(r'<meta\s+name="referrer"[^>]*>', '', markup, flags=re.I)
    tags = '<meta http-equiv="Content-Security-Policy" content="' + escape(policy(markup), quote=True) + '"><meta name="referrer" content="strict-origin-when-cross-origin">'
    # Place after charset, before any resource or script; JSON-LD hashes include exact bytes.
    charset = re.search(r'<meta\s+charset=[^>]+>', markup, re.I)
    if not charset: raise ValueError('Public HTML requires explicit charset')
    return markup[:charset.end()] + tags + markup[charset.end():]
