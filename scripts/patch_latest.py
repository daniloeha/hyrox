from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
p = root / "index.html"
text = p.read_text(encoding="utf-8")
match = re.search(r'<section id="stories">.*?</section>', text, re.S)
if not match:
    raise SystemExit("Stories section not found")
section = match.group(0)

sources = {
    "01": "assets/images/image_16_e629523c1d0a.png",
    "02": "assets/images/image_17_344dac04987d.png",
    "03": "assets/images/image_18_3aa091a37012.png",
    "04": "assets/images/image_19_9e6dd2a74a4a.png",
    "05": "assets/images/image_20_1abcad3ba66d.png",
    "06": "assets/images/image_21_0c1d7afb4e98.png",
    "07": "assets/images/image_22_c0c2ff031ac3.png",
    "08": "assets/images/image_23_06431af2b892.png",
    "09": "assets/stories/story09_amazfit.jpg",
}
for i in range(10, 16):
    b64 = (root / f"assets/stories/story{i:02d}.b64").read_text(encoding="utf-8").strip()
    sources[f"{i:02d}"] = "data:image/webp;base64," + b64

for sid, src in sources.items():
    pattern = re.compile(rf'<img\s+src="[^"]*"\s+data-story-img="{sid}"')
    section, count = pattern.subn(f'<img src="{src}" data-story-img="{sid}"', section)
    if count != 2:
        raise SystemExit(f"Expected 2 image occurrences for Story {sid}, found {count}")

updated = text[:match.start()] + section + text[match.end():]
if updated == text:
    print("Story thumbnails already correct")
else:
    p.write_text(updated, encoding="utf-8")
    print("Corrected all 15 HYROX Top Story thumbnails")
