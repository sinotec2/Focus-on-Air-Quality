---
layout: default
title: CMAQ SO4 issues
parent: Models and Comparisons
grand_parent: Paper Reviews
nav_order: 2
last_modified_date: 2022-06-04 15:49:41
---

# CMAQ SO4 issues
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## Oxidation of SO2
### [Itahashi et al., 2021][Itahashi21], Year-round modeling of sulfate aerosol over Asia through updates of aqueous-phase oxidation and gas-phase reactions with stabilized Criegee intermediates.

Sulfate aerosol (SO<sub>4</sub><sup>2−</sup>) is a main component of particulate matter in Asian countries. Accurate numerical modeling is important for appropriate policy-making aimed at reducing SO<sub>4</sub><sup>2−</sup> concentrations. The modeling performance for SO<sub>4</sub><sup>2−</sup> is superior among aerosol components, however, current models underestimate SO<sub>4</sub><sup>2−</sup> concentrations during winter over Asia. Previous studies have proposed a heterogeneous process for winter haze events, but these kinds of studies are limited spatially and temporally because they cover only mainland China in winter. Underestimation has also been reported in other regions where the aerosol concentration is much lower than in China. 

In this study, the aqueous- and gas-phase oxidation processes in the current modeling were reconsidered, and their roles were evaluated over Asia using a year-round simulation. The existing aqueous-phase oxidation of O<sub>2</sub> with Fe and Mn as catalysts was refined, and oxidation with NO<sub>2</sub> was added due to the neutralized atmosphere over Asia. For gas-phase oxidation, three stabilized Criegee intermediates (SCIs; formaldehyde oxide (CH<sub>2</sub>OO), acetaldehyde oxide (CH<sub>3</sub>CHOO), and propionaldehyde oxide ((CH<sub>3</sub>)<sub>2</sub>COO)) were introduced. Considering the uncertainty of the reaction of CH<sub>2</sub>OO with water, the upper and lower limits of the rate constant were applied. The updated oxidation processes led to an increase in the modeled SO<sub>4</sub><sup>2−</sup> concentration. The model performance over Asia in winter was effectively improved, and the updates did not degrade the model performance in other seasons. The improvements in biases were approximately 3% during winter, whereas the deterioration in biases were within 1% in spring to summer and 2% in autumn, when the lower limit of the CH<sub>2</sub>OO rate constant with water was used. The role of SCIs depended strongly on the rate constants of the reaction of CH<sub>2</sub>OO with water. The simulated concentration of SCIs agreed well with the estimated levels, and the lower limit of the rate constant of CH<sub>2</sub>OO with water fitted within the estimated SCIs concentration levels. SCIs may play an important role in SO<sub>4</sub><sup>2−</sup> production over Asia in winter, especially the downwind region of China. The approach taken in this study has the potential to improve modeling performance in other regions as well.

### [Appel et al., 2021][Appel21], The Community Multiscale Air Quality (CMAQ) model versions 5.3 and 5.3.1: system updates and evaluation. 
<p> The Community Multiscale Air Quality (CMAQ) model version 5.3 (CMAQ53), released to the public in August 2019 and followed by version 5.3.1 (CMAQ531) in December 2019, contains numerous science updates, enhanced functionality, and improved computation efficiency relative to the previous version of the model, 5.2.1 (CMAQ521). Major science advances in the new model include a new aerosol module (AERO7) with significant updates to secondary organic aerosol (SOA) chemistry, updated chlorine chemistry, updated detailed bromine and iodine chemistry, updated simple halogen chemistry, the addition of dimethyl sulfide (DMS) chemistry in the CB6r3 chemical mechanism, updated M3Dry bidirectional deposition model, and the new Surface Tiled Aerosol and Gaseous Exchange (STAGE) bidirectional deposition model. In addition, support for the Weather Research and Forecasting (WRF) model's hybrid vertical coordinate (HVC) was added to CMAQ53 and the Meteorology-Chemistry Interface Processor (MCIP) version 5.0 (MCIP50). Enhanced functionality in CMAQ53 includes the new Detailed Emissions Scaling, Isolation and Diagnostic (DESID) system for scaling incoming emissions to CMAQ and reading multiple gridded input emission files.</p> 

<p><span id="page2868"/>Evaluation of CMAQ531 was performed by comparing monthly and seasonal mean daily 8 h average (MDA8) O<span class="inline-formula"><sub>3</sub></span> and daily PM<span class="inline-formula"><sub>2.5</sub></span> values from several CMAQ531 simulations to a similarly configured CMAQ521 simulation encompassing 2016. For MDA8 O<span class="inline-formula"><sub>3</sub></span>, CMAQ531 has higher O<span class="inline-formula"><sub>3</sub></span> in the winter versus CMAQ521, due primarily to reduced dry deposition to snow, which strongly reduces wintertime O<span class="inline-formula"><sub>3</sub></span> bias (2–4 ppbv monthly average). MDA8 O<span class="inline-formula"><sub>3</sub></span> is lower with CMAQ531 throughout the rest of the year, particularly in spring, due in part to reduced O<span class="inline-formula"><sub>3</sub></span> from the lateral boundary conditions (BCs), which generally increases MDA8 O<span class="inline-formula"><sub>3</sub></span> bias in spring and fall (<span class="inline-formula">∼0.5</span> <span class="inline-formula">µg m<sup>−3</sup></span>). For daily 24 h average PM<span class="inline-formula"><sub>2.5</sub></span>, CMAQ531 has lower concentrations on average in spring and fall, higher concentrations in summer, and similar concentrations in winter to CMAQ521, which slightly increases bias in spring and fall and reduces bias in summer. Comparisons were also performed to isolate updates to several specific aspects of the modeling system, namely the lateral BCs, meteorology model version, and the deposition model used. Transitioning from a hemispheric CMAQ (HCMAQ) version 5.2.1 simulation to a HCMAQ version 5.3 simulation to provide lateral BCs contributes to higher O<span class="inline-formula"><sub>3</sub></span> mixing ratios in the regional CMAQ simulation in higher latitudes during winter (due to the decreased O<span class="inline-formula"><sub>3</sub></span> dry deposition to snow in CMAQ53) and lower O<span class="inline-formula"><sub>3</sub></span> mixing ratios in middle and lower latitudes year-round (due to reduced O<span class="inline-formula"><sub>3</sub></span> over the ocean with CMAQ53). Transitioning from WRF version 3.8 to WRF version 4.1.1 with the HVC resulted in consistently higher (1.0–1.5 ppbv) MDA8 O<span class="inline-formula"><sub>3</sub></span> mixing ratios and higher PM<span class="inline-formula"><sub>2.5</sub></span> concentrations (0.1–0.25 <span class="inline-formula">µg m<sup>−3</sup></span>) throughout the year. Finally, comparisons of the M3Dry and STAGE deposition models showed that MDA8 O<span class="inline-formula"><sub>3</sub></span> is generally higher with M3Dry outside of summer, while PM<span class="inline-formula"><sub>2.5</sub></span> is consistently higher with STAGE due to differences in the assumptions of particle deposition velocities to non-vegetated surfaces and land use with short vegetation (e.g., grasslands) between the two models. For ambient NH<span class="inline-formula"><sub>3</sub></span>, STAGE has slightly higher concentrations and smaller bias in the winter, spring, and fall, while M3Dry has higher concentrations and smaller bias but larger error and lower correlation in the summer.</p>


[Itahashi21]: <https://doi.org/10.1016/j.aeaoa.2021.100123> "Itahashi, S., Uchida, R., Yamaji, K., Chatani, S. (2021). Year-round modeling of sulfate aerosol over Asia through updates of aqueous-phase oxidation and gas-phase reactions with stabilized Criegee intermediates. Atmospheric Environment: X 12, 100123. "
[Appel21]: <https://doi.org/10.5194/gmd-14-2867-2021> "Appel, K.W., Bash, J.O., Fahey, K.M., Foley, K.M., Gilliam, R.C., Hogrefe, C., Hutzell, W.T., Kang, D., Mathur, R., Murphy, B.N., Napelenok, S.L., Nolte, C.G., Pleim, J.E., Pouliot, G.A., Pye, H.O.T., Ran, L., Roselle, S.J., Sarwar, G., Schwede, D.B., Sidi, F.I., et al. (2021). The Community Multiscale Air Quality (CMAQ) model versions 5.3 and 5.3.1: system updates and evaluation. Geoscientific Model Development 14, 2867–2897." 


## DMS concentration in Ocean
### [CMAQ cb6r3m mechanism issues ](https://forum.cmascenter.org/t/cmaq-cb6r3m-mechanism-issues/3125)

- Said by [foley.kristen](https://forum.cmascenter.org/u/foley.kristen/summary)
```
Thank you very much for providing a response, and apologies, @Henry for not following up sooner.

We do not recommend running cb6r3m without DMS and chl-a as this is the marine chemistry version of cb6r3. Zhizhua is correct that they are required for the DMS and detailed halogen chemistry in the mechanism.

Also, while cb6r3 does not include DMS chemistry it does include a simplified version of the halogen chemistry in cb6r5m which does not rely on the chl-a data.

In the next CMAQ release (v5.4), scheduled for this fall, the CMAQ repository will include a new python tool for adding DMS and CHLO to the ocean file.
```

### [Li et al., 2020][Li20], Modeling the Impact of Marine DMS Emissions on Summertime Air Quality Over the Coastal East China Seas

DMS emissions with the Liss and Merlivat parametrization increase atmospheric sulfur dioxide (SO2) and sulfate (SO42−) concentration over the East China seas by 6.4% and 3.3%, respectively. Our results indicate that although the anthropogenic source is still the dominant contributor of atmospheric sulfur burden in China, biogenic DMS emissions source is nonnegligible.

[Li20]: <https://doi.org/10.1029/2020EA001220> "Li, S., Sarwar, G., Zhao, J., Zhang, Y., Zhou, S., Chen, Y., Yang, G., Saiz-Lopez, A. (2020). Modeling the Impact of Marine DMS Emissions on Summertime Air Quality Over the Coastal East China Seas. Earth and Space Science 7, e2020EA001220. "

### [Li et al., 2020][Li20b],  Regional and Urban-Scale Environmental Influences of Oceanic DMS Emissions over Coastal China Seas.

At the urban scale, the addition of DMS emissions increase the SO2 and SO42− levels by 2% and 5%, respectively, and reduce ozone (O3) in the air of Shanghai by 1.5%~2.5%. DMS emissions increase fine-mode ammonium particle concentration distribution by 4% and 5%, and fine-mode nss-SO42− concentration distributions by 4% and 9% in the urban and marine air, respectively. 

[Li20b]: <https://doi.org/10.3390/atmos11080849> "Li, S., Zhang, Y., Zhao, J., Sarwar, G., Zhou, S., Chen, Y., Yang, G., Saiz-Lopez, A. (2020). Regional and Urban-Scale Environmental Influences of Oceanic DMS Emissions over Coastal China Seas. Atmosphere 11, 849. "

### SAGA.PMEL.NOAA
Overall, the concentration of DMS in surface seawater varies from approximately **0.2 nM** in winter to **10 nM** in summer. However, DMS concentrations in excess of **90 nM** have been measured in summer plankton blooms in the North Atlantic (Malin et al., 1993) and Southern Ocean (Gibson et al., 1990; Fogelqvist, 1991).

[Building a Global Database of Surface Seawater][saga]

[saga]: <https://saga.pmel.noaa.gov/dms/DMSweb_program_descript.html> "Building a Global Database of Surface Seawater Dimethylsulfide (DMS) Concentrations"

https://saga.pmel.noaa.gov/dms/

https://saga.pmel.noaa.gov/cache/std/dms_d8i720.dat

### [SOLAS](https://www.bodc.ac.uk/solas_integration/implementation_products/group1/dms/)
- [ monthly DMS concentration climatology zip file](https://www.bodc.ac.uk/solas_integration/implementation_products/group1/dms/documents/dmsclimatology.zip)
- [standard climatology](https://www.bodc.ac.uk/solas_integration/implementation_products/group1/dms/documents/dms-1degrex1degree.zip)

### SAT
- [Galí et al., 2018][Galí18]

[Galí18]: <https://doi.org/10.5194/bg-15-3497-2018> "Galí, M., Levasseur, M., Devred, E., Simó, R., Babin, M. (2018). Sea-surface dimethylsulfide (DMS) concentration from satellite data at global and regional scales. Biogeosciences 15, 3497–3519. "