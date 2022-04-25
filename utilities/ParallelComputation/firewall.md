---
layout: default
title:  工作站防火牆管理
parent:   Parallel Computation
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
- 正常安裝好的CENTOS 7是自帶、並自行啟動[firewalld](https://blog.gtwang.org/linux/centos-7-firewalld-command-setup-tutorial/)服務的，firewalld具備了較為完整、可以完全對外的防火功能。
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
  - 其他詳細的iptables設定，也可以參考[阿新這篇](https://www.796t.com/content/1548640287.html)。
  - 不過目前保持全開、讓工作站之間保持完全暢通是對mpirun最有利的方案。

## Reference
- G. T. Wang, [CentOS Linux 7 以 firewalld 指令設定防火牆規則教學](https://blog.gtwang.org/linux/centos-7-firewalld-command-setup-tutorial/), 2017/12/26
- 程式人生-阿新, [CentOS7安裝iptables防火牆（禁用/停止自帶的firewalld服務）](https://www.796t.com/content/1548640287.html), 2019-01-28
- mtchang's blog-巴克里, [關閉 centos7 防火牆 firewalld 改用傳統的 iptables](https://blog.jangmt.com/2015/09/centos7-firewalld-iptables.html), 2015/09/26
