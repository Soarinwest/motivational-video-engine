# Taxonomy

The overarching map of eras and traditions the content library can draw from. Files under [eras/](eras/) and [traditions/](traditions/) are the canonical pages for each leaf; this document is the index that shows how the leaves relate.

A source can be classified under one era and several traditions. A tradition can persist across many eras (Stoicism lives in Roman, Renaissance, and modern thought). The taxonomy is for navigation, not exclusion.

```
I. Ancient Foundations
   A. Mesopotamian / Biblical / Near Eastern wisdom
   B. Ancient Greece
      1. Homeric epic
      2. Greek tragedy
      3. Socratic philosophy
      4. Plato and Aristotle
      5. Cynicism, Epicureanism, early schools
   C. Ancient Rome
      1. Roman Republic
      2. Roman Empire
      3. Stoicism
      4. Civic duty and political decline
      5. Roman women, household, empire

II. Medieval and Sacred Orders
   A. Christian wisdom and moral discipline
   B. Chivalry, honor, oath, and service
   C. Arthurian romance
   D. Norse and Germanic heroic legend
   E. Dante and moral order
   F. Islamic Golden Age and other medieval wisdom traditions

III. Renaissance and Early Modern Power
   A. Shakespeare and tragedy
   B. Machiavelli and political realism
   C. Montaigne and self-knowledge
   D. Reformation, conscience, and authority
   E. Exploration, empire, ambition

IV. Enlightenment, Revolution, and Civic Man
   A. Reason and duty
   B. Liberty and responsibility
   C. Civic republicanism
   D. Utilitarianism
   E. Rights, law, and social order

V. Romanticism, Nature, and the Individual
   A. Romantic heroism
   B. Transcendentalism
   C. Nature writing
   D. Solitude and self-reliance
   E. Beauty, desire, and the sublime

VI. Industrial Modernity and War
   A. Realism
   B. Existentialism
   C. World War I
   D. World War II
   E. Women and war
   F. Homefront, grief, rebuilding
   G. Technology, alienation, mass society

VII. Contemporary Discipline and Meaning
   A. Habit and systems
   B. Leadership and ownership
   C. Psychology of resilience
   D. Masculinity and responsibility
   E. Anti-doom-scroll attention
   F. Modern love, sexuality, and autonomy

VIII. Cross-Civilizational Wisdom
   A. Taoism
   B. Confucianism
   C. Buddhism
   D. Hindu texts
   E. Japanese warrior traditions
   F. Indigenous and ecological wisdom
```

## Working with the taxonomy

- Era slugs live as files under [eras/](eras/) — one file per top-level era (I, II, III...). Sub-divisions live in the era file as section headings.
- Tradition slugs live as files under [traditions/](traditions/). Cross-era traditions (Stoicism, Christian wisdom) get one file each and link to every era they touch.
- Themes are orthogonal to the taxonomy. A theme like `duty` cuts across Rome, medieval chivalry, and 20th-century war writing. See [themes/](themes/).
- When in doubt about where to file a source, use the era it was *written in* for `era_written`, the era it *depicts* for `world_depicted`, and list every tradition it genuinely belongs to.
