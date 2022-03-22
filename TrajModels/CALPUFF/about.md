---
layout: default
title: CALPUFF模式的法律位階
nav_order: 1
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-03-22 08:56:43
---

# CALPUFF模式的法律位階
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

## 背景
- 這篇筆記是因應環保署修訂模式模擬技術規範的需求收集的，澄清軌跡模式在法律中存在的價值、以及CALPUFF個案的處境。

## Support Center for Regulatory Atmospheric Modeling (SCRAM)

### Air Quality Models

The most commonly used air quality models include the following:
Dispersion Modeling - These models are typically used in the permitting process to estimate the concentration of pollutants at specified ground-level receptors surrounding an emissions source.

Photochemical Modeling - These models are typically used in regulatory or policy assessments to simulate the impacts from all sources by estimating pollutant concentrations and deposition of both inert and chemically reactive pollutants over large spatial scales.

https://www.epa.gov/scram/air-quality-models

---
## CALPUFF Regulatory Status

From April 2003 until January 2017, CALPUFF was the U.S. Environmental Protection Agency (EPA) preferred model for long-range transport for the purposes of assessing National Ambient Air Quality Standards (NAAQS) and/or Prevention of Significant Deterioration (PSD) increments. With the 2017 revisions to the Guideline on Air Quality Models (Appendix W to 40 CFR Part 51), the EPA has established in Section 4.2(c)(ii) a screening approach for long-range transport assessments for NAAQS and PSD increments. This screening approach will streamline the time and resources necessary to conduct such analyses and provides a technically credible and appropriately flexible way to use CALPUFF or other Lagrangian models as a screening technique. With the establishment of the screening approach for long-range transport, CALPUFF was delisted as an EPA preferred model in the 2017 revised Guideline. Should a cumulative impact analysis for NAAQS and/or PSD increments be necessary beyond 50 km, the selection and use of an alternative model shall occur in agreement with the appropriate reviewing authority and approval by the EPA Regional Office based on the requirements of Appendix W, Section 3.2.

As stated in Section 6 of the Final Rulemaking Notice for the January 2017 revision of the U.S. EPA Guideline on Air Quality Models, (82 FR 5196) “EPA’s final action to remove CALPUFF as a preferred appendix A model in this Guideline does not affect its use
under the FLM’s [Federal Land Managers] guidance regarding AQRV [Air Quality Related Values] assessments (FLAG 2010)
nor any previous use of this model as part of regulatory modeling applications required under the CAA [Clean Air Act]. Similarly, this final action does not affect the EPA’s recommendation that
states use CALPUFF to determine the applicability and level of best available retrofit technology in regional haze implementation plans. It is also important to note that
the use of CALPUFF in the near-field as an alternative model for situations involving complex terrain and complex winds is not changed by the removal of CALPUFFas a preferred model in appendix A. The EPA recognizes that AERMOD, as a Gaussian plume dispersion model, may be limited in its ability to appropriately address such situations and that CALPUFF or other Lagrangian models may be more suitable, so we continue to provide the flexibility of alternative model approvals (as has been in place since the 2003 revisions to the Guideline).”

The CALPUFF modeling system is recommended by the Federal Land Managers’ Air Quality Related Values Workgroup (FLAG) for assessing the effects of distant and multi-source plumes on visibility and pollutant wet/dry deposition fluxes. The CALPOST processor implements the algorithms recommended by FLAG for assessing the change in plume extinction due to a modeled source or group of sources. CALPUFF postprocessors allow the calculation of pollutant deposition fluxes of nitrogen and sulfur as described by the FLAG guidance. Download the October 2010 FLAG Phase I Report Revised for more details.

http://www.src.com/calpuff/regstat.htm

---
## guidance_for_o3_pm25_permit_modeling.

### P31

III.4.3 Tier 2 Assessment Approach As discussed in the 2017 Guideline, a Tier 2 assessment involves application of more sophisticated, case-specific CTMs in consultation with the appropriate permitting authority and conducted consistent with the recommendations in the most current version of the Single-source Modeling Guidance. Where it is necessary to estimate O3 and/or secondary PM2.5 impacts with case-specific air quality modeling, a candidate model should be selected for estimating single-source impacts on O3 and/or secondarily formed PM2.5 that meets the general criteria for an “alternative model” where there is no preferred model as outlined in section 3.2.2.e of the 2017 Guideline. The general criteria include:

i. The model has received a scientific peer review; 

ii. The model can be demonstrated to be applicable to the problem on a theoretical basis; 

iii. The databases that are necessary to perform the analysis are available and adequate; 

iv. Appropriate performance evaluations of the model have shown that the model is not biased toward underestimates; and 

iv. A protocol on methods and procedures to be followed has been established.

### P32
Both Lagrangian puff models and photochemical grid models may be appropriate for this purpose where those models satisfy alternative model criteria in section 3.2.2 of the 2017 Guideline. That said, the EPA believes photochemical grid models are generally most appropriate for addressing O3 and secondary PM2.5 impacts because they provide a spatially and temporally dynamic realistic chemical and physical environment for plume growth and chemical transformation. Publicly available and documented Eulerian photochemical grid models such as the Comprehensive Air Quality Model with Extensions (CAMx) (Ramboll Environ, 2018) and the Community Multiscale Air Quality (CMAQ) (Byun and Schere, 2006) model treat emissions, chemical transformation, transport, and deposition using time and space-variant meteorology. These modeling systems include primarily emitted species and secondarily formed pollutants such as O3 and PM2.5 (Chen et al., 2014; Civerolo et al., 2010; 
Russell, 2008; Tesche et al., 2006). In addition, these models have been used extensively to support O3 and PM2.5 SIPs and to explore relationships between inputs and air quality impacts in the United States and elsewhere (Cai et al., 2011; Civerolo et al., 2010; Hogrefe et al., 2011). On August 4, 2017, the EPA released a memorandum (U.S. EPA, 2017b) providing information specific to how the CAMx and the CMAQ model systems were relevant for each of these elements. This memorandum provides an alternative model demonstration for the CAMx and CMAQ photochemical transports models establishing their fitness for purpose in PSD compliance demonstrations for O3 and PM2.5 and in NAAQS attainment demonstrations for O3, PM2.5 and Regional Haze. 

The memorandum also provides for their general applicability for use in PSD compliance demonstrations; however, it does not replace the need for such demonstrations to provide model protocols describing model application choices or the evaluation of model inputs and baseline predictions against measurements relevant for their specific use by permit applicants and state, local, and tribal air agencies. For those situations where a refined Tier 2 demonstration is necessary, the EPA has also provided the Single-source Modeling Guidance that provides recommended, credible procedures to estimate single-source secondary impacts from sources for permit-related assessments. 

Extensive peer-reviewed literature demonstrates/documents that photochemical grid models have been applied for single-source impacts and that the models adequately represent secondary pollutant impacts from a specific facility, in comparison to near-source downwind in-plume measurements. The literature shows that these models can clearly differentiate the impacts of a specific facility from those of other sources (Baker and Kelly, 2014; Zhou et al., 2012). Other peer-reviewed research has clearly shown that photochemical grid models are able to simulate impacts from single sources on secondarily-formed pollutants (Baker et al., 2015; Bergin et al., 2008; Kelly et al., 2015).

 Further, single-source secondary impacts have been provided in technical reports that further support the utility of these tools for single-source scientific and regulatory assessments (ENVIRON 2012a; ENVIRON 2012b; Yarwood et al., 2011). The EPA firmly believes that the peer-reviewed science clearly demonstrates that photochemical grid models can adequately assess single-source impacts. The EPA recognizes that ongoing evaluations in this area will lead to continual improvements in science and associated predictive capabilities of these models. For the purposes of conducting a Tier 2 assessment, the application of a CTM will involve case-specific factors that should be part of the consultation process with the appropriate permitting authority and reflected in the agreed-upon modeling protocol. Consistent with the Single-source Modeling Guidance and section 9.2.1 of the 2017 Guideline, EPA recommends that the modeling protocols for this purpose should include the following elements:

1. Overview of Modeling/Analysis Project
  - Participating organizations
  - Schedule for completion of the project
  - Description of the conceptual model for the project source/receptor area
  - Identify how modeling and other analyses will be archived and documented
  - Identify specific deliverables to the appropriate permitting authority

2. Model and Modeling Inputs
  - Rationale for the selection of air quality, meteorological, and emissions models
  - Modeling domain
  - Horizontal and vertical resolution
  - Specification of initial and boundary conditions
  - Episode selection and rationale for episode selection
  - Rationale for and description of meteorological model setup
  - Basis for and development of emissions inputs
  - Methods used to quality assure emissions, meteorological, and other model inputs

3. Model Performance Evaluation
- Describe ambient database(s)
- Describe evaluation procedures and performance metrics

As stated previously, we expect that the EPA Regional Offices, with assistance from the OAQPS, may assist reviewing authorities, as necessary, to structure appropriate technical demonstrations leading to the development of appropriate chemical transport modeling applications for the purposes of estimating potential O3 and/or secondary PM2.5 impacts.

### P71
V.3.2.2 Assessing Secondary PM2.5 Impacts To assess the impacts from changes in secondary PM2.5 precursor emissions from the new or modified source, as well as from other increment-consuming sources, the EPA recommends the analysis for each applicable precursor of PM2.5 be conducted collectively based on the two-tiered demonstration approach outlined in EPA’s 2017 Guideline. In recent years, several rules promulgated by the EPA have resulted in control requirements that have significantly reduced NOX and SO2 precursor emissions affecting ambient PM2.5 concentrations in many areas.33 This is particularly true in the eastern U.S. As a result, in some cases, the impacts of secondary PM2.5 emissions may be addressed by a demonstration that provides ambient monitoring data that generally confirms a downward trend in contributions of precursor emissions occurring after the applicable PM2.5 minor source baseline date (or the major source baseline date). If it can be confirmed that such secondary emissions reductions have occurred in a particular baseline area, it may be possible to complete the PM2.5 increments modeling analysis simply by focusing on potential increment consumption associated with direct PM2.5 emissions. For areas where PM2.5 precursor emission increases from other increment consuming sources have occurred since the major or minor source baseline dates, and are, thus, likely to have added to PM2.5 concentration increases within the baseline area (and, thus, consume PM2.5 increment), the chemical transport modeling methods (using the emissions input data applicable to increment analyses) discussed in Section IIIof this guidance may be appropriate for estimating the portion of PM2.5 increment consumed due to secondary PM2.5 impacts associated with those increases in precursor emissions.

https://www.epa.gov/sites/production/files/2020-09/documents/draft_guidance_for_o3_pm25_permit_modeling.pdf

---

- U.S. EPA, 2017b. ***Use of Photochemical Grid Models for Single-Source Ozone and secondary PM2.5 impacts for Permit Program Related Assessments and for NAAQS Attainment Demonstrations for Ozone, PM2.5 and Regional Haze. Tyler Fox Memorandum dated August 4, 2017.*** [U.S. Environmental Protection Agency, Research Triangle Park, North Carolina 27711.](https://www3.epa.gov/ttn/scram/guidance/clarification/20170804-Photochemical_Grid_Model_Clarification_Memo.pdf)

- U.S. EPA, 2020, ***Guidance on the Use of Models for Assessing the Impacts of Emissions from Single Sources on the Secondarily Formed Pollutants: Ozone and PM2.5***, [USEPA](https://www.epa.gov/sites/production/files/2020-09/documents/epa-454_r-16-005.pdf)
---
## scram
### air-quality-dispersion-modeling-alternative-models

CALPUFF is a multi-layer, multi-species non-steady-state puff dispersion model that simulates the effects of time- and space-varying meteorological conditions on pollution transport, transformation and removal. CALPUFF can be applied on scales of tens to hundreds of kilometers. It includes algorithms for subgrid-scale effects (such as terrain impingement), as well as, longer-range effects (such as pollutant removal due to wet scavenging and dry deposition, chemical transformation, and visibility effects of particulate matter concentrations).

From April 2003 until January 2017, CALPUFF was the EPA preferred model for long-range transport for the purposes of assessing NAAQS and/or PSD increments. With the 2017 revisions to the Guideline on Air Quality Models (Appendix W to 40 CFR Part 51), the EPA has established in Section 4.2(c)(ii) a screening approach for long-range transport assessments for NAAQS and PSD increments.  This screening approach will streamline the time and resources necessary to conduct such analyses and provides a technically credible and appropriately flexible way to use CALPUFF or other Lagrangian models as a screening technique. With the establishment of the screening approach for long-range transport, CALPUFF was delisted as an EPA preferred model in the 2017 revised Guideline. Should a cumulative impact analysis for NAAQS and/or PSD increments be necessary beyond 50 km, the selection and use of an alternative model shall occur in agreement with the appropriate reviewing authority and approval by the EPA Regional Office based on the requirements of Appendix W, Section 3.2.
- USEPA [Site](https://www.epa.gov/scram/air-quality-dispersion-modeling-alternative-models#calpuff
)
---

- https://gaftp.epa.gov/aqmg/SCRAM/conferences/2015_11th_Conference_On_Air_Quality_Modeling/Review_Material/AERMOD_LRT_TSD.pdf
- https://www.epa.gov/sites/production/files/2020-09/documents/air_quality_analysis_checklist-revised_20161220.pdf

---
## Appendix W to Part 51—Guideline on Air Quality Models

### 4.2cii
ii. For assessment of the significance of ambient impacts for NAAQS and/or PSD increments, there is not a preferred model or screening approach for distances beyond 50 km. Thus, the appropriate reviewing authority (paragraph 3.0(b)) and the EPA Regional Office shall be consulted in determining the appropriate and agreed upon screening technique to conduct the second level assessment. Typically, a Lagrangian model is most appropriate to use for these second level assessments, but applicants shall reach agreement on the specific model and modeling parameters on a case-by-case basis in consultation with the appropriate reviewing authority (paragraph 3.0(b)) and EPA Regional Office. When Lagrangian models are used in this manner, they shall not include plume-depleting processes, such that model estimates are considered conservative, as is generally appropriate for screening assessments.

- https://www.ecfr.gov/cgi-bin/text-idx?SID=b7d0bd27661737a2693ab6aebd83f911&mc=true&node=pt40.2.51&rgn=div5#ap40.2.51_11319.w
---
## Using GTx
https://www.epb.taichung.gov.tw/media/398158/臺中市空氣污染防制計畫書-104-108年版-上.pdf

https://www.twreporter.org/a/shenao-power-plant-coal-fired-health

98年度空氣污染綜合防制計畫 康廷工程顧問企業有限公司執行
桃園縣政府環保局為順利推動空氣品質維護或改善工作，並能達到各項管制計畫預期之目標及效益，故委託執行本計畫，

...期末階段歸納執行所獲成果分項說明如下...二、工作項目成果...(二)評估整體空氣品質改善執行成效...2.完成近年空氣品質不良事件日污染成因分析：
分析桃園縣臭氧之空氣品質不良指標值及各類空氣污染物濃度變成情形，並執行VOCs、粒狀物污染成分分析(金屬元素及陰、陽離子)，並利用空氣污染模式(軌跡模式GTx)模擬近四年空品不良事件日發生之傳輸軌跡。

https://sheethub.com/opendata.epa.gov.tw/%E7%92%B0%E4%BF%9D%E5%B0%88%E6%A1%88%E6%91%98%E8%A6%81%E8%B3%87%E6%96%99?page=79

---
## 媒體報導「不可承受之重-深澳燃煤電廠健康衝擊評估」環保署回應說明
提供單位：行政院環境保護署空保處 發布日期：2018.09.11[金門縣政府下載點](https://ws.kinmen.gov.tw/Download.ashx?u=LzAwMS9VcGxvYWQvMzE3L3JlbGZpbGUvMTAwMTAvNjU5NDA0L2YxODVmOGU0LTQwZjctNGE3Ni04MjFlLWJmZDUyNDAyNTRlYy5wZGY%3D&n=MTA3WTA5LnBkZg%3D%3D&icon=..pdf)

有關 11 日綠色和平組織召開記者會，針對深澳燃煤電 廠所做健康風險評估，環保署回應如下：

環保署肯定綠色和平與民間學者對於深澳電廠相關環境與健康惡化風險的關切，並對其研究內容表示尊重。 惟「深澳發電廠更新擴建計畫環境影響說明書第 1 次 環境影響差異分析報告暨變更審查結論」(以下簡稱深澳環差) 案，屬環保署 95 年即審查通過「深澳電廠更新擴建計畫環 境影響說明書」(以下簡稱深澳環評)之變更案件。由於變更內 容較原方案大幅降低開發規模與污染排放，在環評法規的適 用上，未符環境影響評估法施行細則第 38 條第 1 項各款所 列變更部分造成「加重之影響」，應重辦環評的要件。

此外，由於「健康風險評估技術規範」於 99 年 4 月 9 日方訂定發布，95 年即已通過之深澳環評與後續變更，依法 無須辦理健康風險評估，且由於本案變更內容的實質影響面較原規劃明顯降低，變更方案的健康風險亦無較原方案加重 之理，並不影響相關法規之適用。然而在環差審查過程中， 台電公司為回應外界擔心深澳電廠運轉後對民眾健康產生 影響之疑慮，承諾積極規劃委託學者專家進行健康風險評估， 據了解該單位已在作業中。

另外，環保署指出，今天綠色和平與學者所發表之健康 風險評估，係由空氣品質模式模擬 PM2.5 濃度推估死亡人 數。然而，由於本件健康風險評估，其所採 GTx 空氣品質模 擬模型，

- 未若深澳環差案所採光化網格模式(CAMx)模式，已依空氣品質模式模擬規範規定，進行定性及定量性能評估， 並提出性能評估檢核表，模擬結果與測站觀測結果比較，通過性能評估規範；
- 美國模式中心針對新污染源模式模擬增量採用 5 種推薦高斯擴散模式包括：AEROMOD、CALINE3、 CAL3OHC、CTDMPLUS、OCD。綜整國內外模式模擬專家的意見，GTx 模式是否適合用在本健康風險之模擬，實有待釐清。

本案距離實際建廠期間還有一段時間，將適用新修定的 空污法，授權主管機關可以依最低可達成排放率控制技術要 求大幅降低排放量，以保障民眾健康。

---
## 燃煤就是髒　空汙學者為什麼說的跟賴清德不一樣？
文 呂國禎 天下Web only(2018-03-17)

深澳興建燃煤電廠通過環評引發六縣市政府、學界、民間團體反彈，要求環保署退回深澳電廠環評許可，今天（3月17日）贊成與反對興建深澳電廠的行政院環境保護署副署長詹順貴、台電董事長楊偉甫與台大、成大、中興大學的公衛、環工學者同台，到底深澳電廠蓋了會有什麼空污、健康影響？雙方說法的差異爭點何在？...

各說各話一：燃煤電廠重金屬汙染量不強制公布

各說各話二：學者沒考慮地型，台電沒有考慮熱島效應

至於深澳運轉之後，空污影響範圍有多大，台電與新北市環保局委託莊秉潔的模擬報告，因為雙方使用的模擬方式、地形條件以及取樣的值不同。莊秉潔認為影響範圍從大台北、桃園、宜蘭地區，台電的報告則認為，在地形條件下，對於台北、新北、桃園有影響，但對九份，對於宜蘭地區影響不大。雙方因為研究方法不同，預估範圍、數值大小差了三倍。（見下表）

註：台電取全年平均值，學者取全年最大值。資料來源：台電。

談空污對北部地區影響卻不能只看深澳，莊秉潔說，如果深澳電燃煤電廠興建完成之後，會跟一樣燒煤炭的台電新林口電廠形成南北夾擊大台北都會區，再加上台北都會區的熱島效應，會惡化大台北都會的空氣品質。

所以莊秉潔、詹長權等空污學者建議，深澳電廠應該改成天然氣電廠，台電預計在基隆協和電廠退役後，在基隆港建天然氣接收站、把協和電廠改建為天然氣發電，可以拉一條專用天然氣海管到深澳，就可以讓深澳發電廠由煤改氣。「如果真的不行，那麼燒煤炭的深澳電廠應該蓋來備用，等天然氣發電的電力供應不足的時候再發電。」莊秉潔說。

https://www.cw.com.tw/article/5088779

---
## 媒體報導「不可承受之重-深澳燃煤電廠健康衝擊評估」環保署回應說明
提供單位：行政院環境保護署空保處

發布日期：2018.09.11



詹順貴臉書發三千字聲明　請辭環保署副署長

https://www.cw.com.tw/article/5092428

---
## 揭開蔡英文突襲六輕祕辛　為何六輕無法降空污，由燃煤改燒天然氣？
- 文 呂國禎 天下Web only(2020-11-22)

...計畫卻卡住了。雖然經濟部能源局樂觀其成，但工業局卻陷入了兩難，因為南碼頭...10個碼頭會剩下3個，如果新興、口湖、四湖區有投資者進來，恐怕不敷使用，因此工業局長呂正華回應，南碼頭蓋天然氣接收站，必須要有通盤考量。

但實際上，所謂的新興、台西、四湖工業區，規劃近萬公頃的工業區，大部分的地方仍是汪洋一片，中興大學環工系教授莊秉潔說，「六輕改天然氣發電、接收站應該快做，最好台塑集團所有燃煤的汽電共生也改成燒天然氣，台灣才能持續做深度減煤、減碳、降低空污，未來投資需要碼頭可另作處理、規劃，不應成為改善現況的絆腳石。」

https://www.cw.com.tw/article/5102853

---
## 深澳是台灣最後一座燃煤電廠

深澳電廠爭議之後，環保、台電為對抗空污達成共識。今日，台電亮出最新版長期電源開發方案，台電與環保署做出重大政策宣示：深澳將是台灣最後一座燃煤電廠。

- 文 劉光瑩  呂國禎 天下Web only(2018-03-17)

環保署14日通過深澳燃煤電廠環境影響差異評估，引起擔心空污加劇的民眾抗議。根據台電長期電源開發方案，深澳將會是台灣最後一座燃煤電廠。

「我們正在朝能源轉型的道路上走，」台電董事長楊偉甫，回應民眾對燃煤電廠的疑慮，17日下午，在天下雜誌與群創教育基金會合辦的「思辨：台灣空污習題」座談會上，攤開最新版的台電長期電源開發方案（見下圖），強調深澳電廠會是未來10年內，台灣新建的最後一座燃煤電廠。

https://www.cw.com.tw/article/5088780?rec=i2i&from_id=5088779&from_index=3

---

Here：https://www.evernote.com/shard/s125/sh/8536719e-d974-409f-a589-73d130f3336a/9b8f08515fad3f811d6e1c168ad7a418



