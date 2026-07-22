# Tennis Knowledge Base

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
