# 00 — Project Vision

## What this is

A local-first **cinematic quote-film engine** for producing short-form motivational videos. A disciplined, repeatable system for serious, useful, masculine-coded motivational media — with a clear aesthetic, a clear ethical line, and a human in the loop before anything is published.

## What the videos should feel like

Cinematic, ancient, literary, and grounded. Imagery is symbolic, not literal. Examples:

- a marble bust of Marcus Aurelius in storm light
- a Greek temple above the sea
- Socrates in shadow near the agora
- a candlelit desk with old books and rain on the window
- a forest recovering after disturbance
- a Roman road at dawn
- a mountain silhouette with fog and ash

The engine should not rely on a third-party AI video generator. AI is used only for **still visual assets**; the final video is assembled locally.

## What this is not

- AI spam.
- Ragebait.
- A generic quote machine.
- A SaaS or a content farm.
- An auto-publisher.
- A wrapper around someone else's "AI video" black box.

## Who it speaks to

Men who respond to direct language, responsibility, discipline, restraint, competence, endurance, honor, and service. The tone can be firm and challenging. It is never soft for the sake of being soft, and never hateful, resentful, manipulative, or contempt-driven.

This project exists as an alternative to the negative motivational content common on short-form platforms — content that captures attention through shame, insecurity, dominance, fake urgency, or gender hostility. This engine should do the opposite: say difficult things plainly while preserving dignity.

The central message is **Hard truth. Clean heart.** See [01_CONTENT_PHILOSOPHY.md](01_CONTENT_PHILOSOPHY.md) for the editorial spine.

## MVP

A single clean local loop. See [06_MVP_ROADMAP.md](06_MVP_ROADMAP.md) for milestone status. The end-to-end loop is:

1. Load a content specification from YAML.
2. Generate image-generation prompts from the spec's visual world.
3. Operator runs the prompts in their image tool (ComfyUI, Krea, etc.).
4. Generate voiceover locally (Kokoro TTS).
5. Generate captions.
6. Render a vertical short-form video.
7. Save the output as a **draft**.
8. A human approves before anything is published.

## Operating principles

- **Local-first.** The pipeline runs on the operator's machine. Cloud services are optional, swappable, and never required.
- **Owned artifacts.** Every intermediate output lives on disk in plain formats the operator can inspect or edit.
- **Resumable stages.** Any stage can be re-run from the previous stage's artifact.
- **Editorial responsibility on the operator.** Scripts are hand-authored in YAML and judged against [01_CONTENT_PHILOSOPHY.md](01_CONTENT_PHILOSOPHY.md) by the operator. No automated ethics gate in the MVP.
- **Human approval gate.** Nothing publishes itself. A person watches the draft and says yes.
- **Small surface.** A handful of composable commands beat a sprawling framework.

## Source material, not product

The engine should draw on Stoicism, classical literature, myth, nature writing, speeches, military and exploration history, existential literature, and practical modern wisdom. Quotes and authors are **source material, not the product**. The product is interpretation, application, and clear speech.

## Long-term

The architecture stays modular so the project can eventually support multiple series, voices, render styles, and platforms. Don't over-engineer the early version — prefer clean, explicit, testable Python modules. Earn each abstraction.

## Out of scope (for now)

- Automated publishing to any platform.
- Social media automation.
- Analytics dashboards.
- Multi-agent orchestration.
- Cloud services.
- Multi-user / multi-tenant.
- A hosted web UI. The CLI is the operator interface; a local Streamlit app is allowed for the human-approval review step only.
