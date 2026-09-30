# Personal lab videos

15-second 1080x1080 videos, one per lab, published at /v/<sha1(email)[:10]>/ (noindex, disallowed in robots.txt).
1. `python3 cache_crown.py` once (renders the rotating crown frames into cache/, ~15 min).
2. Put leads in hot_queue.csv (or edit `leads()` in batch.py), copy logo.png from brand/logo/logo-horizontal-transparent-white.png.
3. `python3 batch.py` → writes v/<id>/{video.mp4,poster.jpg,preview.gif,index.html} into the repo and video_links.csv.
