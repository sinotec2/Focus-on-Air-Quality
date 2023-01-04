---
layout: default
title: Mac讀寫ntfs格式外接硬碟
parent: Operation System
grand_parent: Utilities
last_modified_date: 2022-12-13 17:03:13
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

## imackuang 作業

### search device name

```bash
kuang@125-229-149-182 /Users/Seagate/data/NOAA/NCEP
$ diskutil list|grep Seagate
   2:       Microsoft Basic Data ⁨Seagate Expansion Drive⁩ 4.0 TB     disk3s2

```

### mount device unto $vol_nam

- /dev/disk3(type=`GUID_partition_scheme`)與/dev/disk3s2(type=`Microsoft Basic Data`)似乎是2個不同的區位
- 前者無法寫入，後者則可。

```bash
vol_nam=/Volumes/Seagate\ Expansion\ Drive
sudo umount $vol_nam
sudo mkdir  $vol_nam
sudo mount -o rw,auto,nobrowse -t ntfs /dev/disk3s2 $vol_nam
```

### results

```bash
$ mount|grep Seagate
/dev/disk3s2 on /Volumes/Seagate Expansion Drive (ntfs, local, noowners, nobrowse)
$ df -h |grep Seagate
/dev/disk3s2                                     3.6Ti  2.7Ti  961Gi    75%  468252 1007937428    0%   /Volumes/Seagate Expansion Drive
```

### about Finder‘s control

- 似乎不需（不能）由Finder來控制外接硬碟。
- 當`sudo umount $vol_nam`之後，退出finder的連結，似乎在terminal運作外接硬碟才變得順暢。