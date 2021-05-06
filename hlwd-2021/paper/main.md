\newpage
\linenumbers

## Abstract

Fracture and joint measurements from the field, for example, fracture orientation and aperture data, and length measurements by scan line method, can be reproduced to statistically identical joint sets. The statistical joint sets are assumed to have equal hydrogeological and geomechanical properties to those of the original base rocks.

We analyze joints properties obtained in situ to estimate useful hydrogeological parameters such as permeability and anisotropic raito of the fractured aquifer. To do this, first we group all the measured joints into subsets which assumed to follow fisher distribution. Fracture lengths and aperture data are best if obtainable from the field, otherwise it can be set under proper assumptions.

Then joint are generated following strictly rules to match original joint sets statistically.
Finally we conduct numerical modeling to estimate hydrogeological properties using generated joint sets. Generated and discretized fracture system can be upscaled to feed a continuum model which represent regional groundwater flow in the fractured aquifer and is potentially useful to obtain information when constructing nuclear wasted disposal site.

Finally we try to predict the fates of various nuclear species possibly leaked through the waste container to near environment.




## Introduction

There are many precedent research on characterizing hydrogeology of potential nuclear waste disposal sites [many references]. And discrete fracture network (DFN) modeling is one of most frequently used modeling options [reference]. Recently hybrid approach appears that one can use both continuum model and DFN model in the same domain if boundaries of those models are properly treated [reference].

Here we used dfnWorks to generate virtual joints and PFLOTRAN to simulate generated fracture blocks to estimate hydrogelogical properties. Both dfnworks and pflotran are developed in Los Alamos National Laboratory (LANL) and seamlessly operable under python environment [reference].

The purpose of the paper is like below. First, we characterize fractured aquifers in the research area by using fracture properties obtained from various field and borehole tests. Second, we estimate hydrogeological properties by numerically simulating statistically identical joints sets made by DFN model. Finally, the generated model will be upscaled to be utilized by the continuum flow and reactive transport model to predict consequence of contingency leakage scenarios in the potential high-level nuclear waster disposal candidate sites.

The scope of this paper: Generating joint sets representing the sites using borehole test data. Estimating hydraulic conductivity and anisotropic ratio. Building hydrogeological model representing fractured aquifer system of the candidate sites. Modeling leakage scenario and predict efficiency of the candidate site perspective to isolate nuclear waste disposal site from near hydraulic environment.


## Backgrounds

**Discrete fracture network model**

Previous studies on DFN model: history and important issues, Who did what, What important papers directly related to this paper.

**Reactive transport model of nuclear waste disposal site**

Previous studies, case studies, good examples utilize reactive transport model and DFN model techniques.
What they found out and key issues to be solved.

## Methods

**Joint set grouping**

[//]: <> (Filtering joints)
Joint data available from the borehole television include orientation, aperture, and spacing of fracture.
Not all joints are needed to estimate hydraulic properties of the rock. Some joints are closed or isolated from other joint cluster and not involved in groundwater flow. We only consider joints that are assumed to be open and works as groundwater conduits.

How do we know the fracture is open? We assume that the joints located in the permeable intervals which identified as conduits are open and actively engaged in conduit groundwater. The permeable intervals are identified by separately operated Lugeon tests performed 4-8m intervals along the borehole.

Joint data are filtered by depth and only joints in the permeable zones will be used for analysis.
Permeable zones in Wonju testing site are listed in @tbl:permeable_zone.

!include tables/permeable_zone.md
:Permeable zone depths in the test borehole in Wonju {#tbl:permeable_zone}

Generalized qualitative classification criteria for the fracture system is organized in @tbl:class_frac. Order 4 fracture is our concern because we assume that the candidate sites are generally located in a selected pure basement rock block free of regional fracture sets.

!include tables/classification_fracture0.md
:Generalized qualitative classification criteria for the fracture system {#tbl:class_frac}

We consider only Order 4 joints and permeable joints. The joints from the borehole TV data that are not located in permeable zones are considered isolated and not interconnected for flow.

[//]: <> (joint grouping: k-means clustering)
Filtered joints are classified using cluster analysis. We used k-means clustering method.

[//]: <> (Normality test: grouped joint sets fit to fisher distribution)


**Joint generation**

Using statistical properties of each joint sets, virtual joints are generated. dfnWorks requires mean strike/dip, fisher-k, minimum and maximum fracture length, and aperture data. dfnWorks generates joints until desired joint density, $P_{32}$, reached. $P_{32}$ is defined as the total area of fracture per unit volume (@Dershowitz1984) and can be calculated using mean spacing of joint sets in borehole.

$P_{32}$ can be calculated like below (@Park2015).

$$ P_{32} = \frac{A_f}{V_t} $$ {#eq:p32_eq_af_vt}
CCwhere $A_f$ = total area of fracture and $V_t$ = total volume. $P_{32}$ is dimensional (in units of 1/m), but is a scale independent(i.e., it does not depend upon the volume studied or the orientation of the measurement). Alternative measures, such as the number of fractures per unit are, are scale dependent.

CCThe intensity of faults and fractures are frequently represented in mean spacing, $E[S_f])$, between fractures or faults within a set. The relationship between $E[S_f])$ and $P_{32}$ depends upon the distribution of the orientation of fractures relative to the line along which the spacing $S_f$ was measured:

$$ P_{32} = \frac{C_p}{E[S_f]} $${#eq:p32_eq_cp_esf}
CCwhere $C_p$ = constant dependent upon the distribution of the orientation of fractures relative to the line along which the spacing $S_f$ was measured.

CCFor a uniform distribution of fracture organization, @Dershowitz1984 found a value of $C_p$ of 2.0. For most fracture geometries, $C_p$ will vary between 1.0 and 3.0. The exact value of $C_p$ for a particular fracture and borehole geometry can be found by simulated well sampling using FracMan.

A set of joints generated by dfnWorks presented in (figure).

**Estimation of hydraulic conductivity and anisotropic ratio**





## Results and Discussion

Put figure like this.

![Example image](figures/mariecurie.jpg){#fig:fig1 width=75%}

Put equations.

$$ E = mc^2 $$ {#eq:eq_sample}
@eq:eq_sample governs the evolution of something.

## Conclusion

Conclusions here.

### Acknowlegements
Thank you.

### Reference

s
