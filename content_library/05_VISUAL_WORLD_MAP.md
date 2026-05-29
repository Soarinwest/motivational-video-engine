# Visual World Map

Maps content-library entries to the visual worlds under [`assets/backgrounds/`](../assets/backgrounds/). When you set `video.visual_worlds` on a source entry, the slug must match a folder under `assets/backgrounds/`.

Source of truth for what each world looks like: [`assets/figures/visual_asset_prompt_library.md`](../assets/figures/visual_asset_prompt_library.md). Current state of assets: [`assets/CATALOG.md`](../assets/CATALOG.md).

## The 14 worlds

| World slug | Visual identity | Best-fit traditions | Best-fit themes | Default source authors |
|---|---|---|---|---|
| `stoic_rome` | Roman ruins, marble busts, sparse stone rooms, dawn light | stoicism, civic_republicanism | self_command, duty, mortality, restraint | marcus_aurelius, seneca, epictetus |
| `ancient_greece` | Greek temples on cliffs, Mediterranean coast, agora, Bronze-age ships | platonism, aristotelianism, greek_tragedy | courage, mortality, suffering, honor_service | homer, sophocles |
| `literary_dark` | 19th-century interiors, snow-covered St. Petersburg, candlelit desks, gothic chiaroscuro | existentialism, romanticism | suffering, ambition, grief, power_corruption | dostoevsky, tolstoy, shakespeare (interiors) |
| `field_notes` | Forest recovery, old-growth trees, ponds at dawn, ecological detail | transcendentalism, ecological_wisdom | nature_resilience, restraint, attention_anti_doomscroll | thoreau, emerson, aldo_leopold, mary_oliver |
| `modern_discipline` | Workshops at dawn, sparse modern rooms, plowed fields, honest labor | contemporary discipline | usefulness_competence, duty, restraint, honor_service | roosevelt, tolstoy (Levin), modern habit writers |
| `quiet_strength` | Lone figures on ridges, sea cliffs, snow trails — endurance without applause | stoicism, romanticism | restraint, courage, self_command | musashi, marcus_aurelius |
| `existential` | Dry Mediterranean roads, stairway descents into dark, mountain ascents | existentialism | mortality, suffering, courage | camus, nietzsche, kierkegaard (future) |
| `mythic` | Lone warriors before caves, shorelines at storm's end, heroic but grounded | greek_tragedy, war_peace_strategy | courage, honor_service, war_and_peace | homer, beowulf (future) |
| `chivalric` | Castles on rocky outcrops, narrow muddy roads, knightly restraint | chivalry_honor, christian_wisdom | honor_service, duty, restraint | arthurian romance (future), dante (moral order) |
| `hudson_river_school` | Historical landscape paintings (Church, Cole, Bierstadt, et al.) — luminist American wilderness | transcendentalism, romanticism | nature_resilience, restraint, suffering | thoreau, emerson, american 19c writers |
| `anti_doom_scroll` | Phone face-down at dawn, windows instead of screens, choosing attention | contemporary discipline | attention_anti_doomscroll, restraint | modern essayists, contemplative writers |
| `public_duty` | Empty wooden podiums, post-rain arenas, civic dignity | civic_republicanism, christian_wisdom | duty, honor_service, courage | roosevelt (arena), lincoln (future) |
| `abstract_brand` | Marble and shadow, ash and light, parchment textures — caption-friendly backgrounds | any | any | quote-only or series-intro videos |
| `war` | TBD — needs prompt-library entry; battlefields, legions, returning soldiers, homefront | war_peace_strategy, greek_tragedy, christian_wisdom | war_and_peace, women_and_war, grief, homefront_rebuilding, mortality | homer, sophocles, world wars writers |

## Multiple worlds per entry

A source entry's `video.visual_worlds` field is a list. Many entries fit more than one. Marcus Aurelius can sit in both `stoic_rome` (busts, courtyards) and `quiet_strength` (lone figures). List them all — the render stage picks the one that has the best available asset for a given draft.

## Worlds without prompts yet

`war` is a roadmap world with no prompt-library entry. When you set `visual_worlds: [war]` on a source, that's a signal to commission war-world assets next.

## Worlds without assets yet

As of writing, several worlds in [`assets/CATALOG.md`](../assets/CATALOG.md) are empty (anti_doom_scroll, public_duty, abstract_brand). You may still set them on source entries — the render stage will just skip drafts for which assets do not exist yet.
