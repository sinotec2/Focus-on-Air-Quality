---
layout: default
title: Mac 設定及服務
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
# Network
## Mac 網路連線設定
- 乙太網路
  - 點選上方工作列的圖示，選擇「系統偏好設定」。 如圖點選「系統偏好設定」中的「網路」。
  - 乙太網路（固定IP）設定：
  - 設定固定IP，需要改成「手動」。
  - 然後在此畫面，手動輸入相關網路設定。 範例 IP 位址：140.119.XX.XX. 子網路遮罩：255.255.255.0.
- 使用[PPPoE](http://flow2.nccu.edu.tw/Reg/apple_setnet2.pdf) 將Mac 連接Internet
  - 在您的Mac 上，選擇「蘋果」選單 >「系統偏好設定⋯」，然後按一下「網路」。 ...
  - 按一下左側列表底部的「加入」按鈕 ，按一下「介面」彈出式選單，然後選擇PPPoE。
  - (anonymous), **在 Mac OS X 設定網路**, [nccu] (http://flow2.nccu.edu.tw/Reg/apple_setnet2.pdf), ()
- 使用PPPoE 將Mac 連接Internet - [Apple 支援](https://support.apple.com/zh-tw/guide/mac-help/mchlp2714/mac)
  - (anonymous), **非固定制ADSL使用Mac OSX連接HiNet步驟**, [國立臺南大學](http://www2.nutn.edu.tw/gac320/t4/Mac_OSX.pdf)
- wifi
  - (discussion), **Set Mac to use Wifi for Internet, Ethernet for local file transfer**, [apple.stackexchange](https://apple.stackexchange.com/questions/142482/set-mac-to-use-wifi-for-internet-ethernet-for-local-file-transfer), asked Aug 19 '14 at 14:38

## Mac下的 sshd 服务
### 音视频直播技术专家

```python
前言

最近要用到 Mac 下的 sshd 服务, 但每次使用的时候都是出现各种状况，所以特写此篇文章对 Mac下的sshd服务做一下梳理。在 Mac 下启动 sshd 服务的基本流程：

在 Mac 系统上打开 ssh 服务权限
修改 sshd 配置
在登录制生成 rsa key
将 rsa key 存到 server 端的 ~/.ssh/authorized_keys文件中
重启ssh服务
在Mac上打开sshd访问权限
勾选 Apple menu > System Preferences > Sharing > Remote Login
（启动台 ->系统偏好设置->共享->远程登录）
选择任何人
修改 sshd 配置

在/etc/ssh/sshd_config文件中只需打开下面几项：

AuthorizedKeysFile .ssh/authorized_keys 指定被授权的用户的rsa 加密key存放的位置。
UsePAM 使用 PAM 进行权限管理。
AcceptEnv LANG LC_* 指明本地位置信息。
Subsystem sftp /usr/libexec/sftp-server 默认协议。
在客户端生成 ssh rsa key
执行 ssh-genkey -t rsa 命令，然后要求输入的地方一直回车。
打开~/.ssh/id-rsa.pub文件，拷贝里面的内容。
启动 sshd 服务

sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist

停止 sshd 服务

sudo launchctl unload -w /System/Library/LaunchDaemons/ssh.plist

查看sshd服务是否启动

sudo launchctl list | grep ssh

know_hosts 作用

在 Mac 上的~/.ssh/ 目录下有一个 know_hosts文件，里边存放了所以你访问过的 sshd 服务，它是一个缓冲文件。每当你通过 ssh 远程访问时，它都会先到这个文件中去查找是否有以前的记录。

在一些情况下，如果你访问某台sshd服务出现了错误，那么当你下次访问时还是报错，很可能就是这个文件导致的。所以出现类似问题时，你要记得清一下这个文件中的内容。
```
- 作者：[音视频直播技术专家](https://www.jianshu.com/p/d548f8af9f6c)

### limit access
```python
In order to configure sshd to limit access, you will need to edit the file /etc/ssh/sshd_config, and add the following:

AllowUsersusername@192.168.1.32username@192.168.1.33

where you replace "username" with your actual username.

If you want you can replace parts with * to denote a wildcard, such as for example username@192.168.1.* or *@192.168.1.32. You can read more about the options in the man page for sshd_config.
```
- https://apple.stackexchange.com/questions/344095/restrict-ssh-access-to-selected-ip-on-macos

## ssh keygen 免輸入密碼
- client -> server

```bash
ssh-keygen -t rsa 或 ssh-keygen -d (dsa) => 產生出 id_rsa, id_rsa.pub
scp id_rsa.pub server_hostname:~/.ssh/ id_rsa.pub_client
ssh server_hostname
cat .ssh/id_rsa.pub_client >> .ssh/authorized_keys 即可
```
- server -> client
- 在server端重複做一次
- [longwin](https://blog.longwin.com.tw/2005/12/ssh_keygen_no_passwd/)
- [Ssh-keygen](https://docs.joyent.com/public-cloud/getting-started/ssh-keys/generating-an-ssh-key-manually/manually-generating-your-ssh-key-in-mac-os-x)

## ssh white list
- https://blog.wu-boy.com/2016/12/create-account-and-ssh-permission-on-mac/


# Istallation of Tools
- installation of brew：https://brew.sh/index_zh-tw
- installation of wget etc： brew install wget

# install WRF on a Mac
## How to install WRF on a Mac? 
https://earthscience.stackexchange.com/questions/12699/how-to-install-wrf-on-a-mac

```bash
export HOMEBREW_MAKE_JOBS=1
brew tap wrf-cmake/wrf
brew install wrf-cmake -v
```
- Make sure gcc/gfortran are at same version, and able to fetch from $PATH
- XCODE and Command Line Tools are needed, the latter is download from https:/developer.apple.com/downloads/all

```bash
make install
Last 15 lines from /Users/kuang/Library/Logs/Homebrew/wrf-cmake/04.make:
  671 |           CALL SBYTE (IFOVAL,NMIN,IFOPTR,KBDS(11))
      |                      2
Error: Type mismatch between actual argument at (1) and actual argument at (2) (CHARACTER(1)/INTEGER(4)).
/tmp/wrf-cmake-20211111-42688-1m9or16/WPS/ungrib/src/ngl/w3/w3fi75.f:503:22:

  503 |           CALL SBYTE (BDS11,NBITS,80,8)
      |                      1
......
  671 |           CALL SBYTE (IFOVAL,NMIN,IFOPTR,KBDS(11))
      |                      2
Error: Type mismatch between actual argument at (1) and actual argument at (2) (CHARACTER(1)/INTEGER(4)).
make[2]: *** [ungrib/src/ngl/w3/CMakeFiles/w3.dir/w3fi75.f.o] Error 1
make[2]: *** Waiting for unfinished jobs....
make[1]: *** [ungrib/src/ngl/w3/CMakeFiles/w3.dir/all] Error 2
make: *** [all] Error 2

If reporting this issue please do so at (not Homebrew/brew or Homebrew/core):

  /usr/local/Homebrew/Library/Homebrew/vendor/portable-ruby/current/bin/ruby -W1 --disable=rubyopt /usr/local/Homebrew/Library/Homebrew/brew.rb install wrf-cmake
501 72093 70605 0 9:22AM ttys003 0:00.01 /usr/local/Homebrew/Library/Homebrew/vendor/portable-ruby/current/bin/ruby -W1 --disable=rubyopt /usr/local/Homebrew/Library/Homebrew/brew.rb install wrf-cmake
501 72102 72093 0 9:22AM ttys004 0:02.05 /usr/local/Homebrew/Library/Homebrew/vendor/portable-ruby/2.6.8/bin/ruby -W1 -- /usr/local/Homebrew/Library/Homebrew/build.rb /usr/local/Homebrew/Library/Taps/wrf-cmake/homebrew-wrf/wrf-cmake.rb
501 78001 72102 0 9:34AM ttys004 0:00.09 cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local/Cellar/wrf-cmake/4.1.wrf-cmake -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_BUILD_TYPE=Release -DCMAKE_FIND_FRAMEWORK=LAST -DCMAKE_VERBOSE_MAKEFILE=ON -Wno-dev -DBUILD_TESTING=OFF -DCMAKE_OSX_SYSROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX12.sdk -DCMAKE_INSTALL_PREFIX=/usr/local/Cellar/wrf-cmake/4.1.wrf-cmake/wps -DWRF_DIR=/private/tmp/wrf-cmake-20211111-72102-6jtx18/build
```
# fortran compiler
## ifort
- intel® Fortran Compiler 19.0 for macOS* Release Notes for Intel® Parallel Studio XE 2019[intel®](https://software.intel.com/en-us/articles/intel-fortran-compiler-190-for-macos-release-notes-for-intel-parallel-studio-xe-2019)

## 在MacOS下搭建Fortran开发环境by 李宇琨

- https://lyk6756.github.io/fortran/2017/08/04/Fortran_for_MacOS.html
- gcc(gfortran included):

```bash
brew install gcc
gfortran 10 argument mismatch of type
https://github.com/Unidata/netcdf-fortran/issues/212
export FCFLAGS="-w -fallow-argument-mismatch -O2"
export FFLAGS="-w -fallow-argument-mismatch -O2"
```
- Downgrade of gcc

```bash
brew install gcc@9
(brew switch is deprecated, link the file directly or accept the suggestion of brew doctor)
(base) 10:45:59:kuang@MiniWei:/usr/local/opt $ ls -lh
total 0
...
lrwxr-xr-x  1 kuang  admin    21B Dec 16 06:18 gcc -> ../Cellar/gcc@9/9.3.0
lrwxr-xr-x  1 kuang  admin    21B Dec 16 06:18 gcc@9 -> ../Cellar/gcc@9/9.3.0
```

# Mac 鍵盤快速鍵

- 您可以使用特定的按鍵組合，來執行一般需要滑鼠、觸控式軌跡板或其他輸入裝置才能進行的操作。

- 若要使用鍵盤快速鍵，請按住一或多個變更鍵，再按下快速鍵的最後一個按鍵。例如使用 Command-C（拷貝）時，請先按住 Command 鍵，再按 C 鍵，然後放開兩個按鍵。Mac 選單和鍵盤常使用符號來代表特定按鍵，包括變更鍵：

  - Command（或 Cmd）鍵 ⌘
  - Shift 鍵 ⇧
  - Option（或 Alt）鍵 ⌥
  - Control（或 Ctrl）鍵 ⌃
  - Caps Lock 鍵 ⇪
  - Fn 鍵

- 在專為 Windows PC 製造的鍵盤上，請使用 Alt 鍵來取代 Option 鍵，以 Windows 標誌鍵來取代 Command 鍵。

- 某些 Apple 鍵盤上的部分按鍵含有特殊符號與功能，例如顯示器亮度鍵  
  - 鍵盤亮度鍵
  -「指揮中心」等等。如果您的鍵盤不具備這些功能，您也許可以建立自己的鍵盤快速鍵來複製其中一些功能。若要使用這些按鍵做為 F1、F2、F3 或其他標準功能鍵，請同時按下 Fn 鍵。

## 剪下、拷貝、貼上和其他常見快速鍵

|快速鍵|用途|
|----|----|
|Command-X|剪下所選項目，然後拷貝到「剪貼板」|
|Command-C|將所選項目拷貝到「剪貼板」。這也可以用在 Finder 的檔案上|
|Command-V|將「剪貼板」的內容貼上目前的文件或 app 中。這也可以用在 Finder 的檔案上|
|Command-Z|還原前一個指令。您可以按 Shift-Command-Z 以重做，反轉還原指令。在某些 app 中，您可以還原與重做多個指令|
|Command-A|選取所有項目|
|Command-F|尋找文件中的項目或開啟「尋找」視窗|
|Command-G|再次尋找：尋找下一個之前找到的項目。若要尋找上一個，請按 Shift-Command-G|
|Command-H|隱藏最前方 app 的視窗。若要檢視最前方 app 並同時隱藏所有其他 app，請按 Option-Command-H|
|Command-M|將最前方視窗縮到最小並縮到 Dock。若要將最前方 app 的所有視窗縮到最小，請按 Option-Command-M|
|Command-O|開啟所選項目，或開啟對話框以選擇要開啟的檔案|
|Command-P|列印目前文件|
|Command-S|儲存目前文件|
|Command-T|開啟新標籤頁|
|Command-W|關閉最前方視窗。若要關閉 app 的所有視窗，請按 Option-Command-W|
|Option-Command-Esc|強制結束 app|
|Command-空白鍵|顯示或隱藏 Spotlight  搜尋欄位。若要從 Finder 視窗執行 Spotlight 搜尋，按 Command-Option-空白鍵。（若您使用多個輸入方式以不同的語言輸入內容，則這些快速鍵會變更輸入方式，而不是顯示 Spotlight。瞭解如何 更改相衝突的鍵盤快速鍵）|
|Control-Command-空白鍵|顯示「字元檢視器」，讓您選擇表情符號和其他符號|
|Control-Command-F|以全螢幕使用 app（如果 app 支援此功能）|
|空白鍵|使用「快速查看」預覽所選項目|
|Command-Tab|在開啟中的 app 之間切換至下一個最近使用過的 app|
|Shift-Command-5|在 macOS Mojave 中拍攝螢幕快照或進行螢幕錄製。在舊版的 macOS 中，請使用 Shift-Command-3 或 Shift-Command-4 來拍攝螢幕快照。進一步瞭解螢幕快照|
|Shift-Command-N|在 Finder 中建立新檔案夾|
|Command-逗號（,）|開啟最前方 app 的偏好設定|

## 睡眠、登出和關機快速鍵

以下某些快速鍵可能需要比其他快速鍵按住稍微久一點。這樣的設計可以避免您不小心觸碰這些按鍵。
- 電源按鈕：按下可開啟 Mac 或將 Mac 從睡眠中喚醒。按住 1.5 秒可讓 Mac 進入睡眠。*持續按住可將 Mac 強制關機。
  - Option-Command-電源按鈕* 或  Option-Command-媒體退出鍵
- 讓 Mac 進入睡眠。
  - Control-Shift-電源按鈕* 或  Control-Shift-媒體退出鍵 
- 讓顯示器進入睡眠。
  - Control-電源按鈕* 或 Control-媒體退出鍵
- 顯示對話框，詢問您要重新開機、進入睡眠或關機。
  - Control-Command-電源按鈕*：強制 Mac 重新啟動，且不提示要儲存任何開啟中且未儲存的文件。
  - Control-Command-媒體退出鍵
- 結束所有 app，然後重新啟動 Mac。如果任何開啟中文件尚有未儲存的變更，系統會詢問您是否要儲存。
  - Control-Option-Command-電源按鈕* 或 Control-Option-Command-媒體退出鍵
- 結束所有 app，然後將 Mac 關機。如果任何開啟中文件尚有未儲存的變更，系統會詢問您是否要儲存。
  - Shift-Command-Q：登出您的 macOS 使用者帳號。系統會要求您確認。若要不經確認立即登出，請按 Option-Shift-Command-Q。
* 不適用於Touch ID 感應器。

## Finder 和系統快速鍵

|快速鍵|用途|
|----|----|
|Command-D|複製所選檔案|
|Command-E|退出所選磁碟或卷宗|
|Command-F|在 Finder 視窗中開始 Spotlight 搜尋|
|Command-I|顯示所選檔案的「取得資訊」視窗|
|Command-R|(1) 在 Finder 中選取了某個替身時，顯示所選替身的原始檔案。(2) 在部分 app 中（如「行事曆」或 Safari）重新整理或重新載入頁面。(3) 在「軟體更新」偏好設定中，再次檢查是否有軟體更新項目|
|Shift-Command-C|開啟「電腦」視窗|
|Shift-Command-D|開啟桌面檔案夾|
|Shift-Command-F|開啟「最近項目」視窗，顯示最近檢視或變更的所有檔案|
|Shift-Command-G|開啟「前往檔案夾」視窗|
|Shift-Command-H|開啟目前 macOS 使用者帳號的「個人專屬」檔案夾|
|Shift-Command-I|開啟「iCloud 雲碟」|
|Shift-Command-K|開啟「網路」視窗|
|Option-Command-L|開啟「下載項目」檔案夾|
|Shift-Command-N|建立新檔案夾|
|Shift-Command-O|開啟「文件」檔案夾|
|Shift-Command-P|在 Finder 視窗中顯示或隱藏預覽面板|
|Shift-Command-R|開啟 AirDrop 視窗|
|Shift-Command-T|在 Finder 視窗中顯示或隱藏標籤列|
|Control-Shift-Command-T|將所選的 Finder 項目加入 Dock（OS X Mavericks 或以上版本）|
|Shift-Command-U|開啟「工具程式」檔案夾|
|Option-Command-D|顯示或隱藏 Dock|
|Control-Command-T|新增所選項目至側邊欄（OS X Mavericks 或以上版本）|
|Option-Command-P|在 Finder 視窗中顯示或隱藏路徑列|
|Option-Command-S|在 Finder 視窗中顯示或隱藏側邊欄|
|Command-斜線（/）|在 Finder 視窗中顯示或隱藏狀態列|
|Command-J|顯示「顯示方式選項」|
|Command-K|開啟「連接伺服器」視窗|
|Command-L|製作所選項目的替身|
|Command-N|開啟新的 Finder 視窗|
|Option-Command-N|建立新的智慧型檔案夾|
|Command-T|在目前 Finder 視窗中開啟單一標籤頁時顯示或隱藏標籤列|
|Option-Command-T|在目前 Finder 視窗中開啟單一標籤頁時顯示或隱藏工具列|
|Option-Command-V：移動|將「剪貼板」中的檔案從原始位置移到目前位置|
|Command-Y|使用「快速查看」來預覽所選檔案|
|Option-Command-Y|檢視所選檔案的「快速查看」幻燈片秀|
|Command-1|在 Finder 視窗中使用圖像顯示方式檢視項目|
|Command-2|在 Finder 視窗中使用列表顯示方式檢視項目|
|Command-3|在 Finder 視窗中使用直欄顯示方式檢視項目|
|Command-4|在 Finder 視窗中使用「封面暢覽」顯示方式檢視項目|
|Command-左中括號（[）|前往上一個檔案夾|
|Command-右中括號（]）|前往下一個檔案夾|
|Command-向上鍵|開啟包含目前檔案夾的檔案夾|
|Command-Control-向上鍵|在新視窗中開啟包含目前檔案夾的檔案夾|
|Command-向下鍵|開啟所選項目|
|向右鍵|開啟所選檔案夾。這只能在列表顯示方式中使用|
|向左鍵|關閉所選檔案夾。這只能在列表顯示方式中使用|
|Command-Delete|將所選項目移到垃圾桶|
|Shift-Command-Delete|清空垃圾桶|
|Option-Shift-Command-Delete|不顯示確認對話框便直接清空垃圾桶|
|Command-調高亮度鍵|開啟或關閉目標顯示器模式|
|Command-調低亮度鍵|在 Mac 連接多部顯示器時開啟或關閉 影像鏡像輸出|
|Option-調高亮度鍵|開啟「顯示器」偏好設定。也可以使用調低亮度鍵|
|Control-調高亮度鍵或 Control-調低亮度鍵|更改外接顯示器的亮度（若顯示器支援此功能）|
|Option-Shift-調高亮度鍵或 Option-Shift-調低亮度鍵|微調顯示器亮度。在此快速鍵中加入 Control 鍵，可微調外接顯示器的亮度（若顯示器支援此功能）|
|Option-「指揮中心」|開啟「指揮中心」偏好設定|
|Command-「指揮中心」|顯示桌面|
|Control-向下鍵|顯示最前方 app 的所有視窗|
|Option-調高音量鍵|開啟「聲音」偏好設定。也可以使用調低音量鍵|
|Option-Shift-調高音量鍵或 Option-Shift-調低音量鍵|微調音量|
|Option-調高鍵盤亮度鍵|開啟「鍵盤」偏好設定。也可以使用調低鍵盤亮度鍵|
|Option-Shift-調高鍵盤亮度鍵或 Option-Shift-調低鍵盤亮度鍵|微調鍵盤亮度|
|按住 Option 鍵的同時按兩下|在另一個視窗中開啟項目，同時關閉原來的視窗|
|按住 Command 鍵的同時按兩下|在另一個標籤頁或視窗中開啟檔案夾|
|拖到另一個卷宗的同時按住 Command 鍵|將拖移的項目搬移到另一個卷宗，而非拷貝|
|拖移的同時按住 Option 鍵|拷貝拖移的項目。當您拖移項目時，指標會改變|
|按住 Option 和 Command 鍵同時拖移|製作拖移項目的替身。當您拖移項目時，指標會改變|
|按 Option 同時按一下顯示三角形|開啟所選檔案夾中的所有檔案夾。這只能在列表顯示方式中使用|
|按 Command 同時按一下視窗標題|查看包含目前檔案夾的檔案夾|

- 瞭解如何在 Finder 中使用 Command 或 Shift 鍵來選取多個項目
  - 按一下 Finder 選單列中的「前往」選單可以看到多個快速鍵
  - 這些快速鍵可用來開啟「應用程式」、「文件」、「下載項目」、「工具程式」與「iCloud 雲碟」等許多常用檔案夾。

## 文件快速鍵

以下快速鍵的行為可能會因您使用的 app 而不同。

|快速鍵|用途|
|----|----|
|Command-B|讓所選文字變成粗體，或者開啟或關閉文字粗體功能|
|Command-I|讓所選文字變成斜體，或者開啟或關閉文字斜體功能|
|Command-K|加入網頁連結|
|Command-U|為所選文字加上底線，或者開啟或關閉文字底線功能|
|Command-T|顯示或隱藏「字體」視窗|
|Command-D|在「打開」對話框或「儲存」對話框中選擇「桌面」檔案夾|
|Control-Command-D|顯示或隱藏所選字詞的定義|
|Shift-Command-冒號（:）|顯示「拼字和文法檢查」視窗|
|Command-分號（;）|尋找文件中拼字錯誤的字|
|Option-Delete|刪除插入點的左側文字|
|Control-H|刪除插入點的左側字元。或使用 Delete 鍵|
|Control-D|刪除插入點的右側字元。或使用 Fn-Delete|
|Fn-Delete|在沒有往前刪除鍵的鍵盤上執行往前刪除。或使用 Control-D|
|Control-K|刪除從插入點到行尾或段落結尾之間的文字|
|Fn-向上鍵：Page Up|向上捲動一頁|
|Fn-向下鍵：Page Down|向下捲動一頁|
|Fn-向左鍵：Home|捲動到文件的開頭|
|Fn-向右鍵：End|捲動到文件的結尾|
|Command-向上鍵|將插入點移到文件開頭|
|Command-向下鍵|將插入點移到文件結尾|
|Command-向左鍵|將插入點移到目前這一行的開頭|
|Command-向右鍵|將插入點移到目前這一行的結尾|
|Option-向左鍵|將插入點移到上一個字的開頭|
|Option-向右鍵|將插入點移到下一個字的結尾|
|Shift-Command-向上鍵|選擇從插入點到文件開頭之間的文字|
|Shift-Command-向下鍵|選擇從插入點到文件結尾之間的文字|
|Shift-Command-向左鍵|選擇從插入點到目前這一行開頭之間的文字|
|Shift-Command-向右鍵|選擇從插入點到目前這一行結尾之間的文字|
|Shift-向上鍵|將文字所選範圍延伸到位在上面一行相同水平位置的最近字元|
|Shift-向下鍵|將文字所選範圍延伸到位在下面一行相同水平位置的最近字元|
|Shift-向左鍵|把文字所選範圍向左延伸一個字元|
|Shift-向右鍵|把文字所選範圍向右延伸一個字元|
|Option-Shift-向上鍵|把文字所選範圍延伸到目前段落的開頭，再按一次就會延伸到上一個段落的開頭|
|Option-Shift-向下鍵|把文字所選範圍延伸到目前段落的結尾，再按一次就會延伸到下一個段落的結尾|
|Option-Shift-向左鍵|把文字所選範圍延伸到目前這個字的開頭，再按一次就會延伸到上一個字的開頭|
|Option-Shift-向右鍵|把文字所選範圍延伸到目前這個字的結尾，再按一次就會延伸到下一個字的結尾|
|Control-A|移到一行或一段的開頭|
|Control-E|移到一行或一段的結尾|
|Control-F|前進一個字元|
|Control-B|後退一個字元|
|Control-L|將游標或所選範圍移到可視區域中央|
|Control-P|上移一行|
|Control-N|下移一行|
|Control-O|在插入點後面插入新的一行|
|Control-T|將插入點後方的字元與插入點之前的字元互換|
|Command-左花括號（{）|靠左對齊|
|Command-右花括號（}）|靠右對齊|
|Shift-Command-垂直線（|）|中央對齊|
|Option-Command-F|前往搜尋欄位|
|Option-Command-T|顯示或隱藏 app 中的工具列|
|Option-Command-C|拷貝樣式：將所選項目的格式設定拷貝到「剪貼板」|
|Option-Command-V|貼上樣式：將所拷貝的樣式套用到所選項目|
|Option-Shift-Command-V|貼上並符合樣式：將周圍內容的樣式套用到貼入該內容的項目|
|Option-Command-I|顯示或隱藏檢閱器視窗|
|Shift-Command-P|頁面設定：顯示用於選擇文件設定的視窗|
|Shift-Command-S|顯示「儲存為」對話框或複製目前文件|
|Shift-Command-減號（-）|縮小所選項目|
|Shift-Command-加號（+）|放大所選項目。Command-等號（=）可執行相同功能|
|Shift-Command-問號（?）|開啟「輔助說明」選單|

## 其他快速鍵

若要查看更多快速鍵，請參考 app 選單中顯示的快速鍵縮寫。每個 app 都有自己的快速鍵，而可以在某個 app 中使用的快速鍵，不見得適用於其他 app。 

輔助使用快速鍵
Safari 快速鍵
Spotlight 快速鍵
啟動快速鍵
iTunes 快速鍵：在 iTunes 選單列中選擇「輔助說明」>「鍵盤快速鍵」。
其他快速鍵：選擇「蘋果」選單 >「系統偏好設定」，按一下「鍵盤」，然後按一下「快速鍵」。

- [Mac 鍵盤快速鍵](https://support.apple.com/zh-tw/HT201236/localeselector)

# WRF-CMake
A new cross-platform build system for the Advanced Research WRF (ARW)
https://github.com/WRF-CMake

brew install wrf-cmake/wrf/wrf-cmake

# Mac OS X安装gnu-sed等命令行工具
## sed
- sed -i ->sed -ie
  - https://blog.csdn.net/xicikkk/article/details/52559433
  - http://osxdaily.com/2014/02/06/add-user-sudoers-file-mac/

## zsh
- Apple replaces bash with zsh as the default shell in macOS Catalina
  - https://www.theverge.com/2019/6/4/18651872/apple-macos-catalina-zsh-bash-shell-replacement-features
- The default interactive shell is now zsh.
- To update your account to use zsh, please run `chsh -s /bin/zsh`.
  - For more details, please visithttps://support.apple.com/kb/HT208050.
  -As of 2019, macOS Catalina has adopted Z Shell, or zsh for short, as the default login shell. Z Shell is a Unix shell that acts as an interactive login shell and command line interpreter for shell scripting.
  - https://medium.com/dev-genius/customize-the-macos-terminal-zsh-4cb387e4f447

```bash  
PROMPT='%F{green}%*%f:%F{blue}%~%f %% '
chsh -s /bin/bash
```
- how-to-change-the-default-shell-to-bash-in-macos-catalina [howtogeek](https://www.howtogeek.com/444596/how-to-change-the-default-shell-to-bash-in-macos-catalina/)
- Zsh [prompt](https://medium.com/statementdog-engineering/prettify-your-zsh-command-line-prompt-3ca2acc967f)

# Exit macOS, but leave running jobs open?
## NO_HUP
```bash
% setopt NO_HUP

nohup <command> & disown
```
- [stackoverflow](https://stackoverflow.com/questions/19302913/exit-zsh-but-leave-running-jobs-open)
- [maketecheasier](https://www.maketecheasier.com/run-bash-commands-background-linux/)

## tmux

# Utf8-mac
- https://zh.wikipedia.org/wiki/UTF-8#Mac_OS_X
# crontab
https://blog.niclin.tw/2018/04/08/mac-os-%E5%9F%B7%E8%A1%8C-crontab-%E4%BE%8B%E8%A1%8C%E6%80%A7%E5%B7%A5%E4%BD%9C%E6%8E%92%E7%A8%8B/
- 在MAC OS X上如何啟用crontab？ (no use)
  - https://blog.niclin.tw/2018/04/08/mac-os-執行-crontab-例行性工作排程/
- cron jobs crontab 排程教學
  - https://www.puritys.me/docs-blog/article-20-cron-jobs-crontab-排程教學.html
- cron does not execute when user is not logged in
  - https://discussions.apple.com/thread/7701184
- Mac執行定時任務之launchctl
  - https://www.itread01.com/p/353876.html

# anaconda
- https://docs.anaconda.com/anaconda/install/mac-os/
- https://repo.anaconda.com/archive/Anaconda3-2020.11-MacOSX-x86_64.sh
- LC_ALL="C" conda install python=3.7 (locale missing)
- x window (for NCL etc)
  - https://www.xquartz.org/

# MiniWei notes(12/14):

```bash
Installation of Firefox,
substitute of Safari,  which is not sustainable development
FireFOX is ready and more convenient for python crawler programs.
Allow remote login(SETUP-> share)
Install brew(https://brew.sh/index_zh-tw)
initiate the firewall(SETUP->safety)
brew install gfortran
anaconda3.8 download(installation by command line, https://repo.anaconda.com/archive/Anaconda3-2020.11-MacOSX-x86_64.sh)
scp IMacKuang:~/bin
brew install mpich(wrong, wrf uses openmpi)
scp WRF4.1, IOAPI, netCDF4, HDF5
compile camx700nc
argument mismatch-type error, just add followings
export FCFLAGS="-w -fallow-argument-mismatch -O2"
export FFLAGS="-w -fallow-argument-mismatch -O2"
modify NAME->name in routines used for reading netcdf global attribute
modify the NCF_INST path in Makefile
cp 2016_v7 tar and run
conda create -n ncl_stable -c conda-forge ncl
installations of py27 and py37
installation of VERDI
brew installation java
download zip file from CMAS
unpack to /opt
modify VERDI_HOME in /opt/VER*/verdi.command
make link
(base) 6:25:53:kuang@MiniWei:/Users/WRF4.1/WRFv3/201909/run10 $ mpirun -np 6 wrf.exe
dyld: Library not loaded: /usr/local/opt/gcc/lib/gcc/10/libgfortran.5.dylib
  Referenced from: /usr/local/opt/netcdf/lib/libnetcdff.7.dylib
  Reason: image not found
dyld: Library not loaded: /usr/local/opt/gcc/lib/gcc/10/libgfortran.5.dylib
  Referenced from: /usr/local/opt/netcdf/lib/libnetcdff.7.dylib
  Reason: image not found
dyld: Library not loaded: /usr/local/opt/gcc/lib/gcc/10/libgfortran.5.dylib
  Referenced from: /usr/local/opt/netcdf/lib/libnetcdff.7.dylib
  Reason: image not found
dyld: Library not loaded: /usr/local/opt/gcc/lib/gcc/10/libgfortran.5.dylib
  Referenced from: /usr/local/opt/netcdf/lib/libnetcdff.7.dylib
  Reason: image not found
dyld: Library not loaded: /usr/local/opt/gcc/lib/gcc/10/libgfortran.5.dylib
  Referenced from: /usr/local/opt/netcdf/lib/libnetcdff.7.dylib
  Reason: image not found
dyld: Library not loaded: /usr/local/opt/gcc/lib/gcc/10/libgfortran.5.dylib
  Referenced from: /usr/local/opt/netcdf/lib/libnetcdff.7.dylib
  Reason: image not found
--------------------------------------------------------------------------
Primary job  terminated normally, but 1 process returned
a non-zero exit code. Per user-direction, the job has been aborted.
--------------------------------------------------------------------------
--------------------------------------------------------------------------
mpirun noticed that process rank 5 with PID 0 on node MiniWei exited on signal 6 (Abort trap: 6).
--------------------------------------------------------------------------
Homebrew Formulae
brew install nco
https://formulae.brew.sh/formula/nco
version 4.9.6
```
# 在 macOS 安裝 Apache HTTP Server
- http://mt116.blogspot.com/2019/12/macos-apache-http-server.html
- macOSX 開啟內建 Apache 網站伺服器與PHP環境設定

```bash
sudo apachectl start
sudo apachectl restart
sudo apachectl stop
```
- https://www.minwt.com/mac/21769.html

# mapserver
```bash
brew install mapserver
```
- https://formulae.brew.sh/formula/mapserver
  - (fail); try make, need proj4, C# compiler(https://www.mono-project.com/docs/about-mono/supported-platforms/macos/)
- https://www.infoworld.com/article/2939526/automating-osx-server-with-the-serverctl-command.html

# How can I disable Server.app's Webserver?
```bash
edit: /Library/Server/Web/Config/Proxy/apache_serviceproxy.conf
Comment or change these to alternate ports
listen 80
listen 443
sudo killall httpd
```
- https://discussions.apple.com/thread/8273226
- S X El Capitan 10.11.2 & OS X Server 5.0.15 - Turn Off Unused Services
  - https://gist.github.com/minhoryang/4c7b56324c5f2e5a8694

# ganlia setting
https://www.deanspot.org/alex/2009/07/25/compiling-ganglia-gmond-and-gmetad-osx-105.html
https://sourceforge.net/projects/ganglia/

# sleeping of a mac

```bash
pmset -g custom
AC Power:
 Sleep On Power Button 1
 standbydelayhigh     86400
 standbydelaylow      86400
 proximitywake        1
 standby              1
ttyskeepawake        1     
（遠程用戶活動時防止睡眠；1開、0關）
hibernatemode        3
 powernap             1
 gpuswitch            2
 hibernatefile        /var/vm/sleepimage
 highstandbythreshold 50
 displaysleep         0
 womp                 1
 networkoversleep     0
 sleep                0
 halfdim              1
 autorestart          1
 disksleep            10
```
- https://yuripe-murmur.github.io/posts/2019-02-02-sleep/

```bash
pmset -g stats
Sleep Count:0
Dark Wake Count:0
User Wake Count:2
```
- https://www.zhihu.com/question/23644093

- 我在下面添加了以下脚本 .bash_profile
```bash
if expr "$(ps -o comm= $PPID)" : '^sshd:' > /dev/null; then
caffeinate -s $SHELL --login
exit $?
fi
```
- 如果该进程是ssh守护程序的直接子进程，请通过caffeinate（8）命令运行相同的Shell，以防止系统在ssh会话期间进入休眠状态。
https://qastack.cn/unix/1786/os-x-how-to-keep-the-computer-from-sleeping-during-a-ssh-session
## tell mac to sleep

```bash
#!/bin/sh
ssh foo.dyndns.com pmset sleepnow
```
- execute OSA scripts (AppleScript, JavaScript, etc.),[osxdaily](https://osxdaily.com/2012/03/14/remotely-sleep-mac/)

```bash
osascript -e 'tell application "System Events" to sleep'
```

```bash
#!/usr/bin/env python
#
#Note: SSH port needs to have UDP forwarding enabled.

import socket

host = socket.gethostbyname('foo.dyndns.com')
port = 22
mac = '\x12\x34\x56\x78\x9a\xbc'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('\xff' * 6 + mac * 16, (host, port))
```

# 如何使用目標顯示器模式
- 確定iMac 已啟動並符合上述的系統需求。
- 確定另一部Mac 已啟動並已登入macOS 使用者帳號。
- 使用適當的Mini DisplayPort 或Thunderbolt 連接線來連接兩部電腦。 ...
- 在iMac 鍵盤上按下Command-F2。 ...
- 若要退出目標顯示器模式，請再次按下Command-F2。
  - 2021年6月8日

## 利用目標顯示器模式將iMac 當做顯示器使用- Apple 支援(台灣)
- https://support.apple.com/zh-tw/HT204592
- https://superuser.com/questions/14836/crontab-to-wake-osx-from-sleep

# sleepwatcher
https://boyux.com/2017/07/02/sleepwatcher/

# 免安裝軟體讓-mac-也能讀寫-ntfs-格式
- [noter](https://noter.tw/5369/存不進隨身碟？免安裝軟體讓-mac-也能讀寫-ntfs-格式/)

```bash
mount (chk /dev/disk2s1)
sudo umount /Volumes/HansNTFS
sudo mkdir  /Volumes/HansNTFS
sudo mount -o rw,auto,nobrowse -t ntfs /dev/disk2s1 /Volumes/HansNTFS
```
- Disk編號可以由下列指令而得（如果mount df 或Finder都找不到）

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
                                 Physical Stores disk0s2, disk1s2
   1:                APFS Volume Macintosh HD            901.6 GB   disk2s1
   2:                APFS Volume Preboot                 56.0 MB    disk2s2
   3:                APFS Volume Recovery                510.5 MB   disk2s3
   4:                APFS Volume VM                      3.2 GB     disk2s4
/dev/disk3 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *4.0 TB     disk3
   1:         Microsoft Reserved                         134.2 MB   disk3s1
   2:       Microsoft Basic Data Seagate Expansion Drive 4.0 TB     disk3s2

$ sudo mount -o rw,auto,nobrowse -t ntfs /dev/disk3s2 /Volumes/Seagate
```

# gcc version problem (CCTM_RE_COMPILE)

```bash
ioapi, netCDF(4.5) are compile using gcc 9.2.0( /opt/local/bin/x86_64-apple-darwin18-*)
/opt/local/bin/x86_64-apple-darwin18-gfortran-mp-9 differ from /opt/anaconda3/bin/mpifort
althought they are all 9.2.0 (mpifort seems newer)
re_make fail in the last step:
mpifort se_bndy_copy_info_ext.o se_pe_info_ext.o se_comm_info_ext.o se_data_send_module.o se_domain_info_ext.o se_internal_util_module.o se_data_recv_module.o se_disp_info_ext.o se_subgrid_info_ext.o se_global_sum_module.o se_global_max_module.o se_global_min_module.o se_slice_module.o se_init_module.o se_bndy_copy_module.o se_comm_module.o se_reconfig_grid_info_ext.o se_reconfig_grid_module.o se_gather_module.o se_data_copy_module.o se_term_module.o se_twoway_comm_module.o se_util_module.o se_modules.o alloc_data_mod.o parutilio.o piomaps_mod.o get_write_map.o pio_init.o pm3err.o pm3exit.o pm3warn.o pshut3.o ptrwrite3.o pwrgrdd.o pwrite3.o subdmap.o wrsubdmap.o RXNS_DATA_MODULE.o get_env_mod.o RUNTIME_VARS.o UTILIO_DEFN.o VGRD_DEFN.o HGRD_DEFN.o GRID_CONF.o STM_VARS.o DEPVVARS.o VDIFF_DATA.o CGRID_SPCS.o LSM_MOD.o depv_data_module.o biog_emis_param_module.o BIDI_MOD.o crop_data_module.o em_param_module.o ob_param_module.o AEROMET_DATA.o AERO_DATA.o lus_data_module.o UDTYPES.o stack_group_data_module.o station_group_data_module.o EMIS_VARS.o OBSS_VARS.o STK_PRMS.o OBS_PRMS.o centralized_io_util_module.o LUS_DEFN.o centralized_io_module.o PCGRID_DEFN.o PTBILIN.o PTMET.o STK_EMIS.o STN_OBSS.o ASX_DATA_MOD.o PRECURSOR_DATA.o DEPV_DEFN.o LTNG_DEFN.o DUST_EMIS.o BIOG_EMIS.o STD_CONC.o CSQY_DATA.o CLOUD_OPTICS.o complex_number_module.o twoway_rrtmg_aero_optics.o SOA_DEFN.o AERO_PHOTDATA.o PA_DEFN.o RXNS_FUNC_MODULE.o AERO_BUDGET.o VDIFF_MAP.o BEIS_DEFN.o PT3D_DEFN.o OB2D_DEFN.o AEROSOL_CHEMISTRY.o SA_DEFN.o PHOT_MOD.o PAGRD_DEFN.o PA_IRR_CTL.o PA_IRR_module.o PISAM_DEFN.o MGEMIS.o SA_IRR_DEFN.o SA_LAYERS.o AVG_CONC.o SSEMIS.o WVEL_DEFN.o vertext_module.o STM_MODULE.o AERO_EMIS.o HGSIM.o EMIS_DEFN.o distr_env.o mpcomm_init.o advstep.o cmaq_main.o driver.o hveloc.o sciproc.o wr_aconc.o wr_cgrid.o wr_conc.o wr_init.o diffmsg.o flcheck.o grdcheck.o initscen.o load_cgrid.o opaconc.o opconc.o couplewrf.o advbc_map.o hadvppm.o hcontvel.o hppm.o rdbcon.o x_ppm.o y_ppm.o zfdbc.o vppm.o zadvppmwrf.o deform.o hcdiff3d.o hdiff.o rho_j.o VDIFF_DIAG.o SEDIMENTATION.o aero_depv.o aero_sedv.o conv_cgrid.o eddyx.o matrix1.o opddep.o rddepv.o tri.o vdiffacmx.o vdiffproc.o ABFLUX_MOD.o cgrid_depv.o gas_depv_map.o m3dry.o opdepv_diag.o cropcal.o opemis.o tfabove.o tfbelow.o beis3.o checkmem.o chkgrid.o czangle.o getfline.o getparb.o hrno.o parsline.o tmpbeis.o wrdaymsg.o delta_zs.o fire_plmris.o openlayout.o oppt3d_diag.o plmris.o plsprd.o preplm.o write3_distr.o PHOT_MET_DATA.o PHOTOLYSIS_ALBEDO.o SEAS_STRAT_O3_MIN.o concld_prop_acm.o o3totcol.o opphot.o phot.o DEGRADE_SETUP_TOX.o hrdata_mod.o degrade_data.o degrade.o final_degrade.o find_degraded.o hrdriver.o hrg1.o hrg2.o hrg3.o hrg4.o hrinit.o hrprodloss.o hrrates.o hrsolver.o init_degrade.o PMDIAG_DATA.o aero_driver.o aero_subs.o coags.o getpar.o isocom.o isofwd.o isorev.o opapmdiag.o oppmdiag.o AQ_DATA.o acmcld.o aqchem.o aq_map.o cldproc_acm.o convcld_acm.o getalpha.o hlconst.o indexn.o opwdep.o rescld.o scavwdep.o PA_GLOBAL.o PA_IPRDEF.o PA_VARS.o PA_PARSE.o PA_IPRVARS.o pa_compmech.o pa_datagen.o pa_errcheck.o pa_getcoef.o pa_getcycle.o pa_getdesc.o pa_getfamily.o pa_getiprout.o pa_getirrout.o pa_getrxns.o pa_getrxnsum.o pa_init.o pa_mkhdr.o pa_molcloss.o pa_molcprod.o pa_output.o pa_read.o pa_report.o pa_setup_ipr.o pa_setup_irr.o pa_update.o pa_wrtpadefn.o op_sa.o sa_array_init.o sa_dim.o sa_matrix1.o sa_opwddep.o sa_tri.o SA_WRAP_AE.o wr_avg_sa.o wr_sa_cgrid.o wr_sa.o log_header.o cksummer.o findex.o lstepf.o setup_logdev.o subhdomain.o subhfile.o -L/Users/cmaqruns/CMAQ_Project/lib/x86_64/gcc/ioapi/lib -lioapi -L/Users/cmaqruns/CMAQ_Project/lib/x86_64/gcc/netcdff/lib -lnetcdff -L/Users/cmaqruns/CMAQ_Project/lib/x86_64/gcc/netcdf/lib -lnetcdf -L/usr/local/Cellar/gcc@9/9.4.0/lib/gcc/9 -lgcc -lgomp -o CCTM_v53K.exe
ld: library not found for -lSystem
collect2: error: ld returned 1 exit status
gcc 9.2 is not provided by brew any more(gcc@9=gcc 9.4.0)
gcc 9.4/10/11 not compatible with IOAPI (gfortran too stringent for subroutine arguments), can't be rebuilt
gcc 11 need newer Xcode, which not compatible with Mojave(macOS 10)
```
# How to add a user from the command line in macOS?
- [apple.stackexchange](https://apple.stackexchange.com/questions/286749/how-to-add-a-user-from-the-command-line-in-macos/286829)