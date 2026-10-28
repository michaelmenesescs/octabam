# GRAIN: a granular machine for FLEX tracks

Status: **proposal, nothing built.** No claim below is measured unless it
cites where; addresses marked 🟡 are read from another document in this repo
and have not been exercised by this module.

## What it is

A FLEX track that plays its own sample as a cloud of grains instead of one
stream. Position, grain size, spray and density are knobs, so a pad, a vocal
or a field recording can be frozen, scanned, smeared and pitched
independently of time. The idea is the classic granular instrument (Truax,
Roads; Ableton's Granulator III is the familiar modern example). Nothing is
copied from any product: the engine, the parameter set and the name are this
module's own.

The DSP is untouched: the ColdFire generates the track's source frames at
rate 1.0, and AMP, filter, FX1/FX2, level, pan, scenes and cue treat them as
a sample, exactly as the FM SYNTH machine does (`modules/synth`).

## How it hooks in (the synth's proven path)

| | octabam (card build) | Modwerk (USB base) |
|---|---|---|
| Selecting the machine | FLEX track whose sample file name starts `GRN` (e.g. `GRN pad.wav`); stock plays the file normally without the module | Its own row in the machine chooser and SRC SETUP through the base table `ot_machines` |
| Render entry | Kind table FLEX entry `0x400d6438` → `gr_render` (SymbolRef, stock value asserted) | `struct modwerk_machine.render` (same signature) |
| Page | PLAYBACK page clone via the resolver detour, as `modules/synth/page.s` | `struct modwerk_machine.page` |
| Conflicts | Refused beside `synth` and POLY8's card list (same kind-table byte). Inherent to the card build. | None by byte. `ot_machines` room is 4 and the catalogue already has 4 machines: a room proposal is part of the Modwerk PR |

One engine source serves both; only the glue differs. Build octabam first
(faster loop, your fork), then package for Modwerk.

The render wrapper is the synth's: neutralise PTCH/RATE to 1.0 around the
stock call so the voice lifecycle, positions and record headers stay stock's,
clear the latched retrig, then overwrite the shipped source pairs
(`synth.s` header documents the record: 16-byte header, then 8-byte L/R
longs, sample in the top 24 bits). **The stock voice ends when its stream
reaches the trim end at rate 1.0**, so the README tells the player to set
the slot's LOOP to ON; with it the cloud runs until the AMP envelope ends it.

## Reading the sample at any position

Grains need random access, the stock streamer is sequential. The pool page
walk does exactly this for the sample-save path:

- 🟡 `0x4009499c(slotId, position, 1)` → `d0` pointer, `d1` contiguous run
  at that frame (`docs/firmware/SAMPLE_SAVE.md` §4; two callers; branches on
  recorder slots 128–135).
- 🟡 Pool: 6,144-byte blocks from `0x40A955E0`, 6 B per 24-bit stereo frame
  in recorder buffers (`RECORDER.md` §2). Whether FLEX slots loaded from a
  16-bit file are packed 4 B or 6 B per frame is **unknown** — the save path's
  16/24-bit converter switch (`0x40021042`) suggests both exist.
- The settings record (`0x100b14f0 + 0x448·slot`) and the voice struct's
  `+4/+8` give the slot; `+40` holds the trim region (`COLDFIRE_PORT.md`).

**Risk to measure first:** whether the page walk is safe and cheap in the
frame interrupt (a mutex, a cache miss chain, a long walk on a fragmented
pool). The design calls it once per grain chunk, not per sample, and caches
`(pointer, run)` per grain; a grain crossing a run boundary re-walks.

## The engine

Per track, up to 8 grain slots. Each grain: start frame, phase (Q16 frames),
increment (pitch), length, window position, pan.

Per output sample: for each live grain, read two packed frames at
`pos >> 16`, interpolate linearly, multiply by the window, pan, accumulate.
Scheduler: a grain starts every `size / density` samples; its start is
`position + scan_offset ± spray·random`, clamped to the trim region.

Window: a 257-entry Hann table (like `sy_tab`), stretched to the grain
length. SHAPE morphs Hann → trapezoid (flat top, for denser, smoother
textures) by indexing the table with a clamped, scaled phase.

### Controls (PLAYBACK page, 6 slots, all lockable / LFO-able)

| Slot | Stock | GRAIN | Range |
|---|---|---|---|
| A | PTCH | PITCH | grain pitch, stock arithmetic (keys, quantizer, locks) |
| B | STRT | POS | 0–127 across the trim region |
| C | LEN | SIZE | 5 ms – 1 s, exponential |
| D | RATE | SCAN | playhead motion, bipolar: 64 frozen, 127 forward at 1×, 0 reverse at 1× |
| E | RTRG | SPRY | position randomisation, 0 – the whole region |
| F | RTIM | DENS | grains per grain-length, 1–8 |

A second page (the LFO-page clone the synth uses for VOIC/CHRD) is phase 2:
SHAPE, PITCH SPRAY, STEREO spread, MODE (CLASSIC / LOOP / CLOUD).

### Cost budget

The synth's measured mono path costs ~900–1,150 instructions a frame for a
playing track (`modules/synth/upstream/synth/README.md`, stock FLEX cost
table). GRAIN at 8 grains × 16 samples × ~30 instructions ≈ 3,800 per frame
per track before page walks — roughly 4× the synth. POLY8 hit 100 % CPU at
four uncached voices and needed a governor. So GRAIN ships with one:

- time its own render each frame (DTCN3, as POLY8 0.3.1);
- above a per-track budget, lower the live grain cap (oldest first);
- run its buffers through the cached alias.

Target: one GRAIN track at full density under 10 % of a 362.8 µs frame;
four tracks playable.

## Plan

0. **Measure** (port, no hardware): page walk from the frame interrupt —
   pointer, run, cost, and the FLEX frame packing for a 16-bit and a 24-bit
   file. Go/no-go for random access.
1. **Mono grain, fixed window, POS/SIZE only.** `make check` + an emulator
   capture of a known sample: grains land at POS, window is Hann.
2. **Scheduler, SPRY, DENS, SCAN, PITCH.** Governor and cost table.
3. **Page** (labels, formatters) by cloning the synth's page mechanism.
4. **Card image on your MKI**, LOOP ON, one pad sample. Hardware notes in
   `README.md`, flashed image in `CHANGELOG.md`.
5. **Modwerk package:** `ot_machines` contribution, `runtime.json`,
   `octamod.module.json`, `evidence/performance.json`, the room proposal for
   `ot_machines`, thumbnail. Owner approves the first release.

## What would falsify this

- The page walk takes a lock or blocks → random access needs a per-grain
  prefetch on the UI task into a ring, which changes the design.
- FLEX samples are not packed the way recorder buffers are → the read path
  needs the converter's two formats.
- The trim end ends the voice even with LOOP ON at rate 1.0 → the wrapper
  must keep the stock stream alive another way.
