# Raw dataset sources

Raw, uncurated downloads for the PLeW-NLG dataset-compilation demo (INLG 2026). Everything in this
folder is **staging material** — not yet mapped into PLeW's `dim::`/`med::`/`desc::`/`res::`
schema. Curated, PLeW-ready CSVs will live in `static/data/` and their Hugo pages in
`content/examples/`, built from a *subset* of what's downloaded here.

Downloaded: 2026-07-10.

---

## 1. WebNLG (`webnlg/`)

**What it is:** RDF triples → English text. Each entry is a small set of DBpedia triples (1-7)
that share a connected subgraph, paired with 1+ crowdsourced verbalizations. Classic structured
data-to-text benchmark (WebNLG Challenge, INLG 2017 / WebNLG+ 2020).

**Field:** Structured data-to-text generation.

**Downloaded from:** Hugging Face `datasets-server` REST API, mirroring the GEM benchmark's
`GEM/web_nlg` dataset (itself a repackaging of the official WebNLG v3.0 release from
[gitlab.com/shimorina/webnlg-dataset](https://gitlab.com/shimorina/webnlg-dataset)).
```
https://datasets-server.huggingface.co/rows?dataset=GEM/web_nlg&config=en&split=train&offset=0&length=100
```
**File:** `webnlg_en_train_sample.json` — first 100 rows of the English train split.

**Fields of interest:** `input` (list of RDF triples as strings), `target` (verbalization),
`category` (DBpedia domain, e.g. Airport, Astronaut), `webnlg_id`.

**License:** CC BY-NC-SA 4.0 (per WebNLG project license — non-commercial, share-alike; fine for
an academic demo, cite the WebNLG Challenge papers).

**Citation:** Gardent, Shimorina, Narayan, Perez-Beltrachini. "The WebNLG Challenge: Generating
Text from RDF Data." INLG 2017. / Castro Ferreira et al., WebNLG+ 2020 shared task overview.

---

## 2. ViGGO (`viggo/`)

**What it is:** ~6,900 meaning-representation → conversational-utterance pairs about video games
(9 dialogue-act types: inform, request, give_opinion, etc.), covering 100+ games with
game-specific slots (genre, platform, release year, rating...). Designed for chatbot-style NLG,
more conversational than typical slot-filling corpora.

**Field:** Structured data-to-text generation (conversational/open-domain NLG).

**Downloaded from:** Hugging Face `datasets-server` REST API, mirroring the GEM benchmark's
`GEM/viggo` dataset (the original dataset requires filling out a request form at
[nlds.soe.ucsc.edu/viggo](https://nlds.soe.ucsc.edu/viggo); the GEM mirror does not).
```
https://datasets-server.huggingface.co/rows?dataset=GEM/viggo&config=default&split=train&offset=0&length=100
```
**File:** `viggo_train_sample.json` — first 100 rows of the train split.

**Fields of interest:** `meaning_representation` (DA + slot-value string, e.g.
`inform(name[Dirt: Showdown], release_year[2012], ...)`), `target` (utterance), `gem_id`.

**License:** CC BY-SA 4.0 (redistribution-friendly).

**Citation:** Juraska, Bowden, Walker. "ViGGO: A Video Game Corpus for Data-To-Text Generation
in Open-Domain Conversation." INLG 2019.

---

## 3. SummEval (`summeval/`)

**What it is:** Human evaluation of 16 summarization systems on 100 CNN/DailyMail articles
(1,600 system outputs total), each scored by 3 expert + 5 crowd annotators along 4 dimensions:
coherence, consistency, fluency, relevance (1-5 Likert). One of the most-used meta-evaluation
sets in summarization/NLG-eval research.

**Field:** Human evaluation / meta-evaluation of NLG systems (summarization).

**Downloaded from:** official public annotation file linked from
[github.com/Yale-LILY/SummEval](https://github.com/Yale-LILY/SummEval):
```
https://storage.googleapis.com/sfr-summarization-repo-research/model_annotations.aligned.jsonl
```
**File:** `model_annotations.aligned.jsonl` — full file, 1,600 lines (one per article×system pair).

**Fields of interest:** `id` (article id), `model_id` (system name), `decoded` (system summary),
`expert_annotations` / `turker_annotations` (lists of per-annotator score dicts with `coherence`,
`consistency`, `fluency`, `relevance`), `references` (reference/human summaries — note: the
**original source article text is not included** in this file by design; SummEval ships model
outputs and annotations only, and expects pairing with a separately-downloaded CNN/DailyMail
corpus for the source text).

**License:** research use per SummEval repo (no explicit OSS license file; standard academic
redistribution norms, cite the paper).

**Citation:** Fabbri, Kryscinski, McCann, Xiong, Socher, Radev. "SummEval: Re-evaluating
Summarization Evaluation." TACL 2021.

---

## 4. FRANK (`frank/`)

**What it is:** Factuality/hallucination benchmark: 2,250 summaries from 9 summarization models
on CNN/DailyMail and XSum articles, annotated with a fine-grained typology of factual-error
categories (semantic frame, discourse, content-verifiability errors, and sub-types like entity,
predicate, circumstance errors) plus an overall factuality score.

**Field:** Human evaluation / meta-evaluation (factual consistency / hallucination detection).

**Downloaded from:** [github.com/artidoro/frank](https://github.com/artidoro/frank), `data/` folder
(raw GitHub content, no form/gate):
```
https://raw.githubusercontent.com/artidoro/frank/main/data/benchmark_data.json
https://raw.githubusercontent.com/artidoro/frank/main/data/human_annotations.json
```
**Files:**
- `benchmark_data.json` — 2,246 records with `hash`, `model_name`, `article` (**full source text,
  included**), `summary` (model output), `reference`.
- `human_annotations.json` — 2,246 records, joinable on `hash`, with `Factuality` (0-1 score) and
  per-category error counts (`RelE`, `EntE`, `CircE`, `OutE`, `GramE`, `CorefE`, `LinkE`, `Other`,
  plus `Flip_*` ablation fields), `dataset` (cnndm / xsum), `split`.

**License:** research use per repo (no explicit license file; cite the paper, standard academic
redistribution norms — note articles are themselves sourced from CNN/DailyMail and XSum).

**Citation:** Pagnoni, Balachandran, Tsvetkov. "Understanding Factuality in Abstractive
Summarization with FRANK: A Benchmark for Factuality Metrics." NAACL 2021.

---

## 5. Flickr8k (`flickr8k/`)

**What it is:** 8,092 photographs (everyday scenes, no celebrities/landmarks), each with 5
independently crowdsourced English captions. One of the most widely used image-captioning
benchmarks pre-COCO.

**Field:** Multimodal / grounded generation (image captioning).

**Downloaded from:** Hugging Face `datasets-server` REST API (image assets + metadata), mirroring
`intro/flickr8k` (an `imagefolder`-formatted repackaging of the original Flickr8k corpus, whose
official distribution point at University of Illinois now requires a request form):
```
https://datasets-server.huggingface.co/rows?dataset=intro/flickr8k&config=default&split=test&offset=0&length=20
```
**Files:**
- `flickr8k_test_sample_meta.json` — row metadata (signed, time-limited image URLs + all 5 captions
  per image) for the first 20 rows of the `test` split.
- `manifest.json` — cleaned-up `{row_idx, image_url, width, height, captions[5]}` list derived
  from the above.
- `images/flickr8k_00.jpg` … `flickr8k_19.jpg` — the 20 actual JPEG files, downloaded locally
  (~650 KB total) so the curated PLeW example stays fully offline, consistent with the tool's
  no-server philosophy.

**License:** original Flickr8k images/captions are distributed for **non-commercial
research/educational use only** (University of Illinois terms); this demo/academic use qualifies,
but the images should not be redistributed for commercial purposes. CC0 tag on the HF mirror
refers to the repackaging, not underlying photo rights.

**Citation:** Hodosh, Young, Hockenmaier. "Framing Image Description as a Ranking Task: Data,
Models and Evaluation Metrics." JAIR 2013.

---

## Next step

Curate a small (~15-25 row) subset of each into PLeW's `dim::`/`med::`/`desc::`/`res::` CSV
schema under `static/data/`, with a matching `content/examples/*.md` page — see the plan agreed
in chat before building each one.
