import re

# This file is an ACIP to EWTS converter. ACIP is defined by
# https://web.archive.org/web/20080828031427/http://www.asianclassics.org/download/tibetancode/ticode.pdf

def ACIPtoEWTS(s):
    #s = s.strip(" \n")
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
    s = re.sub(r'\*+', lambda m: '@' + '#' * (len(m.group(0))), s)
    s = s.replace("\\", "?")
    # the case will change
    s = s.replace("^", "\\U0F38") # this is also sometimes encoded as 7
    s = s.replace(",", "/")
    s = s.replace("`", "!")
    s = s.replace("`", "!")
    s = s.replace("V", "W")
    s = s.replace("TS", "TSH")
    s = s.replace("TZ", "TS") 
    # - => .
    # GA-YAS is not the canonical form but is commonly found
    s = re.sub(r"([BCDGHJKLMN'PRSTWYZhdtn])A-", r"\1.", s)
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
    s = re.sub(r"([BCDGHJKLMNPRSTWYZ'hdtn])'([AEOUI])", lambda m: m.group(1)+m.group(2).lower(), s)
    # this case is a bit complex, it's correcting the previous line for cases where A is the main letter
    s = re.sub(r"(^|[^BCDGHJKLMNPR'STWYZhdtn])A'([AEOUI])", lambda m: m.group(1)+m.group(2).lower(), s)
    #   - A + vowel => vowel
    s = re.sub(r"A([AEIOUaeiou])", r"\1", s)
    #   - sh => sH
    s = s.replace("sh", "sH")
    # normalize apostrophes
    s = re.sub(r"[’ʼʹ‘ʾ]", "'", s)
    #   - inverse case
    s = s.swapcase()
    #   - ee => ai
    #   - oo => au
    s = s.replace("ee", "ai")
    s = s.replace("oo", "au")
    #   - : => H
    s = s.replace(":", "H")
    s = add_plus(s)
    s = normalize_spaces(s)
    return s

def normalize_spaces(s):
    """
    in ACIP transliteration, space can mean tsheg or space, we make a guess in this function
    """
    s = re.sub(r"([aeiouIAEU]g|[gk][aeiouAEIU]|[;!/|]) +([;!/|])", lambda m: m.group(1)+"_"+m.group(2), s)
    s = re.sub(r"([;!/|H]) +", lambda m: m.group(1)+"_", s)
    return s

def EWTStoACIPContent(s):
    # Things have to be done in the right order:
    # remove square brackets (used in EWTS for non-Tibetan, no equivalent in ACIP?)
    # but do not by default not to break ACIP comments
    #s = s.replace("[", "")
    #s = s.replace("]", "")
    # normalize apostrophes
    s = re.sub(r"[’ʼʹ‘ʾ]", "'", s)
    #   - (...) => /.../ 
    s = re.sub(r"\(([^/]*)\)", r"\/\1\/", s)
    # simple substitutions
    s = s.replace("|", ";")
    s = re.sub(r"(^|\[)\*", lambda m: m.group(1), s) # remove * not after [
    s = s.replace("@##", "ZZ")
    s = s.replace("@#", "*")
    s = s.replace("_", " ") # no space in ACIP
    # s = s.replace("@", "") # when not followed by #, we assume @ is the ACIP @
    s = re.sub(r"(^|\[)#", lambda m: m.group(1), s) # remove # not after [
    s = s.replace("ZZ", "#")
    s = s.replace("?", "\\")
    # the case will change
    s = re.sub(r"\\U0F38", "^", s, flags=re.I)
    s = s.replace("/", ",")
    s = s.replace("!", "`")
    s = s.replace("w", "v")
    s = s.replace("tsh", "ZZZ")
    s = s.replace("ts", "tz")
    s = s.replace("ZZZ", "ts")
    #   - % => ~x
    s = s.replace("~X", "%")
    #   - H => :
    s = s.replace("H", ":")
    #   + is ok in ACIP even if it's not recommended. It is mandatory in some cases
    #   like d+m, n+y, t+s
    #   - inverse case
    s = s.swapcase()
    # the i... case is swapped at this point
    s = s.replace("-I", "w") # -> i (later)
    s = s.replace("-i", "q") # -> 'i (later)
    # . => -
    s = s.replace(".", "-")
    #   - ai => EE
    #   - au => OO
    s = s.replace("AI", "EE")
    s = s.replace("AU", "OO")
    # add A for ཨ
    s = re.sub(r"(^|[^BCDGHJKLMNPR'STVYZhdtnEO])([AEOUIqaewiou])", lambda m: m.group(1)+"A"+m.group(2), s)
    s = s.replace("a", "'A")
    s = s.replace("u", "'U")
    s = s.replace("o", "'O")
    s = s.replace("e", "'E")
    s = s.replace("i", "'I")
    s = s.replace("q", "'i")
    s = s.replace("w", "i")
    #   - X => o
    s = s.replace("x", "o")
    #   - Sh => sh
    s = s.replace("sH", "sh")
    return s

# standard Tibetan roots (what's before the vowel), with an adjustment: all can take r, y or w or any combination at the end
STD_TIB_PATTERN = re.compile(r"([bcdgjklm'npstzhSDTN]|bgl|dm|sm|sn|kl|dk|bk|bkl|rk|lk|sk|brk|bsk|kh|mkh|'kh|gl|dg|bg|mg|'g|rg|lg|sg|brg|bsg|ng|dng|mng|rng|lng|sng|brng|bsng|gc|bc|lc|ch|mch|'ch|mj|'j|rj|lj|brj|ny|gny|mny|rny|sny|brny|bsny|gt|bt|rt|lt|st|brt|blt|bst|th|mth|'th|gd|bd|md|'d|rd|ld|sd|brd|bld|bsd|gn|mn|rn|brn|bsn|dp|lp|sp|ph|'ph|bl|db|'b|rb|lb|sb|rm|ts|gts|bts|rts|sts|brts|bsts|tsh|mtsh|'tsh|dz|mdz|'dz|rdz|brdz|zh|gzh|bzh|zl|gz|bz|bzl|rl|brl|sh|gsh|bsh|sl|gs|bs|bsl|lh)[rwy]*")

STD_TIB_STACKS_PREFIX = [
    "bg",
    "dm",
    "dk",
    "bk",
    "brk",
    "bsk",
    "mkh",
    "'kh",
    "dg",
    "bg",
    "mg",
    "'g",
    "brg",
    "bsg",
    "dng",
    "mng",
    "brng",
    "bsng",
    "gc",
    "bc",
    "ch",
    "mch",
    "'ch",
    "mj",
    "'j",
    "brj",
    "gny",
    "mny",
    "brny",
    "bsny",
    "gt",
    "bt",
    "brt",
    "blt",
    "bst",
    "mth",
    "'th",
    "gd",
    "bd",
    "md",
    "'d",
    "brd",
    "bld",
    "bsd",
    "gn",
    "mn",
    "brn",
    "bsn",
    "dp",
    "ph",
    "'ph",
    "bl",
    "db",
    "'b",
    "gts",
    "bts",
    "brts",
    "bsts",
    "tsh",
    "mtsh",
    "'tsh",
    "mdz",
    "'dz",
    "brdz",
    "gzh",
    "bzh",
    "gz",
    "bz",
    "bzl",
    "brl",
    "gsh",
    "bsh",
    "gs",
    "bs",
    "bsl"
]

CONSONNANTS_PATTERN = re.compile(r"([bcdgjklm'nprstwyzhSDTN]+)([aeiouAEIOU.-])") # we only check the consonnants before a vowel

def tokenize_consonnants(s):
    # Define multi-character tokens
    multi_char_tokens = ["zh", "ny", "dz", "ts", "tsh", "ch", "ph", "th", "sh", "Sh", "kh", "ng"]
    # Sort by length (longest first) to ensure maximal matching
    multi_char_tokens.sort(key=len, reverse=True)
    
    # Define all valid single characters
    single_chars = "NDTRYWbcdghjklmnprstwyz'"
    
    result = []
    i = 0
    while i < len(s):
        # Try to match multi-character tokens first
        matched = False
        for token in multi_char_tokens:
            if s[i:].startswith(token):
                result.append(token)
                i += len(token)
                matched = True
                break
        
        # If no multi-character token matched, try to match a single character
        if not matched:
            if i < len(s) and s[i] in single_chars:
                result.append(s[i])
            i += 1
    
    return result

STD_TIB_STACKS_PREFIX_TOKENS = []
for s in STD_TIB_STACKS_PREFIX:
    STD_TIB_STACKS_PREFIX_TOKENS.append(tokenize_consonnants(s))

def add_plus_to_consonnants(c):
    if STD_TIB_PATTERN.fullmatch(c):
        return c
    # less common case, for Sanskrit, we have to add the +
    c_tokens = tokenize_consonnants(c)
    # if we have a full match in STD_TIB_STACKS_PREFIX_TOKENS, we only add + after the first token
    # because we consider the first letter is a prefix
    if len(c_tokens) == 1:
        return c
    if c_tokens[:2] in STD_TIB_STACKS_PREFIX_TOKENS or c_tokens[:2] in STD_TIB_STACKS_PREFIX_TOKENS:
        return c_tokens[0]+"+".join(c_tokens[1:])
    return "+".join(c_tokens)

def add_plus(src):
    # for all matches of bcdgjklm'nprstvyzhSDTN
    return CONSONNANTS_PATTERN.sub(lambda x: add_plus_to_consonnants(x.group(1))+x.group(2), src)


def test_assert(orig, expected, aciptoewts=True):
    res = ACIPtoEWTS(orig) if aciptoewts else EWTStoACIPContent(orig)
    if res != expected:
        print("error: %s => %s but %s expected" % (orig, res, expected))

def testACIPtoEWTS():
    test_assert("KA(BA)CA()BA[ABC]BA@001A BA", "kabacabababa")
    test_assert("KA/BA/CA//DA/", "ka(ba)ca()da")
    test_assert("A'I", "I")
    test_assert("^", "\\u0f38")
    test_assert("Ai", "-i")
    test_assert("A'i", "-I")
    test_assert("B'I", "bI")
    test_assert("'I ’OD", "'i 'od")
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
    test_assert("DRA", "dra")
    test_assert("PAndI", "paN+Di")
    test_assert("PAn+dI T+SA", "paN+Di t+sa")
    test_assert("BSGRUBS", "bsgrubs")
    test_assert("BSGRVUBS", "bsgrwubs")
    test_assert("KHAMS", "khams")
    test_assert("ARTHA", "ar+tha")
    test_assert("DHA KshA", "d+ha k+Sha")
    test_assert("TSA TZA", "tsha tsa")
    test_assert("SV'A", "swA")
    test_assert("TZTSA", "ts+tsha")
    # PH'O TH'O SHAN ZHES YUL GYI 'PHAGS PA SPYAN RAS GZIGS DAN , 
    test_assert("*, ,'PHAGS PA GSER 'OD DAM PA MDO SDE DBANG PO'I BSDUS PA BSHUGS SO, ,", "@#/_/'phags pa gser 'od dam pa mdo sde dbang po'i bsdus pa bshugs so/_/")

def testEWTStoACIP():
    test_assert("I", "A'I", False)
    test_assert("\\u0f38", "^", False)
    test_assert("-i", "Ai", False)
    test_assert("-I", "A'i", False)
    test_assert("bI", "B'I", False)
    test_assert("'i ’od", "'I 'OD", False)
    test_assert("ba'i", "BA'I", False)
    test_assert("i", "AI", False)
    test_assert("U", "A'U", False)
    test_assert("aH", "AA:", False)
    test_assert("AH", "A'A:", False)
    test_assert("g.yas", "G-YAS", False)
    test_assert("ga.yas", "GA-YAS", False)
    test_assert("zhwa", "ZHVA", False)
    test_assert("l-I", "L'i", False)
    test_assert("ai", "AEE", False)
    test_assert("kaiM", "KEEm", False)
    test_assert("dra", "DRA", False)
    test_assert("paN+Di", "PAn+dI", False)
    test_assert("paN+Di t+sa", "PAn+dI T+SA", False)
    test_assert("bsgrubs", "BSGRUBS", False)
    test_assert("bsgrwubs", "BSGRVUBS", False)
    test_assert("khams", "KHAMS", False)
    test_assert("ar+tha", "AAR+THA", False)
    test_assert("d+ha k+Sha", "D+HA K+shA", False)
    test_assert("tsha tsa", "TSA TZA", False)
    # PH'O TH'O SHAN ZHES YUL GYI 'PHAGS PA SPYAN RAS GZIGS DAN , 
    test_assert("@#/ /'phags pa gser 'od dam pa mdo sde dbang po'i bsdus pa bshugs so/_/", "*, ,'PHAGS PA GSER 'OD DAM PA MDO SDE DBANG PO'I BSDUS PA BSHUGS SO, ,", False)


if __name__ == "__main__":
    testACIPtoEWTS()
    testEWTStoACIP()