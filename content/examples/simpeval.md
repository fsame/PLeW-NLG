+++
title = "SimpEval (LENS)"
weight = 1
task = "simplification"
description = "Human simplification evaluation (Rank & Rate, 0–100 quality) with five raters per source sentence and system. 600 rows: 20 ASSET sentences × 6 systems × 5 raters."
dataset_url = "data/simpeval.csv"
layout = "example-viz"

[[viz_presets]]
label = "Annotator × score band"
url = "data/plew-setup-simpeval-annotators-only.json"

[[viz_presets]]
label = "Annotator × score band by system"
url = "data/plew-setup-simpeval-annotators-system.json"
+++
