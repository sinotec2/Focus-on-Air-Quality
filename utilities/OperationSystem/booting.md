---
layout: default
title: linux之啟動
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2022-11-11 09:01:53
tags: reboot
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

# linux之啟動

## libc version not right

- kernel找不到正確版本的/lib64/libstdc++.so.6、libgcc_s.so.1
- 造成效果
  - i8042: no controller found 
  -  booting hang-on
- solve
  - reboot on USB
  - re-link right version

## mount of nfs

### nas1

- nas1的格式是nfs3，但是-t沒有nfs3的選項，需用-o
- `mount -o vers=3 200.200.121.71:/nas1 /nas1`

## gmond

- 檢查狀態：`systemctl status gmond`
- 重新啟動：`systemctl restart gmond`

