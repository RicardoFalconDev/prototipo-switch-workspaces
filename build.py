"""Genera prototipo.html: index.html con todos los assets embebidos (un solo archivo para compartir)."""
import base64, json, pathlib, re

root = pathlib.Path(__file__).parent
html = (root / 'index.html').read_text()
mime = {'.svg': 'image/svg+xml', '.png': 'image/png'}
assets = {
    f.name: f'data:{mime[f.suffix]};base64,' + base64.b64encode(f.read_bytes()).decode()
    for f in sorted((root / 'assets').iterdir()) if f.suffix in mime
}
html = re.sub(r'src="assets/([\w.-]+)"', lambda m: f'src="{assets[m.group(1)]}"', html)
html = html.replace('<script>\nconst ASSETS', f'<script>window.__ASSETS__={json.dumps(assets)};</script>\n<script>\nconst ASSETS', 1)
(root / 'prototipo.html').write_text(html)
print(f'prototipo.html  {len(html)/1024:.0f} KB  ({len(assets)} assets)')
