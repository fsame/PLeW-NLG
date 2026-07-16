+++
title = "Book highlights (faithfulness)"
weight = 2
task = "llm-as-judge"
description = "LLM factuality checks on generated book highlights — whether each highlight is supported by source reviews, with divergence type and severity. 5,493 rows: one check per generated highlight across all pairwise comparisons."
dataset_url = "data/book_highlights_llm_as_a_judge_faithfulness.csv"
layout = "example-viz"

[[viz_presets]]
label = "Model × divergence by system"
url = "data/plew-setup-book-highlights-faithfulness.json"
+++
