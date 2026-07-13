# PLeW-NLG

Interactive exploration of **human evaluation data** across NLG tasks. Load a PLeW-ready CSV (`dim::`, `desc::`, `med::`, `res::` columns), map dimensions to axes, and inspect individual judgments in the record window.

Built on [PLeW](https://github.com/len-sprague/PLeW) (multi-dimensional data visualizer).

## Quick start

1. **Install Hugo Extended** — macOS: `brew install hugo`; Windows: `winget install Hugo.Hugo.Extended` ([releases](https://github.com/gohugoio/hugo/releases))
2. **Run the dev server** from the project root:
   ```
   hugo server
   ```
3. **Open in browser:** http://localhost:1313/

**Useful links (local dev only — run `hugo server` first):**
- **Full editor** (upload your own CSV): http://localhost:1313/
- **Example datasets:** http://localhost:1313/examples/

This repo is not deployed to GitHub Pages yet. Links in the app stay on localhost; ignore `*.github.io` URLs until you push the repo and enable Pages.

---

## Data pipeline

| Layer | Purpose |
|-------|---------|
| `eval-data-raw/<dataset>/` | Raw downloads (see `eval-data-raw/SOURCES.md`) |
| `eval-data-processed/<dataset>/` | PLeW transforms: `*_plew_ready.csv`, `transform.py`, `PLEW_MANIFEST.md` |
| `static/data/` | Demo CSVs served by Hugo |
| `content/examples/` | Example pages pointing at `static/data/` |

To prepare a new dataset, use the `plew-prepare-dataset` skill or run the transform script in `eval-data-processed/<dataset>/`, then copy the ready CSV into `static/data/` and add an example page.

---

## Troubleshooting

| Problem | What to try |
|--------|-------------|
| "hugo is not recognized" | Install Hugo Extended and open a **new** terminal. |
| Page won't load | Make sure `hugo server` is still running. |
| Port 1313 in use | Run `hugo server --port 1314` and use http://localhost:1314/ instead. |
| Examples link → GitHub 404 | Use **http://localhost:1313/examples/** while developing. The site is not on GitHub Pages until you push and deploy. |

---

## Citation

If you use PLeW-NLG in research, cite the INLG 2026 demo paper (draft in `paper/`).
