---
layout: default
title: Linux Administration
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## Create Swap File on CentOS Linux

Swap is a space on a disk that is used when the amount of physical RAM memory is full. When a Linux system runs out of RAM, inactive pages are moved from the RAM to the swap space.

Swap space can take the form of either a dedicated swap partition or a swap file. In most cases when running CentOS on a virtual machine a swap partition is not present so the only option is to create a swap file.

This tutorial explains how to add a swap file on CentOS 7 systems.

### Before You Begin
- Before proceeding with this tutorial, check if your CentOS installation already has swap enabled by typing:

```bash
sudo swapon --show
```

If the output is empty, it means that your system does not have swap space enabled.
Otherwise if you get something like below, you already have swap enabled on your machine.

```bash
NAME      TYPE      SIZE USED PRIO
/dev/dm-1 partition 1.5G   0B   -1
```

Although possible, it is not common to have multiple swap spaces on a single machine.

### Creating a Swap File
The user you are logged in as must have sudo privileges to be able to activate swap. In this guide, we will add 1G of swap, if you want to add more swap, replace 1G with the size of the swap space you need.

Follow the steps below to add swap space on a CentOS 7 system.

First, create a file which will be used as swap space:

sudo fallocate -l 1G /swapfile

If the fallocate utility is not available on your system or you get an error message saying fallocate failed: Operation not supported, use the following command to create the swap file:

sudo dd if=/dev/zero of=/swapfile bs=1024 count=1048576

Ensure that only the root user can read and write the swap file by setting the correct permissions :

sudo chmod 600 /swapfile

Next, set up a Linux swap area on the file:

sudo mkswap /swapfile

Run the following command to activate the swap:

sudo swapon /swapfile

Make the change permanent by opening the /etc/fstab file:

sudo nano /etc/fstab

and pasting the following line:

/etc/fstab
/swapfile swap swap defaults 0 0

Verify that the swap is active by using either the swapon or the free command as shown below:

sudo swapon --show

NAME      TYPE  SIZE   USED PRIO
/swapfile file 1024M 507.4M   -1
sudo free -h

              total        used        free      shared  buff/cache   available
Mem:           488M        158M         83M        2.3M        246M        217M
Swap:          1.0G        506M        517M
Adjusting the Swappiness Value
Swappiness is a Linux kernel property that defines how often the system will use the swap space. Swappiness can have a value between 0 and 100. A low value will make the kernel to try to avoid swapping whenever possible while a higher value will make the kernel to use the swap space more aggressively.

The default swappiness value on CentOS 7 is 30. You can check the current swappiness value by typing the following command:

cat /proc/sys/vm/swappiness

30

While the swappiness value of 30 is OK for desktop and development machines, for production servers you may need to set a lower value.


For example, to set the swappiness value to 10, type:

sudo sysctl vm.swappiness=10

To make this parameter persistent across reboots append the following line to the /etc/sysctl.conf file:

/etc/sysctl.conf
vm.swappiness=10

The optimal swappiness value depends on your system workload and how the memory is being used. You should adjust this parameter in small increments to find an optimal value.

Removing a Swap File
To deactivate and remove the swap file, follow these steps:


Start by deactivating the swap space by typing:

sudo swapoff -v /swapfile

Next, remove the swap file entry /swapfile swap swap defaults 0 0 from the /etc/fstab file.

Finally, delete the actual swapfile file with rm :

sudo rm /swapfile

Conclusion

You have learned how to create a swap file and activate and configure swap space on your CentOS 7 system.

## CentOS8之映象移動
[CentOS8提前EOL，阿里雲源停止維護後的更新配置方法 2022-2-17](https://www.796t.com/article.php?id=468029)

[How To Install the Apache Web Server on CentOS 8](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-8)

## csh 貼上選取文字前後出現 \~00, 01\~
- askubuntu.com, [Why bracketed paste mode is enabled sporadically in my terminal screen?](https://askubuntu.com/questions/662222/why-bracketed-paste-mode-is-enabled-sporadically-in-my-terminal-screen), Aug 16, 2015.
  - close it by $ printf "\e[?2004l" (lowercase of L)
