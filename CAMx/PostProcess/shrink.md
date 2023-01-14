---
layout: default
title: Shrink of CAMx avrg
parent: Postprocess of CAMx 
grand_parent: CAMx
nav_order: 1
last_modified_date: 2022-06-13 12:08:20
tags: CAMx shk
---

# CAMx模擬結果之空品項目壓縮
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

## [shkavgcb6.f90](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/CAMx/PostProcess/shkavgcb6.f90)程式設計


#### Table 5-2. CAMx species names and descriptions common to all Carbon Bond Mechanisms.
|Model Species|Description|Carbon #1|Mol. Wt.2|
|-|-|-|-|
|BZO2|Peroxy radical from OH addition to  benzene|6|159.1|
|C2O3|Acetylperoxy radical|2|75.0|
|CRO|Alkoxy radical from cresol|7|107.1|
|CXO3|C3 and higher acylperoxy radicals|3|89.0|
|EPX2|Peroxy radical from EPOX reaction  with OH|5|149.1|
|HCO3|Adduct from HO2 plus formaldehyde|1|63.0|
|HO2|Hydroperoxy radical|1|28.0|
|ISO2|Peroxy radical from OH addition to  isoprene|5|117.1|
|MEO2|Methylperoxy radical|1|47.0|
|NO3|Nitrate radical|0|62.0|
|O|Oxygen atom in the O3 (P) electronic  state|0|16.0|
|O1D|Oxygen atom in the O1 (D) electronic  state|0|16.0|
|OH|Hydroxyl radical|0|17.0|
|OPO3|Peroxyacyl radical from OPEN|4|115.0|
|RO2|Operator to approximate total peroxy  radical concentration|0|87.1|
|ROR|Secondary alkoxy radical|1|71.1|
|TO2|Peroxy radical from OH addition to  TOL|7|173.1|
|XLO2|Peroxy radical from OH addition to  XYL|8|187.1|
|XO2|NO to NO2 conversion from  alkylperoxy (RO2) radical|0|87.1|
|XO2H|NO to NO2 conversion (XO2)  accompanied by HO2 production|0|87.1|
|XO2N|NO to organic nitrate conversion  from alkylperoxy (RO2) adical|0|87.1|
|AACD|Acetic acid|2|60.0|
|ACET|Acetone|3|58.1|
|ALD2|Acetaldehyde|2|44.0|
|ALDX|Propionaldehyde and higher aldehydes|2|58.1|
|BENZ|Benzene|6|78.1|
|CAT1|Methyl-catechols|7|124.1|
|CO|Carbon monoxide|1|28.0|
|CH4|Methane|1|16.0|
|CRES|Cresols|7|108.1|
|CRON|Nitro-cresols|7|153.1|
|EPOX|Epoxide formed from ISPX reaction with OH|5|118.1|
|ETH|Ethene|2|28.0|
|ETHA|Ethane|2|30.1|
|ETHY|Ethyne|2|26.0|
|ETOH|Ethanol|2|46.1|
|FACD|Formic acid|1|46.0|
|FORM|Formaldehyde|1|30.0|
|GLY|Glyoxal|2|58.0|
|GLYD|Glycolaldehyde|2|60.0|
|H2O2|Hydrogen peroxide|0|34.0|
|HNO3|Nitric acid|0|63.0|
|HONO|Nitrous acid|0|47.0|
|HPLD|hydroperoxyaldehyde|5|116.1|
|INTR|Organic nitrates from ISO2 reaction with NO|5|147.1|
|IOLE|Internal olefin carbon bond (R-C=C-R)|4|56.1|
|ISOP|Isoprene|5|68.1|
|ISPD|Isoprene product (lumped methacrolein, methyl  vinyl ketone, etc.)|4|70.1|
|ISPX|Hydroperoxides from ISO2 reaction with HO2|5|118.1|
|KET|Ketone carbon bond (C=O)|1|72.1|
|MEOH|Methanol|1|32.0|
|MEPX|Methylhydroperoxide|1|48.0|
|MGLY|Methylglyoxal|3|72.0|
|N2O5|Dinitrogen pentoxide|0|108.0|
|NO|Nitric oxide|0|30.0|
|NO2|Nitrogen dioxide|0|46.0|
|NTR|Organic nitrates|4|119.1|
|O3|Ozone|0|48.0|
|OLE|Terminal olefin carbon bond (R-C=C)|3|42.1|
|OPAN|Peroxyacyl nitrate (PAN compound) from OPO3|4|161.0|
|OPEN|Aromatic ring opening product (unsaturated  dicarbonyl)|4|84.0|
|PACD|Peroxyacetic and higher peroxycarboxylic acids|2|76.0|
|PAN|Peroxyacetyl Nitrate|2|121.0|
|PANX|C3 and higher peroxyacyl nitrate|3|135.0|
|PAR|Paraffin carbon bond (C-C)|1|72.1|
|PNA|Peroxynitric acid|0|79.0|
|PRPA|Propane|3|44.1|
|ROOH|Higher organic peroxide|0|90.1|
|SO2|Sulfur dioxide|0|64.0|
|SULF|Sulfuric acid (gaseous)|0|98.0|
|TERP|Monoterpenes|10|136.2|
|TOL|Toluene and other monoalkyl aromatics|7|92.1|
|XOPN|Aromatic ring opening product (unsaturated  dicarbonyl)|5|98.1|
|XYL|Xylene and other polyalkyl aromatics|8|106.2|
|NTR1|Simple organic nitrates|0|119.1|
|NTR2|Multi-functional organic nitrates|0|135.1|
|ECH4|Emitted methane (to enable tracking separate from  CH4)|1|16.0|
|XPRP|Operator for organic nitrates from PRPA|3|89.1|
|XPAR|Operator for organic nitrates from PAR|1|117.1|
|CRNO|Nitro-cresol oxy radical|7|152.1|
|CRN2|Nitro-cresol peroxy radical|7|168.1|
|CRPX|Nitro-cresol hydroperoxide|7|169.1|
|CAO2|Ring-opening product from methyl catechol|7|173.1|

1. Carbon # is the precise number of carbon atoms for each model species.
2. Mol. Wt. is a representative molecular weight, intended only for estimating molecular diffusivity, e.g. in dry deposition calculations. Diffusivity requires a different interpretation (complete molecules) than Carbon Bond chemistry (chemical groups).

