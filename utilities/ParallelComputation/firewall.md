---
layout: default
title:  工作站防火牆管理
parent:   ParallelComputation
grand_parent: Utilities
last_modified_date: 2022-04-25 12:20:36
---
# 工作站防火牆管理
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
- 正常安裝好的CENTOS 7是自帶、並自行啟動firewalld服務的
- 因工作站在公司內部、公司已有完善的防火牆、且防火牆會限制工作站間的連繫(mpirun)，因此可以、也必須將其關閉。
- 工作站防火牆並不屬於一般OS會動到的範圍，因為平行運作需要，因此將其放在此處說明。
- 作業目標
  - 停用firewalld，以iptables-service取代
  - iptables設定

## 預備動作
### 裝置iptables及iptables-service
- OS內設是有iptables程式的，但沒有iptables-service，一樣不能作動
  - `yum install iptables-services`
- 停止firewalld服務
  - `systemctl stop firewalld`
- 禁用firewalld服務，避免系統自行啟動造成干擾。
  - `systemctl mask firewalld`
- 檢視iptables現有規則
  - `iptables -L -n`

## 啟動與設置iptables

- 設定防火牆開機啟動：`systemctl enable iptables.service`
- 允許所有輸入：`iptables -P INPUT ACCEPT`

## Reference
-程式人生-阿新, [CentOS7安裝iptables防火牆（禁用/停止自帶的firewalld服務）](https://www.796t.com/content/1548640287.html), 2019-01-28
