# pyewts

Tibetan Unicode to Wylie converter (EWTS-Extended Wylie Transliteration Scheme)

## Language

Python

## Description

The goal of this code is to provide a library to convert back and forth between Tibetan Unicode and [EWTS](http://www.thlib.org/reference/transliteration/#!essay=/thl/ewts/). The code is adapted from Java ewts-converter. It also provides a conversion from the ACIP Transliteration to EWTS.

## Installation

```bash
pip install pyewts
```

## Usage

```python
import pyewts
converter = pyewts.pyewts()
print(converter.toUnicode("ba b+ba [a] ba\u0f0b"))
# བ་བྦ་a་བ་

print(converter.toWylie("༼༽"))
# ()
```

## License

MIT License

## How to get help

- Open an issue at https://github.com/OpenPecha/pyewts/issues
- Check existing issues for solutions

## Terms of use

This project is part of OpenPecha. See https://openpecha.org for terms of use.