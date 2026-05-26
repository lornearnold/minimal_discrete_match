# Storyboard

General storyboard sketches are in "Research Notes.pdf"

Use the scenes elements that are appropriate from the "manim_exploration" project, which is similar to this, but a different audience. Also use the style choices (avoid fades to black between scenes, dark background with light text)

The entire video should be 1 minute in length, with roughly equal time for each scene.


## Scene 1

Frame has a top, title level blank space, a figure axes on the left half, an image frame on the right half, with a little space between the halves for a left-to-right block arrow.

On the figure axes, start with a cumulative distribution function curve that's towards the larger grain size end, then show the arrow, then GSD_0.png.
Above the arrow, add: $N_{min} = $???
Cycle to GSD_1.png, then GSD_2.png and add a line to the figure axes with each new GSD image that stretches the CDF lower end further to the left. Only the lower left side of the CDF should be changing. the upper right can stay at the same place.

Then add the question prominently across the entire top of the slide: "What is the smallest number of discrete particles needed to match a given grain size distribution?"
Place a box around the question

Just below the box, add the text: Minimal Discrete Match (MDM)


## Scene 2

Title text: Total mass ratios

Start with array of horizontal dashed lines on the left side. Three dashed lines and the bottom line solid. use dots between the upper two and the lower ones to indicate an arbitrary number.

Add shapes representing piles of mass lying flat on the bottom and upper two dashed lines. The shapes should be different sizes, but arbitrarily so. Use thick solid lines for the shape border and lighter fill of similar color. Place $M_i$ inside each shape with the top shape's index = N, the next N-1 and the bottom =1. 

Then show the division symbol and $M_N$ as denominator.

Then show the resulting array/vector with 1 at the top and the "real number" symbol and ellipses elsewhere. The vector = uppercase Phi (mod. from Research Notes layout: place Phi above the vector)


## Scene 3



Title text: Particle "Volume" Ratios

Start with same array of horizontal lines (keep them from previous and fade everything else away)

Add circles representing the size of individual particles in the same size categories that there were piles for before. The smallest circle should just be a bold dot. Draw the circles towards the right side of the dashed lines because when the division slash is added, the next part will go in the numerator.

Then show the division symbol and the largest particle size as numerator.

Then show the resulting array/vector with 1 at the top and the "$R > 1$" (use real number symbol) and ellipses elsewhere. The vector = uppercase Zeta (mod. from Research Notes layout: place Zeta above the vector)

## Scene 4

Title text: Quantity ratios

Fade the vector away and slide the particle volume sieve stack figure over to the right just enough to let the mass ratio sieve stack figure appear on the left.

Add a multiplication symbol between each of the corresponding ratios and then add a vector.

Add vector labels above the sieve stack figures and resulting vector: $\Phi \times \Zeta = \Kappa$

Add a box around all vector entries except the top one with a callout box: "Non integers!"

mod. from Research Notes layout: Overlay a text box that says "How to find the minimum possible integer representation of $\Kappa$ for a zero error match? Come see Poster 2205!"

The textbox overlay can cover the portion of the sieve stack figures and vector that all have the ellipses. Include a short pause before the "come see poster" text.

## Scene 5

Title text: Verification and/nExample usage

Left side, verification plot (from other manim exploration). Similar reveal sequencing, with verification data shown first, circled (with slope-aligned ellipse) and labeled "Verification". Then show and circle the four unscaled prediction points. instead of labeling them, add an arrow that goes off to the right and points to the first entry in a list of text that gets revealed from top to bottom:

- Experimental design
- Any grain size dist.
- Arbitrary shapes
- Closed form 
- $N_{min}(GSD)$
- GSD --> computation cost
- Representative volume

mod. from Research Notes layout: don't include bold MDM = N... text at the top (using a bullet instead). Instead of green/red checks/X on the right, use them as the bullets for the list.
