---
layout: default
title: math in Jekyll
parent: Markdown
grand_parent: Utilities
last_modified_date: 2022-06-17 10:21:23
---

# math in Jakyll
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
### _config.yml
- adding ...

```
kramdown:
  syntax_highlighter_opts:
    block:
      line_numbers: false
```

### layout html
- in C:\Users\4139\Documents\Focus-on-Air-Quality\_includes\head.html (included by default.html)
- before </head> adding...

```html
  <!-- Mathjax Support -->
  <script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
  </script>
```
### edit on line
- [overleaf][overleaf]
### pandoc
- `pandoc -o TARGET.FMT sourcefile`
  - FMT=docx for ms Word file
  - FMT=tex for LaText file
- math display mode in ms Word, english text form may be disturbed
  -   
## reference
- 李宇琨的博客, [Write LaTeX Equations in Jekyll Using MathJax & Kramdown](https://lyk6756.github.io/2016/11/25/write_latex_equations.html), Nov 25, 2016
- 玉樹芝蘭，[如何用Markdown寫論文？](https://kknews.cc/zh-tw/education/rpgy9vv.html)，2017-12-04
- Zhelin Chen, [How to Convert from Latex to MS Word with ‘Pandoc’](https://medium.com/@zhelinchen91/how-to-convert-from-latex-to-ms-word-with-pandoc-f2045a762293)

[overleaf]: <https://www.overleaf.com/user/subscription/plans> "Overleaf is the world’s easiest to use LaTeX editor. Stay up to date with your collaborators, keep track of all changes to your work, and use our LaTeX environment from anywhere in the world."