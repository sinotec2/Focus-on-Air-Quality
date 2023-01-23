---
layout: default
title: VS Code安裝使用
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2022-11-10 09:01:53
tags: note_system
---

# VS Code安裝使用

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## 背景

- [VS Code][vsc_wiki]作為一個現代的整合發展環境([IDE][ide])，除了傳統的編輯功能、檔案總管界面、以及終端機執行與偵錯界面，還必須具備智能提示、與GitHub連絡協作、預覽、外掛等等的能力。
- 什麼樣的人會需要使用[VS Code][vsc_wiki]
  - 程式發展者(程式及偵錯功能，本文較少涉獵此領域)
  - md檔案及部落客([編輯](#編輯窗格)及[預覽](#預覽)功能)
  - 厭倦word或其他軟體，尋找更好的數位化筆記系統的人([檔案總管](#大綱開合及移動)、[跨檔搜尋](#搜尋)與[前往](#移至移動前往功能)功能)

### 推介

- 台大資訊系計算機程式設計課程指定使用、([鄭士康 2018](https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=901%2033900&class=&dpt_code=0000&ser_no=21041&semester=107-2)、[鄭士康 2020](http://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/cou/106S201/1/V/1?v=ntu))

- 10 Best IDE For Web Developers in 2022，名列第1, [GeeksForGeeks, 2022](https://www.geeksforgeeks.org/10-best-ide-for-web-developers-in-2022/)。
- The 12 best IDEs for programming, 名列第1,[TechRepublic, 2022](https://www.techrepublic.com/article/best-ide-software/)

### 使用介紹

- Visual Studio Code開發網站入門教學、[Romaz Rau, 2020](https://medium.com/@success85911/visual-studio-code開發網站入門教學-7514ea9299bf)
- Visual Studio Code 介面的基礎使用介紹(使用Python)、[ITWALKER,2020](https://walker-a.com/archives/6242)
- 在無人之境初次見面的 C 語言與 VSCode - IDE 與編輯器淺談、[PenutChen, 2020](https://hackmd.io/@PenutChen/BJEQsNX3v)
- Markdown and Visual Studio Code, [code.visualstudio.com](https://code.visualstudio.com/docs/languages/markdown)，Code提供Markdown的特別功能。

## [VS Code][vsc_wiki]安裝

### 免安裝版本

- 上網編輯雲端檔案，可以說是現代數位筆記系統的重要功能之一(google doc、evernote etc.)。Code也可以直接在browser上執行，或在[GitHub][gh]界面直接啟動程式開啟雲端檔案進行編輯(圖1)。功能與桌機安裝版一樣。
- 如果使用公用電腦、沒有足夠的硬碟空間容納另一套軟體、或對手機或平版上的使用者而言，都是項福音。
- 網路版Code與桌機版一樣，可以選擇編輯本地版本，在本地複製一份進行編輯還是比較安全些。
- 程式網址[https://vscode.dev/](https://vscode.dev/)


| ![web_code.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/web_code.png "圖1 GitHub檔案編輯之提示，讓使用者可以選擇是否使用Code或傳統編輯界面")|
|:--:|
| <b>圖1 [GitHub][gh]檔案編輯之提示，讓使用者可以選擇是否使用Code或傳統編輯界面</b>| 

### 下載

- 前往[Visual Studio Code官網](https://code.visualstudio.com/Download)，有window、MacOS、與linux 等3種版本可供選擇。
- 有[過去版本](https://code.visualstudio.com/docs/supporting/faq#_previous-release-versions)可下載。如機器太舊可選擇舊版。

### 安裝

- 不需要系統管理者、一般使用者即可安裝。可參考[IThome](https://ithelp.ithome.com.tw/articles/10195139)這篇。

## 開啟[VS Code][vsc_wiki]

### 新增檔案

- 如果沒有既有資料夾或檔案，
  - 可以選擇開新檔案(鍵入檔名、與儲存目錄)。

### 開啟(個別)檔案

- [VS Code][vsc_wiki]也可以開啟個別檔案，但就不會有檔案總管(Explorer)功能。

### 開啟檔案夾([存放庫,Repo][repo])

- 如已有檔案夾([Repo][repo])，可以選擇在window開始畫面(圖2)、或[VS Code][vsc_wiki]歡迎畫面點選(圖3)。
- [VS Code][vsc_wiki]的檔案管理是[git][git]**相對路徑**的概念
  - **絕對路徑**只能在此階段處理
  - 如果要同時開起其他位置的檔案，必須啟動另一個[VS Code][vsc_wiki]來開啟該檔案所在[Repo][repo]。
  - 不同[VS Code][vsc_wiki]的檔案總管(Explorer)間可以使用滑鼠**拖放**

| ![code_2.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_2.PNG)|![code_1.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_1.PNG)|
|:--:|:--:|
| <b>圖2 window開始點選[VS Code][vsc_wiki]右邊箭頭可以選取最近開啟目錄([Repo][repo])</b>| <b>圖3 [VS Code][vsc_wiki]歡迎畫面提示</b>|

### 從[GitHub][gh]複製存放庫

- 或者由**Git存放庫**下載(即為GitHub Code點選複製的clone https，如圖4)。
- 在空格處貼上.git網址後，需要指定[Repo][repo]之根目錄絕對路徑(圖5)。

| ![code_3.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_3.PNG)|![code_4.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_4.PNG)|
|:--:|:--:|
| <b>圖4 在空格處貼上.git網址按enter下載檔案</b>| <b>圖5 指定[Repo][repo]之根目錄絕對路徑</b>|

### 從[GitHub Desktop][gh_dt]啟動VS Code

- 作為[GitHub][gh]預設的編輯軟體，在[GitHub][gh]官網上、或是從[GitHub Desktop][gh_dt]歡迎畫面上，都可以啟動指定[Repo][repo]為根目錄的Code作業，如圖6所示。
  - 必須先在本地建立該[Repo][repo]的clone。
  - 如已建立，每次編輯需先從雲端Pull最新版本
  - 再開啟Code、繼續編輯或新增檔案

| ![code_5.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/ghdesktop_welcom.png)|
|:--:|
| <b>圖6 在[GitHub Desktop][gh_dt]p歡迎畫面開啟指定[Repo][repo]為根目錄的Code作業</b>| 

- 當然在本地複製雲端存放庫的方法不是只有這一種。
  1. 可以直接以命令列指令複製(`git clone https:...git`)
  1. 使用[GitHub Desktop][gh_dt] 程式來[開啟](https://docs.github.com/cn/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop)
  1. 其他軟體參考[Best Git GUI Clients for Windows](https://blog.devart.com/best-git-gui-clients-for-windows.html)

## [VS Code][vsc_wiki]界面外框

### 界面左側主要提示欄(primary side bar)介紹

- 2022版將左側欄名稱更改了，分為主要提示與次要提示，讓二者有上下的從屬關係。
- 左上(圖7)
  1. 檔案總管(Explorer)。又分為[Repo][repo](以下所有的目錄文件)、[大綱](#大綱開合及移動)(選取md檔案的大綱)、時間表(作業過程的儲存版本。[本地歷史](https://code.visualstudio.com/assets/updates/1_66/local-history.gif)是2022版本的特色之一)。如有未存檔案會出現藍色圓點數字，提示要存檔再離開。
  1. [搜尋(置換)](#搜尋)。可指定包含、排除檔案(類型)、大小寫、逐一確認等。
  1. 原始控制檔。如出現藍色圓點數字表示還未Push到[GitHub][gh](雲端儲存)。
  1. 執行與偵錯，如果開啟的是程式碼，按此處就會執行。
  1. 延伸模組。可下載特輸功能的外掛(免費)。
  1. [Docker][Docker]。如果需要整個[Repo][repo]做備份或傳遞給他人，可以考慮使用[Docker][Docker]。

| ![code_5.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_5.PNG)|![code_6.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_6.PNG)|
|:--:|:--:|
| <b>圖7 [VS Code][vsc_wiki]界面左上角功能</b>| <b>圖8 左下角功能</b>|

- 左下角(圖8)
  1. 帳戶。指得是[GitHub][gh]帳戶，如使用Code直接進行GitHub更新，則會需要輸入正確的帳密(也需要正確版本的.net，如否，也可以使用[GitHub Desktop][gh_dt]進行檔案交換)。
  1. 管理。有關Code的設定在此彙總統一管理。
  1. Git分支名稱。協作時需注意自己在處理的版本，以避免覆蓋他人版本。
  1. Git同步處理。按下去就會將雲端檔案更新。
  1. 編譯程式碼的錯誤或警告(條列數)

### [VS Code][vsc_wiki]界面右側介紹

- 右上(圖9)
  - 最上一行
    1. 切換主要提要欄位(即前述左上各項功能之開合切換，以使畫面更大一些)
    1. 切換面版。下方(命令列)出現與否。
    1. 自訂版面配置。提要欄位、面版等控制，也可以直接選取既定模式。
    1. 視窗縮到最小
    1. 視窗重疊 
    1. 關閉視窗
  - 第2行    
    1. 開啟變更。以顯示上次存檔與修改後的對照。
    1. 在一側開啟**預覽**。編輯md檔案時，需要預先知道提交後文件結果如何。
    1. 向右分割編輯器。同時編輯2個或更多檔案時可以使用。
    1. 更多操作
    1. 文件[縮圖](#縮圖顯示)。對捲動長檔案時非常好用。

| ![code_7.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_7.PNG)|![code_8.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/code_8.PNG)|
|:--:|:--:|
| <b>圖9 [VS Code][vsc_wiki]界面右上角功能、文件右上側為整個文件之[縮圖預覽](#縮圖顯示)(含[大綱開合](#大綱開合及移動)及[編輯](#編輯窗格)、[尋找](#文件內搜尋取代)之效果)</b>| <b>圖10 右下角功能</b>|

- 右下角(圖10)
  1. 游標停留位置。當滑鼠將畫面移開後，要回到游標位置，可以直接點此處。
  1. 空格。一個tab有幾格。python程式需2或4格，Fortran需7格。
  1. UTF-8。編碼，跨機器時會出現問題。
  1. CRLF。行尾順序。也是跨機器時的重要約定項目。
  1. 選取語言模式Markdown。Code程式會自行判斷文件內容是哪種語言，如果選錯了，可以在此修正。
  1. 推文意見反映
  1. 系統通知。如果有更新項目，會在此處通知。

## 編輯窗格

- 點選檔案總管的文件，就會在中央的窗格中出現。
  - 文字檔案會進入編輯窗格
  - 圖檔格式，則會在窗格中預覽。
  - 其他檔案，如沒有外掛延伸模組，理論上是無法開啟、預覽的。
- 五種顏色，顯示特殊意義、協助辨識、方便[移動](#滑鼠)位置
- 語言意義
  - （#）註解或標題：咖啡色字（mac為藍色）
  - [...]、“...”、\`...\`字串：橘色字
  - http://aaa、\[...\](#aaa)：藍色或白色(mac)底線
- 語言偵錯：底線、[縮圖](#縮圖顯示)橫線、拉桿右側
  - 黃色：警告
  - 紅色：錯誤
- 文件版本比較之顏色表示(行號右側之垂直線條[-詳gif](https://code.visualstudio.com/assets/updates/1_66/scm.gif)、[縮圖](#縮圖顯示)左側、拉桿左側，如圖11)
  - 相對於GitHub上的版本
  - 綠色：此次新增
  - 藍色：修改
  - 紅色向下箭頭：刪除行
  - Push更新GitHub之後，這些顏色就會消失

| ![find_snip.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/find_snip.png "圖11 右側文件縮圖與拉桿上顏色的分布：尋到之關鍵字詞(橘色底橫線與方塊)、新增文字區塊(綠色)、修改(藍色)")|
|:--:|
| <b>圖11 右側文件縮圖與拉桿上顏色的分布：[搜尋](#文件內搜尋取代)到之關鍵字詞(橘色底橫線與方塊)、新增文字區塊(綠色)、修改(藍色)</b>| 

### 重要的移動鍵組合

- ctrl 上/下：移動畫面(向上移/向下移)而不移動游標
- ctrl 左/右：跳越一詞
- ctrl 上頁/下頁：已開啟的檔案中，換到左(右)側檔。
- ctrl Home/End：將游標移動到文件的最前/後
- shift 上/下/左/右：選取
- Alt 左：上次滑鼠移動前的游標位置(上一步)
- Alt 上/下：將所在行文字向上移/向下移
- Alt 上頁/下頁：翻動畫面(向上一頁/向下一頁)而不移動游標
- F2 :重新命名變數名稱，方便更改當前檔案中的變數名稱。
- 更多快捷鍵請參考 [官方文件](https://github.com/Microsoft/vscode-tips-and-tricks)
  - ctrl-shift-I：貼上時間標籤(現在時刻)，這對筆記系統文件而言非常重要。

### 大綱開合及移動

- 文件上方會出現檔案目錄、及游標位置之大綱從屬
  - md檔案為井字號(`#` hashtag)開始的headline、python則為變數名稱
  - 會按照游標位置自動切換大綱
  - 點選箭頭可以開合其內容
- 行號數字與文件中有箭頭
  - 出現在第1個字是`#`、`-`、`for`、`if`等區段
  - 滑鼠滑過才會出現
  - 點選箭頭可以開合其內容(不影響預覽)
  - 整段剪下複製：不必害怕滑鼠選取錯誤。
- 開啟檔案總管中的大綱，所有檔案中以井字號(`#` hash tag)的headline都會出現在此。
  - 此處大綱功能與點選文件上之大綱一樣，但編輯文件時不會消失，是常設之視窗，可以用來參考上下文內容。
  - 可以選擇**全部折疊**與否、排序方式、以及是否**追蹤游標**(會在大綱中呈現灰底，以顯示在文章中的相對位置)。
  - 點選箭頭可以開合其內容
  - 直接點選即會移動游標  

### 文件內搜尋、移動、及取代

- ctrl-F：如未有反白文字，會將游標跳到搜尋欄，搜尋反白或附近文字。
  - 按上下鍵尋找前、後1個、或在選取範圍中尋找
  - F3 / Shift F3 也有相同功能
  - 可指定是否認大小寫、適用外卡(wild card)
  - 關鍵字標記（見前[圖11](#編輯窗格)）
    - 文件中（或指定範圍中）所有該項關鍵字都會有橘色底，以顯示其位置。
    - 文件編輯器右側拉桿，會在相對位置出現橘色點(拉桿中央線)。
    - 文件編輯器右側縮圖，也會在關鍵字所在位置出現橘色橫線。
- 按搜尋欄右邊箭頭->取代
  - 可指定逐一或全部取代

## 預覽

- Code有2個預覽畫面
  - 一者在文件編輯器的右側拉桿邊，類似MS Word的縮圖顯示，如[圖11](#編輯窗格)所示。
    - 會呈現文件的段落、文字顏色、以及編輯(版本比較)、尋找、預編譯(錯誤碼位置)等等概略樣貌、以及效果訊息。
    - 功能為提供使用者在文件中快速移動游標。
  - 一者以分割畫面型態，出現在文件編輯器的右側視窗
    - 只適用在md指令的文件檔案，系統將，預覽內容則為編譯後的樣貌。
    - 翻動預覽，文件編輯器也會同步翻動。
  - 二者都可以在**管理**與**設定**(ctrl ,)內更改縮放比例。

### 縮圖顯示

- 和MS Word最大不同之處，Code的縮圖顯示會隨著文件的編輯、大綱的開合而改變。
- 確認游標所在的位置。雖然Code都會提供行號，但是相對其他段落是前還是後，並沒有整體的概念。
  - 縮圖在該行會有呈現灰底線條，
  - 滑鼠滑過縮圖該區域(頁面範圍，會呈現灰底)
  - 在文件中選取某個範圍，縮圖中也會出現灰底藍字。
- 開合文件中的區段，在縮圖中也會同步反映。
- 移動(前往)
  - 滑鼠在縮圖上直擊：去到指定位置
  - 滑鼠在縮圖上拖動：快速、無間隔翻頁效果。

### md檔預覽

- 因md格式之文件內含許多樣式、格式的控制碼，需要有程式進行轉譯，才能顯示出預期發布的結果。
- 會需要使用預覽確認的情況
  1. 表格之編寫
  1. 特殊字形、數學公式
  1. 引述、片段、區段(snippet)
  1. 網址與圖片之連結
  1. 流程圖
- 如果因為文件含有太多引述、或者按照大綱予以閉合，文件和預覽會不同步，可以按預覽右上方**顯示來源**，強迫二者可以同步翻頁。

## 搜尋

- 文件內的搜尋詳[上述](#文件內搜尋取代)。
- 此處說明左側主要提示欄(primary side bar)的尋找功能、以及移至(G)功能。也是Code作為筆記系統的強項之一。
- 此處功能為關鍵字索引的完全版本，亦即全[Repo][repo]、全文的文字，都可以是關鍵字。可以執行快速搜尋、前往、置換等等作業。

### 跨檔案全文搜尋

- 可以指定英文字的大小寫、\*是普通字元或是外卡(用以尋找部分文字)
- 指定搜尋特定目錄或包含特定類型的檔案
  - 在對話框處的\*是一律是外卡
  - 也可以在檔案總管的目錄按右鍵，指定在某個目錄下搜尋或取代。
- 指定排除的檔案
- 點在檔名上：只會收合，不會作用。須點在符合條件的文字上，才會開啟該檔案。如未移動到該列，需再點一下該處。
- 在檔名上按右鍵，可以顯示該檔案在整體目錄中的位置。

### 跨檔案取代

- 筆記系統會需要更新錯誤的內容。如果錯誤出現在很多檔案，要一一尋找修改，那會很痛苦。有了跨檔案取代就不怕了。
- 搜尋窗格左側箭頭下拉會出現取代功能。
- 同樣也可以選擇逐一檢查後取代、或全部取代。

### 搜尋(前往)檔案名稱

- 這個功能隱藏在**移至**(G)->**移至檔案...**，也可以用ctrl-P直接開啟對話框。
- 鍵入關鍵字後系統就會出現符合的檔案名稱(與目錄)，
- 如果是已經開啟的檔案，
  - 關鍵字後再鍵入 `:` 與數字(行號)，即會前往該檔案該位置，
  - 關鍵字後鍵入 `@` 即會出現大綱，再點選要去的位置。

## 程式之執行

### (預)編譯

- [IDE][ide]強項功能之一，就是在撰寫程式時提供程式語言自動填字、以及預先編譯功能，在還沒有執行前，就可以知道錯誤碼會在何處發生、錯誤為何等等訊息，不必真正執行程式。
- 一般會在程式碼下方出現紅色底線、在[縮圖](#縮圖顯示)出現紅色橫條、在文件右惻拉桿的右側出現紅色方塊。

### 執行程式

- 直接按左側執行與偵錯即可。
- 開啟終端機
  - 右上方可開啟。目錄位置為[Repo][repo]下
  - 如需開啟在特定的目錄位置，可以先在檔案總管移動到正確的位置，再按滑鼠右鍵選取「在整合式終端機中開啟」
- window系統為powershell(DOS命令為主)，mac及linux則為bash環境。

### [IDE][ide]的必要性檢討

- 對習慣使用[IDE][ide]來開發程式的人來說，Code算是蠻理想的，算是充份。
- 但就必要性而言，其實就執行程式的角度而言，還是有諸多不順之處：
  1. **多視窗**的必要性：同時開這麼多視窗還蠻干擾思路的，畢竟數據結果和程式碼是不同類物件，不同類如何比較，一起看的必要性不高。寧可做什麼特定的動作來變換整個視窗畫面、也轉換一下心情，而不是同時開啟，分散注意力。
  1. **多工**運作：[IDE][ide]在早期個人電腦或是window不能多工運作的環境，是有其必要性的。如果要測試多個程式，可以一直開啟終端機視窗來運作。但這在工作站似乎就沒有這個必要了，再開啟putty登入就好了。
  1. **滑鼠**倚賴性：對習慣滑鼠作業方式的人來說，越少用到鍵盤是越好，[IDE][ide]提供很多有用的功能、在檔案、大綱之間的流覽跳躍等等。可惜程式設計、報告(程式說明、心得筆記等等)撰寫，目前輸入方式還是以鍵盤為主流，否則[IDE][ide]也不會設計這麼多**按鍵組合**，來避免再用滑鼠造成思路中斷。

## 移至(移動、前往)功能

- 不論是文件或是程式系統，在編輯或執行階段，會需要快速在檔案內、或檔案間移動游標。為此Code提供了專用的下拉選單，可見得其重要性與必要性。
  - 熟悉前往功能對於Code使用，可以說是發揮其軟體精髓到極致。
  - 中文翻做「移至」，實為英文之前往「Go」，此功能延續自vim的[Shift-G](https://kb.iu.edu/d/adxw#:~:text=If%20you're%20already%20in,last%20line%20in%20the%20file.)功能，該功能讓使用者可以在快速的在文件內移動游標。
- 此處將所有關於移動游標的方式、鍵盤或滑鼠操作等予以彙總。  

### 移至(G)下拉選單

| ![goto](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/goto_win.png){:width="360px"}|![goto](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/goto_mac.png){:width="360px"}|
|:--:|:--:|
| <b>圖12(a)window版</b>| <b>圖12(b)mac版</b>|

### 鍵盤

- 詳參前述[重要的移動鍵組合](#重要的移動鍵組合)
- 選單(G)中列出「上一步」及「上次編輯位置」，是有別於編輯的「復原 」。這是在其他編輯軟體不曾出現的功能。讓使用者可以反覆檢討剛剛修正之處。
- 切換編輯器：即為切換已經開啟的文件。
- 切換群組：執行程式時相關程式之群組
- 移至檔案：在已開啟(最近開啟)的文件中移動
- 前往工作區中的符號(symbol)：預設是hashtag，工作區(workplace)即為整個[Repo][repo]，亦即ctrl T將會出現所有檔案、所有以# hashtag為首的內容(按照字母排序)。

### 滑鼠

- 滑鼠的快速移動非常直覺。Code還提供了顏色作為重要標示。
- 文件內移動
  - 右側拉桿上下拖動(同ctrl 上/下、Alt 上頁/下頁)
  - 拉桿之顏色標記
    - 左：文件與雲端備份之比較，綠色方塊表新增、藍色為修訂。git同步後，這些顏色就會消失。
    - 中：搜尋結果之相對位置，會出現橘色方塊。取消搜尋即消失。
    - 右：程式碼錯誤之相對位置，警告為黃色方塊、錯誤為紅色方塊。
  - [縮圖](#縮圖顯示)之上下拖動、(同拉桿拖動)
    - 顏色意義同上。
      - 橘色或紅色為一整行底色
      - 如同時出現時，該行為紅色底
      - 綠色及藍色為左側方塊。
    - 點選處為灰藍色底
  - [預覽](#預覽)
    - 在預覽畫面上雙擊左鍵，就可以跳到該處文字位置進行編輯。
    - 翻動預覽畫面，本文也會隨之翻動，如果本文中含有很多註釋、直接翻動會很煩瑣，因其不在預覽畫面出現，此時翻動預覽畫面會比較快速且明確。
  - 大綱之點選，見前述[大綱開合及移動](#大綱開合及移動)，主要有2處
    - 文件上方之位置提示。
    - 左欄(主要提示欄)檔案總管之「大綱」
- 文件之間的移動
  - 檔案總管[Repo][repo]下按照目錄、檔案名稱點選、開啟檔案
  - ctrl-P、ctrl-T，也可以滾輪點選其他文件的# hashtag，直接跳到該檔案位置。
  - [搜尋](#搜尋)結果中，直接點選搜尋到的文字，即可開啟檔案、跳到該行檢視、更換或編輯。
  - 檔案總管中的「時間表」
    - 除了有最近編輯的檔案、也有個檔案編輯過程的重要里程碑，點入將出現新增或修改之對照，且將游標直接移至該處。
    - 以鍵盤alt-F3也會出現(上次)編輯對照。

## Code的缺點與因應

### 檔案管理

- 一專案開啟一個Code，對跨專案作業來說，會有很大困擾。
  - 這是個限制也是個保護。試想在window的檔案總管，如果要跨檔搜尋特定的一個檔名，也是在某個目錄以下搜尋，如果都是從磁碟機根目錄開始搜尋，那會是一個怎樣的災難。
  - 如果是linux/macOS，用[locate指令](https://officeguide.cc/linux-locate-command-tutorial-examples/)會輕鬆很多。
  - 還好Code的啟動很快、佔用記憶體不多，開個2~3個還不成問題。如果要開啟3個Code才能整併特定的專案，那要先整理的似乎不是檔案了。
  - linux/macOS有好用的unix指令可以跨檔搜尋：`grep --color=auto -ni $1 $(find . -name "*.$2")`

- 找不到「最近編輯的檔案」功能，因為隱藏在**移至**(G)->**移至檔案...**。
  - 如前所述，visual studio系列[IDE][ide]很早的觀念就是以專案為單元，而不是以檔案為單元，進到git系統也是以[Repo][repo]為單元，
  - 所以如果去檔案(F)下拉選單找到的「開啟最近檔案」會是其他專案(檔案)，而不是正編輯[Repo][repo]最近的編輯檔案，需要去到**移至**(G)->**移至檔案...**。
  - 因應這項缺點，
    - ctrl-P直接Goto
    - 使用日期當做檔名的前綴，會是一個不錯的作法。
    - 或者是在跨檔搜尋當中，以日期標籤來尋找，也是一個快速啟動的方式。

### 預覽或提交

- 預覽與提交GitHub Pages(GHP)之後的效果，有些微不同之處，似乎短時間之內也無法合理的解決。
  - 流程圖。GHP處理效率不好、常常會失敗。但預覽是OK的。
  - md檔案如含有js指令，Code也無法辨識執行。

[ide]: <https://zh.wikipedia.org/zh-tw/集成开发环境> "集成开发环境、整合開發環境"
[vsc_wiki]: <https://zh.wikipedia.org/wiki/Visual_Studio_Code> "Visual Studio Code（簡稱 VS Code）是一款由微軟開發且跨平台的免費原始碼編輯器[6]。該軟體支援語法突顯、程式碼自動補全（又稱 IntelliSense）、程式碼重構功能，並且內建了命令列工具和 Git 版本控制系統[7]。使用者可以更改佈景主題和鍵盤捷徑實現個人化設定，也可以透過內建的擴充元件程式商店安裝擴充元件以加強軟體功能。"
[gh]: <https://zh.wikipedia.org/zh-tw/GitHub> "GitHub是一個線上軟體原始碼代管服務平台，使用Git作為版本控制軟體，由開發者Chris Wanstrath、P. J. Hyett和湯姆·普雷斯頓·沃納使用Ruby on Rails編寫而成。在2018年，GitHub被微軟公司收購。GitHub同時提供付費帳戶和免費帳戶。這兩種帳戶都可以建立公開或私有的代碼倉庫，但付費使用者擁有更多功能。根據在2009年的Git使用者調查，GitHub是最流行的Git存取站點。[5]除了允許個人和組織建立和存取保管中的代碼以外，它也提供了一些方便社會化共同軟體開發的功能，即一般人口中的社群功能，包括允許使用者追蹤其他使用者、組織、軟體庫的動態，對軟體代碼的改動和bug提出評論等。GitHub也提供了圖表功能，用於概觀顯示開發者們怎樣在代碼庫上工作以及軟體的開發活躍程度。 "
[gh_dt]: <https://desktop.github.com/> " GitHub Desktop, Focus on what matters instead of fighting with Git. Whether you're new to Git or a seasoned user, GitHub Desktop simplifies your development workflow. "
[git]: <https://backlog.com/git-tutorial/tw/intro/intro1_1.html> "git是一個分散式版本控制軟體，最初由林納斯·托瓦茲創作，於2005年以GPL授權條款釋出。最初目的是為了更好地管理Linux核心開發而設計。應注意的是，這與GNU Interactive Tools不同。 git最初的開發動力來自於BitKeeper和Monotone。"
[repo]: <https://zh.wikipedia.org/wiki/儲存庫> "儲存庫（英語：repository）[1]亦稱倉庫、資源庫、資源庫、版本庫、代碼庫、存放庫，在版本控制系統中是指在磁碟儲存上的資料結構，其中包含了檔案、目錄以及元資料。儲存庫可能為分散式（如Git）或集中式（如Subversion）。[2]分散式的儲存庫可以複製到每個使用者的本地；集中式的儲存庫只能儲存在伺服器上。[3]"
[Docker]: <https://zh.wikipedia.org/zh-tw/Docker> "Docker是一個開放原始碼的開放平臺軟體，用於開發應用、交付（shipping）應用、執行應用。Docker允許使用者將基礎設施（Infrastructure）中的應用單獨分割出來，形成更小的顆粒（容器），從而提高交付軟體的速度。"
