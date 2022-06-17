---
layout: default
title: md2ipynb
parent: Markdown
grand_parent: Utilities
last_modified_date: 2022-06-17 10:21:23
---

# Markdown轉Jupyter筆記檔
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

雖然Jupyter提供了轉換MyST格式的[小工具](https://jupyterbook.org/file-types/myst-notebooks.html)，但對大多數的markdown並不能適用。
此處記錄簡易的轉檔歷程，以簡單[python程式](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Markdown/md2ipynb.py)下進行，有需要的讀者也許可以參考一下。

## 基本格式定義

### Markdown
- 此處以`jtd`內設版面為例，包含：
  - **jekyll**表頭([front matter](https://jekyllrb.com/docs/front-matter/))、內容表(`{:toc}`)、程式碼區段等。
  - 因每個表頭可能有差異，程式未設計偵測去除這一段，不影響jupyter的執行。
- 包括程式碼編號：在jupyter無法執行，必須去除

### ipynb
基本上`ipynb`檔案是個`dict`，可以用`json`來解讀(假設為變數`js`)，其架構如下：
- 第1層：共有4項物件`[i for i in js]=['cells', 'metadata', 'nbformat', 'nbformat_minor']`，主要各命令列的內容放在'cells'，另外說明，其餘3項分別核心及格式編號：
  - 'metadata'為python核心相關說明(`dict`)：

  ```python
  {
  'kernelspec': {'display_name': 'Python 3 (ipykernel)',
  'language': 'python',
  'name': 'python3'},
 'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3},
  'file_extension': '.py',
  'mimetype': 'text/x-python',
  'name': 'python',
  'nbconvert_exporter': 'python',
  'pygments_lexer': 'ipython3',
  'version': '3.9.7'}}
  ```
  - nbformat'：為格式編號(整數4)
  - nbformat_minor：為次格式編號(整數5)
- 命令列內容`cells`是個dict，每行命令列(md、code)各有4、6個內容，
  - markdown命令列項目：`['cell_type', 'id', 'metadata', 'source']`
    - `[i for i in js['cells'][0]]`=`['cell_type', 'id', 'metadata', 'source']`
    - cell_type：值為`markdown`(string)
    - id：為每行不一樣的8位亂碼(0~9、a~Z)(string length 8)
    - metadata：{}(dict)
    - source:為說內容之序列，項目為行，以`'\n'`跳行(list of strings)
  - code命令列項目：除了前述之外，外加輸出結果及執行序`['cell_type', 'execution_count', 'id', 'metadata', 'outputs', 'source']`
    - execution_count：將會顯示在jpyter-notebook上的序號(int)
    - outputs：如有標準輸出，則會出現在此(dict)。其下也有"data"、再下層為"text/plain"(list of strings)等內容。

## 程式說明
基本上ipynb是以命令列的程式碼為主軸，其間、前、後的文字則為markdown格式的說明。在markdown的程式碼有quotation框住，因此只要辨識quotation的位置，即可區隔各命令列的內容，將其存成codes序列，而其間、前、後，則存成marks序列的內容，另存新檔即可。分段說明如下，程式碼可自[github](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Markdown/md2ipynb.py)下載。

### 分段說明
- 輸入`md`檔案名稱，並準備輸出檔名
  - `md`檔內容含有跳行指令(`\n`)，不可將其去掉(`strip()`)
  - 結果檔的主檔名稱將與輸入檔的主檔名一致，附加檔名為`ipynb`，以利`jupyter-notebook`或其他軟體直接開啟。

```python
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n md2ipynb.py
     1  import numpy as np
     2  import sys, json
     3
     4  fname=sys.argv[1]
     5  fnameO=fname.replace('md','ipynb')
     6  with open(fname,'r') as f:
     7    l=[i for i in f]
     8  nln=len(l)
```
- 去除行數編號
  - 此處編號是由`cat`指令產生的，為6碼整數，其後還空2格。

```python

     9  for n in range(nln):
    10    for b in ['{:6d}  ','{:6d} \n','{:6d}\n']:
    11      s=b.format(n)
    12      for m in range(nln):
    13        if s in l[m]:l[m]=l[m].replace(s,'')
```
- `idx`為quotation所在的行數標籤。此處嘗試過以np.where來辨識，因為是文字辨識，其實還是在序列中一一確認比較妥當。
  - `idx`必須成對存在，如果不是，必須放棄重來。

```python
    14  idx=[i for i in range(len(l)) if l[i][:3]=='```']
    15  ncells=len(idx)//2
    16  if len(idx)%2 !=0 : sys.exit('wrong pair in code quotations')
    17
```
- `codes`及`marks`2個序列的起迄行數標籤
  - `codes`必須規避quotation起始行(\`\`\`python)，因此行數要加**1**。
  - `marks`則必須規避quotation結束行(\`\`\`)，因此行數也要加**1**。
    - 含有quotation的`ipynb`說明，jupyter是不會執行的，**一定**要予以去除。
  - 如果有結尾的說明，`marks`序列的長度會比`codes`多一項

```python
    18  beg,end=[idx[i*2]+1 for i in range(ncells)], [idx[i*2+1] for i in range(ncells)]
    19  mbeg,mend=[0],[beg[0]-1]
    20  mbeg+=[i+1 for i in end[0:]]
    21  mend+=beg[1:]
    22  nmarks=ncells
    23  if end[-1]<nln:
    24    nmarks+=1
    25    mend+=[nln]
```
- 定義最終成果`dict`為`ipynb`
  - 如果`ipynb`的格式、kernel的版本有異，要在此處修改
  - 此一模版由`jupyter-notebook 6.4.6`存檔取得，python版本為**3.9.7**

```python
    26  ipynb={
    27  'cells':{},
    28  'nbformat':4,
    29  'nbformat_minor':5,
    30  'metadata':{
    31    'kernelspec':{
    32          'display_name': 'Python 3 (ipykernel)',
    33          'language': 'python',
    34          'name': 'python3',
    35          },
    36    'language_info': {
    37          'codemirror_mode': {'name': 'ipython', 'version': 3},
    38          'file_extension': '.py',
    39          'mimetype': 'text/x-python',
    40          'name': 'python',
    41          'nbconvert_exporter': 'python',
    42          'pygments_lexer': 'ipython3',
    43          'version': '3.9.7'
    44          }
    45    }
    46  }
```
- 形成`codes`序列
  - 按照每個程式碼區段的行號(`beg`、`end`)依序產生序列即可，最後再與`marks`序列交叉合併
  - `codes`的內容有**6**項

```python
    47  #code lines
    48  codes=[{
    49          'cell_type': 'code',
    50          'execution_count': i+1,
    51          'id': '{:08d}'.format(i*2+1),
    52          'metadata': {},
    53          'outputs': [],
    54          'source': l[beg[i]:end[i]],
    55          } for i in range(ncells)]
```
- 形成`marks`序列
  - 按照每個說明區段的行號(`mbeg`、`mend`)依序產生序列即可，再與前述`codes`序列交叉合併
  - `marks`的內容有**4**項

```python
    56  #mark lines
    57  marks=[{
    58     "cell_type": "markdown",
    59     "id": '{:08d}'.format(i*2),
    60     "metadata": {},
    61     "source": l[mbeg[i]:mend[i]],
    62          } for i in range(nmarks)]
```
- 交叉合併。如有最後段的說明，再累加到最後即可。

```python
    63  mix=[]
    64  for i in range(ncells):
    65    mix+=[marks[i],codes[i]]
    66  if nmarks>ncells:
    67    mix+=[marks[-1]]
```
- 輸出

```python
    68  ipynb['cells']=mix
    69  with open(fnameO,'w', newline='') as jsonfile:
    70    json.dump(ipynb, jsonfile)
    71
    72  sys.exit()
```

### 程式下載
- 程式碼可自[github](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Markdown/md2ipynb.py)下載。