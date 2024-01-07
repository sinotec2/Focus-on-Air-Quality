---
layout: default
title:  GPU supported OLAP
parent: DB_servers
grand_parent: Utilities
last_modified_date: 2024-01-07 20:26:18
tags: DB_servers
---

# GPU supported OLAP
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

- 是有一些OLAP方案支持GPU加速並且是開源的。例如，MapD（現在被稱為OmniSci）是一個基於GPU的OLAP系統，它已經開源了其核心數據庫和相關的可視化庫¹。
- 這個項目的源代碼在Github上以Apache 2.0許可證開源，包含構建完整的MapD Core數據庫所需的所有內容，可以在多GPU服務器上跨數十億條記錄進行二次查詢¹。
- 這可能是您正在尋找的一種解決方案。請注意，雖然這些工具是開源的，但在實際使用時可能需要相關的技術知識來配置和優化。希望這對您有所幫助！

來源: 與 Bing 的交談， 2024/1/7
(1) 基于 GPU 的 OLAP 系统 MapD 开源其核心数据库 - [阿里云开发者社区](https://developer.aliyun.com/article/114413).
(2) GPU数据库OLAP优化技术研究 - [软件学报](http://www.jos.org.cn/jos/ch/reader/view_abstract.aspx?file_no=6739).
(3) 浅谈OLAP系统核心技术点 - [知乎](https://zhuanlan.zhihu.com/p/163236128).
(4) [undefined](http://www.oschina.net).
(5) [undefined](https://www.aliyun.com/product/ApsaraDB/ads).

## NVIDIA technical reports

### GPU‑ACCELERATED APPLICATIONS

- [source:NVIDIA](https://www.nvidia.com/content/tesla/pdf/gpu-accelerated-applications-for-hpc.pdf)

APPLICATION|DESCRIPTION|SUPPORTED FEATURES|MULTI-GPU SUPPORT
-|-|-|-
[Polymatica](https://www.polymatica.com/)|商業分析平台，使用資料探勘演算法和機器學習方法快速分析處理大數據。 Polymatica 基於 OLAP GPU 記憶體技術構建，完全支援 OLAP 即席操作和資料探勘運算中的 GPU 加速。|OLAP、商業智慧、資料發現、資料探勘、多維資料分析、視覺化分析工作、互動式儀表板|Yes

### GPU ACCELERATION FOR OLAP

[Tim Kaldewey, Jiri Kraus, Nikolay Sakharnykh 03/26/2018](https://on-demand.gputechconf.com/gtc/2018/presentation/s8289-how-to-get-the-most-out-of-gpu-accelerated-database-operators.pdf)


## 相關論文

- Broneske, D., Drewes, A., Gurumurthy, B. et al. [In-Depth Analysis of OLAP Query Performance on Heterogeneous Hardware](https://doi.org/10.1007/s13222-021-00384-w). [Datenbank Spektrum 21, 133–143 (2021).
  - 傳統資料庫系統面臨著以盡可能高效的方式處理以前所未有的速度產生的大容量資料流的挑戰，同時還要最小化能源消耗。 
  - 由於僅基於CPU的機器達到了極限，資料庫系統設計者正在研究諸如GPU和FPGA之類的協處理器，以發揮其獨特的能力。 
  - 因此，基於異質處理架構的資料庫系統正在崛起。 為了更好地理解它們的潛力和局限性，深入的性能分析至關重要。 
  - 本文透過在CPU、GPU和FPGA上對基於列的系統進行基準測試，提供了有趣的效能數據，所有這些處理設備都在同一系統中可用。 
  - 作者們考慮了TPC-H查詢Q6以及額外的雜湊連接以對系統間的執行進行分析。 
  - 作者們展示了系統記憶體存取和/或緩衝區管理仍然是設備整合的主要瓶頸，而架構特定的執行引擎和操作符則提供了顯著更高的效能。
- Yansong Zhang, Yu Zhang, Jiaheng Lu, Shan Wang, Zhuan Liu & Ruichen Han （2020）[One size does not fit all: accelerating OLAP workloads with GPUs](https://link.springer.com/article/10.1007/s10619-020-07304-z)、Distrib Parallel Databases 38, 995–1037 
  - 本論文研究GPU作為實時查詢處理數據庫的下一代平台。
  - 實證結果顯示，代表性的GPU數據庫（如OmniSci）在典型OLAP工作負載中可能比代表性的內存數據庫（如Hyper）慢，即使每個查詢的實際數據集大小完全適應GPU內存。
  - 因此，論文主張GPU數據庫設計不應是一刀切的，通用的GPU數據庫引擎可能不適用於沒有仔細設計GPU內存分配和GPU計算位置性的OLAP工作負載。
  - 為了實現更好的GPU OLAP性能，需要重新組織OLAP運算符並優化OLAP模型。作者提出了3層OLAP模型以匹配異構計算平台。
  - 實驗結果顯示，通過矢量分組和GPU加速星型連接實現，OLAP加速引擎在SF = 100的SSB評估中運行速度分別為Hyper、OmniSci GPU和OmniSci CPU的1.9倍、3.05倍和3.92倍。
- 張延松、劉專、韓瑞琛、張宇、王珊（2023）[GPU資料庫OLAP最佳化技術研究](https://www.jos.org.cn/jos/article/abstract/6739)、軟件學報2023年第34卷第11期 >5205-5229. DOI:10.13328/j.cnki.jos.006739
  - GPU資料庫在學術界和工業界引起廣泛關注。 儘管一些原型系統和商業系統開發了作為下一代資料庫系統的GPU-OLAP引擎，但其效能相較於CPU系統仍有疑問。 
  - 本研究探討了兩種主要的GPU-OLAP引擎技術路線：GPU記憶體處理與GPU加速。 
  - 透過整合這兩種技術路線，設計了在混合CPU-GPU平台上的OLAP框架OLAP Accelerator。 研究了CPU記憶體運算、GPU記憶體運算和GPU加速等三種OLAP運算模型，實現了GPU平台向量化查詢處理技術，最佳化了顯存利用率和查詢效能。 
  - 實驗結果表明，在效能和記憶體利用率方面，GPU記憶體向量化查詢處理模型達到最佳效能，相較於OmniSciDB和Hyper資料庫，效能分別提高了3.1倍和4.2倍。 分區的GPU加速模式在平衡CPU和GPU端負載方面取得了顯著成果，能夠支援更大的資料集。


## Terminology

### Hash Join

"Hash Join" 是資料庫中一種連接（Join）兩個表的演算法。 它是一種高效的連接演算法，特別適用於大型資料集的連接操作。

在 Hash Join 中，連接的關鍵在於使用**雜湊函數**將兩個表的連接列對應到相同的**雜湊桶**（Hash Bucket）。 這樣，具有相同哈希值的資料行將被分配到相同的桶中。 然後，對每個**雜湊桶**進行連接操作，這可以在較小的資料集上更快地完成。

Hash Join 的步驟通常包括：

1. **建立雜湊表：** 對於較小的輸入表，系統將建立一個雜湊表，將連接列的值對應到**雜湊桶**。

2. **雜湊過程：** 對於較大的輸入表，系統將使用相同的雜湊函數將連接列的值對應到相同的**雜湊桶**。

3. **連接：** 然後，系統將對每個**雜湊桶**進行連接操作。 這涉及將兩個表中具有相同雜湊值的資料行進行匹配。

4. **輸出結果：** 最終，系統將產生連接後的結果集。

Hash Join 的優點是它對大型資料集有很好的擴展性，尤其是在記憶體中無法容納整個資料集時。 然而，它可能會佔用較多的內存，因為需要建立哈希表。 在某些情況下，可能會選擇其他連接演算法，例如 Nested Loop Join 或 Merge Join，具體取決於資料集的大小、索引情況和可用的系統資源。
