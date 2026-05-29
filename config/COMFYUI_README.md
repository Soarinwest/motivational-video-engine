# ComfyUI integration — setup

The `motive make-images` stage POSTs a workflow JSON to a local ComfyUI server,
polls for completion, and writes the resulting PNG to
`assets/backgrounds/<world>/<background_prompt_key>.png`. See the plan at
[../docs/03_PIPELINE_ARCHITECTURE.md](../docs/03_PIPELINE_ARCHITECTURE.md) for
where this sits in the pipeline.

## Files

- [`comfyui.yaml`](comfyui.yaml) — server profiles. The active profile sets the
  base URL, workflow JSON path, output resolution, and timeouts.
- [`comfyui_workflow.json`](comfyui_workflow.json) — workflow template in
  ComfyUI's **API format**. Ships with a minimum SDXL skeleton pointing at a
  placeholder checkpoint. Replace with your own.

## Setup steps

1. **Start ComfyUI locally.** From your ComfyUI install:
   ```
   python main.py --listen 127.0.0.1 --port 8188
   ```
   Confirm `http://127.0.0.1:8188` loads the UI in a browser.

2. **Export your workflow in API format.** In the ComfyUI UI:
   - Settings (gear icon) → enable **"Enable Dev mode Options"**.
   - Build (or open) any text-to-image graph: `CheckpointLoaderSimple` →
     two `CLIPTextEncode` (positive + negative) → `EmptyLatentImage` →
     `KSampler` → `VAEDecode` → `SaveImage`.
   - Click **"Save (API Format)"** → save as `comfyui_workflow.json`.

3. **Inject the six tokens** into the exported JSON. The stage substitutes
   these as raw text before parsing the file:

   | Token | Where to put it | JSON slot |
   |---|---|---|
   | `__POSITIVE__` | positive `CLIPTextEncode` → `inputs.text` | inside the surrounding `"..."` |
   | `__NEGATIVE__` | negative `CLIPTextEncode` → `inputs.text` | inside `"..."` |
   | `__FILENAME_PREFIX__` | `SaveImage` → `inputs.filename_prefix` | inside `"..."` |
   | `__SEED__` | `KSampler` → `inputs.seed` | bare number (no quotes) |
   | `__WIDTH__` | `EmptyLatentImage` → `inputs.width` | bare number |
   | `__HEIGHT__` | `EmptyLatentImage` → `inputs.height` | bare number |

   Missing tokens trigger a yellow warning but won't fail the run — useful if
   you've intentionally hard-coded a value.

4. **Copy** the edited workflow to `config/comfyui_workflow.json` (overwriting
   the placeholder skeleton).

5. **Confirm `comfyui.yaml`** points at the right `base_url` and uses your
   intended output resolution (default `1080x1920` matches `render.resolution`
   in the example specs).

## Usage

```
motive make-images examples/specs/marcus_self_command.yaml
```

Flags:

- `--force` — regenerate even if `assets/backgrounds/<world>/<key>.png` exists.
- `--random-seed` — use a random seed instead of the deterministic one derived
  from `spec.id|kind|key`.
- `--profile <name>` — pick a profile from `comfyui.yaml` (default: the value
  under `default_profile:`).
- `--workflow <path>` — override the workflow JSON path (default: from
  profile).
- `--config <path>` — override the comfyui.yaml path.

Subsequent re-renders without `--force` skip cleanly with a yellow `skip`
message and exit 0.

## Known pitfalls

- **API format vs UI format.** ComfyUI's `/prompt` endpoint takes the
  flat `{node_id: {class_type, inputs}}` shape, not the UI's
  `{nodes: [...], links: [...]}`. "Save (API Format)" is the right export.
- **Missing checkpoint** surfaces as `node_errors` on `/prompt`. The stage
  prints the verbatim message — fix the `ckpt_name` in your workflow.
- **First call on cold GPU** can take 60+ seconds for SDXL, longer for Flux.
  Default timeout is 300s.
- **`filename_prefix` uses forward slashes** for subfolders. Never pass
  backslashes (Windows path separators will break the server's output path).
