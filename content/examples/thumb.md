+++
title = "THumB 1.0"
weight = 3
task = "image-captioning"
description = "MSCOCO image-captioning rubric evaluation (precision, recall, penalties) across 5 systems plus human references. Demo subset: 1,250 rows from 50 images with live COCO image URLs."
dataset_url = "data/thumb.csv"
layout = "example-viz"

[[viz_presets]]
label = "Model × criterion"
url = "data/plew-setup-thumb-by-model.json"
default = true

[[viz_presets]]
label = "Human vs machine"
url = "data/plew-setup-thumb-human-vs-machine.json"

[[viz_presets]]
label = "By image"
url = "data/plew-setup-thumb-by-image.json"
+++
