#!/usr/bin/env python3
"""Convierte la copia de voces (voces-del-club.json) en la carpeta voces/ de la web."""
import json, sys, base64, hashlib, pathlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
j = json.loads(src.read_text()); out.mkdir(parents=True, exist_ok=True)
old = {}
mf = out / 'manifest.json'
if mf.exists(): old = json.loads(mf.read_text()).get('files', {})
files = dict(old)
for k, b64 in j.get('a', {}).items():
    text = k.split('|', 2)[2] if k.count('|') >= 2 else k
    name = hashlib.sha1(text.encode()).hexdigest()[:14] + '.mp3'
    (out / name).write_bytes(base64.b64decode(b64)); files[text] = name
cfg = j.get('cfg', {})
mf.write_text(json.dumps({'voice': cfg.get('voice', ''), 'vname': cfg.get('vname', ''), 'files': files}, ensure_ascii=False))
print(len(files), 'frases en', out)
