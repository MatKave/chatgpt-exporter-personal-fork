#!/usr/bin/env python3
"""Wrap compiled upstream build with unique personal identity and update links."""
from pathlib import Path
import argparse, json, re
p=argparse.ArgumentParser()
p.add_argument('source',type=Path)
p.add_argument('output',type=Path)
p.add_argument('--repo',default='',help='public GitHub owner/repo; omit for local offline install')
p.add_argument('--revision',required=True,type=int)
args=p.parse_args()
if args.repo and not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',args.repo):
    raise SystemExit('Invalid GitHub repo name')
s=args.source.read_text(encoding='utf-8')
pkg=json.loads((args.source.parent.parent/'package.json').read_text(encoding='utf-8'))
original=pkg['version']
vers=f'{original}.{args.revision}'
url=f'https://raw.githubusercontent.com/{args.repo}/main/dist/ChatGPT_Exporter_Personal.user.js' if args.repo else None
if not s.startswith('// ==UserScript=='):
    raise SystemExit('Missing userscript metadata')
header,rest=s.split('// ==/UserScript==',1)
header,cnt=re.subn(r'(?m)^// @version\s+[^\r\n]+',f'// @version            {vers}',header)
if cnt!=1: raise SystemExit('Expected one @version')
# Independent name, namespace, author and update channel.
header=re.sub(r'(?m)^(// @name(?::zh-(?:CN|TW))?)\s+[^\r\n]+',lambda m:m.group(1)+'               ChatGPT Exporter Personal',header)
header=re.sub(r'(?m)^// @namespace\s+[^\r\n]+', '// @namespace          ' + (args.repo or 'chatgpt-exporter-personal-local'), header)
header=re.sub(r'(?m)^// @author\s+[^\r\n]+', '// @author             Personal Fork (' + (args.repo or 'local build') + ')', header)
header=re.sub(r'(?m)^// @updateURL\s+[^\r\n]+\n?', '', header)
header=re.sub(r'(?m)^// @downloadURL\s+[^\r\n]+\n?', '', header)
header += ('\n// @updateURL          '+url+'\n// @downloadURL        '+url+'\n') if url else '\n'
# Include the copyright and permission notice in the standalone distributed file.
license_path = Path(__file__).resolve().parents[1] / 'LICENSE'
license_text = license_path.read_text(encoding='utf-8').strip()
if 'Copyright (c) 2022-Present Pionxzh' not in license_text:
    raise SystemExit('Upstream MIT license notice missing or changed')
s=header+'// ==/UserScript==\n\n/*\n'+license_text+'\n*/'+rest
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(s,encoding='utf-8')
print(f'{vers}, bytes {len(s)}, url {url}')
