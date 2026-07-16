+++
title = "SEAHORSE"
weight = 2
task = "summarization"
description = "Multilingual summarization human evaluation (Yes/No/Unsure) across six quality dimensions and multiple systems. Demo subset: 3,856 rows from 411 articles × 6 models × 6 criteria (SEAHORSE validation, seed 42)."
dataset_url = "data/seahorse.csv"
layout = "example-viz"

[[viz_presets]]
label = "Model × criterion"
url = "data/plew-setup-seahorse-by-model.json"
default = true

[[viz_presets]]
label = "By dataset"
url = "data/plew-setup-seahorse-by-dataset.json"

[[viz_presets]]
label = "By language"
url = "data/plew-setup-seahorse-by-language.json"
+++
