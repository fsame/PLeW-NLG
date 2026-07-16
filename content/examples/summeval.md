+++
title = "SummEval"
weight = 1
task = "summarization"
description = "CNN/DailyMail summarization human evaluation (1–5 Likert) with expert and crowd annotators across four criteria. Demo subset: 1,920 rows from 15 articles × 4 models × 4 criteria × 8 annotators (seed 42)."
dataset_url = "data/summeval.csv"
layout = "example-viz"

[[viz_presets]]
label = "Model × criterion"
url = "data/plew-setup-summeval-by-model.json"

[[viz_presets]]
label = "Expert vs crowd"
url = "data/plew-setup-summeval-expert-vs-crowd.json"
+++
