+++
title = "SimpEval (LENS)"
weight = 1
task = "simplification"
description = "Human simplification evaluation (Rank & Rate, 0–100 quality) with five raters per source sentence and system. 600 rows: 20 ASSET sentences × 6 systems × 5 raters."
dataset_url = "data/simpeval.csv"
layout = "example-viz"

[[viz_presets]]
label = "System × score band"
url = "data/plew-setup-simpeval-by-system.json"
default = true

[[viz_presets]]
label = "By sentence"
url = "data/plew-setup-simpeval-by-sentence.json"
+++
