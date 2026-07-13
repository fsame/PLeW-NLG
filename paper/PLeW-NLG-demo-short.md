# PLeW-NLG: Interactive Exploration of Human Evaluation Data across NLG Tasks

> **Status:** condensed draft for INLG 2026 demo track — sized for 2 pages
> (incl. references) in ACL format. Companion to the fuller
> `PLeW-NLG-demo-draft.md`. `[cite:…]` = citation placeholder.

---

## Abstract

Human evaluation results in NLG are usually released only as aggregate score
tables, detached from the judgments and texts they summarize, and reported
under heterogeneous protocols that differ across subfields. We present
**PLeW-NLG**, a browser-based tool that maps judgment-level evaluation data
onto an interactive grid of scatter plots — up to six categorical dimensions
at once — with per-record inspection of source and generated text, in-place
annotation editing with an auditable change log, and exportable, reproducible
views. To handle the many shapes evaluation data takes, we release a
dataset-agnostic transformation skill and a curated suite of public
human-evaluation datasets spanning several NLG tasks.

## 1 Introduction

Human evaluation is standard practice in NLG [cite:vanderlee2019best;
cite:howcroft2020twenty], but two problems limit how much we learn from it.
First, **practices are heterogeneous**: criteria, scales (Likert, sliders,
pairwise, MQM spans), and terminology vary across subfields, and
standardization efforts [cite:howcroft2020twenty; cite:belz2021reprogen;
cite:gehrmann2021gem] are only partially adopted. Second, results are
**detached from the data**: readers see mean scores per system and a few
inline examples, while judgment-level files — if released at all — sit in
CSV/JSON that require scripting to explore. Basic questions (Where do
annotators disagree? Which input categories drive low fluency?) stay
unanswered.

**PLeW-NLG** targets the consumption side. It lets researchers (1) *visualize*
judgment-level data across dimensions (system, criterion, annotator, domain),
(2) *inspect* any point down to its full text and media, and (3) *edit*
annotations in place with a persistent, exportable change log. To absorb the
heterogeneity of released files, we pair the tool with a reusable
**transformation skill** and demonstrate it on a curated set of public
human-evaluation datasets across NLG tasks.

## 2 Interface

PLeW is a static, install-free web app that ingests flat CSV/JSON whose
columns carry four role prefixes: `dim::` (categorical axes), `desc::` (long
text for the record window), `med::` (image/audio/video), `res::` (numeric
results). The first six `dim::` columns map to grid X/Y, color, panel X/Y, and
shape. For a typical (item × system × criterion × annotator) file, placing
*system* × *criterion* on the grid, *score* as color, and *annotator* as
panels exposes disagreement and per-category weaknesses at once; dimensions
are re-mapped by drag-and-drop. Values can be filtered from the legends (the
dimension list shows *3 of 4 values*), points open a record window with full
source/generated text and media, and points can be dragged to reclassify
annotations — every edit logged with undo/redo and CSV/JSON export. The whole
view (dimensions, filters, colors) exports as JSON and re-imports for
reproducible, shareable figures.

## 3 Methodology

**Dataset selection.** We focus on human-evaluation data: it is the
underexploited artifact our tool targets, and its structure (a few categorical
dimensions around long, unique text) suits PLeW. We use the GEM benchmark data
cards [cite:gehrmann2021gem] as a curated, multi-task seed taxonomy, then
search the ACL Anthology (2022+) for papers that both evaluate a GEM dataset
with humans and release the judgments, combining dataset names (*XSum, WebNLG,
ToTTo, ASSET, CommonGen, …*) with evaluation terms (*human evaluation,
annotations, ratings, error analysis*) and release cues. Candidates are scored
on a 1–5 suitability scale favouring per-(item × system × criterion ×
annotator) granularity and inspectable text, yielding sources such as SEAHORSE
[cite:clark2023seahorse], SimpEval [cite:maddela2023lens], RoSE
[cite:liu2023rose], and WebNLG 2017 [cite:shimorina2018webnlg], plus SummEval
[cite:fabbri2021summeval] and FRANK [cite:pagnoni2021frank].

**Transformation skill.** Released files vary widely, so we package conversion
as a dataset-agnostic skill, `plew-prepare-dataset`, that (1) profiles the
data (cardinality, uniqueness, length, nesting, media), (2) applies a
pass/marginal/fail suitability gate, (3) reshapes via a small pattern library
(melt criteria to long form, explode per-annotator arrays, join
content/annotation files, resolve blinded pairwise winners), (4) assigns
prefixes by inferred role rather than column name, and (5) subsets to demo
scale with a fixed seed — emitting a validated `PLEW_READY.csv`, a reproducible
`transform.py`, and a documenting manifest.

## 4 Case studies & availability (TODO)

<!-- 3–4 sentences + one figure: e.g., WebNLG 2017 view surfacing annotator
disagreement and seen/unseen category effects invisible in aggregate tables;
tool URL + screencast; catalog/skill release. -->

---

## Length notes

- Keep §1 + §2 + §3 to ~1.2 pages; §4 + one figure ~0.5 page; references ~0.3.
- First cut if over length: dataset name list in §3, the record-window detail
  in §2.
