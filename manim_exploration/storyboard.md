# Storyboard


Order 
 - intro
   - In soil mechanics, we have this problem: we want to model soil, but there are too many particles to count. And even if we could, there would be far too many particles to simulate.
 - sieve stack
   - So we use sieves to find out how much mass is in different size ranges.
 - continuum reveal (defining "g")
   - In practice, we'd use many more sieve sizes to get a smoother curve, but we're going to stick with three for the rest of the visuals
 - define "s"
   - there are many sets of particles that could be compatible with G, but we're interested in finding the one with the smallest number of particles. We call this the Minimal Discrete Match (MDM) to find the MDM, it's helpful to have some ratios to work with
 - mass ratio
 - volume ratio 
 - define quantity ratio
   - multiply mass ratio times volume ratio
   - problem: only one entry is guaranteed to be an integer
 - error



# script

When faced with a soil mechanics problem, we may need to simulate the soil itself. The problem with this is we can't individually measure all the particles, and even if we could, there would be far too many particles to simulate. 

To help with this, we can use sieves to find the weight of all the grains within a certain diameter. 

This curve describes the mass distribution of the sample's grain sizes, which we will call "G." We can use this as a baseline to find a set of particles to simulate - we will try to find a solution that satisfies G. 

There are many sets of particles (or "S") that are compatible "G," but we are interested in finding the one with the fewest particles. We call this solution the Minimal Discrete Match. (MDM)

To find the MDM, it is helpful to have some ratios.

We can calculate the ratios of mass by dividing each mass by the mass of the biggest grains.

(define volume ratios - in a way that leaves speculation about being able to move them around)

By multiplying these ratios, we get quantity ratios - or ratios of how many particles are in each size range. The problem now becomes finding an integer solution to these ratios.

We can now write an algorithm to find an integer solution by duplicating and rounding the quantity ratio until we fall under our margin of error. 

This approach uses only fixed volume ratios, but we can utilize the ability to change them to find a smaller solution. We can calculate a range of quantity ratios and find an integer number of particles falls between them. Using this new algorithm, we can accurately predict the number of particles needed to build models of real-world soil.
