# ICSMGE 2026 Poster Template — Extracted Specification

Source: `cmlkirsa4129c0qy1p2e5rt4e-icsmge-2026-template-poster-a0.pptx`

## Page

- Size: **A0 portrait**, 841 mm × 1189 mm
- Margins (effective): 39.5–40.0 mm left/right, 26.5 mm top, ~12 mm bottom (below footer line)

## Color palette (theme `ICSMGE`)

| Role | Hex | Notes |
|------|-----|-------|
| Brand red (accent1) | `#AB2847` | Title, headings, top/bottom rules, paper ID box |
| Dark gray (accent2) | `#5B5B5B` | Affiliations, secondary text |
| Light gray (accent3) | `#B2B3B3` | Decorative |
| Dark text (dk1) | `#000000` | Body text |
| Slate (dk2) | `#44546A` | Theme dark-2 |
| Light bg (lt2) | `#E7E6E6` | Theme light-2 |

The poster uses **RGB 171/40/71 = #AB2847** as its single brand color.

## Fonts

- Major / minor in theme: Calibri Light / Calibri
- **Template explicitly specifies Arial** for all visible body content (title, authors, affiliations, headings, body, captions). Use Arial in the typst version.

## Text styles

| Element | Font | Size | Align | Color | Notes |
|---------|------|-----:|-------|-------|-------|
| Conference banner (top) | Arial | ~16–18 pt | left | `#5B5B5B` | "21st ICSMGE \| Vienna, Austria, 14–19 June 2026" |
| Title | Arial Bold | 44 pt | left | `#AB2847` | Edit title of paper |
| Authors | Arial | 32 pt | left | `#000000` | Superscript affiliation markers; presenting author **bold** |
| Affiliations | Arial | 24 pt | left | `#5B5B5B` | Superscript numbers `1)`, `2)`… |
| Section heading | Arial Bold | 36 pt | justified | `#AB2847` | Single level |
| Body text | Arial | 32 pt | justified | `#000000` | First paragraph not indented; subsequent paragraphs indent **10 mm**; no blank lines between paragraphs |
| Figure/table caption | Arial | 24 pt | justified | `#000000` | Numbering separated by period |
| Footer paper ID label | Arial Bold | small | left | white on `#AB2847` | Box at bottom-left |
| Footer contact | Arial | small | left | `#5B5B5B` | Below paper ID |
| Footer right contact | Arial | small | left | `#5B5B5B` | "Contact information for the presenting author:" |

## Layout positions (all in mm on A0 portrait)

Top zone
- Conference banner text: `x=40, y=26.5, w=594.3, h=12.0`
- Title: `x=40, y=45, w=594.3, h=60`
- Authors: `x=40, y=112.3, w=594.3, h=33.8`
- Affiliations: `x=40, y=150.7, w=594.3, h=46.1`
- **Conference logo (image1.jpg)**: `x=677.2, y=64.3, w=128.0, h=80.2` (top-right)
- Horizontal red rule across full content width: `y=209.6, x=39.5, w=762, thickness ~1.6mm`

Body zone (3 columns)
- Bounding box: `x=39.8, y=220.5, w=761.0, h=863.4`
- Three columns × **245.2 mm** each
- Gutter ≈ 12.7 mm (so 245.2 + 12.7 + 245.2 + 12.7 + 245.2 ≈ 761)
- Body fills column-by-column, top to bottom

Footer zone
- Horizontal red rule: `y=1096.1, x=39.5, w=762, thickness ~1.6mm`
- Paper ID red box ("Paper ID:" white text + number): `x=39.1, y=1124.6, w=73.1, h=29.0`
- SIMSG / ISSMGE logo (image4.png): `x=260.4, y=1111.4, w=64.8, h=52.1`
- OGG / Austrian Society for Geomechanics (image2.png): `x=358.8, y=1128.8, w=113.6, h=23.8`
- Austrian Geotechnical Society (image3.png): `x=501.3, y=1124.9, w=73.3, h=30.0`
- Bottom-right contact text: `x=574.7, y=1102.7, w=227.2, h=22.2`

## Logos (extracted into `assets/logos/`)

| File | Source | Purpose |
|------|--------|---------|
| `icsmge_2026_vienna_large.jpg` | image1.jpg | Header, top-right |
| `icsmge_2026_vienna_small.png` | image6.png | (Body sample logo in template; not used here) |
| `oegg_austrian_society_geomechanics.png` | image2.png | Footer center |
| `austrian_geotechnical_society.png` | image3.png | Footer right of center |
| `simsg_issmge.png` | image4.png | Footer left of center |

## Header banner text

`21st International Conference on Soil Mechanics and Geotechnical Engineering | Geotechnical Challenges in a Changing Environment | Vienna, Austria, 14 – 19 June 2026`
