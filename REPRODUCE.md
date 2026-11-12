# Reproduce

Tools: https://github.com/lpurdy01/video_pipeline_workspace cdbab44, a modified copy of it (the changes are not published yet)

The video was rendered with a copy of Levi Purdy's verification-compiler video pipeline (branch
`video2-section1-hook` at `cdbab44` in his repository), with changes made for this video: new chart kinds, the
voice step, and fixes to the gate and the assembly. That copy is not published yet. Releasing it as the channel's
shared tools repository is planned, not done; if it is released, this file will name its version.

- Environment: Python 3, Manim Community v0.22.1, ffmpeg 9.0.2 (conda-forge).
- What is here: the video's own code, `video/style.py` (palette, type scale, shape grammar), `video/sections.py` and
  one scene per section in `video/scenes/`. The scenes import the pipeline as `moats_video.pipeline`; put
  `style.py` and `sections.py` in that package and the scenes in `moats_video/scenes/`.
- Commands, once the pipeline is published: time the narration, render each section, run the frame gate, assemble
  (the pipeline's README gives each).
- What cannot be reproduced exactly: model outputs (the checks, the frame review) and the voice render.
