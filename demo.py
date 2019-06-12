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

print(converter.toWylie("རིགས"))

print(converter.toWylie("བའམ"))

print(converter.toWylie("In Chinese"))

warns = []
orig = "snga 'phros a ri gzhung dang rgya gar gzhung so sor gsang ba'i thog nas nang don mthun lam chen po zhig nges par tu thugs zab  thog/"

print(converter.toUnicode(orig, warns))
print(warns)