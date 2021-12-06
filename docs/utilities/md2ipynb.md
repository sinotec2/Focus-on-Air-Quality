---
layout: default
title: md2ipynb
parent: Utilities
---

# Markdown轉Jupyter筆記
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

雖然Jupyter提供了轉換MyST格式的[小工具](https://jupyterbook.org/file-types/myst-notebooks.html)，但對大多數的markdown並不能適用。
此處記錄簡易的轉檔歷程，以簡單的sed指令進行，有需要的讀者也許可以參考一下。

## 基本定義

### Markdown
- 此處以`jtd`內設版面為例，包含：
  - **jekyll**表頭([front matter](https://jekyllrb.com/docs/front-matter/))、內容表(`{:toc}`)、程式碼區段等。
- 包括程式碼編號

### ipynb
基本上ipynb檔案是個dict，可以用json來解讀(假設為變數`js`)，其架構如下：
- 第1層：共有4項物件`[i for i in js]=['cells', 'metadata', 'nbformat', 'nbformat_minor']`，主要各命令列的內容放在'cells'，另外說明，其餘3項分別核心及格式編號：
  - 'metadata'為python核心相關說明(dict)：{
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
  - nbformat'：為格式編號(整數4)
  - nbformat_minor：為次格式編號(整數5)

-命令列內容'cells'：每行命令列(md、code)各有4、6個內容，
  - markdown命令列項目：['cell_type', 'id', 'metadata', 'source']
    - `[i for i in js['cells'][0]]`=`['cell_type', 'id', 'metadata', 'source']`
    - cell_type：值為`markdown`(string)
    - id：為每行不一樣的8位亂碼(0~9、a~Z)(string length 8)
    - metadata：{}(dict)
    - source:為說內容之序列，項目為行，以`'\n'`跳行(list of strings)
  - code命令列項目：除了前述之外，外加輸出結果及執行序`['cell_type', 'execution_count', 'id', 'metadata', 'outputs', 'source']`
    - execution_count：將會顯示在jpyter-notebook上的序號(int)
    - outputs：如有標準輸出，則會出現在此(dict)。其下也有"data"、再下層為"text/plain"(list of strings)等內容。

