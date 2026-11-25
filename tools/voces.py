#!/usr/bin/env python3
"""Convierte la copia de voces (voces-del-club.json) en la carpeta voces/ de la web."""
import json, sys, base64, hashlib, pathlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
j = json.loads(src.read_text()); out.mkdir(parents=True, exist_ok=True)
mf = out / 'manifest.json'; old = json.loads(mf.read_text()) if mf.exists() else {}
files = {}
for t, f in old.get('files', {}).items():
    files[t] = f if isinstance(f, dict) else {'f': f, 'm': old.get('model', 'eleven_multilingual_v2'), 'v': old.get('voice', '')}
n = 0
for k, b64 in j.get('a', {}).items():
    voice, model, text = k.split('|', 2) if k.count('|') >= 2 else ('', '', k)
    name = hashlib.sha1((model + '|' + text).encode()).hexdigest()[:14] + '.mp3'
    (out / name).write_bytes(base64.b64decode(b64)); files[text] = {'f': name, 'm': model, 'v': voice}; n += 1
cfg = j.get('cfg', {})
mf.write_text(json.dumps({'voice': cfg.get('voice', old.get('voice', '')), 'vname': cfg.get('vname', old.get('vname', '')), 'model': cfg.get('model', ''), 'files': files}, ensure_ascii=False))
print(n, 'nuevas ·', len(files), 'frases en', out)
