# Python Tibetan Wylie (EWTS) converter

## Description

The goal of this code is to provide a library to convert back and forth between Tibetan Unicode and [EWTS](http://www.thlib.org/reference/transliteration/#!essay=/thl/ewts/). The code is adapted from Java [ewts-converter](https://github.com/buda-base/ewts-converter).

## Installation

```bash
pip install pyewts
```

## Example

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
