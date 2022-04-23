---
layout: default
title: Mac網路設定及服務
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---
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
- 在 Mac 系统上打开 ssh 服务权限
- 修改 sshd 配置
- 在登录制生成 rsa key
- 将 rsa key 存到 server 端的 ~/.ssh/authorized_keys文件中

### 重启ssh服务
- 在Mac上打开sshd访问权限
- 勾选 Apple menu > System Preferences > Sharing > Remote Login
  -（启动台 ->系统偏好设置->共享->远程登录）
- 选择任何人、或白名單。

### 修改 sshd 配置
- 在/etc/ssh/sshd_config文件中只需打开下面几项：
  - AuthorizedKeysFile .ssh/authorized_keys 指定被授权的用户的rsa 加密key存放的位置。
  - UsePAM 使用 PAM 进行权限管理。
  - AcceptEnv LANG LC_* 指明本地位置信息。
  - Subsystem sftp /usr/libexec/sftp-server 默认协议。

### 在客户端生成 ssh rsa key
  - 执行 ssh-genkey -t rsa 命令，然后要求输入的地方一直回车。
  - 打开~/.ssh/id-rsa.pub文件，拷贝里面的内容。

### macOS 開關sshd
- 启动 sshd 服务

```bash
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
```
- 停止 sshd 服务
```bash
sudo launchctl unload -w /System/Library/LaunchDaemons/ssh.plist
```
- 查看sshd服务是否启动

```bash
sudo launchctl list | grep ssh
```
### know_hosts 作用
- 在 Mac 上的~/.ssh/ 目录下有一个 know_hosts文件，里边存放了所以你访问过的 sshd 服务，它是一个缓冲文件。每当你通过 ssh 远程访问时，它都会先到这个文件中去查找是否有以前的记录。
- 在一些情况下，如果你访问某台sshd服务出现了错误，那么当你下次访问时还是报错，很可能就是这个文件导致的。所以出现类似问题时，你要记得清一下这个文件中的内容。
- 作者：[音视频直播技术专家](https://www.jianshu.com/p/d548f8af9f6c)

### ssh keygen 免輸入密碼
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
- [ssh-keygen](https://docs.joyent.com/public-cloud/getting-started/ssh-keys/generating-an-ssh-key-manually/manually-generating-your-ssh-key-in-mac-os-x)

### ssh white list
- https://blog.wu-boy.com/2016/12/create-account-and-ssh-permission-on-mac/
### MAC 封鎖存取特定 IP 
- https://blog.yowko.com/mac-block-outgoing-ip/

## 在 macOS 安裝 Apache HTTP Server
- http://mt116.blogspot.com/2019/12/macos-apache-http-server.html
- macOSX 開啟內建 Apache 網站伺服器與PHP環境設定

```bash
sudo apachectl start
sudo apachectl restart
sudo apachectl stop
```
- https://www.minwt.com/mac/21769.html

## mapserver
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
- [apple.discussion](https://discussions.apple.com/thread/8273226)
- [SXEl Capitan 10.11.2 & OS X Server 5.0.15 - Turn Off Unused Services](https://gist.github.com/minhoryang/4c7b56324c5f2e5a8694)

# Monterey Pbms
- [Setting up a local web server on macOS 12 “Monterey”](https://discussions.apple.com/docs/DOC-250004361)  
- 重裝httpd，不要用自帶httpd([如何在 macOS 12 Monterey 上設定 MAMP本地伺服器](https://www.796t.com/article.php?id=453663))
## httpd.conf設定
- `sudo vi /usr/local/etc/httpd/httpd.conf`
- LoadModule：按照[前述](https://www.796t.com/article.php?id=453663)建議
- 更改CGI目錄
  - alias_module

```bash
<IfModule alias_module>
...
  ScriptAliasMatch ^/cgi-bin/((?!(?i:webobjects)).*$) "/Library/WebServer/CGI-Executables/$1"`
</IfModule>
```
  - Directory

```bash
#
# "/usr/local/var/www/cgi-bin" should be changed to whatever your ScriptAliased
# CGI directory exists, if you have that configured.
#
<Directory "/Library/WebServer/CGI-Executables">
    AllowOverride All 
    Options +ExecCGI
    Require all granted
</Directory>
```
- 新增CGI程式附加檔名

```bash
<IfModule mime_module>
...
    #
    # AddHandler allows you to map certain file extensions to "handlers":
    # actions unrelated to filetype. These can be either built into the server
    # or added with the Action directive (see below)
    #
    # To use CGI scripts outside of ScriptAliased directories:
    # (You will also need to add "ExecCGI" to the "Options" directive.)
    #
    AddHandler cgi-script .cgi .pl .py
...
</IfModule>
```
- `Listen 114.32.164.198:80`
## 啟動方式
- [前述](https://www.796t.com/article.php?id=453663)建議用`brew services restart httpd`無法連上，還是需要`sudo apachectl start`
- `sudo chmod +a "_www allow execute" /Library/WebServer/CGI-Executables` also `/Library/WebServer/Documents`

