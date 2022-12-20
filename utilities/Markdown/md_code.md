---
layout: default
title: VS Code提供Markdown語言的功能
parent: Markdown
grand_parent: Utilities
last_modified_date: 2022-11-15 10:21:23
---

# VS Code提供Markdown語言的功能
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 背景

- 此處要探討的是VSCode中支援markdown(md)語言的詳細功能。主要參考[官網][dev]的說明，同時也參考了一些外掛的推介。
- 由於此處的目標是建立GitHub Pages筆記系統，可以接受很多不太正統的md寫法，因此也不建議進行太過於嚴苛的語言檢查。

## 文件編輯

### 文件上方>路徑

- **路徑**在一般網頁畫面上是很常見的訊息，Code也將此一功能加進來，而且習慣性地使用`>`符號將其隔開。
- 內容包括檔案目錄、及游標位置之大綱從屬、如圖1黃色標籤所示。
  - 根目錄為[Repo][repo]。無法在此切換絕對路徑。
  - md檔案為井字號(`#` hashtag)開始的headline、python則為變數名稱
  - 點選大綱會跳到指定位置，而移動滑鼠也會按照游標位置自動切換大綱。
  - 點選箭頭可以開合特定目錄、檔案、或內容、進而切換游標位置。(即使關閉檔案總管也能運作檔案開啟)

| ![path_above_doc](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/path_above_doc.png "圖1 檔案上方與左側之大綱")|
|:--:|
| 圖1 檔案上方(黃標)與左側(紅標)之大綱|

### 行號數字與文件中箭頭

- 出現在第1個字是`#`、`-`、`for`、`if`等區段(圖1紅標所示)
- 滑鼠滑到該處才會出現
- 點選箭頭可以開合其內容(會影響縮圖、但不影響預覽)
- 方便整段剪下、移動、複製。不必害怕滑鼠選取錯誤。

### 檔案總管下的大綱

- 開啟檔案總管中的大綱，所有檔案中以井字號(`#` hash tag)的headline都會出現在此。
- 內設是按照「位置」排序，也可以按照名稱(字母)、類別(語言之物件)排序
  - 此處大綱功能與點選文件上之大綱一樣，但編輯文件時不會消失，是常設之視窗，可以用來參考上下文內容。
  - 可以選擇**全部折疊**與否、
  - 排序方式可以按照名稱(字母)、類別(語言之物件)排序。這項功能對於標題數量很多、層次繁瑣的文件而言很方便，可依字母排序、直接跳到特定標題位置，不必層層打開、尋找。
  - 選擇是否**追蹤游標**(會在大綱中呈現灰底，以顯示在文章中的相對位置)，可以知道目前處在文件中的甚麼位置。
  - 點選箭頭可以開合其內容
  - 直接點選即會移動游標。
- 出現語言錯誤的位置上層會出現圓點、第三層會出現錯誤(含警告)的訊息個數。

| ![markdown-outline-view](https://code.visualstudio.com/assets/docs/languages/Markdown/markdown-outline-view.png "圖2 檔案總管功能之大綱")|
|:--:|
| 圖2 檔案總管功能之大綱([官網][dev])|

- 與[官網][dev]差異
  1. 新版大綱不是自動出現篩選框，而是在大綱處按下Ctrl-F。
  1. 大綱之類別是字串不會在前方出現`abc`

### 自動觸發建議

- 針對特定語言，輸入前幾碼英文字母，Code就會出現可能的選項視窗(包括程式碼、參照、標題、常用關鍵詞、路徑及檔名等等)，讓使用者選擇(上下鍵及tab鍵決定)。
- Code的自動觸發不但針對英文的關鍵詞，曾經鍵入的中文標題也適用。
- 需要修改`settings.js`檔案
  - `ctrl-P`找出此一檔案
  - 按照[網友](https://mileslin.github.io/2017/05/vscode-設定自動觸發-suggestions/)的建議修改。
  - 每個[Repo][repo]作業環境都需要設定。內容如下：

```java
{
  "editor.wordWrap": "on",
  "markdown.preview.fontSize": 18,
  "[markdown]": {
    "editor.formatOnSave": true,
    "editor.renderWhitespace": "all",
    "editor.acceptSuggestionOnEnter": "off",
    "editor.snippetSuggestions": "top",
    "editor.quickSuggestions": {
      "comments": "on",
      "strings": "on",
      "other": "on"
    }
  }  
}
```

- 路徑
  - `/`：表示[Depo][repo]的根目錄
  - `./`:表示與正編輯檔案相同的目錄
  - 參照括弧內如果以`#`為開始`[...](#)`，將會出現檔案內的標題

### 滑鼠的拖放動作

- 滑鼠的拖放在Code除了一般的移動與複製之外，還有特殊的功能
- 參照括弧內的檔案名稱，也可以用滑鼠的拖放來作業
  1. 到檔案總管處點選檔案(只點不放)
  2. 按shift鍵
  3. 拖到文件指定位置放開，就會做成一個連結了。
- 跨[Depo][repo]檔案複製(可以是本地或是網路版dev)
  1. 同時開啟2個工作環境(控制視窗不要最大化)
  2. 到檔案總管處點選檔案(只點不放)
  3. 拖到另一[Depo][repo]工作環境指定目錄處放開

### 全段選取

- [官網][dev]謂此組選取組合為'smart selection'，可以選取整段不致出錯。
  - 應該是對照到ms word 有選取整段的滑鼠點選方式(三擊滑鼠左鍵)，
  - Code三擊滑鼠左鍵會選取單行，還是需要有選取整段的方式。
- macOS、window選取整段的方式略有不同

動作|macOS|window
:-:|:-:|:-:
Expand|⌃⇧⌘→|shift Alt →
Shrink|⌃⇧⌘←|shift Alt ←

[dev]: <https://code.visualstudio.com/docs/languages/markdown> "Markdown and Visual Studio Code, code.visualstudio.com"
[repo]: <https://zh.wikipedia.org/wiki/儲存庫> "儲存庫（英語：repository）[1]亦稱倉庫、資源庫、資源庫、版本庫、代碼庫、存放庫，在版本控制系統中是指在磁碟儲存上的資料結構，其中包含了檔案、目錄以及元資料。儲存庫可能為分散式（如Git）或集中式（如Subversion）。[2]分散式的儲存庫可以複製到每個使用者的本地；集中式的儲存庫只能儲存在伺服器上。[3]"
