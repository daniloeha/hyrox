from pathlib import Path
import base64, gzip, hashlib

root = Path(__file__).resolve().parents[1]
parts = [
    root / '.publish' / 'compact_0.b64',
    root / '.publish' / 'compact_1.b64',
]
out = root / 'index.html'

encoded = ''.join(p.read_text(encoding='utf-8').strip() for p in parts)
payload = base64.b64decode(encoded)
html = gzip.decompress(payload)
expected = '412af5ab887dea176ddf033addbebf4ab68bd38f308a56b032aadcf3e56e18ee'
actual = hashlib.sha256(html).hexdigest()
if actual != expected:
    raise SystemExit(f'Checksum mismatch: {actual}')

out.write_bytes(html)

# Clean interrupted staging files; keep the two compact source parts for reproducibility.
for p in (root / '.publish').glob('report_*.b64'):
    p.unlink(missing_ok=True)
(root / '.publish' / 'approved_compact.b64').unlink(missing_ok=True)
for name in ('tmp_ref_test.txt', 'tmp_test_literal.txt'):
    (root / name).unlink(missing_ok=True)

print(f'Published {len(html)} bytes to index.html · sha256 {actual}')
