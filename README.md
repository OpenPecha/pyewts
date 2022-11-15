<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<h3 align="center">Python Tibetan Unicode to Wylie (EWTS) Converter</h3>

<!-- Replace the title of the repository -->


<p align="center">
  <a href="#description">Description</a> •
  <a href="#Installation">Installation</a> •
  <a href="#Examples">Examples</a> •
  <a href="#Changes">Changes</a> •
  <a href="#License">License</a> •
  <a href="#Maintenance">Maintenance</a> •
  <a href="#owner">Owner</a>
</p>
<hr>

## Description

The goal of this code is to provide a library to convert back and forth between Tibetan Unicode and [EWTS](http://www.thlib.org/reference/transliteration/#!essay=/thl/ewts/). The code is adapted from Java [ewts-converter](https://github.com/buda-base/ewts-converter).

It also provides a conversion from the [ACIP Transliteration](https://web.archive.org/web/20080828031427/http://www.asianclassics.org/download/tibetancode/ticode.pdf) to EWTS.

<!-- This section provides a high-level overview for the repo -->


## Installation

```bash
pip install pyewts
```

## Examples

Convert Wylie to Unicode

```python
import pyewts

converter = pyewts.pyewts()
print(converter.toUnicode("ba b+ba [a] ba\\u0f0b"))
# བ་བྦ་a་བ་
```

Convert Unicode to Wylie

```python
print(converter.toWylie("༼༽"))
# ()
```

Catch Wylie warnings

```python
>>> orig = """dangs
... zhwa
... dwang
... rma
... tshe
... phywa
... dge
... rgya
... dwags
... (rtse mgron)"""
>>> 
>>> print(orig)
dangs
zhwa
dwang
rma
tshe
phywa
dge
rgya
dwags
(rtse mgron)
>>> warns = []
>>> res = converter.toUnicode(orig, warns)
>>> print(res)
དངས
ཞྭ
དྭང
རྨ
ཚེ
ཕྱྭ
དགེ
རྒྱ
དྭགས
༼རྩེ་མགྲོན༽
>>> print(warns)
['line 1: "dangs": Syllable should probably be "dngas".']
```

See [demo.py](demo.py)

## Changes

See [CHANGELOG.md](CHANGELOG.md).

## License

The Python code is Copyright (C) 2018 Esukhia, provided under [MIT License](LICENSE). See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of authors and contributors.

## Maintenance

Build the source dist:

```
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```
twine upload dist/*
```

## Owner

- [@eroux](https://github.com/eroux)

<!-- This section lists the owners of the repo -->
