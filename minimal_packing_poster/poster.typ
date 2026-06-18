// =============================================================================
// ICSMGE 2026 Poster — Minimal discrete matches for target GSDs
// A0 portrait (841 mm x 1189 mm).
// Layout reproduces cmlkirsa4129c0qy1p2e5rt4e-icsmge-2026-template-poster-a0.pptx
// =============================================================================

#let brand-red  = rgb("#AB2847")
#let dark-gray  = rgb("#5B5B5B")
#let light-gray = rgb("#B2B3B3")

#let paper-id   = "2205"

// =============================================================================
// LAYOUT VARIABLES
// Positions derive from these, so the layout reflows when you change one knob.
// Tweak `header-rule-y` to make the header taller/shorter (the body follows);
// tweak `footer-rule-y` to move the footer (the body height resizes to fit).
// =============================================================================

// ---- Page ----
#let page-w = 841mm
#let page-h = 1189mm

// ---- Margins / content box ----
#let margin    = 39.5mm                  // left & right margin for content + rules
#let content-w = page-w - 2 * margin     // full content width (≈ 762 mm)

// ---- Header zone (everything above the red rule) ----
#let header-top    = 26.5mm              // y of the first header element (banner)
#let header-rule-y = 130mm               // y of the red rule that closes the header
// Header elements stack downward from `header-top`:
#let banner-y  = header-top              // conference banner
#let bline-y   = header-top + 7.5mm      // thin rule under the banner
#let title-y   = header-top + 18.5mm     // title
#let authors-y = header-top + 43.5mm     // author line
#let affil-y   = header-top + 63.5mm     // affiliations
#let header-text-w = 594.3mm             // text column width (leaves room for logo)
#let bline-w   = 495mm                   // length of the thin banner rule
// Conference logo, right side of the header:
#let logo-w = 128mm
#let logo-x = page-w - margin - logo-w + 3.7mm   // sits flush right (slight overhang)
#let logo-y = header-top - 0.2mm

// ---- Footer zone (everything below the red rule) ----
#let footer-rule-y = 1096.1mm            // y of the red rule that opens the footer
// Paper-ID box, left:
#let paper-id-w = 73.1mm
#let paper-id-h = 29mm
#let paper-id-x = margin
#let paper-id-y = footer-rule-y + 28.5mm
// Contact block, right (right-aligned to the content edge):
#let contact-w = 230mm
#let contact-x = page-w - margin - contact-w
#let contact-y = footer-rule-y + 6.6mm

// ---- Body zone (the 3 columns between the two red rules) ----
#let body-gap        = 11mm              // gap from header rule down to body top
#let body-bottom-gap = 10mm              // gap from body bottom up to footer rule
#let body-top   = header-rule-y + body-gap
#let body-h     = footer-rule-y - body-top - body-bottom-gap
#let n-cols     = 3
#let col-gutter = 12.7mm
#let col-w      = (content-w - (n-cols - 1) * col-gutter) / n-cols  // one column
// The hero figure + intro text occupy columns 1+2 (a 2-column flow with the
// figure floated across the top). Column 3 is independent and runs the full
// body height from the top, so it reaches up to the header rule.
#let left-block-w = 2 * col-w + col-gutter            // span of columns 1+2
#let col3-x       = margin + left-block-w + col-gutter // left edge of column 3

// ---- Page setup ----
#set page(
  width:  page-w,
  height: page-h,
  margin: 0mm,
)

// Default text style for the whole poster.
#set text(font: ("Arial", "Helvetica"), size: 32pt, fill: black)
#set par(justify: true, leading: 0.55em, first-line-indent: 0mm)

// =============================================================================
// HEADER ZONE
// =============================================================================

// Conference banner — top of page, above title
#place(
  top + left,
  dx: margin, dy: banner-y,
  box(width: header-text-w,
    text(size: 18pt, fill: dark-gray)[
      21#super[st] International Conference on Soil Mechanics and Geotechnical
      Engineering #h(0.4em) | #h(0.4em) Geotechnical Challenges in a Changing
      Environment #h(0.4em) | #h(0.4em) Vienna, Austria, 14 – 19 June 2026
    ],
  ),
)

#place(
  top + left,
  dx: margin, dy: bline-y,
  line(length: bline-w, stroke: 1pt + dark-gray),
)

// Title
#place(
  top + left,
  dx: margin, dy: title-y,
  box(width: header-text-w, height: 60mm,
    text(size: 44pt, weight: "bold", fill: brand-red)[
      Minimal discrete matches for target grain size distributions
    ],
  ),
)

// Authors (presenting author bold; affiliation superscript)
#place(
  top + left,
  dx: margin, dy: authors-y,
  box(width: header-text-w, height: 33.8mm,
    text(size: 32pt, fill: black)[
      *Lorne Arnold*#super[1)], Caleb Arnold#super[2)]
    ],
  ),
)

// Affiliations
#place(
  top + left,
  dx: margin, dy: affil-y,
  box(width: header-text-w, height: 46.1mm,
    text(size: 24pt, fill: dark-gray)[
      #super[1)] University of Washington Tacoma, School of Engineering and
      Technology, Tacoma, WA, USA \
      #super[2)] Hunt Middle School, Tacoma, WA, USA
    ],
  ),
)

// Conference logo, top-right
#place(
  top + left,
  dx: logo-x, dy: logo-y,
  image("assets/logos/icsmge_2026_vienna_large.jpg", width: logo-w),
)

// Red rule below header
#place(
  top + left,
  dx: margin, dy: header-rule-y,
  line(length: content-w, stroke: 1.6mm + brand-red),
)

// =============================================================================
// FOOTER ZONE
// =============================================================================

// Red rule above footer
#place(
  top + left,
  dx: margin, dy: footer-rule-y,
  line(length: content-w, stroke: 1.6mm + brand-red),
)

// Paper ID — gray label + brand-red bold number, baseline-aligned on one line
#place(
  top + left,
  dx: paper-id-x, dy: paper-id-y,
  box(height: paper-id-h,
    text(size: 32pt, fill: light-gray)[Paper ID:]
      + h(0.3em)
      + text(size: 44pt, weight: "bold", fill: brand-red)[#paper-id],
  ),
)

// Footer logos (bespoke horizontal placement; vertical tied to footer rule)
#place(
  top + left,
  dx: 260.4mm, dy: footer-rule-y + 15.3mm,
  image("assets/logos/simsg_issmge.png", width: 64.8mm, height: 52.1mm),
)
#place(
  top + left,
  dx: 358.8mm, dy: footer-rule-y + 32.7mm,
  image("assets/logos/oegg_austrian_society_geomechanics.png", width: 113.6mm),
)
#place(
  top + left,
  dx: 501.3mm, dy: footer-rule-y + 28.8mm,
  image("assets/logos/austrian_geotechnical_society.png", width: 73.3mm),
)

// Contact info for presenting author (bottom-right)
#place(
  top + left,
  dx: contact-x, dy: contact-y,
  box(width: contact-w, height: 22.2mm,
    align(right,
      text(size: 32pt)[
        #text(fill: light-gray)[Contact information for the presenting author:]\
        *arnoldl\@uw.edu*
      ],
    ),
  ),
)

// =============================================================================
// BODY ZONE — 3 columns between the two red rules
// =============================================================================

// Heading helper — red bold heading, no extra space above when first in column
#let heading-style(body) = {
  set text(size: 36pt, weight: "bold", fill: brand-red)
  set par(justify: true, first-line-indent: 0mm)
  v(0.6em, weak: true)
  body
  v(0.4em, weak: true)
}

#let h1(body) = heading-style(body)

// Heading helper 2 — black bold heading
#let heading-style2(body) = {
  set text(size: 33pt, weight: "bold")
  set par(justify: true, first-line-indent: 0mm)
  v(0.6em, weak: true)
  // Wrap in a block so the following paragraph doesn't count as "following a
  // paragraph" — this suppresses the 10 mm first-line-indent after the heading.
  block(spacing: 0pt, body)
  v(0.4em, weak: true)
}

#let h2(body) = heading-style2(body)

// Subsequent-paragraph indent of 10 mm is achieved with first-line-indent
// applied to non-first paragraphs.  Typst's `first-line-indent` only applies
// to paragraphs after the first by default, which matches the template spec.
#set par(first-line-indent: (amount: 10mm, all: false))

// Figure caption helper (24 pt, justified, "Figure N. ...")
#let fig-cap(num, body) = {
  set text(size: 24pt, fill: black)
  set par(justify: true, first-line-indent: 0mm)
  v(0.4em)
  [*Figure #num.* #body]
}


// ---- LEFT BLOCK: columns 1+2, hero figure floated across the top ----
#place(
  top + left,
  dx: margin, dy: body-top,
  box(width: left-block-w, height: body-h,
    columns(2, gutter: col-gutter)[
      // Hero figure spans the full width of columns 1+2 and reserves its own
      // height automatically — text flows below it, no manual spacing needed.
      #place(top, scope: "parent", float: true,
        block[
          #image("assets/figures/PosterVersion0000.png", width: 100%)
          #fig-cap(1)[The aim of this work is a rigorous mathematical answer to this question. The answer is the *minimal discrete match* (MDM).]
        ]
      )

      #h1[Introduction]
      Soil is fundamentally a discrete material but commonly modeled as a continuum.
      DEM is computationally expensive and lags behind predictions of feasibility (Cundall 2001). 
      But how computationally expensive will a DEM simulation of a particular soil be?
      In other words, What is the smallest number of discrete particles needed to match a given grain size distribution? The *minimal discrete match* (MDM) is the smallest set of discrete particles needed to match a given GSD.\


      #h1[GSD study suite]
      A series of grain size distributions is considered to study the spread of MDM across the USCS.
      #figure(
        image("assets/figures/figure1_gsd_curvature_index.png", width: 100%),
        caption: none,
      )
      #fig-cap(1)[Representative subset of the GSD suite with one example
        highlighted. The ratio of the red to blue dashed areas defines the
        curvature index $I_C$.]

      
      #h1[Discrete definitions]
      Mathematical definitions of common soil descriptions are needed (see paper for details):

      #h2[Sample definition]
      $S = {(X_S,Q_S) in I_S}$ where \
      $X_S$: an ordered set of sizes in $S$,
      $Q_S$: an unordered set of quantities,
      $I_S$:the index set of the sample.

      #h2[Grain size distribution definition]
      $G = {(X_S,M_S) in I_S}$ where\
      $X_G$: an ordered set of sizes in $G$,
      $M_G$: an unordered set of masses,
      $I_G$: the index set of the grain size distribution. 
    
      // Conditions summary:\
      // There are at least four conditions relating $S$ and $G$ to be satisfied (see Paper 2205 for details).
      // In summary, the conditions say that a discrete sample, $S$, is a discrete match for a grain size distribution, $G$, if the sum of all the massess of all the particles between each size in $X_G$ is equal to the associated mass $M_G$.













      #h1[Minimal discrete match solution]
      The solution to the minimal discrete match is built from the bulk mass ratio, $Phi$, the "volume ratio" (i.e., the individual particle mass ratio), $Zeta$, and the quantity ratio, $Kappa$:

      $Phi = {m_j/m_(n_G-1) : j in I_G - 1}$; with elements $phi_j$ \ \

      $Zeta = {f(x_(n_S))/f(x_i) : i in I_S}$; with elements $zeta_i$ and where $f(x)$ is some mapping of $x arrow $ mass. \ 


      $Kappa = {phi_i times zeta_i: i in I_S}$; with elements $kappa_i$\

      Only $kappa_(n_S)$ is an integer.
      The *Fixed Size* algorithm rounds $Kappa$ to the nearest integer set (sufficiency varies by application).
      The *Spanned Integer* algorithm takes advantage of the full range of possible values for $X_S$ and identifies whether the quantity ratios for the largest and smallest allowable sizes ($kappa_+$ and $kappa_-$, respectively) span an integer.
      Iteration is only required until they do.
      // This finds the number of particles for each size in the MDM.
      // The specific sizes in $X_S$ are found by inverting the mass scaling function $f(x)$ (see paper for details).

      #figure(
        image("assets/figures/figure2_convergence.png", width: 100%),
        caption: none,
      )
      #fig-cap(3)[Convergence of discrete match error for the fixed-size and
        spanned-integer algorithms across the GSD suite.]
      
      The spanned integer algorithm is an analytical solution for a zero-error match between any GSD and the minimum number of  discrete particles needed to replicate its mass distribution. 
      *NOTE: the MDM $!=$ the representative volume (RV).*
      // NOTE: the MDM is a mass-based quantity, not a mechanical one. The MDM $!=$ the representative volume (RV)!

      // A brute force approach would be to incrementally increase $Kappa$ and re-round to the nearest integer (see paper for details).
      // This assumes the sizes are fixed (therefore it's the Fixed Size algorithm).
      // But this is inefficient (requires several iterations) and incorrect because of the over-constraint of fixing size.


      // Spanned integer algorithm.
      // The Spanned Integer algorithm takes advantage of the full range of possible values for $X_S$ and only iterates if the quantity ratios for the largest and smallest allowable sizes ($kappa_+$ and $kappa_-$, respectively) span an integer (thus the Spanned Integer algorithm).
      // This finds the number of particles for each size in the MDM.
      // The specific sizes in $X_S$ are found by inverting the mass scaling function $f(x)$ (see paper for details).
    ]
  ),
)

// ---- COLUMN 3: independent, full body height, reaches up to the header ----
// To rebalance, move content across this divider: anything above stays in the
// left two-column block; anything below renders in column 3.
#place(
  top + left,
  dx: col3-x, dy: body-top,
  box(width: col-w, height: body-h, [
      #h1[Results]
      The MDM shows a broad range (9 orders of magnitude!) of minimum particles to match granular USCS soils.
    
      #figure(
        image("assets/figures/figure6_uscs_n.png", width: 100%),
        caption: none,
      )
      #fig-cap(3)[Convergence of discrete match error for the fixed-size and
        spanned-integer algorithms across the GSD suite.]
      
      The MDM matches independent DEM studies and predicts unscaled DEM time complexity.
      #figure(
        image("assets/figures/figure3_demo_comparison.png", width: 100%),
        caption: none,
      )
      #fig-cap(3)[Convergence of discrete match error for the fixed-size and
        spanned-integer algorithms across the GSD suite.]

      #h1[Conclusions]
      MDM is a powerful analytical tool for experimental design in DEM. 
      It maps GSDs to computational effort without generating a DEM sample.

      #h1[References]
      #set text(size: 22pt)
      #set par(first-line-indent: 0mm, hanging-indent: 10mm, leading: 0.4em)
      Cundall, P. A. (2001). A discontinuous future for numerical modelling in geomechanics? Proceedings of the Institution of Civil Engineers - Geotechnical Engineering, 149(1), 41–47. https://doi.org/10.1680/geng.2001.149.1.41


      #v(0.4em)
      Esperança, C. (2023, June 23). 3D Apollonian Sphere Packings (Observable). https://observablehq.com/@esperanc/3d-apollonian-sphere-packings


      #v(0.4em)
      Zeraati-Shamsabadi, M., & Sadrekarimi, A. (2025). A DEM study on the effects of specimen and particle sizes on direct simple shear tests. Granular Matter, 27(2). https://doi.org/10.1007/s10035-025-01513-y




    ]
  ),
)
