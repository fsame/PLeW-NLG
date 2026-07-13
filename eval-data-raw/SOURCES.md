# Human evaluation & annotation datasets (raw)

Staging area for **human-eval / meta-eval / annotation** datasets intended for
PLeW-NLG. Files here are **raw downloads only** — not yet mapped into PLeW's
`dim::` / `med::` / `desc::` / `res::` schema. A future data-transformation
skill will handle that step.

Downloaded / organized: 2026-07-11.

For NLG *generation* corpora (WebNLG, ViGGO, etc.) see `data-raw/SOURCES.md`.

---

## Folder index

| Folder | Task | Eval type | Rows (approx.) |
|---|---|---|---|
| `summeval/` | Summarization | Likert quality (4 dims) | 1,600 pairs |
| `hanna/` | Story generation | Likert quality (6 dims) | 19,008 annotations |
| `flickr8k/` | Image captioning | Expert + crowd caption judgments | 5,664 expert + 48k CF pairs |
| `frank/` | Summarization | Hallucination / error taxonomy | 2,246 summaries |
| `wmt-mqm/` | Machine translation | MQM error spans + severity | 150k+ segments (CSV) |
| `dailydialog/` | Dialogue | Dialogue acts + emotions (per utterance) | 11k dialogues (sample: 100) |
| `book_highlights_llm_as_a_judge/` | Book-highlight generation | LLM pairwise preference + faithfulness | 5,448 pairs (+ 1 faithfulness example) |

---

## 1. SummEval (`summeval/`)

**What it is:** Human evaluation of 16 summarization systems on 100 CNN/DailyMail
articles. Each (article × system) summary scored by 3 expert + 5 crowd annotators
on coherence, consistency, fluency, relevance (1–5 Likert).

**Field:** Summarization — human quality evaluation.

**Files:**
- `model_annotations.aligned.jsonl` — 1,600 lines, one JSON object per line.

**Key fields:** `id`, `model_id`, `decoded` (summary text), `expert_annotations`,
`turker_annotations` (lists of per-annotator score dicts), `references`.

**Note:** Source article text is **not** included; only summaries and scores.

**Downloaded from:**
```
https://storage.googleapis.com/sfr-summarization-repo-research/model_annotations.aligned.jsonl
```
(GitHub: [Yale-LILY/SummEval](https://github.com/Yale-LILY/SummEval))

**Citation:** Fabbri et al. "SummEval: Re-evaluating Summarization Evaluation." TACL 2021.

---

## 2. HANNA (`hanna/`)

**What it is:** 1,056 stories (96 prompts × 11 generators incl. human reference),
each annotated by 3 mTurk workers on 6 narrative criteria: Relevance, Coherence,
Empathy, Surprise, Engagement, Complexity (1–5 Likert).

**Field:** Story generation — human quality evaluation.

**Files:**
- `hanna_stories_annotations.csv` — raw per-annotator rows (~19k rows).

**Key columns:** `Story ID`, `Prompt`, `Human`, `Story`, `Model`, six score columns,
`Worker ID`, `Assignment ID`, `Work time in seconds`.

**Downloaded from:**
```
https://raw.githubusercontent.com/dig-team/hanna-benchmark-asg/main/hanna_stories_annotations.csv
```
(GitHub: [dig-team/hanna-benchmark-asg](https://github.com/dig-team/hanna-benchmark-asg))

**Citation:** Chhun et al. "Of Human Criteria and Automatic Metrics: A Benchmark
of the Evaluation of Story Generation." COLING 2022.

---

## 3. Flickr8k human judgments (`flickr8k/`)

**What it is:** Human evaluation of image–caption pairs from the Flickr8k corpus.
Two judgment sets:
- **Flickr8k-Expert** (`ExpertAnnotations.txt`) — 3 expert annotators, 1–4 scale.
- **Flickr8k-CF** (`CrowdFlowerAnnotations.txt`) — crowd yes/no match judgments.

**Field:** Image captioning — multimodal human evaluation.

**Files:**
- `text_extracted/ExpertAnnotations.txt` — expert judgments.
- `text_extracted/CrowdFlowerAnnotations.txt` — crowd judgments.
- `text_extracted/Flickr8k.token.txt` — 5 captions per image.
- `text_extracted/Flickr_8k.{train,dev,test}Images.txt` — split lists.
- `Flickr8k_text.zip` — original archive (kept for provenance).
- `images/flickr8k_00.jpg` … `flickr8k_19.jpg` — 20 local JPEGs (test-split subset).
- `manifest.json` — `{row_idx, captions[5], local image filename}` for the 20 images.

**Note:** Full Flickr8k image corpus is ~1 GB; only 20 demo images are stored
locally. Caption/judgment files cover the full 8k image set.

**Downloaded from:**
```
https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip
```
(Images previously fetched via Hugging Face `intro/flickr8k` datasets-server.)

**License:** Non-commercial research/educational use (University of Illinois terms).

**Citation:** Hodosh et al. "Framing Image Description as a Ranking Task." JAIR 2013.

---

## 4. FRANK (`frank/`)

**What it is:** Factuality benchmark — 2,246 summaries from 9 models on CNN/DM and
XSum, annotated with fine-grained error categories and an overall factuality score.

**Field:** Summarization — hallucination / factual consistency evaluation.

**Files:**
- `benchmark_data.json` — source article, model summary, reference, model name.
- `human_annotations.json` — document-level error counts + `Factuality` score.
- `human_annotations_sentence.json` — sentence-level annotations (3 annotators per
  sentence, error category labels).

**Key fields:** `hash` (join key), `model_name`, `dataset` (cnndm/xsum), error
category fields (`RelE`, `EntE`, `CircE`, …), `Factuality` (0–1).

**Downloaded from:**
```
https://raw.githubusercontent.com/artidoro/frank/main/data/benchmark_data.json
https://raw.githubusercontent.com/artidoro/frank/main/data/human_annotations.json
https://raw.githubusercontent.com/artidoro/frank/main/data/human_annotations_sentence.json
```
(GitHub: [artidoro/frank](https://github.com/artidoro/frank))

**Citation:** Pagnoni et al. "Understanding Factuality in Abstractive Summarization
with FRANK." NAACL 2021.

---

## 5. WMT MQM (`wmt-mqm/`)

**What it is:** Multidimensional Quality Metrics (MQM) human annotations for
machine translation — span-level error markup with category and severity, plus
aggregated segment scores.

**Field:** Machine translation — error taxonomy evaluation.

**Files:**
- `mqm_generalMT2022_ende.tsv` — official WMT 2022 General MT en→de annotations
  (span-level, from Google repo). Use for error-category / severity analysis.
- `wmt_mqm_train.csv` — consolidated CSV (~150k rows) from Hugging Face, with
  columns: `lp`, `src`, `mt`, `ref`, `score`, `system`, `annotators`, `domain`,
  `year`. Aggregated scores only (no span markup).

**Downloaded from:**
```
https://raw.githubusercontent.com/google/wmt-mqm-human-evaluation/main/generalMT2022/ende/mqm_generalMT2022_ende.tsv
https://huggingface.co/datasets/RicardoRei/wmt-mqm-human-evaluation/resolve/main/train.csv
```

**Citation:** Freitag et al. "Results of WMT22 Metrics Shared Task." WMT 2022.
Also: Freitag et al. "Experts, Errors, and Context." TACL 2021.

---

## 6. DailyDialog (`dailydialog/`)

**What it is:** Multi-turn casual dialogues with per-utterance dialogue-act and
emotion labels (integer-coded). Useful as a dialogue-generation eval corpus with
built-in categorical structure.

**Field:** Dialogue — act/emotion annotation (not pairwise quality judgment).

**Files:**
- `dailydialog_train_sample.json` — first 100 dialogues from train split
  (Hugging Face datasets-server format: `{ rows: [{ row: { id, acts, emotions, utterances } }] }`).

**Full dataset:** 11,118 train / 1,000 val / 1,000 test dialogues on HF
`roskoN/dailydialog`.

**Downloaded from:**
```
https://datasets-server.huggingface.co/rows?dataset=roskoN/dailydialog&config=full&split=train&offset=0&length=100
```

**License:** CC BY-NC-SA 4.0.

**Citation:** Li et al. "DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset." IJCNLP 2017.

---

## 7. Book highlights — LLM-as-a-judge (`book_highlights_llm_as_a_judge/`)

**What it is:** Project-specific LLM evaluation of generated book "highlights"
(blurb-style snippets). Pairwise A/B preference judgments and single-candidate
faithfulness checks.

**Field:** Data-to-text (book marketing copy) — LLM-as-judge evaluation.

**Files:**
- `llm_judge_preference.json` — 5,448 pairwise comparisons. Each record: two
  candidate texts, 5 criteria + overall preference (winner A/B/tie, confidence,
  rationale), comparison metadata (architecture vs size axis, blinded order).
- `llm_judge_faithfulness.json` — single-record example of factuality check
  (`factually_accurate`, `divergence_type`, `severity`, `rationale`).

**Note:** Provided by user; not a public benchmark. `pair_id` links preference
and faithfulness records.

---

## Next step

Build a data-transformation skill (or script) that maps each folder's raw format
into PLeW-ready CSV with explicit `dim::` / `desc::` / `med::` columns. See
design notes in project chat for per-dataset melt/join strategies.
