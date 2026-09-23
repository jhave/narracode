"""Synchronize the existing reading skill with the active drafts and rendered book."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'package-v4/machine-liberation'
edition = json.loads((ROOT / 'edition-v4.json').read_text())
for source, destination in [
    (edition['components'][0], 'assets/manifesto.md'),
    (edition['components'][1], 'assets/result.md'),
    ('Machine-Liberation-v4.md', 'assets/book.md'),
    ('ATTRIBUTION.md', 'references/attribution.md'),
]:
    shutil.copyfile(ROOT / source, PACKAGE / destination)
manifest = json.loads((PACKAGE / 'manifest.json').read_text())
manifest['date'] = edition['date']
manifest['result_draft'] = Path(edition['components'][1]).name
manifest['files'] = {
    str(p.relative_to(PACKAGE)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'manifest.json'
}
(PACKAGE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
# Fixed entry metadata makes repeated builds byte-identical.
date = tuple(map(int, edition['date'].split('-'))) + (0, 0, 0)
with zipfile.ZipFile(ROOT / 'Machine-Liberation-skill-v4.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(PACKAGE.rglob('*')):
        if path.is_file():
            info = zipfile.ZipInfo(str(path.relative_to(PACKAGE.parent)), date_time=date)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
