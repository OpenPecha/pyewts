import re

# This file is an ACIP to EWTS converter. ACIP is defined by
# https://web.archive.org/web/20080828031427/http://www.asianclassics.org/download/tibetancode/ticode.pdf

def ACIPtoEWTS(s):
    # Things have to be done in the right order:
    # @..., [...] => ignored (comments)
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = re.sub(r"\@[^ ]* *", "", s)
    # (yichung): remove parentheses
    s = s.replace("(", "")
    s = s.replace(")", "")
    #   - /.../  =>  (...)
    s = re.sub(r"\/([^/]*)\/", r"(\1)", s)
    s = s.replace("/", "") # for leftover /
    # simple substitutions
    s = s.replace(";", "|")
    s = s.replace("#", "@##")
    s = s.replace("*", "@#")
    s = s.replace("\\", "?")
    s = s.replace("^", "\\u0f38")
    s = s.replace(",", "/")
    s = s.replace("`", "!")
    s = s.replace("`", "!")
    s = s.replace("V", "W")
    s = s.replace("TS", "TSH")
    s = s.replace("TZ", "TS") 
    # - => .
    # GA-YAS is not the canonical form but is commonly found
    s = re.sub(r"([BCDGHJKLMNPRSTVYZhdtn])A-", r"\1.", s)
    s = s.replace("-", ".")
    #   - i => -I (we will reverse the case later)
    s = re.sub(r"A?i", "-I", s)
    #   - 'i => -i (but 'i was turned into '-I by previous substitution)
    s = re.sub(r"A?'-I", "-i", s)
    #   - o => x (we will reverse the case later)
    #   - % => ~x
    s = s.replace("o", "x")
    s = s.replace("%", "~x")
    #   - non-vowel + apostrophe + vowel (except i) => lower case vowel (idem)
    s = re.sub(r"([BCDGHJKLMNPRSTVYZhdtn])'([AEOUI])", lambda m: m.group(1)+m.group(2).lower(), s)
    # this case is a bit complex, it's correcting the previous line for cases where A is the main letter
    s = re.sub(r"(^|[^BCDGHJKLMNPRSTVYZhdtn])A'([AEOUI])", lambda m: m.group(1)+m.group(2).lower(), s)
    #   - A + vowel => vowel
    s = re.sub(r"A([AEIOUaeiou])", r"\1", s)
    #   - sh => sH
    s = s.replace("sh", "sH")
    #   - inverse case
    s = s.swapcase()
    #   - ee => ai
    #   - oo => au
    s = s.replace("ee", "ai")
    s = s.replace("oo", "au")
    #   - : => H
    s = s.replace(":", "H")
    #   - add pluss?
    return s

def test_assert(orig, expected):
    res = ACIPtoEWTS(orig)
    if res != expected:
        print("error: %s => %s but %s expected" % (orig, res, expected))

def testACIPtoEWTS():
    test_assert("KA(BA)CA()BA[ABC]BA@001A BA", "kabacabababa")
    test_assert("KA/BA/CA//DA/", "ka(ba)ca()da")
    test_assert("A'I", "I")
    test_assert("Ai", "-i")
    test_assert("A'i", "-I")
    test_assert("B'I", "bI")
    test_assert("'I 'OD", "'i 'od")
    test_assert("BA'I", "ba'i")
    test_assert("AI", "i")
    test_assert("A'U", "U")
    test_assert("AA:", "aH")
    test_assert("A'A:", "AH")
    test_assert("G-YAS", "g.yas")
    test_assert("GA-YAS", "g.yas")
    test_assert("ZHVA", "zhwa")
    test_assert("L'i", "l-I")
    test_assert("AEE", "ai")
    test_assert("KEEm", "kaiM")
    test_assert("KshA", "kSha")
    test_assert("TSA TZA", "tsha tsa")
    test_assert("*, ,'PHAGS PA GSER 'OD DAM PA MDO SDE DBANG PO'I BSDUS PA BSHUGS SO, ,", "@#/ /'phags pa gser 'od dam pa mdo sde dbang po'i bsdus pa bshugs so/ /")

if __name__ == "__main__":
    testACIPtoEWTS()