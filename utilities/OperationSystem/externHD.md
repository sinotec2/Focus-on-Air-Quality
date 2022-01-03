---
layout: default
title: Mac讀寫ntfs格式外接硬碟
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## 免安裝軟體讓-mac-也能讀寫-ntfs-格式
- [noter](https://noter.tw/5369/存不進隨身碟？免安裝軟體讓-mac-也能讀寫-ntfs-格式/)

```bash
mount (chk /dev/disk2s1)
sudo umount /Volumes/HansNTFS
sudo mkdir  /Volumes/HansNTFS
sudo mount -o rw,auto,nobrowse -t ntfs /dev/disk2s1 /Volumes/HansNTFS
```
## Disk編號
- 可以由下列指令而得（如果mount df 或Finder都找不到）

```bash
$ diskutil list
ob-working-directory: error retrieving current directory: getcwd: cannot access parent directories: No such file or directory
/dev/disk0 (internal):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                         28.0 GB    disk0
   1:                        EFI EFI                     314.6 MB   disk0s1
   2:                 Apple_APFS Container disk2         27.6 GB    disk0s2
/dev/disk1 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *1.0 TB     disk1
   1:                        EFI EFI                     209.7 MB   disk1s1
   2:                 Apple_APFS Container disk2         1000.0 GB  disk1s2
/dev/disk2 (synthesized):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      APFS Container Scheme -                      +1.0 TB     disk2
```
