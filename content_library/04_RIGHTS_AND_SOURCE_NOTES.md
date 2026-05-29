# Rights and Source Notes

How the project handles copyright, translation rights, and attribution for both text sources and downloaded asset files.

## Rules for text

1. **Prefer public-domain sources where possible.** Original texts older than ~1929 (US) are generally public domain in their original language.
2. **Public-domain original text does not guarantee every modern translation is public domain.** A 2015 translation of Marcus Aurelius is copyrighted even though the Latin is not. The translator owns the translation.
3. **For modern copyrighted authors, use paraphrase, commentary, and short references rather than long quotes.** Short fair-use quotation with attribution is generally defensible; long passages are not.
4. **Store source URL, translator name, edition, and rights status whenever possible.** Future-you will need this to verify or defend a claim.
5. **Keep direct quotes separate from paraphrases.** The `direct_quote` and `paraphrase` fields in the schema exist for exactly this reason. Never use a paraphrase as if it were a quote.
6. **When in doubt, paraphrase.** A clean paraphrase + attribution + interpretation is always safe and is often the better video voiceover anyway.

## Rules for assets

1. **Use real historical images only when rights are confirmed or the image is clearly public domain / CC0 / appropriately licensed.** Museum websites usually state the license.
2. **Save metadata for every downloaded real-image, music, font, and overlay asset.** Filename, source URL, license, attribution requirement.
3. **AI-generated assets carry their own concerns.** Most platforms grant the user broad rights to outputs, but check the terms of the platform you used. Save the prompt and the generation date in the asset metadata.
4. **Attribution required by license must propagate to the published video description.** This is non-negotiable.

## Controlled vocabulary: `rights_status`

Use one of these values for the `source.rights_status` field in source entries, and the analogous field for assets:

| Status | Meaning | Safe to quote directly? |
|---|---|---|
| `public_domain_original` | The original text is in the public domain (e.g. Latin, ancient Greek). | Yes, in the original language. For translation, depends on translator. |
| `public_domain_translation` | A specific translation is also in the public domain (pre-1929 in the US, or explicitly released). | Yes — note translator and year. |
| `public_domain_translation_needed` | Original is PD; we have not yet sourced a PD translation. | No — paraphrase only until a PD translation is sourced. |
| `copyrighted_modern_use_paraphrase` | Modern copyrighted work. | No — paraphrase and short attributed reference only. |
| `copyright_status_unknown` | Status not yet verified. | No — paraphrase until verified. |
| `cc0` | Released under Creative Commons Zero. | Yes. |
| `creative_commons_attribution_required` | CC-BY or similar — usable with attribution. | Yes, with attribution in the video description. |
| `licensed_asset` | A specific license has been purchased (e.g. stock music, stock footage). | Per license terms; store the license file path or order ID. |

## Practical workflow

When adding a new source entry:

1. Find the canonical text. Record `source.author`, `source.work`, `source.section`.
2. Look up the translation source. Record `source.translator` and `source.source_url`.
3. Determine `source.rights_status` from the table above.
4. If status permits, populate `content.direct_quote`. Otherwise leave it empty and write a `content.paraphrase`.
5. Always write `content.core_idea` and `content.interpretation`. These are the project's voice, not the source's.

When adding a new asset (image, music, font, overlay):

1. Record the source URL and license in a sidecar metadata file (TBD format — likely a small YAML next to the asset, or a single `ASSETS_METADATA.md` per folder).
2. If attribution is required, capture the required attribution text verbatim.
3. Confirm the license permits use in monetized video before relying on the asset in a published draft.
