+++
title = "NeuralREG human evaluation"
weight = 1
task = "referring-expression-generation"
description = "Human evaluation of referring-expression realizations (fluency, grammar, clarity, 1–7) for six REG systems on 24 WebNLG-style passages. 4,407 rows: 24 texts × 6 systems × 3 criteria × ~10 raters."
dataset_url = "data/neuralreg_humaneval.csv"
layout = "example-viz"

[[viz_presets]]
label = "System × text size"
url = "data/plew-setup-neuralreg-humaneval-system-score.json"

[[viz_presets]]
label = "System × score"
url = "data/plew-setup-neuralreg-humaneval-system-x-score.json"
+++
