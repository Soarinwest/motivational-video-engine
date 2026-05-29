# 06 — MVP Roadmap

Milestones in order. Each is a complete, testable surface. No milestone starts until the previous one is green.

## [done] M0 — Scaffold
Repo structure, docs, dependencies installed, scaffold imports clean.

## [done] M1 — Spec validation
- `ContentSpec` Pydantic schema for the YAML format.
- `motive validate-spec <path>` CLI command.
- `motive lint <path>` cross-config reference check (added post-M1).
- Three example specs in `examples/specs/`.

## [done] M2 — Visual prompt generation
- `config/visual_worlds.yaml` fleshed out with templates, palette, motifs, background_prompts, figure_prompts.
- `motive make-image-prompt <spec>` emits a full image-generator prompt + negative prompt.

## [done] M2.5 — Image generation (local ComfyUI)
- `motive make-images <spec>` POSTs the M2 prompts to a local ComfyUI HTTP server, polls `/history`, downloads the PNG, and writes it to `assets/backgrounds/<world>/<key>.png`.
- `config/comfyui.yaml` declares named server profiles (`base_url`, workflow path, resolution, timeouts) in the same shape as `voices.yaml` / `brand.yaml`.
- `config/comfyui_workflow.json` is a user-replaceable workflow template in ComfyUI's API format with six injection tokens (`__POSITIVE__`, `__NEGATIVE__`, `__SEED__`, `__WIDTH__`, `__HEIGHT__`, `__FILENAME_PREFIX__`).
- Deterministic seed by default (`sha256(spec.id|kind|key)`); `--random-seed` for variation; `--force` to regenerate over an existing file.
- v1 is backgrounds only — figures still flow through the manual path. Figure auto-gen is a v2 add-on.

## [done] M3 — Voiceover (Kokoro)
- Local Kokoro TTS behind a small injectable synthesizer.
- `motive make-voice <spec>` writes per-line WAVs + `voice/index.json` + copies `spec.yaml` into the draft dir.
- Voice profile chosen from `config/voices.yaml`.

## [done] M4 — Captions
- Generates ASS captions (line-locked to voice timing) from `voice/index.json`.
- `motive make-captions <spec>` writes `outputs/drafts/<id>/captions.ass`.
- Caption style picked from a small named set (`serif_quiet`, `sans_quiet`); registry lives in `stages/captions.py` and is lint-checked.

## [done] M5 — Render
- Composites background + figure + motion + voice + captions into a vertical MP4.
- `motive render <spec>` → `outputs/drafts/<id>/<id>.mp4`.
- MoviePy for compositing, FFmpeg (via `imageio_ffmpeg`) for two-pass caption burn-in.

## [done] M6 — Review queue
- Local Streamlit page that lists drafts in `outputs/drafts/`, plays them, and routes to `outputs/approved/` or `outputs/rejected/` (with reason on reject).
- `motive review` launches it on `localhost:8501`.

## Open polish work (not blocking the MVP)
- **Music mixing** — `audio.music_profile` parsed but ignored by render. Needs an `assets/music/` convention + ducking under voice.
- **Visual overlays** — `visual.overlays` parsed but ignored by render. Needs an overlay-asset catalog and per-overlay compositing.
- **Word-level caption sync** — current captions are line-locked to voice chunks. Word-level needs Whisper forced-alignment over the rendered audio.
- **Catalog-backed lint coverage** — `motion_profile` and `overlays` are not yet lint-checked because they have no canonical catalog. Add to `lint.py` once those land.

## Out of scope (deliberately)
- Social media publishing.
- Cloud services.
- Multi-agent orchestration.
- Analytics, A/B, recommendations.
- Web UI beyond local Streamlit.
- Multi-user.
