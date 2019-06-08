import pyewts

converter = pyewts.pyewts()
#print(converter.toUnicode("ba b+ba [a] ba\\u0f0b"))

orig = "ba b+ba [a] ba\\u0f0b"
print(orig)
warns = []
res = converter.toUnicode(orig, warns)
print(res)
print(warns)

print(converter.toWylie("བ་བྦཀཱྀ་ཀཱ"))

print(converter.toWylie("རབ་ཏུ་འབྱུང་བའི་གཞི་རྫོགས་སྷོ"))

print(converter.toWylie("In Chinese"))

