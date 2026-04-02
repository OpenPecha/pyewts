<h1 align="center">
  <br>
  <a href="https://buddhistai.tools/"><img src="https://raw.githubusercontent.com/WeBuddhist/visual-assets/refs/heads/main/logo/WB-logo-purple.png" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<h1 align="center">pyewts</h1>

<p align="center">
  |Python| |MIT|
</p>

Tibetan Unicode to Wylie converter (EWTS-Extended Wylie Transliteration Scheme)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#contributing)
- [How to get help](#how-to-get-help)
- [Terms of use](#terms-of-use)

## Features

- Convert Tibetan Unicode to Wylie transliteration
- Support for Extended Wylie Transliteration Scheme (EWTS)
- Bidirectional conversion (Unicode ↔ Wylie)
- Python library with simple API

## Prerequisites

- Python 3.7+

## Installation

```bash
pip install pyewts
```

Or from source:

```bash
git clone https://github.com/OpenPecha/pyewts.git
cd pyewts
pip install -e .
```

## Usage

```python
import pyewts

converter = pyewts.Pyewts()

# Unicode to Wylie
wylie = converter.toWylie("བོད་ཡིག")
print(wylie)  # bod.yig

# Wylie to Unicode
unicode_text = converter.toUnicode("bod.yig")
print(unicode_text)  # བོད་ཡིག
```

## How to get help
* File an issue.
* Join our [discord](https://discord.com/invite/7GFpPFSTeA).

## Terms of use
pyewts is licensed under the [MIT License](/LICENSE).