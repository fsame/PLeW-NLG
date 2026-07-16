+++
title = "Flickr8k"
weight = 2
task = "image-captioning"
description = "Multimodal image-caption human evaluation: expert Likert scores (1–4) on ranking-style image–caption pairs. Demo subset: 345 rows from 20 test images with local JPEGs (3 experts × 115 pairs)."
dataset_url = "data/flickr8k.csv"
layout = "example-viz"

[[viz_presets]]
label = "Expert disagreement"
url = "data/plew-setup-flickr8k-expert-scores.json"
default = true

[[viz_presets]]
label = "By image"
url = "data/plew-setup-flickr8k-by-image.json"
+++
