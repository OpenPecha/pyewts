import pyewts

converter = pyewts.pyewts()
print(converter.toUnicode("ba b+ba"))

print(converter.toWylie("བ་བྦ"))
