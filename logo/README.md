# Yorosum Breath Mark (v1.1 proposal)

A redraw of the v1.0 breath mark: a still dot with two open arcs, Deep Berry `#8E2149` inside and Antique Gold `#B08A62` outside.

- **concept-A/**: Refined Breath. Symmetric about the horizontal axis.
- **concept-B/**: Rising Exhale (recommended). The arcs sweep further above the axis than below.
- **concept-B/small/**: small cut for 32 px and below, or under 8 mm in print. It has a bigger dot and heavier strokes.

All lettering is converted to outlines (Schibsted Grotesk 800/700 and Pretendard Regular), so no fonts are needed.

## Construction
- The dot radius is 9 and the stroke is 7. There is one equal gap *g* = 11.5 between the dot and the inner arc, and between the two arcs.
- Each arc's centre sits behind the dot, with radius 1.30× (inner) and 1.15× (outer) its distance along the axis.
- Concept B sweeps the inner arc from −40° to +58° and the outer arc from −42° to +62°.
- Clearspace is one dot diameter on every side. The minimum size is 24 px or 6 mm for the mark alone (small cut) and 96 px or 24 mm for the lockup.

## Variants
`primary` (on Bone or white) · `reversed` (on Deep Berry, gold arc kept, wordmark at weight 700) · `mono` (all Deep Berry) · `black` · `white` (knockout)

## Regenerate
```
pip install fonttools
python3 logo/source/generate_logo.py <fonts_dir> logo
```
`<fonts_dir>` must contain `sg600.ttf`, `sg700.ttf` and `sg800.ttf` (Schibsted Grotesk, from Google Fonts) and `Pretendard-Regular.otf` (from the `pretendard` npm package).

`source/yorosum-logo-v1.0.svg` is the original logo, kept for reference.
