# Python EWTS converter

## Description

The goal of this code is to provide a library to convert back and forth between Tibetan Unicode and [EWTS](http://www.thlib.org/reference/transliteration/#!essay=/thl/ewts/). The code is adapted from Java [ewts-converter](https://github.com/buda-base/ewts-converter).

## Installation

This library should appear soon enough on pip.

## Example

See [demo.py](demo.py)

## Changes

See [CHANGELOG.md](CHANGELOG.md).

## License

The Python code is Copyright (C) 2018 Esukhia, provided under [MIT License](LICENSE). See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of authors and contributors.

## Maintainance

Build the source dist:

```
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```
twine upload dist/*
```