import pyewts

converter = pyewts.pyewts()
print(converter.toUnicode("ba b+ba [a] ba\\u0f0b"))

print(converter.toWylie("བ་བྦཀཱྀ་ཀཱ"))
