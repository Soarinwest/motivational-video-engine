"""motive — local-first cinematic quote-film engine.

CLI surface. Each subcommand corresponds to one pipeline stage:
validate-spec, lint, make-image-prompt, make-images, make-voice,
make-captions, render.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import typer
import yaml
from pydantic import ValidationError
from rich.console import Console

from motive_engine.lint import (
    DEFAULT_BRAND_PATH,
    DEFAULT_SERIES_PATH,
    lint_spec,
)
from motive_engine.schemas import ContentSpec
from motive_engine.stages import build_image_prompt
from motive_engine.stages import voice as voice_stage
from motive_engine.stages.captions import write_captions
from motive_engine.stages.images import (
    DEFAULT_COMFYUI_CONFIG_PATH,
    DEFAULT_WORKFLOW_PATH,
    ComfyUIError,
    ComfyUITimeout,
    ComfyUIUnreachable,
    generate_image,
)
from motive_engine.stages.render import DEFAULT_ASSETS_ROOT, write_render
from motive_engine.stages.visual_prompts import DEFAULT_WORLDS_PATH
from motive_engine.stages.voice import DEFAULT_VOICES_PATH
from motive_engine.utils import load_yaml

app = typer.Typer(
    add_completion=False,
    help="Local-first cinematic quote-film engine. Hard truth. Clean heart.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def _main() -> None:
    """Local-first cinematic quote-film engine. Hard truth. Clean heart."""


@app.command("validate-spec")
def validate_spec(
    path: Path = typer.Argument(
        ...,
        help="Path to a YAML content specification file.",
    ),
) -> None:
    """Validate a YAML content specification against the ContentSpec schema."""
    try:
        data = load_yaml(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]File not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML parse error:[/bold red] {e}")
        raise typer.Exit(code=2)

    try:
        spec = ContentSpec.model_validate(data)
    except ValidationError as e:
        console.print(f"[bold red]Spec invalid:[/bold red] {path}")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"]) or "<root>"
            console.print(f"  [yellow]{loc}[/yellow] — {err['msg']}")
        raise typer.Exit(code=1)

    console.print(f"[bold green]OK[/bold green] {path}")
    console.print(f"  id:        {spec.id}")
    console.print(f"  series:    {spec.series}")
    console.print(f"  theme:     {spec.theme}")
    console.print(f"  duration:  {spec.duration_seconds}s")
    console.print(f"  world:     {spec.visual.world}")


@app.command("make-image-prompt")
def make_image_prompt(
    path: Path = typer.Argument(
        ...,
        help="Path to a YAML content specification file.",
    ),
    worlds: Path = typer.Option(
        DEFAULT_WORLDS_PATH,
        "--worlds",
        "-w",
        help="Path to visual_worlds.yaml.",
    ),
) -> None:
    """Emit an image-generator prompt + negative prompt for a content spec."""
    try:
        data = load_yaml(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]File not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML parse error:[/bold red] {e}")
        raise typer.Exit(code=2)

    try:
        spec = ContentSpec.model_validate(data)
    except ValidationError as e:
        console.print(f"[bold red]Spec invalid:[/bold red] {path}")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"]) or "<root>"
            console.print(f"  [yellow]{loc}[/yellow] — {err['msg']}")
        raise typer.Exit(code=1)

    try:
        result = build_image_prompt(spec, worlds_path=worlds)
    except FileNotFoundError as e:
        console.print(f"[bold red]Worlds file not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except (KeyError, ValueError) as e:
        console.print(f"[bold red]Prompt build failed:[/bold red] {e}")
        raise typer.Exit(code=1)

    console.print("[bold green]== Image prompt ==[/bold green]")
    console.print(result.positive)
    console.print()
    console.print("[bold green]== Negative prompt ==[/bold green]")
    console.print(result.negative)


@app.command("make-images")
def make_images(
    path: Path = typer.Argument(
        ...,
        help="Path to a YAML content specification file.",
    ),
    assets_dir: Path = typer.Option(
        DEFAULT_ASSETS_ROOT,
        "--assets-dir",
        "-a",
        help="Root of the assets tree (backgrounds/, figures/, ...).",
    ),
    worlds: Path = typer.Option(
        DEFAULT_WORLDS_PATH,
        "--worlds",
        "-w",
        help="Path to visual_worlds.yaml.",
    ),
    config: Path = typer.Option(
        DEFAULT_COMFYUI_CONFIG_PATH,
        "--config",
        "-c",
        help="Path to comfyui.yaml.",
    ),
    workflow: Path = typer.Option(
        DEFAULT_WORKFLOW_PATH,
        "--workflow",
        help="Path to the ComfyUI workflow JSON template.",
    ),
    profile: str | None = typer.Option(
        None,
        "--profile",
        "-p",
        help="Named profile from comfyui.yaml. Defaults to the file's default_profile.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Regenerate even if the target asset already exists.",
    ),
    random_seed: bool = typer.Option(
        False,
        "--random-seed",
        help="Use a random seed instead of the deterministic one.",
    ),
) -> None:
    """Generate the spec's background image via local ComfyUI (writes to assets/)."""
    try:
        data = load_yaml(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]File not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML parse error:[/bold red] {e}")
        raise typer.Exit(code=2)

    try:
        spec = ContentSpec.model_validate(data)
    except ValidationError as e:
        console.print(f"[bold red]Spec invalid:[/bold red] {path}")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"]) or "<root>"
            console.print(f"  [yellow]{loc}[/yellow] - {err['msg']}")
        raise typer.Exit(code=1)

    try:
        result = generate_image(
            spec,
            assets_root=assets_dir,
            worlds_path=worlds,
            config_path=config,
            workflow_path=workflow,
            profile_name=profile,
            force=force,
            random_seed=random_seed,
        )
    except FileNotFoundError as e:
        console.print(f"[bold red]Not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except ComfyUIUnreachable as e:
        console.print(f"[bold red]ComfyUI unreachable:[/bold red] {e}")
        raise typer.Exit(code=1)
    except ComfyUITimeout as e:
        console.print(f"[bold red]ComfyUI timeout:[/bold red] {e}")
        raise typer.Exit(code=1)
    except ComfyUIError as e:
        console.print(f"[bold red]ComfyUI error:[/bold red] {e}")
        raise typer.Exit(code=1)

    if result.skipped:
        console.print(
            f"[yellow]skip[/yellow] {result.output_path} "
            f"(already exists; pass --force to regenerate)"
        )
        return

    console.print(
        f"[bold green]OK[/bold green] wrote {result.output_path} (seed={result.seed})"
    )


@app.command("make-voice")
def make_voice(
    path: Path = typer.Argument(
        ...,
        help="Path to a YAML content specification file.",
    ),
    output_dir: Path = typer.Option(
        Path("outputs") / "drafts",
        "--output-dir",
        "-o",
        help="Base output directory; a <spec.id>/voice/ subdir is created underneath.",
    ),
    voices: Path = typer.Option(
        DEFAULT_VOICES_PATH,
        "--voices",
        help="Path to voices.yaml.",
    ),
) -> None:
    """Render the spec's voiceover via Kokoro and write WAVs to disk."""
    try:
        data = load_yaml(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]File not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML parse error:[/bold red] {e}")
        raise typer.Exit(code=2)

    try:
        spec = ContentSpec.model_validate(data)
    except ValidationError as e:
        console.print(f"[bold red]Spec invalid:[/bold red] {path}")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"]) or "<root>"
            console.print(f"  [yellow]{loc}[/yellow] — {err['msg']}")
        raise typer.Exit(code=1)

    try:
        profile = voice_stage.load_voice_profile(
            spec.audio.voice_profile, voices_path=voices
        )
    except FileNotFoundError as e:
        console.print(f"[bold red]Voices file not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except (KeyError, ValueError, ValidationError) as e:
        console.print(f"[bold red]Voice profile error:[/bold red] {e}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold]Rendering[/bold] {spec.id} via {profile.voice_id} "
        f"(speed {profile.speed}, lang {profile.lang_code})"
    )
    console.print("(First run downloads Kokoro weights from Hugging Face — ~325 MB)")

    # Copy spec into the draft dir so downstream stages and the review UI
    # have full context without scanning back to examples/.
    draft_dir = output_dir / spec.id
    draft_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(path, draft_dir / "spec.yaml")

    try:
        synthesizer = voice_stage.make_kokoro_synthesizer(profile)
        track = voice_stage.render_voice(
            spec, profile, output_root=output_dir, synthesizer=synthesizer
        )
    except Exception as e:
        console.print(f"[bold red]Voice render failed:[/bold red] {e}")
        raise typer.Exit(code=1)

    voice_dir = output_dir / spec.id / "voice"
    total = sum(line.duration_seconds for line in track.lines)
    console.print(
        f"[bold green]OK[/bold green] wrote {len(track.lines)} line(s) to {voice_dir}"
    )
    console.print(f"  total duration: {total:.1f}s (target: {spec.duration_seconds}s)")


@app.command("make-captions")
def make_captions(
    path: Path = typer.Argument(
        ...,
        help="Path to a YAML content specification file.",
    ),
    output_dir: Path = typer.Option(
        Path("outputs") / "drafts",
        "--output-dir",
        "-o",
        help="Base output directory; reads <spec.id>/voice/ and writes <spec.id>/captions.ass.",
    ),
) -> None:
    """Generate styled ASS captions from the rendered voice timing."""
    try:
        data = load_yaml(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]File not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML parse error:[/bold red] {e}")
        raise typer.Exit(code=2)

    try:
        spec = ContentSpec.model_validate(data)
    except ValidationError as e:
        console.print(f"[bold red]Spec invalid:[/bold red] {path}")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"]) or "<root>"
            console.print(f"  [yellow]{loc}[/yellow] — {err['msg']}")
        raise typer.Exit(code=1)

    try:
        output_path, track = write_captions(spec, output_root=output_dir)
    except FileNotFoundError as e:
        console.print(f"[bold red]Missing voice output:[/bold red] {e}")
        raise typer.Exit(code=2)
    except KeyError as e:
        console.print(f"[bold red]Caption style error:[/bold red] {e}")
        raise typer.Exit(code=1)

    total = track.lines[-1].end_seconds if track.lines else 0.0
    console.print(
        f"[bold green]OK[/bold green] wrote {output_path} ({len(track.lines)} line(s))"
    )
    console.print(f"  total duration: {total:.1f}s (target: {spec.duration_seconds}s)")
    console.print(f"  style: {track.style}")


@app.command("render")
def render(
    path: Path = typer.Argument(
        ...,
        help="Path to a YAML content specification file.",
    ),
    output_dir: Path = typer.Option(
        Path("outputs") / "drafts",
        "--output-dir",
        "-o",
        help="Base output directory; final video at <output_dir>/<spec.id>/<spec.id>.mp4.",
    ),
    assets_dir: Path = typer.Option(
        DEFAULT_ASSETS_ROOT,
        "--assets-dir",
        "-a",
        help="Root of the assets tree (backgrounds/, figures/, ...).",
    ),
) -> None:
    """Composite background + figure + motion + voice + captions into a vertical MP4."""
    try:
        data = load_yaml(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]File not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML parse error:[/bold red] {e}")
        raise typer.Exit(code=2)

    try:
        spec = ContentSpec.model_validate(data)
    except ValidationError as e:
        console.print(f"[bold red]Spec invalid:[/bold red] {path}")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"]) or "<root>"
            console.print(f"  [yellow]{loc}[/yellow] — {err['msg']}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Rendering[/bold] {spec.id}")
    console.print(f"  resolution: {spec.render.resolution} @ {spec.render.fps}fps")
    console.print(f"  motion:     {spec.visual.motion_profile}")

    try:
        summary = write_render(spec, output_root=output_dir, assets_root=assets_dir)
    except FileNotFoundError as e:
        console.print(f"[bold red]Missing input:[/bold red] {e}")
        raise typer.Exit(code=2)
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode("utf-8", errors="replace") if e.stderr else ""
        console.print(f"[bold red]FFmpeg caption burn-in failed:[/bold red]")
        console.print(stderr[-2000:] if stderr else "(no stderr captured)")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Render failed:[/bold red] {e}")
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]OK[/bold green] wrote {summary.output_path} "
        f"({summary.duration_seconds:.1f}s)"
    )
    if not summary.captions_burned:
        console.print(
            "  [yellow]note:[/yellow] no captions.ass found — rendered without captions. "
            "Run `motive make-captions` then re-render to include them."
        )


@app.command("review")
def review(
    outputs_dir: Path = typer.Option(
        Path("outputs"),
        "--outputs-dir",
        "-o",
        help="Root outputs directory containing drafts/, approved/, rejected/.",
    ),
    port: int = typer.Option(
        8501,
        "--port",
        "-p",
        help="Port for Streamlit to listen on.",
    ),
    no_browser: bool = typer.Option(
        False,
        "--no-browser",
        help="Don't auto-open the browser.",
    ),
) -> None:
    """Open the local review queue in a Streamlit browser tab."""
    # Derive the bundled app path WITHOUT importing it — importing would
    # execute the Streamlit script outside a Streamlit runtime and crash.
    app_path = Path(__file__).parent / "review_app.py"
    if not app_path.is_file():
        console.print(f"[bold red]Review app not found at {app_path}[/bold red]")
        raise typer.Exit(code=1)

    env = os.environ.copy()
    env["MOTIVE_OUTPUTS_ROOT"] = str(outputs_dir.resolve())

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(port),
    ]
    if no_browser:
        cmd.extend(["--server.headless", "true"])

    console.print(
        f"[bold]Review queue[/bold] -> http://localhost:{port}  "
        f"(watching {outputs_dir.resolve() / 'drafts'})"
    )
    console.print("Press Ctrl-C to stop the server.")
    subprocess.run(cmd, env=env, check=False)


@app.command("lint")
def lint(
    path: Path = typer.Argument(
        ...,
        help="Path to a YAML content specification file.",
    ),
    worlds: Path = typer.Option(
        DEFAULT_WORLDS_PATH, "--worlds", help="Path to visual_worlds.yaml."
    ),
    voices: Path = typer.Option(
        DEFAULT_VOICES_PATH, "--voices", help="Path to voices.yaml."
    ),
    series: Path = typer.Option(
        DEFAULT_SERIES_PATH, "--series", help="Path to series.yaml."
    ),
    brand: Path = typer.Option(
        DEFAULT_BRAND_PATH, "--brand", help="Path to brand.yaml."
    ),
) -> None:
    """Check that every config-driven reference in a spec resolves."""
    try:
        data = load_yaml(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]File not found:[/bold red] {e}")
        raise typer.Exit(code=2)
    except yaml.YAMLError as e:
        console.print(f"[bold red]YAML parse error:[/bold red] {e}")
        raise typer.Exit(code=2)

    try:
        spec = ContentSpec.model_validate(data)
    except ValidationError as e:
        console.print(f"[bold red]Spec invalid:[/bold red] {path}")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"]) or "<root>"
            console.print(f"  [yellow]{loc}[/yellow] — {err['msg']}")
        raise typer.Exit(code=1)

    issues = lint_spec(
        spec,
        worlds_path=worlds,
        voices_path=voices,
        series_path=series,
        brand_path=brand,
    )

    if not issues:
        console.print(f"[bold green]OK[/bold green] {path}")
        console.print("  (checked: series, world, prompts, voice, music)")
        return

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]

    if errors:
        console.print(f"[bold red]Lint failed:[/bold red] {len(errors)} error(s)")
    if warnings:
        console.print(f"[bold yellow]Warnings:[/bold yellow] {len(warnings)}")

    for issue in issues:
        color = "red" if issue.severity == "error" else "yellow"
        console.print(
            f"  [{color}]{issue.severity}[/{color}] "
            f"[yellow]{issue.field}[/yellow] — {issue.message}"
        )

    if errors:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
