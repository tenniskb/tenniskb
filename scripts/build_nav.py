"""Generate mkdocs.yml for en/ and vi/, plus extra CSS and a root index.html.

For each language:
  - mkdocs.yml uses the default mkdocs theme (Bootstrap, light blue #2fa4e7)
  - No 'material' theme, no repo URL (per user preference: no GitHub link in nav)
  - site_url ends in /en/ or /vi/ respectively

Also writes a root index.html that links to /en/ and /vi/ for the public site
landing page at https://tenniskb.github.io/tenniskb/.
"""
import os

en_dir = r"C:\Users\Henry\Downloads\Tenniskb\tenniskb\en\docs"
vi_dir = r"C:\Users\Henry\Downloads\Tenniskb\tenniskb\vi\docs"
repo_root = r"C:\Users\Henry\Downloads\Tenniskb\tenniskb"

# === Nav categories ===
# EN key -> category.  Vietnamese has one translated key: 5R-Movement-System
# becomes "He-Thong-Di-Chuyen-5R" in the VI folder.
EN_CAT = {
    # Serve
    "Arming-Serve": "Serve",
    "Eight-Stage-Serve-Model": "Serve",
    "Return-Serve-Anticipation": "Serve",
    "Return-Serve-Pressure": "Serve",
    "Second-Serve-Aggression": "Serve",
    "Serve-Backswing-Types": "Serve",
    "Serve-Cartwheel": "Serve",
    "Serve-Launch-CoM": "Serve",
    "Serve-Reading": "Serve",
    # Forehand
    "Fault-Tolerant-Forehand": "Forehand",
    "Forehand-Stance-Selection": "Forehand",
    "Forehand-Superiority": "Forehand",
    "Run-Around-Forehand": "Forehand",
    # Backhand
    "Backhand-Grips": "Backhand",
    "Nondominant-Arm-Backhand-Drill": "Backhand",
    "Two-Handed-Backhand": "Backhand",
    # Volley & Net Play
    "Approach-Shot": "Volley & Net Play",
    "Arming-Volley": "Volley & Net Play",
    "Back-Foot-Volley-Footwork": "Volley & Net Play",
    "Body-Volley-Protocol": "Volley & Net Play",
    "Drop-Shot-Trap": "Volley & Net Play",
    "Drop-Volley": "Volley & Net Play",
    "Half-Volley": "Volley & Net Play",
    "Heavy-Approach": "Volley & Net Play",
    "High-Volley-Termination": "Volley & Net Play",
    "Linear-Momentum-Volley": "Volley & Net Play",
    "Return-Volley": "Volley & Net Play",
    "Still-Wall-Volley": "Volley & Net Play",
    "Touch-Volley": "Volley & Net Play",
    "Volley-Footwork-Sequence": "Volley & Net Play",
    "Volley-Mechanics": "Volley & Net Play",
    # Grip & Pressure
    "Continental-Grip-Anatomy": "Grip & Pressure",
    "Grip-Anchor": "Grip & Pressure",
    "Grip-Dynamics": "Grip & Pressure",
    "Grip-Pressure": "Grip & Pressure",
    "Grip-Pressure-Kinetic-Chain": "Grip & Pressure",
    "Grip-Pulse": "Grip & Pressure",
    "Grip-Pulse-Timing": "Grip & Pressure",
    "Grip-Reference-Table": "Grip & Pressure",
    "Grip-Tension": "Grip & Pressure",
    "Isometric-Grip-Pulse": "Grip & Pressure",
    "Semi-Western-Grip": "Grip & Pressure",
    # Footwork & Movement
    "5R-Movement-System": "Footwork & Movement",
    "Active-Split-Step": "Footwork & Movement",
    "Advanced-Split-Step": "Footwork & Movement",
    "Doubles-Tactics": "Footwork & Movement",
    "Split-Step": "Footwork & Movement",
    "Split-Step-Calibration": "Footwork & Movement",
    "Transitional-Net-Footwork": "Footwork & Movement",
    # Mental & Pressure
    "15-Second-Reset-Protocol": "Mental & Pressure",
    "Amygdala-Hijack": "Mental & Pressure",
    "Arousal-Channelling": "Mental & Pressure",
    "Biological-Threat-Response": "Mental & Pressure",
    "Choking": "Mental & Pressure",
    "Choking-Mechanism": "Mental & Pressure",
    "Mu-Beta-Suppression": "Mental & Pressure",
    "Neural-Pressure": "Mental & Pressure",
    "Sympathetic-Activation-Petit-Bras": "Mental & Pressure",
    "Tensegrity-Fascia-Kinh": "Mental & Pressure",
    # Other
    "Chest-Engine": "Other",
    "Head-Position-Vestibular": "Other",
    "Petit-Bras": "Other",
    "Slice-Eccentric-Loading": "Other",
    "Slice-Topspin-Height-Tactics": "Other",
}

VI_CAT = {k: v for k, v in EN_CAT.items()}
VI_CAT["He-Thong-Di-Chuyen-5R"] = "Footwork & Movement"

# (en_cat, en_label, vi_label) — used for both languages
CATS = [
    ("Serve",              "Serve",                "Giao Bóng"),
    ("Forehand",           "Forehand",             "Thuận Tay"),
    ("Backhand",           "Backhand",             "Trái Tay"),
    ("Volley & Net Play",  "Volley & Net Play",    "Bóng Bên Lưới"),
    ("Grip & Pressure",    "Grip & Pressure",      "Cầm Vợt & Áp Lực"),
    ("Footwork & Movement","Footwork & Movement",  "Di Chuyển"),
    ("Mental & Pressure",  "Mental & Pressure",    "Tâm Lý & Áp Lực"),
    ("Other",              "Other",                "Khác"),
]


def build_nav(letter, cat_map, docs_dir, suffix):
    files = sorted(os.listdir(docs_dir))
    key_to_file = {f.replace(suffix + ".md", ""): f for f in files if f.endswith(suffix + ".md")}
    lines = []
    for cat_en, en_label, vi_label in CATS:
        keys = sorted([k for k, c in cat_map.items() if c == cat_en and k in key_to_file])
        if not keys:
            continue
        section_label = en_label if letter == "en" else vi_label
        lines.append(f"  - {section_label}:")
        for k in keys:
            fn = key_to_file[k]
            # Display title from key: "Forehand-Stance-Selection" -> "Forehand Stance Selection"
            display = k.replace("-", " ")
            # Title-case but preserve all-caps acronyms (5R, 2X, etc.)
            # Simple: lowercase everything then uppercase first letter of each word,
            # except for tokens that already contain digits or all-caps.
            words = display.split(" ")
            tc = []
            for w in words:
                if any(ch.isdigit() for ch in w) or (w.isupper() and len(w) > 1):
                    tc.append(w)
                else:
                    tc.append(w.capitalize())
            display = " ".join(tc)
            lines.append(f"      - {display}: {fn}")
    return lines


def write_mkdocs_yml(letter, nav_lines, out_path, site_url):
    home_label = "Home" if letter == "en" else "Trang Chủ"
    site_name = "Tennis Knowledge Base" if letter == "en" else "Cẩm Nang Tennis"
    # Per user preference: NO repo URL or repo name in the nav (verified 2026-07-20).
    yml = f"""site_name: {site_name}
docs_dir: docs
site_url: {site_url}

theme:
  name: mkdocs
  # Default mkdocs theme (Bootstrap, light blue #2fa4e7).
  # Custom CSS overrides colors to match the TennisKB brand.
  # No 'material' theme — Henry's confirmed preference (July 2026).

extra_css:
  - assets/tenniskb-extra.css

extra:
  generator: false

nav:
  - {home_label}: index.md
{chr(10).join(nav_lines)}

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true
  - attr_list
  - md_in_html
  - tables
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(yml)
    print(f"Wrote {out_path}")


# === CSS ===
CSS = """/* Tennis Knowledge Base — light-blue brand overrides for default mkdocs theme.
   Default mkdocs uses Bootstrap with #2fa4e7 (light blue) as primary.
   This file nudges the palette and styles the language-toggle in the top nav. */

.navbar-default {
  background-color: #2fa4e7;
  border-color: #2580be;
}
.navbar-default .navbar-brand,
.navbar-default .navbar-nav > li > a {
  color: #ffffff;
}
.navbar-default .navbar-brand:hover,
.navbar-default .navbar-nav > li > a:hover,
.navbar-default .navbar-nav > .active > a,
.navbar-default .navbar-nav > .active > a:hover {
  color: #ffffff;
  background-color: #2580be;
}
a, a:visited, a code { color: #2fa4e7; }
a:hover, a:focus { color: #2580be; }

.btn-primary {
  background-color: #2fa4e7;
  border-color: #2580be;
}
.btn-primary:hover, .btn-primary:focus {
  background-color: #2580be;
  border-color: #1d6fa6;
}

body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }

/* Language toggle pill in navbar */
.nav-lang {
  display: inline-block;
  margin-left: 12px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.15);
  color: #fff !important;
  border-radius: 4px;
  font-weight: 500;
}
.nav-lang:hover { background: rgba(255, 255, 255, 0.3); text-decoration: none; }
"""

# === Root index.html ===
INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Tennis Knowledge Base | Cẩm Nang Tennis</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Bilingual tennis coaching library — English & Tiếng Việt.  64 coaching guides on serve, forehand, backhand, volley, grip, footwork, mental, and more.">
  <link rel="alternate" hreflang="en" href="https://tenniskb.github.io/tenniskb/en/">
  <link rel="alternate" hreflang="vi" href="https://tenniskb.github.io/tenniskb/vi/">
  <style>
    :root { --tkb-blue: #2fa4e7; --tkb-blue-dark: #2580be; --tkb-navy: #1d3a52; --tkb-bg: #f5f9fc; }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: var(--tkb-bg); color: #1f2937; line-height: 1.6; }
    .hero { background: linear-gradient(135deg, var(--tkb-blue) 0%, var(--tkb-navy) 100%); color: white; padding: 80px 24px 60px; text-align: center; }
    .hero h1 { margin: 0 0 12px 0; font-size: 42px; letter-spacing: -0.5px; }
    .hero h2 { margin: 0 0 24px 0; font-size: 26px; font-weight: 400; opacity: 0.95; }
    .hero p { margin: 0 auto; max-width: 720px; font-size: 17px; opacity: 0.92; }
    .lang-switch { margin: 28px 0 0 0; }
    .lang-switch a { display: inline-block; margin: 0 8px; padding: 12px 32px; background: rgba(255, 255, 255, 0.15); color: white; border: 2px solid rgba(255, 255, 255, 0.6); border-radius: 6px; text-decoration: none; font-size: 16px; font-weight: 500; transition: all 0.2s; }
    .lang-switch a:hover { background: white; color: var(--tkb-navy); border-color: white; }
    .container { max-width: 1080px; margin: 0 auto; padding: 60px 24px; }
    .stats { display: flex; flex-wrap: wrap; gap: 24px; justify-content: center; margin: 0 0 40px 0; }
    .stat { background: white; padding: 24px 32px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); text-align: center; min-width: 160px; }
    .stat-num { font-size: 32px; font-weight: 700; color: var(--tkb-blue); display: block; }
    .stat-label { font-size: 13px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }
    h3.section-h { text-align: center; color: var(--tkb-navy); font-size: 22px; margin: 0 0 32px 0; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
    .card { background: white; padding: 28px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); }
    .card h4 { margin: 0 0 8px 0; color: var(--tkb-blue-dark); font-size: 18px; }
    .card p { margin: 0 0 16px 0; color: #4b5563; font-size: 14px; }
    .card a { display: inline-block; padding: 8px 18px; background: var(--tkb-blue); color: white; text-decoration: none; border-radius: 4px; font-size: 14px; font-weight: 500; }
    .card a:hover { background: var(--tkb-blue-dark); }
    footer { background: var(--tkb-navy); color: rgba(255, 255, 255, 0.85); padding: 32px 24px; text-align: center; font-size: 14px; }
    footer a { color: #a8d4f5; text-decoration: none; }
    footer a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <section class="hero">
    <h1>Tennis Knowledge Base</h1>
    <h2>Cẩm Nang Tennis</h2>
    <p>A bilingual library of 64 tennis coaching guides — biomechanics, technique, mental game, and the kinetic chain behind every stroke.  Built for serious players and coaches who want a structured reference they can return to.</p>
    <div class="lang-switch">
      <a href="en/">English</a>
      <a href="vi/">Tiếng Việt</a>
    </div>
  </section>

  <div class="container">
    <div class="stats">
      <div class="stat">
        <span class="stat-num">64</span>
        <span class="stat-label">Coaching Guides</span>
      </div>
      <div class="stat">
        <span class="stat-num">2</span>
        <span class="stat-label">Languages</span>
      </div>
      <div class="stat">
        <span class="stat-num">8</span>
        <span class="stat-label">Topic Areas</span>
      </div>
    </div>

    <h3 class="section-h">Browse the library / Khám phá thư viện</h3>
    <div class="cards">
      <div class="card">
        <h4>English Edition</h4>
        <p>Read the 64 coaching guides in English — serve mechanics, footwork, mental pressure protocols, and more.</p>
        <a href="en/">Open English site →</a>
      </div>
      <div class="card">
        <h4>Phiên Bản Tiếng Việt</h4>
        <p>Đọc 64 hướng dẫn huấn luyện bằng tiếng Việt — kỹ thuật giao bóng, di chuyển, giao thức tâm lý, và hơn thế nữa.</p>
        <a href="vi/">Mở bản Tiếng Việt →</a>
      </div>
    </div>
  </div>

  <footer>
    <p>Tennis Knowledge Base · Cẩm Nang Tennis · 64 coaching guides in 8 topic areas</p>
    <p style="margin: 8px 0 0 0; font-size: 12px; opacity: 0.7;">Built for players, by players.  Bilingual EN | VI.</p>
  </footer>
</body>
</html>
"""


def write_root_landing():
    out = os.path.join(repo_root, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(INDEX_HTML)
    print(f"Wrote {out}")


def write_assets_dirs():
    # MkDocs needs the assets/ directory to exist for the extra_css to resolve.
    for lang in ("en", "vi"):
        d = os.path.join(repo_root, lang, "docs", "assets")
        os.makedirs(d, exist_ok=True)
        css_path = os.path.join(d, "tenniskb-extra.css")
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(CSS)
        print(f"Wrote {css_path}")


def write_index_md():
    """Write docs/index.md for both languages (mkdocs homepage file)."""
    en_index = """# Tennis Knowledge Base

A structured library of 64 tennis coaching guides — biomechanics, technique, mental game, and the kinetic chain behind every stroke.  Browse by topic in the sidebar, or jump straight to a category below.

## Topic areas

- **Serve** — 8-stage serve model, cartwheel, backswing types, CoM launch, return-serve pressure
- **Forehand** — stance selection, run-around, fault-tolerant patterns
- **Backhand** — two-handed, grips, non-dominant arm drill
- **Volley & Net Play** — approach shots, drop volleys, half-volley, footwork sequences
- **Grip & Pressure** — continental, semi-western, grip pulse, pressure dynamics
- **Footwork & Movement** — split-step calibration, 5R system, doubles tactics
- **Mental & Pressure** — choking, amygdala hijack, 15-second reset, sympathetic activation
- **Other** — chest engine, head position, slice, petit bras

## How to use this library

Each guide is a self-contained deep-dive on a single technique or concept.  Cross-references between guides are listed at the bottom of each page.  Start with the topic that matters most to your game this week.

Browse the full sidebar on the left, or click any topic above to see its guides.
"""
    vi_index = """# Cẩm Nang Tennis

Một thư viện có cấu trúc gồm 64 hướng dẫn huấn luyện tennis — cơ sinh học, kỹ thuật, tâm lý thi đấu, và chuỗi động lực đằng sau mỗi cú đánh.  Duyệt theo chủ đề trong thanh bên, hoặc nhảy thẳng đến một danh mục bên dưới.

## Các chủ đề

- **Giao Bóng** — mô hình 8 giai đoạn, cartwheel, kiểu đưa vợt về sau, khởi động trọng tâm, áp lực trả giao
- **Thuận Tay** — chọn vị trí, chạy vòng, mẫu chịu lỗi
- **Trái Tay** — hai tay, cầm vợt, bài tập tay không thuận
- **Bóng Bên Lưới** — cú tiếp cận, drop volley, half-volley, chuỗi di chuyển
- **Cầm Vợt & Áp Lực** — continental, semi-western, nhịp cầm vợt, áp lực
- **Di Chuyển** — hiệu chỉnh split-step, hệ thống 5R, chiến thuật đánh đôi
- **Tâm Lý & Áp Lực** — choking, amygdala hijack, nghi thức 15 giây, kích hoạt giao cảm
- **Khác** — chest engine, vị trí đầu, slice, petit bras

## Cách sử dụng thư viện này

Mỗi hướng dẫn là một bài phân tích sâu độc lập về một kỹ thuật hoặc khái niệm duy nhất.  Liên kết chéo giữa các hướng dẫn được liệt kê ở cuối mỗi trang.  Hãy bắt đầu với chủ đề quan trọng nhất với lối chơi của bạn tuần này.

Duyệt toàn bộ thanh bên bên trái, hoặc nhấp vào bất kỳ chủ đề nào ở trên để xem các hướng dẫn của nó.
"""
    with open(os.path.join(en_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(en_index)
    print(f"Wrote {os.path.join(en_dir, 'index.md')}")
    with open(os.path.join(vi_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(vi_index)
    print(f"Wrote {os.path.join(vi_dir, 'index.md')}")


def write_deploy_yml():
    """Two-stage build + deploy: build en/, then build vi/ into the same site/."""
    yml = """name: Deploy TennisKB site

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs mkdocs-material

      - name: Build EN site
        run: |
          cd en
          # Build EN with site_url ending in /en/ so relative links resolve to /en/
          mkdocs build --site-dir ../site/en --strict

      - name: Build VI site
        run: |
          cd vi
          # Build VI with site_url ending in /vi/ so relative links resolve to /vi/
          mkdocs build --site-dir ../site/vi --strict

      - name: Copy landing page
        run: |
          cp index.html site/index.html

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    out = os.path.join(repo_root, ".github", "workflows", "deploy.yml")
    with open(out, "w", encoding="utf-8") as f:
        f.write(yml)
    print(f"Wrote {out}")


def write_gitignore():
    gi = """# MkDocs build output (built by GitHub Actions)
site/

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Editor backup
*.swp
*~
"""
    out = os.path.join(repo_root, ".gitignore")
    with open(out, "w", encoding="utf-8") as f:
        f.write(gi)
    print(f"Wrote {out}")


def write_readme():
    readme = """# Tennis Knowledge Base

Bilingual tennis coaching library — 64 guides in English & Tiếng Việt.

**Live site:** https://tenniskb.github.io/tenniskb/

## Structure

```
tenniskb/
├── en/
│   ├── mkdocs.yml          # EN build config
│   └── docs/               # 64 EN .md files + index.md
├── vi/
│   ├── mkdocs.yml          # VI build config
│   └── docs/               # 64 VI .md files + index.md
├── index.html              # Bilingual landing page (root)
├── .github/workflows/
│   └── deploy.yml          # GitHub Pages auto-deploy
└── scripts/
    └── build_nav.py        # Regenerate mkdocs.yml nav blocks
```

## Topic areas (8)

Serve · Forehand · Backhand · Volley & Net Play · Grip & Pressure · Footwork & Movement · Mental & Pressure · Other

## Local preview

```bash
# EN site: http://127.0.0.1:8000/en/
cd en && mkdocs serve

# VI site: http://127.0.0.1:8000/vi/
cd vi && mkdocs serve
```

## Build

```bash
# Build both languages
cd en && mkdocs build --strict
cd ../vi && mkdocs build --strict
```

The GitHub Actions workflow (`.github/workflows/deploy.yml`) builds both sites on every push to `main` and deploys the combined output to GitHub Pages.
"""
    out = os.path.join(repo_root, "README.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"Wrote {out}")


if __name__ == "__main__":
    en_nav = build_nav("en", EN_CAT, en_dir, "-Coaching-Guide")
    vi_nav = build_nav("vi", VI_CAT, vi_dir, "-Huong-Dan-VI")

    write_mkdocs_yml("en", en_nav,
                     os.path.join(repo_root, "en", "mkdocs.yml"),
                     "https://tenniskb.github.io/tenniskb/en/")
    write_mkdocs_yml("vi", vi_nav,
                     os.path.join(repo_root, "vi", "mkdocs.yml"),
                     "https://tenniskb.github.io/tenniskb/vi/")
    write_assets_dirs()
    write_index_md()
    write_root_landing()
    write_deploy_yml()
    write_gitignore()
    write_readme()
