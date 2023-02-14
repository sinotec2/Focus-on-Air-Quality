---
layout: default
title: grep
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2023-02-11 10:12:36
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

##  背景

## grep with color

- activate: `grep --color`, means `grep --color=always` or `grep --color=auto`
- de-activate: `grep --color=never`
- $GREP_COLOR: match words color,see [stackexchange](https://unix.stackexchange.com/questions/705097/default-value-for-the-grep-colors-environment-variable), eg `export GREP_COLORS='ms=01;31:mc=01;31:sl=:cx=:fn=35:ln=32:bn=32:se=36'`

```bash
The GNU grep default colors are defined into grep.c:

/* The color strings used for matched text.
   The user can overwrite them using the deprecated
   environment variable GREP_COLOR or the new GREP_COLORS.  */
static const char *selected_match_color = "01;31";      /* bold red */
static const char *context_match_color  = "01;31";      /* bold red */

/* Other colors.  Defaults look damn good.  */
static const char *filename_color = "35";       /* magenta */
static const char *line_num_color = "32";       /* green */
static const char *byte_num_color = "32";       /* green */
static const char *sep_color      = "36";       /* cyan */
static const char *selected_line_color = "";    /* default color pair */
static const char *context_line_color  = "";    /* default color pair */
```

- examples
  - `grep -b --colour -n foo myfile`

## grep 的邏輯應用[^1]

### Grep OR Operator

1. `grep 'pattern1\|pattern2' filename`
2. `grep -E 'pattern1|pattern2' filename`
3. `egrep 'pattern1|pattern2' filename`
4. `grep -e pattern1 -e pattern2 filename`

### Grep AND

1. `grep -E 'pattern1.*pattern2' filename`
2. `grep -E 'pattern1.*pattern2|pattern2.*pattern1' filename`

### Grep AND using Multiple grep command

- `grep -E 'pattern1' filename | grep -E 'pattern2'`

### Grep NOT

`grep -v 'pattern1' filename`

[^1]: 7 Linux Grep OR, Grep AND, Grep NOT Operator Examples,  by Ramesh Natarajan on October 21, 2011, [thegeekstuff][thegeekstuff]

[thegeekstuff]: https://www.thegeekstuff.com/2011/10/grep-or-and-not-operators/ "7 Linux Grep OR, Grep AND, Grep NOT Operator Examples"