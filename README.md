# PLeW-NLG

Interactive exploration of **human evaluation data** across NLG tasks. Load a PLeW-ready CSV (`dim::`, `desc::`, `med::`, `res::` columns), map dimensions to grid axes, color, and shape, then inspect or edit individual judgments in a record window.

Built on PLeW, a browser-based multi-dimensional data visualizer.

## Quick start

1. Install Hugo Extended.
   - macOS: `brew install hugo`
   - Windows: `winget install Hugo.Hugo.Extended`
   - Other platforms: [Hugo releases](https://github.com/gohugoio/hugo/releases)
2. Run the dev server from the project root:
   ```
   hugo server
   ```
3. Open http://localhost:1313/ in your browser.

Two entry points once the server is running:
- **Full editor** (upload your own CSV/JSON): http://localhost:1313/
- **Example datasets**: http://localhost:1313/examples/

## Data pipeline

| Layer | Purpose |
|-------|---------|
| `eval-data-raw/<dataset>/` | Raw downloads. See `eval-data-raw/SOURCES.md`. |
| `eval-data-processed/<dataset>/` | Transformed data: `*_plew_ready.csv`, `transform.py`, `PLEW_MANIFEST.md`. |
| `static/data/` | Demo CSVs and saved visualization presets served by Hugo. |
| `content/examples/` | Example pages that point at files in `static/data/`. |

To add a new dataset: profile and reshape the raw data into the `dim::` / `desc::` / `med::` / `res::` schema (the `plew-prepare-dataset` skill automates this), copy the resulting CSV into `static/data/`, then add a page under `content/examples/`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "hugo is not recognized" | Install Hugo Extended and open a new terminal. |
| Page will not load | Check that `hugo server` is still running. |
| Port 1313 in use | Run `hugo server --port 1314` and use that port instead. |
| Examples link to a 404 | Use http://localhost:1313/examples/ while developing; the site is not deployed until pushed with Pages enabled. |

## Example datasets and references

The `examples/` gallery ships with the following public human-evaluation datasets, each transformed into PLeW's judgment-level schema.

| Example | Task | Source |
|---------|------|--------|
| WebNLG 2017 human evaluation | Data-to-text | Shimorina et al., WebNLG 2017 human evaluation. [GitLab](https://gitlab.com/webnlg/webnlg-human-evaluation) |
| NeuralREG human evaluation | Referring expression generation | Castro Ferreira et al., "NeuralREG: An end-to-end approach to referring expression generation." ACL 2018. [GitHub](https://github.com/ThiagoCF05/NeuralREG) |
| SummEval | Summarization | Fabbri et al., "SummEval: Re-evaluating Summarization Evaluation." TACL 2021. [GitHub](https://github.com/Yale-LILY/SummEval) |
| SEAHORSE | Summarization | Clark et al., "SEAHORSE: A Multilingual, Multifaceted Dataset for Summarization Evaluation." EMNLP 2023. |
| SimpEval (LENS) | Text simplification | Maddela et al., "LENS: A Learnable Evaluation Metric for Text Simplification." ACL 2023. [GitHub](https://github.com/Yao-Dou/LENS) |
| Flickr8k | Image captioning | Hodosh, Young, and Hockenmaier, "Framing Image Description as a Ranking Task." JAIR 2013. |
| THumB 1.0 | Image captioning | Kasai et al., "Transparent Human Evaluation for Image Captioning." NAACL 2022. |
| Book highlights (preference judgment, faithfulness) | LLM-as-judge | Same et al., RetroEval 2026. [Paper](https://aclanthology.org/2026.retroeval-main.6/), [GitHub](https://github.com/fsame/book_summarization_e2e_pipeline) |

<!-- Full source notes, licenses, and download links are in `eval-data-raw/SOURCES.md`. -->

<!-- ## Citation -->
