"""Rebuild docs/pdf/*.pdf from the hub page.

Run from the repo root:  python3 docs/tools/build_pdfs.py
Needs: pip install playwright && playwright install chromium
"""
import json, threading, http.server, socketserver, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parent.parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

handler = functools.partial(Quiet, directory=str(DOCS))
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
PORT = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()

manifest = json.loads((DOCS / 'manifest.json').read_text())
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for d in manifest['docs']:
        page.goto(f'http://127.0.0.1:{PORT}/index.html?print={d["id"]}')
        page.wait_for_selector('body[data-ready="1"]')
        page.wait_for_load_state('networkidle')
        out = DOCS / d['pdf']
        out.parent.mkdir(exist_ok=True)
        page.pdf(path=str(out), format='Letter', print_background=True,
                 margin={'top': '0.55in', 'bottom': '0.6in', 'left': '0.5in', 'right': '0.5in'},
                 display_header_footer=True,
                 header_template='<div></div>',
                 footer_template=f'<div style="font-size:8px;color:#888;width:100%;padding:0 0.5in;display:flex;justify-content:space-between">'
                                 f'<span>{d["title"]} · {d["version"]} · {d["updated"]}</span>'
                                 f'<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
        print('wrote', out.relative_to(DOCS))
    browser.close()
httpd.shutdown()
