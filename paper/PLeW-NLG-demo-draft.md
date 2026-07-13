# PLeW-NLG: Interactive Exploration of Human Evaluation Data across NLG Tasks

> **Status:** working draft for INLG 2026 demo track (2 pages + references).
> Citation placeholders are marked `[cite:…]`. Sections marked `TODO` are stubs.

---

## Abstract (TODO)

<!-- 3–4 sentences: problem (aggregated, heterogeneous NLG human-eval reporting),
tool (PLeW-NLG: browser-based multidimensional exploration of per-judgment data),
resource (curated suite of transformed human-eval datasets + transformation skill),
availability (URL / screencast). -->

---

## 1 Introduction

Evaluation is a central practice in natural language generation (NLG): virtually
every system paper reports automatic metrics, and a large share additionally
report human judgments of output quality [cite:vanderlee2019best; cite:howcroft2020twenty].
Yet the way these evaluations are conducted and, crucially, the way their
results are *communicated* suffer from two persistent issues.

**Heterogeneous evaluation practices.** NLG spans diverse subfields —
data-to-text generation, summarization, text simplification, dialogue response
generation, image captioning, commonsense generation — each with its own
evaluation traditions, criteria, and terminology. The same underlying notion
surfaces as *fluency*, *readability*, or *naturalness*; quality is elicited as
Likert ratings, 0–100 slider scores, pairwise preferences, or span-level error
annotations in MQM-style taxonomies [cite:howcroft2020twenty; cite:freitag2021mqm].
Standardization efforts exist — shared terminology and reporting guidelines
[cite:howcroft2020twenty; cite:shimorina2022heds], reproducibility initiatives
[cite:belz2021reprogen], and benchmark ecosystems such as GEM
[cite:gehrmann2021gem] — but their adoption remains partial, and published
evaluations continue to differ in granularity, scale design, and released
artifacts.

**Detachment from the actual data.** Human evaluation results are almost
always consumed as *aggregates*: a table of mean scores per system, a
significance marker, sometimes a handful of cherry-picked examples in the
running text. The judgment-level data — which annotator gave which score to
which output, and how the underlying text reads — is at best released as raw
CSV or JSON files that require scripting to inspect. This detachment makes it
hard to ask basic questions of the data: Where do annotators disagree? Are
low fluency scores concentrated in a particular input category or output
length band? Does a system's semantic-adequacy advantage hold across seen and
unseen inputs?

**PLeW-NLG** addresses both issues from the consumption side. PLeW (a
browser-based, dependency-free visualization tool) renders flat annotated
data as a grid of scatter plots in which up to six categorical dimensions are
mapped simultaneously to grid axes, panel axes, color, and shape. Applied to
NLG human-evaluation data, it lets researchers (1) *visualize* judgment-level
results across dimensions such as system, criterion, annotator, and input
category; (2) *inspect* every point down to the full source input, generated
text, and media in a record window; and (3) *edit* annotation values directly
in the interface — e.g., when re-annotating or correcting — with a persistent,
exportable change log that supports auditable revision. Visualization
configurations (dimension order, filters, color/shape assignments) can be
exported and re-imported as JSON, making a specific analytical view of an
evaluation dataset reproducible and shareable.

Because evaluation datasets arrive in heterogeneous shapes — nested JSON,
wide CSVs with one column per criterion, pairwise preference records — we
additionally provide a reusable, dataset-agnostic **transformation skill**
that profiles an arbitrary evaluation dataset, decides whether it is suitable
for grid exploration, and reshapes it into PLeW's simple column-prefix schema.
We demonstrate the pipeline on a curated suite of publicly released human
evaluations covering data-to-text, summarization, simplification, and more.

## 2 Interface

PLeW runs entirely in the browser as a static site (Hugo); no server-side
processing or installation beyond a local web server is required. It ingests
flat CSV or JSON/JSONL files whose columns are role-annotated with four
lightweight prefixes: `dim::` for low-cardinality categorical dimensions
(system, criterion, score band, domain), `desc::` for long text shown in the
record window (source input, generated output, rationales), `med::` for
image/audio/video attachments, and `res::` for numeric results (raw scores,
automatic metrics). Unprefixed data remains usable through fallback
heuristics.

**Multidimensional grid.** The first six enabled dimensions are mapped to
grid X, grid Y, color, panel X, panel Y, and shape. For a typical evaluation
dataset — one row per (item × system × criterion × annotator) judgment — a
natural view places *system* against *criterion* on the outer grid, colors
points by *score*, and panels by *annotator* or input *category*, exposing
disagreement patterns and per-category weaknesses at a glance. Dimensions are
reordered by drag-and-drop, so switching analytical perspective takes seconds
rather than a plotting-script edit.

**Filtering and legends.** Every dimension value can be toggled on or off,
including directly from the color and shape legends; the dimension list
reports visible counts (e.g., *3 of 4 values*). This supports drill-down on,
say, only the lowest scores or a single system pair.

**Record-level inspection.** Hovering a point shows its dimension values;
clicking opens a record window with all `desc::` fields (full source text,
generated text, references) and `res::` values, plus media popups for
`med::` columns — reconnecting the aggregate view with the underlying data.

**Annotation editing with audit trail.** Points can be dragged between cells
to reclassify them (e.g., correcting an error-category label), or edited via
context menu. All modifications are recorded in a change log with timestamps,
undo/redo support, and CSV/JSON export; the edited dataset can be downloaded
for downstream use. Anchor rows preserve the full value space of each
dimension so that categories are not silently lost during editing.

**Reproducible views.** The full visualization setup — dimension order and
selection, value filters, custom colors/shapes, display options — can be
exported as a small JSON file and re-imported later or by another user,
enabling replicable figures and shareable "analysis states" alongside the
data.

## 3 Methodology

### 3.1 Dataset selection

We focus on **human evaluation data** for two reasons. First, human judgments
remain the gold standard of NLG evaluation, yet released judgment files are
rarely explored beyond the aggregate tables of the original paper; they are
exactly the underexploited artifact our tool targets. Second, human-eval data
has the structural profile PLeW handles best: a few low-cardinality
categorical dimensions (system, criterion, annotator, domain) wrapped around
long, unique text that belongs in a record window rather than on an axis.

As a seed taxonomy we use the **GEM benchmark data cards**
([gem-benchmark.com/data_cards](https://gem-benchmark.com/data_cards))
[cite:gehrmann2021gem], because GEM provides a curated, documented,
multi-task and multi-lingual registry of NLG datasets spanning data-to-text,
dialogue, paraphrasing, question generation, reasoning, simplification, and
summarization — a principled way to cover the field's subareas rather than an
ad-hoc dataset list. Starting from the GEM dataset inventory, we searched the
ACL Anthology (2022 onward) for papers that (i) conduct human evaluation on a
GEM-listed dataset and (ii) publicly release the resulting judgments.
Search keys combined dataset names (e.g., *XSum, XLSum, WebNLG, ToTTo, E2E,
ASSET, CommonGen*) with evaluation terms (*human evaluation, human judgments,
annotations, annotator, ratings, error analysis*) and release cues
(*data available, released annotations, repository*). Candidates were scored
on a 1–5 PLeW-suitability scale that prioritizes per-(item × system ×
criterion × annotator) granularity, inspectable text, and permissive access;
sources releasing only aggregated scores or protocol descriptions were
catalogued but deprioritized. The resulting catalog covers, i.a., SEAHORSE
[cite:clark2023seahorse], SimpEval/LENS [cite:maddela2023lens], mFACE
[cite:aharoni2023mface], RoSE [cite:liu2023rose], WebNLG 2017 human
evaluation [cite:shimorina2018webnlg], HEAP [cite:mehri2023heap], and MQM
error annotations for data-to-text [cite:yin2022seq2seq], complemented by
established non-GEM suites such as SummEval [cite:fabbri2021summeval] and
FRANK [cite:pagnoni2021frank].

### 3.2 Transformation skill

Released judgment files are heterogeneous: nested JSON keyed by annotator,
wide CSVs with one column per criterion, pairwise A/B preference records with
blinded system identities. To make conversion repeatable rather than a
per-dataset scripting effort, we packaged the workflow as an **agent skill**
(a structured, tool-executable instruction set) named `plew-prepare-dataset`.
Given a raw dataset, the skill (1) **profiles** it — row counts, per-column
cardinality and uniqueness ratios, string lengths, nesting, media references;
(2) applies a **suitability gate** with explicit pass/marginal/fail criteria
(e.g., at least two low-cardinality dimensions and one inspectable text
field), producing a documented rejection when data cannot support grid
exploration; (3) **reshapes** the data using a small pattern library — melting
multi-criterion columns to long format, exploding per-annotator arrays,
joining annotation and content files, resolving blinded pairwise winners to
system labels; (4) assigns the `dim::`/`desc::`/`med::`/`res::` prefixes by
*role* inferred from the profile, never by hardcoded column names; and
(5) **subsets** to demo scale with a recorded random seed, emitting a
validated `PLEW_READY.csv`, a reproducible `transform.py`, and a manifest
documenting the observation unit, column mapping, and known limitations.
The skill is dataset-agnostic and openly released with the tool.

## 4 Evaluation (TODO)

<!-- Options to discuss:
- Case studies: walk through 2–3 transformed datasets (e.g., WebNLG 2017,
  SummEval) showing insights not visible in aggregate tables (annotator
  disagreement patterns, category-specific failures).
- Coverage statistics: N GEM datasets screened, N papers catalogued,
  N datasets transformed, transformation effort per dataset.
- Optional small user walkthrough / demo scenario for the session.
-->

## 5 Conclusion (TODO)

---

## Notes / decisions

- Title fixed earlier: *PLeW-NLG: Interactive Exploration of Human Evaluation
  Data across NLG Tasks*.
- Target: 2 pages (excl. references), INLG 2026 demo track — port to ACL-style
  LaTeX template when structure settles.
- Citations to resolve: vanderlee2019best, howcroft2020twenty, freitag2021mqm,
  shimorina2022heds (HEDS datasheet), belz2021reprogen, gehrmann2021gem,
  clark2023seahorse, maddela2023lens, aharoni2023mface, liu2023rose,
  shimorina2018webnlg, mehri2023heap, yin2022seq2seq, fabbri2021summeval,
  pagnoni2021frank.
- Screenshot candidates: WebNLG 2017 view (system × criterion grid, score as
  color, annotator panels); record window with MR + generated text.
