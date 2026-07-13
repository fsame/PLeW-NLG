# GEM human-evaluation catalog (ACL Anthology 2022+)

Curated papers that **conduct human evaluation** on datasets listed on the [GEM data cards](https://gem-benchmark.com/data_cards), with download links and PLeW curation notes.

**Scope:** ACL Anthology, 2022 onwards (plus a few closely related TACL / INLG GenChal papers).  
**Goal:** Prioritize sources where **human judgments are released** in a shape that can become `dim::` / `desc::` / `med::` / `res::` rows for PLeW.

---

## PLeW suitability score (1–5)

| Score | Meaning |
|------:|---------|
| **5** | Public per-(item × system × criterion × annotator) judgments; long generated text + structured scores; demo-friendly after melt/join |
| **4** | Public judgments with minor gaps (e.g. source article via separate GEM/HF join; aggregated min/avg/max only) |
| **3** | Human eval + partial release, or span/error taxonomy rather than Likert; needs non-trivial reshape |
| **2** | Human eval reported in paper; raw annotations not clearly public |
| **1** | Protocol / meta-eval / shared-task overview only |

---

## Priority download checklist

Suggested staging folders under `eval-data-raw/`. **Status** reflects this repo as of 2026-07-11.

| Priority | Staging folder | GEM dataset(s) | PLeW | Status | Next action |
|:--:|---|---|:--:|---|---|
| **P1** | `seahorse/` | xsum, xlsum, mlsum, wiki_lingua | 5 | not downloaded | Download [seahorse_data.zip](https://storage.googleapis.com/seahorse-public/seahorse_data.zip); join source articles via `gem_id` → [GEM HF datasets](https://huggingface.co/GEM) |
| **P1** | `simpeval/` | wiki_auto_asset_turk (ASSET) | 5 | not downloaded | Clone [Yao-Dou/LENS](https://github.com/Yao-Dou/LENS) `data/` or HF [tasksource/simpeval](https://huggingface.co/datasets/tasksource/simpeval) |
| **P1** | `mface/` | xlsum | 4 | not downloaded | Download [Google Drive spreadsheet](https://drive.google.com/file/d/1fsIK2pLMnzeIYlVH3j4APVBdxz-Zu6V0/view) (CC BY-NC-SA 4.0) |
| **P1** | `rose/` | xsum | 5 | not downloaded | `load_dataset("Salesforce/rose", "xsum")` — [HF](https://huggingface.co/datasets/Salesforce/rose) |
| **P1** | `zhang2024_news_summ/` | xsum | 4 | not downloaded | Clone [Tiiiger/benchmark_llm_summarization](https://github.com/Tiiiger/benchmark_llm_summarization) (also has cnndm; not a GEM card) |
| **P2** | `heap/` | common_gen | 4 | not downloaded | Clone [Shuhaibm/heap](https://github.com/Shuhaibm/heap) (pairwise comparative judgments, 22 criteria) |
| **P2** | `seq2seq_mqm/` | e2e_nlg, web_nlg, totto | 4 | not downloaded | Clone [xunjianyin/Seq2SeqOnData2Text](https://github.com/xunjianyin/Seq2SeqOnData2Text) (MQM error spans × severity) |
| **P2** | `webnlg2017_humaneval/` | web_nlg | 5 | not downloaded | [GitLab webnlg-human-evaluation](https://gitlab.com/webnlg/webnlg-human-evaluation) — **2017** challenge (pre-2022 but best public WebNLG human-eval CSV) |
| **P2** | `assetann/` | wiki_auto_asset_turk (ASSET) | 3 | not downloaded | Clone [remicardon/assetann](https://github.com/remicardon/assetann) (linguistic operation spans, not quality Likert) |
| **P3** | `webnlg2023_humaneval/` | web_nlg | 2 | not downloaded | Protocol: [nlgcat/webnlg2023_human_eval_preregistration](https://github.com/nlgcat/webnlg2023_human_eval_preregistration); **raw 2023 per-rater CSV not public** — email organizers or scrape from [2025.findings-acl.542](https://aclanthology.org/2025.findings-acl.542/) if they share |
| **P3** | `gem24_humaneval/` | web_nlg (+ new FA/CFA/FI sets) | 2 | not downloaded | Read [2025.inlg-genchal.1](https://aclanthology.org/2025.inlg-genchal.1/); contact GEM organizers for raw ratings (paper has aggregated tables) |
| **P3** | `totto_errors/` | totto | 3 | not downloaded | Guidelines/samples: [BarkaviSJ/totto_politics_human_annotations](https://github.com/BarkaviSJ/totto_politics_human_annotations) (docx; full 3k spans may need author request) |
| **P3** | `genie_xsum/` | xsum | 3 | not downloaded | Leaderboard pipeline [genie.apps.allenai.org](https://genie.apps.allenai.org); bulk export unclear — may need submission export |
| **P4** | — | dart | 2 | skip for now | [2022.gem-1.50](https://aclanthology.org/2022.gem-1.50/) — small author annotation, no release |
| **P4** | — | common_gen | 2 | skip for now | [2022.findings-naacl.129](https://aclanthology.org/2022.findings-naacl.129/), [2024.findings-emnlp.492](https://aclanthology.org/2024.findings-emnlp.492/) — eval only, no release |

### Already staged (strong PLeW sources, **not** GEM data cards)

| Folder | Field | PLeW | Notes |
|---|---|:--:|---|
| `summeval/` | Summarization (CNN/DM) | 5 | Done → `PLEW_READY.csv` |
| `frank/` | Summarization factuality | 5 | Done → `PLEW_READY.csv` |
| `hanna/` | Story generation | 5 | Raw CSV ready |
| `flickr8k/` | Image captioning | 5 | Raw + 20 images |
| `book_highlights_llm_as_a_judge/` | Custom D2T / LLM judge | 4 | Pairwise preference JSON |

---

## Master table (GEM datasets × human-eval papers)

GEM card name = slug on [gem-benchmark.com/data_cards](https://gem-benchmark.com/data_cards).

| NLG field | GEM dataset | Paper | Year | ACL link | Download / repo | ~Scale | Judgment type | Releases raw judgments? | PLeW | Planned folder |
|---|---|---|---|---|---|---|:--:|:--:|:--:|---|
| Summarization | **xsum**, **xlsum**, **mlsum**, **wiki_lingua** | SEAHORSE: A Multilingual, Multifaceted Dataset for Summarization Evaluation (Clark et al.) | 2023 | [2023.emnlp-main.584](https://aclanthology.org/2023.emnlp-main.584/) | [GitHub](https://github.com/google-research-datasets/seahorse) · [ZIP](https://storage.googleapis.com/seahorse-public/seahorse_data.zip) · [HF SEACrowd/seahorse](https://huggingface.co/datasets/SEACrowd/seahorse) | ~96K ratings | Yes/No/unsure × 6 criteria × 9 systems | **Yes** | 5 | `seahorse/` |
| Summarization | **xlsum** | Multilingual Summarization with Factual Consistency Evaluation / mFACE (Aharoni et al.) | 2023 | [2023.findings-acl.220](https://aclanthology.org/2023.findings-acl.220/) | [google-research/mface README](https://github.com/google-research/google-research/tree/master/mface) · [Drive CSV](https://drive.google.com/file/d/1fsIK2pLMnzeIYlVH3j4APVBdxz-Zu6V0/view) | ~31.5K summaries | Quality, attribution, informativeness (min/avg/max) | **Yes** (aggregated per summary) | 4 | `mface/` |
| Summarization | **xsum** (+ CNN/DM, SamSum — latter not GEM) | Revisiting the Gold Standard: RoSE (Liu et al.) | 2023 | [2023.acl-long.228](https://aclanthology.org/2023.acl-long.228/) | [Yale-LILY/ROSE](https://github.com/Yale-LILY/ROSE) · [HF Salesforce/rose](https://huggingface.co/datasets/Salesforce/rose) (`xsum` split) | ~4K summaries (XSum test) | ACU + 4 protocol variants | **Yes** | 5 | `rose/` |
| Summarization | **xsum** | Benchmarking LLMs for News Summarization (Zhang et al.) | 2024 | [2024.tacl-1.3](https://aclanthology.org/2024.tacl-1.3/) | [Tiiiger/benchmark_llm_summarization](https://github.com/Tiiiger/benchmark_llm_summarization) | 100 articles × models (Likert subset) | Faithfulness, coherence, relevance + pairwise | **Yes** | 4 | `zhang2024_news_summ/` |
| Summarization | **xsum** | GENIE: Toward Reproducible Human Evaluation (Khashabi et al.) | 2022 | [2022.emnlp-main.787](https://aclanthology.org/2022.emnlp-main.787/) | [genie.apps.allenai.org](https://genie.apps.allenai.org) · [allenai/genie-worker-scoring](https://github.com/allenai/genie-worker-scoring) | Leaderboard-scale | Likert (fluency, conciseness, correctness, …) | **Partial** (via leaderboard) | 3 | `genie_xsum/` |
| Simplification | **wiki_auto_asset_turk** (ASSET test) | LENS / SimpEval (Maddela et al.) | 2023 | [2023.acl-long.905](https://aclanthology.org/2023.acl-long.905/) | [Yao-Dou/LENS](https://github.com/Yao-Dou/LENS) · [HF tasksource/simpeval](https://huggingface.co/datasets/tasksource/simpeval) | ~13K ratings | 0–100 overall quality (Rank & Rate) | **Yes** | 5 | `simpeval/` |
| Simplification | **wiki_auto_asset_turk** (ASSET) | Linguistic Corpus Annotation for ATS Evaluation / ASSETann (Cardon et al.) | 2022 | [2022.emnlp-main.121](https://aclanthology.org/2022.emnlp-main.121/) | [remicardon/assetann](https://github.com/remicardon/assetann) | ASSET test pairs | Linguistic operation labels (9 annotators) | **Yes** | 3 | `assetann/` |
| Simplification | **wiki_auto_asset_turk** | Meta-Evaluation of Sentence Simplification Metrics (LREC) | 2024 | [2024.lrec-main.981](https://aclanthology.org/2024.lrec-main.981/) | Uses SimpEval + NEWSELA-Likert (not GEM) | meta-study | Reuses SimpEval | Reuses | 2 | — |
| Data-to-text | **web_nlg** | WebNLG 2023 Shared Task overview (Cripwell et al.) | 2023 | [2023.mmnlg-1.6](https://aclanthology.org/2023.mmnlg-1.6/) | [WebNLG/2023-Challenge](https://github.com/WebNLG/2023-Challenge/) · [eval prereg](https://github.com/nlgcat/webnlg2023_human_eval_preregistration) | 100 inputs × systems × langs | Fluency (1–5); additions/omissions/repetition (Y/N) | **No** (aggregated in paper) | 2 | `webnlg2023_humaneval/` |
| Data-to-text | **web_nlg** | Semantic Evaluation of Multilingual KG-to-Text via NLI (Findings ACL) | 2025 | [2025.findings-acl.542](https://aclanthology.org/2025.findings-acl.542/) | Uses WebNLG 2017/2020/2023 annotations (see repos below) | WebNLG 2023 subset | Same as 2023 task | **Unclear** | 2 | — |
| Data-to-text | **web_nlg** | WebNLG 2017 human eval (Shimorina et al.) — *pre-2022 but best public CSV* | 2018 report | [HAL report](https://hal.archives-ouvertes.fr/hal-03007072) | [GitLab webnlg-human-evaluation](https://gitlab.com/webnlg/webnlg-human-evaluation) (`all_data_final_scores_anonymised.csv`) | 223 pairs × 9 systems | Fluency, grammar, semantics | **Yes** | 5 | `webnlg2017_humaneval/` |
| Data-to-text | **web_nlg** (+ novel FA/CFA/FI) | GEM 2024 Shared Task — human eval results (Sedoc et al.) | 2025 | [2025.inlg-genchal.1](https://aclanthology.org/2025.inlg-genchal.1/) | Overview: [2024.inlg-genchal.2](https://aclanthology.org/2024.inlg-genchal.2/) · sampling code: [mille-s/GEM24_D2T_StratifiedSampling](https://github.com/mille-s/GEM24_D2T_StratifiedSampling) | EN+ES D2T subsets | Fluency, grammaticality, no-omissions, no-additions (1–7) | **Partial** (tables in proc.) | 2 | `gem24_humaneval/` |
| Data-to-text | **e2e_nlg**, **web_nlg**, **totto** | How Do Seq2Seq Models Perform on E2E D2T? (Yin et al.) | 2022 | [2022.acl-long.531](https://aclanthology.org/2022.acl-long.531/) | [xunjianyin/Seq2SeqOnData2Text](https://github.com/xunjianyin/Seq2SeqOnData2Text) | 4 datasets × 5 models | MQM-style error types + severity | **Yes** | 4 | `seq2seq_mqm/` |
| Data-to-text | **totto** | Error Analysis of ToTTo Neural NLG Models (Sundararajan et al.) | 2022 | [2022.gem-1.43](https://aclanthology.org/2022.gem-1.43/) | [BarkaviSJ/totto_politics_human_annotations](https://github.com/BarkaviSJ/totto_politics_human_annotations) (guidelines + samples) | 3,016 Politics outputs | 8 error categories (span-level) | **Partial** | 3 | `totto_errors/` |
| Data-to-text | **dart** | What Makes D2T Hard for PLMs? (Chowdhury et al.) | 2022 | [2022.gem-1.50](https://aclanthology.org/2022.gem-1.50/) | Paper only | DART subsets | Hallucination, missing info, fluency (Likert) | **No** | 2 | — |
| Reasoning | **common_gen** | HEAP — Automatic Evaluation with Instruction Tuning (Mehri & Shwartz) | 2023 | [2023.gem-1.4](https://aclanthology.org/2023.gem-1.4/) | [Shuhaibm/heap](https://github.com/Shuhaibm/heap) | ~1,079 CR pairs | Pairwise better/worse (22 criteria total corpus) | **Yes** | 4 | `heap/` |
| Reasoning | **common_gen** | Revisiting Generative Commonsense Reasoning (Yu et al.) | 2022 | [2022.findings-naacl.129](https://aclanthology.org/2022.findings-naacl.129/) | Paper only | 100 test instances | Likert quality | **No** | 2 | — |
| Reasoning | **common_gen** | Compositional Generalization in Graph-based CR (EMNLP Findings) | 2024 | [2024.findings-emnlp.492](https://aclanthology.org/2024.findings-emnlp.492/) | Paper only | 400 samples | Plausibility / concept coverage | **No** | 2 | — |
| Dialog | **schema_guided_dialog**, **viggo**, etc. | Evaluation of Response Generation Models (Mousavi et al.) | 2022 | [2022.gem-1.12](https://aclanthology.org/2022.gem-1.12/) | [Protocol repo linked in paper](https://aclanthology.org/2022.gem-1.12/) | Demo eval | Response quality protocol | **Protocol** | 1 | — |
| Dialog | **viggo** | Controllable Dialogue Acts via Few-Shot Ranking (SIGDIAL) | 2023 | [2023.sigdial-1.32](https://aclanthology.org/2023.sigdial-1.32/) | Paper only | 100 outputs | Expert perfect/hallucination check | **No** | 2 | — |
| Summarization | *(not GEM cards)* arXiv, CNN/DM, … | Multi-domain Summarization from Leaderboards to Practice (Demeter et al.) | 2023 | [2023.gem-1.20](https://aclanthology.org/2023.gem-1.20/) | Paper only | 60 docs × 3 annotators | Readability, recall, precision, hallucination | **No** | 2 | — |

---

## Thin coverage on GEM cards (2022+ ACL, little or no released human eval)

Worth knowing for breadth; lower priority until a compilation paper appears:

| NLG field | GEM datasets with sparse released human eval |
|---|---|
| Question generation | fairytaleqa, squad_v2 |
| Paraphrasing | opusparcus, turku_paraphrase_corpus |
| Dialog | CrossWOZ, cs_restaurants, dstc10_track2_task2, RiSAWOZ, schema_guided_dialog, Taskmaster |
| Data-to-text | conversational_weather, e2e_nlg (except Seq2Seq MQM), mlb_data_to_text, sportsett_basketball, turku_hockey, surface_realisation_st_2020, RotoWire_English-German |
| Simplification | BiSECT, cochrane-simplification, SIMPITIKI |
| Summarization | indonlg, OrangeSum, squality, wiki_cat_sum, xwikis |
| Other | ART, SciDuet |

---

## Suggested PLeW row shapes (top picks)

| Source | Granularity | Good `dim::` axes | `desc::` | `res::` |
|---|---|---|---|---|
| SEAHORSE | article × system × criterion × (single rater) | `dataset`, `language`, `system`, `criterion`, `rating` | `summary` (+ join `article` via GEM) | optional duplicate of rating |
| SimpEval | sentence × system × rater | `system`, `split`, `annotator` | `source`, `simplification` | `score` (0–100) |
| mFACE | doc × system × criterion | `lang`, `system`, `criterion` | `input`, `summary` | `avg` / min / max |
| RoSE (xsum) | doc × system × protocol | `system`, `protocol`, `metric` | `summary`, `source` | ACU-based scores |
| Seq2Seq MQM | output × error span | `dataset`, `model`, `error_type`, `severity` | `output`, `span` | error count |
| HEAP | pair × criterion | `source_task`, `criterion`, `winner` | `good_text`, `bad_text`, `context` | implicit in pair |

---

## License notes

| Resource | License / constraint |
|---|---|
| SEAHORSE | CC BY 4.0 |
| mFACE, XLSum | [CC BY-NC-SA 4.0](https://huggingface.co/datasets/csebuetnlp/xlsum) |
| RoSE | Check HF dataset card |
| WebNLG 2023 challenge data | Request via [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfytc1rUMUOKrDc9vV658uiLh1_jUS7G0XesylaOLrfDYqXBA/viewform) |
| Flickr8k (already staged) | Non-commercial |

---

## References

- GEM data cards: https://gem-benchmark.com/data_cards  
- GEM shared task 2024: https://gem-benchmark.com/shared_task  
- Existing non-GEM staging index: [SOURCES.md](./SOURCES.md)  
- PLeW transform skill: [.cursor/skills/plew-prepare-dataset/SKILL.md](../.cursor/skills/plew-prepare-dataset/SKILL.md)
