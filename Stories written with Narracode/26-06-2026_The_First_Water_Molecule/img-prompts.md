# Image prompts — The First Water Molecule

Concept brief and generation prompts for the story's cover icon and five movement banners.

## Style: luminous fluid abstraction / camera-less scientific-sublime

Chosen to fit the poetics:
- **No human figures, no anatomy** — the piece was deliberately de-anatomized (hand/shoulder/"the bend" removed). The "I" is a substance and light, not a person.
- **Radical scale-shift + the prismatic turn** — quasar → magma → membrane → spectrum → vapour; Movement 3 opened an explicitly luminous/prismatic register (refraction, caustics, the bow).
- **Both/and unity** — one house treatment, re-tuned per movement, so the five read as a single substance in five phases ("Oneness sliding into one").

The visual language draws from how water is actually *imaged*, pushed to the lyric edge: macro water + caustics, ink/dye diffusion in water, interference & refraction spectra, microscopy of membranes, deep-field astro for the cosmic end — treated like camera-less photography / photograms.

**Alternatives considered:** (B) cyanotype / chemigram / cameraless darkroom (water makes its own image — beautiful, but narrow tonal range for magma-orange and full spectrum); (C) scientific-diagram-as-lyric (apt but risks the "explainer" register the poetics refused). Recommendation: **A**, with an optional whisper of C (faint 104.5° / isotope notation ghosted into Movement 1).

**Hard constraints:** no human figures/faces/hands; no recognizable everyday objects; **no Haida/Skaay visual motifs** (the poetics borrow the mythteller's *posture*, never costume as Haida — applies doubly to imagery).

## House treatment (paste into every prompt)
> Camera-less luminous fluid abstraction. Macro water, caustic light, ink-in-water diffusion, refraction spectra, scientific-imaging aesthetic. Entirely abstract — no human figures, no faces, no hands, no recognizable objects. Analog film grain, deep blacks, archival texture, painterly light. Subtle, restrained, contemplative; gallery print, not digital render.

## Palette / scale arc
| Image | Scale | Palette | Core image | Aspect |
|---|---|---|---|---|
| Cover | the one | prismatic on black | a droplet refracting a whole cosmos | 1:1 (640×640) |
| 0 Arising | interstellar | blue-black, faint gold | frost on a dust grain; first molecule; distant beacon | 2:1 |
| 1 Made Here | planetary | molten orange / char | water sweated from a magma ocean | 2:1 |
| 2 Permeation | cellular | wet green→crimson | water crossing a leaking membrane | 2:1 |
| 3 Synchrony | field/optical | full spectrum, silver | a billion dew-lenses gathering into one beam | 2:1 |
| 4 Dissipation | evaporative | dissolving pearl-white | a drop spending itself upward into vapour | 2:1 |

## Prompts

### Cover (1:1, story icon)
> [house treatment] A single suspended droplet of water against deep black, refracting an entire faint starfield and nebula within its curve; thin prismatic caustics fanning from its edge; the drop both microscopic and cosmic. Centered, quiet, luminous. Square.

### 0 · Arising (2:1)
> [house treatment] The cold of deep space: a frost-furred grain of interstellar dust, a single bent filament of light suggesting one forming molecule, a distant quasar beacon bleeding faint gold into blue-black. Vast, still, beginningless. No figures.

### 1 · Made Here (2:1)
> [house treatment] An ocean of molten rock to the horizon, dull glowing orange under a crushing dark sky; fine threads of water condensing and rising out of the melt as steam; charred blacks and ember light; a planet sweating its own sea. Faintly, almost invisibly, a ghosted 104.5° angle / isotope notation in the haze. No figures.

### 2 · Permeation (2:1)
> [house treatment] Extreme microscopy: a translucent lipid membrane, an oily bilayer, water beading and seeping through a pore; wet greens shading to blood-crimson; capillary and root-hair filaments; the shimmer of a film one cell thick. Intimate, glistening. No figures.

### 3 · Synchrony (2:1)
> [house treatment] A field of countless dew-droplets at dawn, each a tiny lens holding a spark, their scattered light gathering into a single coherent beam and a faint rainbow bow; refraction and interference patterns; the full visible spectrum unspooling and folding back to one. Radiant, unified. No figures.

### 4 · Dissipation (2:1)
> [house treatment] A single drop on a dark leaf in early light, half-dissolved into rising vapour; surface-tension dome dimming; the wet thinning into pearl-white mist and a hint of distant snow; soft, evaporating, luminous, almost gone. Continuation, not ending. No figures.

## Wiring notes (for after generation)
- **Cover** → save as `img/header.webp` (or `img/banners/0.webp`); `build_helpers.get_story_icon` auto-detects `img/header.png|webp` or `img/banners/0.png|webp` and the builder will place it as the story-page icon and the homepage thumbnail. Re-run `build_story_index.py`.
- **Banners** → the builder supports per-chapter banners (`.chapter-banner`); place per-movement images and re-run. Optionally lean 2 and 4 warmer/sensual to echo the dissolution movement's eros.
