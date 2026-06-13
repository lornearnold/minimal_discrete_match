// =============================================================================
// ICSMGE 2026 Poster — Minimal discrete matches for target GSDs
// A0 portrait (841 mm x 1189 mm).
// Layout reproduces cmlkirsa4129c0qy1p2e5rt4e-icsmge-2026-template-poster-a0.pptx
// =============================================================================

#let brand-red  = rgb("#AB2847")
#let dark-gray  = rgb("#5B5B5B")
#let light-gray = rgb("#B2B3B3")

#let paper-id   = "2205"

// ---- Page setup ----
#set page(
  width:  841mm,
  height: 1189mm,
  margin: 0mm,
)

// Default text style for the whole poster.
#set text(font: ("Arial", "Helvetica"), size: 32pt, fill: black)
#set par(justify: true, leading: 0.55em, first-line-indent: 0mm)

// =============================================================================
// HEADER ZONE (top, above red rule at y = 209.6 mm)
// =============================================================================

// Conference banner — top of page, above title
#place(
  top + left,
  dx: 40mm, dy: 26.5mm,
  box(width: 594.3mm,
    text(size: 18pt, fill: dark-gray)[
      21#super[st] International Conference on Soil Mechanics and Geotechnical
      Engineering #h(0.4em) | #h(0.4em) Geotechnical Challenges in a Changing
      Environment #h(0.4em) | #h(0.4em) Vienna, Austria, 14 – 19 June 2026
    ],
  ),
)

#place(
  top + left,
  dx: 39.5mm, dy: 34mm,
  line(length: 495mm, stroke: 1pt + dark-gray),
)

// Title
#place(
  top + left,
  dx: 40mm, dy: 45mm,
  box(width: 594.3mm, height: 60mm,
    text(size: 44pt, weight: "bold", fill: brand-red)[
      Minimal discrete matches for target grain size distributions
    ],
  ),
)

// Authors (presenting author bold; affiliation superscript)
#place(
  top + left,
  dx: 40mm, dy: 70mm,
  box(width: 594.3mm, height: 33.8mm,
    text(size: 32pt, fill: black)[
      *Lorne Arnold*#super[1)], Caleb Arnold#super[2)]
    ],
  ),
)

// Affiliations
#place(
  top + left,
  dx: 40mm, dy: 90mm,
  box(width: 594.3mm, height: 46.1mm,
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
  dx: 677.2mm, dy: 26.3mm,
  image("assets/logos/icsmge_2026_vienna_large.jpg", width: 128mm),
)

// Red rule below header
#place(
  top + left,
  dx: 39.5mm, dy: 130mm,
  line(length: 762mm, stroke: 1.6mm + brand-red),
)

// =============================================================================
// FOOTER ZONE (bottom, below red rule at y = 1096.1 mm)
// =============================================================================

// Red rule above footer
#place(
  top + left,
  dx: 39.5mm, dy: 1096.1mm,
  line(length: 762mm, stroke: 1.6mm + brand-red),
)

// Paper ID box — brand-red fill, white text
#place(
  top + left,
  dx: 39.1mm, dy: 1124.6mm,
  box(
    width: 73.1mm, height: 29mm,
    fill: brand-red,
    inset: (x: 4mm, y: 3mm),
    text(fill: white, weight: "bold")[
      #text(size: 14pt)[Paper ID:]
      #v(-3pt)
      #text(size: 22pt)[#paper-id]
    ],
  ),
)

// Footer logos
#place(
  top + left,
  dx: 260.4mm, dy: 1111.4mm,
  image("assets/logos/simsg_issmge.png", width: 64.8mm, height: 52.1mm),
)
#place(
  top + left,
  dx: 358.8mm, dy: 1128.8mm,
  image("assets/logos/oegg_austrian_society_geomechanics.png", width: 113.6mm),
)
#place(
  top + left,
  dx: 501.3mm, dy: 1124.9mm,
  image("assets/logos/austrian_geotechnical_society.png", width: 73.3mm),
)

// Contact info for presenting author (bottom-right)
#place(
  top + left,
  dx: 574.7mm, dy: 1102.7mm,
  box(width: 227.2mm, height: 22.2mm,
    text(size: 14pt, fill: dark-gray)[
      Contact information for the presenting author: \
      Lorne Arnold — arnoldl\@uw.edu
    ],
  ),
)

// =============================================================================
// BODY ZONE — 3 columns inside (x=39.8, y=220.5, w=761.0, h=863.4 mm)
// Columns: 245.2 mm wide, 12.7 mm gutter, 3 columns
// =============================================================================

// Heading helper — red bold heading, no extra space above when first in column
#let heading-style(body) = {
  set text(size: 36pt, weight: "bold", fill: brand-red)
  set par(justify: true, first-line-indent: 0mm)
  v(0.4em, weak: true)
  body
  v(0.3em, weak: true)
}

#let h1(body) = heading-style(body)

// Subsequent-paragraph indent of 10 mm is achieved with first-line-indent
// applied to non-first paragraphs.  Typst's `first-line-indent` only applies
// to paragraphs after the first by default, which matches the template spec.
#set par(first-line-indent: (amount: 10mm, all: false))

// Figure caption helper (24 pt, justified, "Figure N. ...")
#let fig-cap(num, body) = {
  set text(size: 24pt, fill: black)
  set par(justify: true, first-line-indent: 0mm)
  v(0.3em)
  [*Figure #num.* #body]
}

#let lorem-para = [
  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
  eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
  voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet
  clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit
  amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
  nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.
]

#let lorem-short = [
  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
  eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
  voluptua.
]


#place(
  top + left,
  dx: 80mm, dy: 131mm,
  figure(
        image("assets/figures/PosterVersion0000.png", width: 425mm),
        caption: none,
      )
  
)

#place(
  top + left,
  dx: 39.8mm, dy: 141mm,
  box(width: 761mm, height: 930mm,
    columns(3, gutter: 12.7mm)[
      #v(220mm)

    #fig-cap(1)[The problem: minimal mapping of GSD to DEM] 
      #h1[Introduction]
      Soil is fundamentally a discrete material that is, nevertheless, commonly modeled as a continuum in part because of the computational expense of large-scale discrete element models (DEMs).
      But exactly how computationally expensive is it to represent a given soil with discrete particles?
      In other words, What is the smallest number of discrete particles needed to match a given grain size distribution?
      
      The *minimal discrete match (MDM)* is the smallest set of discrete particles needed to match a given GSD.\
      \
      

      #h1[GSD study suite]
      #figure(
        image("assets/figures/figure1_gsd_curvature_index.png", width: 100%),
        caption: none,
      )
      #fig-cap(1)[Representative subset of the GSD suite with one example
        highlighted. The ratio of the red to blue dashed areas defines the
        curvature index #math.italic("I_C").]
      
      \
      #h1[Discrete definitions]
      Definitions needed: Sample, Grain Size Distribution, Conditions 1 - 4.

      *Sample*: \ 
      $S = {(X_S,Q_S) in I_S}$ where \
      $X_S$ is an ordered set of sizes in $S$,\
      $Q_S$ is an unordered set of quantities,\
      $I_S$ is the index set of the sample.\

      *Grain size dist.*:\
      $G = {(X_S,M_S) in I_S}$ where \
      $X_G$ is an ordered set of sizes in $G$,\
      $M_G$ is an unordered set of masses,\
      $I_G$ is the index set of the grain size distribution. \
      #linebreak()
      
      \
      #v(220mm) 

      

      Conditions summary:\
      // There are at least four conditions relating $S$ and $G$ to be satisfied (see Paper 2205 for details).
      // In summary, the conditions say that a discrete sample, $S$, is a discrete match for a grain size distribution, $G$, if the sum of all the massess of all the particles between each size in $X_G$ is equal to the associated mass $M_G$.

      

      



      



      #h1[Minimal discrete match solution]
   

Quantity Ratio:\
      $Phi = {m_j/m_(n_G-1) : j in I_G - 1}$; with elements $phi_j$ \ \
      
      $Zeta = {f(x_(n_S))/f(x_i) : i in I_S}$; with elements $zeta_i$ and where $f(x)$ is some mapping of $x arrow $ mass. \ \


      $Kappa = {phi_i times zeta_i: i in I_S}$; with elements $kappa_i$\

      Unfortunately, only $kappa_(n_S)$ is an integer and partial discrete particles are not allowed.
      Rounding $Kappa$ to the nearest integer set gives a first-order approximation of the $M D M$, possibly sufficient or wildly inadequate depending on the application.

      #figure(
        image("assets/figures/figure2_convergence.png", width: 100%),
        caption: none,
      )
      #fig-cap(3)[Convergence of discrete match error for the fixed-size and
        spanned-integer algorithms across the GSD suite.]
        In addition to showing an extremely broad span over common soil types, the MDM concept can predict the number of particles needed to produce discrete samples of any volume.

      // A brute force approach would be to incrementally increase $Kappa$ and re-round to the nearest integer (see paper for details). 
      // This assumes the sizes are fixed (therefore it's the Fixed Size algorithm).
      // But this is inefficient (requires several iterations) and incorrect because of the over-constraint of fixing size.
      

      // Spanned integer algorithm.
      // The Spanned Integer algorithm takes advantage of the full range of possible values for $X_S$ and only iterates if the quantity ratios for the largest and smallest allowable sizes ($kappa_+$ and $kappa_-$, respectively) span an integer (thus the Spanned Integer algorithm).
      // This finds the number of particles for each size in the MDM.
      // The specific sizes in $X_S$ are found by inverting the mass scaling function $f(x)$ (see paper for details).

      

      #h1[Results]

      Comparison with independent DEM work verifies the MDM's capability.
      Because the MDM answers the fundamental question What is the ...
      it's a powerful tool for experimental design in DEM for geomechanics simulations.

      Essentially, MDM represents an analytical mapping from grain size distribution directly to computational time complexity without the need to generate any DEM samples.

      #figure(
        image("assets/figures/figure6_uscs_n.png", width: 100%),
        caption: none,
      )
      #fig-cap(3)[Convergence of discrete match error for the fixed-size and
        spanned-integer algorithms across the GSD suite.]
      
      

      #figure(
        image("assets/figures/figure3_demo_comparison.png", width: 100%),
        caption: none,
      )
      #fig-cap(3)[Convergence of discrete match error for the fixed-size and
        spanned-integer algorithms across the GSD suite.]


      

      #h1[Conclusions]
      #lorem-short

      #h1[References]
      #set text(size: 22pt)
      #set par(first-line-indent: 0mm, leading: 0.4em)
      Asadzadeh, M. and Soroush, A., 2017. Macro- and micromechanical
      evaluation of cyclic simple shear test by discrete element method.
      _Particuology_ 31, 129–139.

      #v(0.4em)
      Been, K., Jefferies, M. and Hachey, J., 1991. The critical state of
      sands. _Géotechnique_ 41(3), 365–381.

      #v(0.4em)
      Terzaghi, K., 1925. _Erdbaumechanik auf bodenphysikalischer Grundlage._
      Vienna: Deuticke.


      
    ]
  ),
)
