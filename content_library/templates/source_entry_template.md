# {{ Work Title }} — {{ Author }}

**Source ID prefix:** `{{ author_slug }}_{{ work_slug }}_`

## Source metadata defaults

- **Author:** {{ Author }}
- **Work:** {{ Work Title }}
- **Era written:** `{{ era_slug }}`
- **World depicted:** `{{ world_slug }}`
- **Traditions:** `{{ tradition_slug }}`
- **Default rights status:** `{{ rights_status }}`
- **Translator notes:** TBD
- **Source URLs:** TBD

## Entries

<!--
Each entry is one YAML block separated by `---` lines.
Schema is defined in ../01_SCHEMA.md.
Always fill at least one of: direct_quote, paraphrase, core_idea.
Use paraphrase for anything not confirmed public domain.
-->

```yaml
id: {{ author_slug }}_{{ work_slug }}_{{ topic }}_001

source:
  author: {{ Author }}
  work: {{ Work Title }}
  section: ""
  translator: null
  source_url: null
  rights_status: {{ rights_status }}
  notes: ""

classification:
  era_written: {{ era_slug }}
  world_depicted: {{ world_slug }}
  traditions:
    - {{ tradition_slug }}
  themes:
    - {{ theme_slug }}
  tone:
    - severe
    - restrained
    - direct

content:
  direct_quote: ""
  paraphrase: ""
  core_idea: ""
  interpretation: ""

video:
  series:
    - {{ series_slug }}
  visual_worlds:
    - {{ visual_world_slug }}
  voice_profile: null
  music_profile: null
  script_angle: ""
  final_line: ""
```

---

<!-- Add the next entry here, in another YAML block. -->
