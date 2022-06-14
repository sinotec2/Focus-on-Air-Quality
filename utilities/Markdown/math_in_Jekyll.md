---
layout: default
title: math in Jekyll
parent: Utilities
permalink: /utilities/Markdown/
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
## reference
- 李宇琨的博客, [Write LaTeX Equations in Jekyll Using MathJax & Kramdown](https://lyk6756.github.io/2016/11/25/write_latex_equations.html), Nov 25, 2016