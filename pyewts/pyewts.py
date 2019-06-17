import re

# 
#  * Copyright (C) 2010 Roger Espel Llima
#  * Copyright (c) 2011-2017 Buddhist Digital Resource Center (BDRC)
#  * 
#  * If this file is a derivation of another work the license header will appear below; 
#  * otherwise, this work is licensed under the Apache License, Version 2.0 
#  * (the "License"); you may not use this file except in compliance with the License.
#  * 
#  * You may obtain a copy of the License at
#  * 
#  *    http://www.apache.org/licenses/LICENSE-2.0
#  * 
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * 
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
class pyewts(object):
    #  various options for Converter conversion
    check = bool()
    check_strict = bool()
    print_warnings = bool()
    fix_spacing = bool()

    #  constant hashes and sets to help with the conversion
    m_subjoined = None
    m_vowel = None
    m_final_uni = None
    m_final_class = None
    m_other = None
    m_ambiguous_wylie = None
    m_tib_vowel_long = None
    m_tib_caret = None
    m_tib_top = None
    m_tib_subjoined = None
    m_tib_vowel = None
    m_tib_final_wylie = None
    m_tib_final_class = None
    m_tib_other = None
    m_ambiguous_key = None
    m_tokens_start = None
    m_special = None
    m_suffixes = None
    m_tib_stacks = None
    m_tokens = None
    m_affixedsuff2 = None
    m_superscripts = None
    m_subscripts = None
    m_prefixes = None
    m_suff2 = None
    repls = []

    class Mode:
        WYLIE = u'WYLIE'
        EWTS = u'EWTS'
        DWTS = u'DWTS'
        DTS = u'DTS'
        ALALC = u'ALALC'
        ACIP = u'ACIP'

    class State:
        PREFIX = u'PREFIX'
        MAIN = u'MAIN'
        SUFF1 = u'SUFF1'
        SUFF2 = u'SUFF2'
        NONE = u'NONE'

    mode = Mode.EWTS

    class WylieStack(object):
        uni_string = None
        tokens_used = int()
        single_consonant = None
        single_cons_a = None
        warns = None
        visarga = bool()
        def __str__(self):
            return "uni_string: %s tokens_used: %d single_consonant %s single_cons_a %s" % (self.uni_string, self.tokens_used, self.single_consonant, self.single_cons_a)

    class WylieTsekbar(object):
        uni_string = None
        tokens_used = int()
        warns = None

    #  EWTS by default
    #  initialize all the hashes with the correspondences between Converter and Unicode.  
    #  this gets called from a 'static section' to initialize the hashes the moment the
    #  class gets loaded.

    m_consonant = {
        "k": "\u0f40",
        "kh": "\u0f41",
        "g": "\u0f42",
        "gh": "\u0f42\u0fb7",
        "g+h": "\u0f42\u0fb7",
        "ng": "\u0f44",
        "c": "\u0f45",
        "ch": "\u0f46",
        "j": "\u0f47",
        "ny": "\u0f49",
        "T": "\u0f4a",
        "-t": "\u0f4a",
        "Th": "\u0f4b",
        "-th": "\u0f4b",
        "D": "\u0f4c",
        "-d": "\u0f4c",
        "Dh": "\u0f4c\u0fb7",
        "D+h": "\u0f4c\u0fb7",
        "-dh": "\u0f4c\u0fb7",
        "-d+h": "\u0f4c\u0fb7",
        "N": "\u0f4e",
        "-n": "\u0f4e",
        "t": "\u0f4f",
        "th": "\u0f50",
        "d": "\u0f51",
        "dh": "\u0f51\u0fb7",
        "d+h": "\u0f51\u0fb7",
        "n": "\u0f53",
        "p": "\u0f54",
        "ph": "\u0f55",
        "b": "\u0f56",
        "bh": "\u0f56\u0fb7",
        "b+h": "\u0f56\u0fb7",
        "m": "\u0f58",
        "ts": "\u0f59",
        "tsh": "\u0f5a",
        "dz": "\u0f5b",
        "dzh": "\u0f5b\u0fb7",
        "dz+h": "\u0f5b\u0fb7",
        "w": "\u0f5d",
        "zh": "\u0f5e",
        "z": "\u0f5f",
        "'": "\u0f60",
        "y": "\u0f61",
        "r": "\u0f62",
        "l": "\u0f63",
        "sh": "\u0f64",
        "Sh": "\u0f65",
        "-sh": "\u0f65",
        "s": "\u0f66",
        "h": "\u0f67",
        "W": "\u0f5d",
        "Y": "\u0f61",
        "R": "\u0f6a",
        "f": "\u0f55\u0f39",
        "v": "\u0f56\u0f39"
        }
    m_subjoined = {
        "k": "\u0f90",
        "kh": "\u0f91",
        "g": "\u0f92",
        "gh": "\u0f92\u0fb7",
        "g+h": "\u0f92\u0fb7",
        "ng": "\u0f94",
        "c": "\u0f95",
        "ch": "\u0f96",
        "j": "\u0f97",
        "ny": "\u0f99",
        "T": "\u0f9a",
        "-t": "\u0f9a",
        "Th": "\u0f9b",
        "-th": "\u0f9b",
        "D": "\u0f9c",
        "-d": "\u0f9c",
        "Dh": "\u0f9c\u0fb7",
        "D+h": "\u0f9c\u0fb7",
        "-dh": "\u0f9c\u0fb7",
        "-d+h": "\u0f9c\u0fb7",
        "N": "\u0f9e",
        "-n": "\u0f9e",
        "t": "\u0f9f",
        "th": "\u0fa0",
        "d": "\u0fa1",
        "dh": "\u0fa1\u0fb7",
        "d+h": "\u0fa1\u0fb7",
        "n": "\u0fa3",
        "p": "\u0fa4",
        "ph": "\u0fa5",
        "b": "\u0fa6",
        "bh": "\u0fa6\u0fb7",
        "b+h": "\u0fa6\u0fb7",
        "m": "\u0fa8",
        "ts": "\u0fa9",
        "tsh": "\u0faa",
        "dz": "\u0fab",
        "dzh": "\u0fab\u0fb7",
        "dz+h": "\u0fab\u0fb7",
        "w": "\u0fad",
        "zh": "\u0fae",
        "z": "\u0faf",
        "'": "\u0fb0",
        "y": "\u0fb1",
        "r": "\u0fb2",
        "l": "\u0fb3",
        "sh": "\u0fb4",
        "Sh": "\u0fb5",
        "-sh": "\u0fb5",
        "s": "\u0fb6",
        "h": "\u0fb7",
        "a": "\u0fb8",
        "W": "\u0fba",
        "Y": "\u0fbb",
        "R": "\u0fbc"
        }
    m_vowel = {
        "a": "\u0f68",
        "A": "\u0f71",
        "i": "\u0f72",
        "I": "\u0f71\u0f72",
        "u": "\u0f74",
        "U": "\u0f71\u0f74",
        "e": "\u0f7a",
        "ai": "\u0f7b",
        "o": "\u0f7c",
        "au": "\u0f7d",
        "-i": "\u0f80",
        "-I": "\u0f71\u0f80"
    }
    #  final symbols to unicode
    m_final_uni = {
        "M": "\u0f7e",
        "~M`": "\u0f82",
        "~M": "\u0f83",
        "X": "\u0f37",
        "~X": "\u0f35",
        "H": "\u0f7f",
        "?": "\u0f84",
        "^": "\u0f39"
    }
    #  final symbols organized by class
    m_final_class = {
        "M": "M",
        "~M`": "M",
        "~M": "M",
        "X": "X",
        "~X": "X",
        "H": "H",
        "?": "?",
        "^": "^"
    }
    #  other stand-alone symbols
    m_other = {
        "0": "\u0f20",
        "1": "\u0f21",
        "2": "\u0f22",
        "3": "\u0f23",
        "4": "\u0f24",
        "5": "\u0f25",
        "6": "\u0f26",
        "7": "\u0f27",
        "8": "\u0f28",
        "9": "\u0f29",
        " ": "\u0f0b",
        "*": "\u0f0c",
        "/": "\u0f0d",
        "//": "\u0f0e",
        ";": "\u0f0f",
        "|": "\u0f11",
        "!": "\u0f08",
        ":": "\u0f14",
        "_": " ",
        "=": "\u0f34",
        "<": "\u0f3a",
        ">": "\u0f3b",
        "(": "\u0f3c",
        ",": "\u0f3d",
        "@": "\u0f04",
        "#": "\u0f05",
        "$": "\u0f06",
        "%": "\u0f07"
    }
    #  special characters: flag those if they occur out of context
    m_special = [".","+","-","~","^","?","`","]"]
    #  superscripts: hashmap of superscript => set of letters or stacks below
    m_superscripts = {
        "r": ["k","g","ng","j","ny","t","d","n","b","m","ts","dz","k+y","g+y","m+y","b+w","ts+w","g+w"],
        "l": ["k","g","ng","c","j","t","d","p","b","h"],
        "s": ["k","g","ng","ny","t","d","n","p","b","m","ts","k+y","g+y","p+y","b+y","m+y","k+r","g+r","p+r","b+r","m+r","n+r"],
        "y": ["k","kh","g","p","ph","b","m","r+k","r+g","r+m","s+k","s+g","s+p","s+b","s+m"]
    }
    m_subscripts = {
        "y": ["k","kh","g","p","ph","b","m","r+k","r+g","r+m","s+k","s+g","s+p","s+b","s+m"],
        "r": ["k","kh","g","t","th","d","n","p","ph","b","m","sh","s","h","dz","s+k","s+g","s+p","s+b","s+m","s+n"],
        "l": ["k","g","b","r","s","z"]
    }
    m_prefixes = {
        "w": ["k","kh","g","c","ny","t","d","ts","tsh","zh","z","r","l","sh","s","h","g+r","d+r","ph+y","r+g","r+ts"],
        "g": ["c","ny","t","d","n","ts","zh","z","y","sh","s"],
        "d": ["k","g","ng","p","b","m","k+y","g+y","p+y","b+y","m+y","k+r","g+r","p+r","b+r"],
        "b": ["k","g","c","t","d","ts","zh","z","sh","s","r","l","k+y","g+y","k+r","g+r","r+l","s+l","r+k","r+g","r+ng",
                "r+j","r+ny","r+t","r+d","r+n","r+ts","r+dz","s+k","s+g","s+ng","s+ny","s+t","s+d","s+n","s+ts","r+k+y",
                "r+g+y","s+k+y","s+g+y","s+k+r","s+g+r","l+d","l+t","k+l","s+r","z+l","s+w"],
        "m": ["kh","g","ng","ch","j","ny","th","d","n","tsh","dz","kh+y","g+y","kh+r","g+r"],
        "'": ["kh","g","ch","j","th","d","ph","b","tsh","dz","kh+y","g+y","ph+y","b+y","kh+r","g+r","d+r","ph+r","b+r"]
    }

    #  set of suffix letters
    #  also included are some Skt letters b/c they occur often in suffix position in Skt words
    m_suffixes = ["'","g","ng","d","n","b","m","r","l","s","N","T","-n","-t"]    
    #  suffix2 => set of letters before
    m_suff2 = {
        "s": ["g","ng","b","m"],
        "d": ["n","r","l"]
    }
    m_affixedsuff2 = ["ng","m"]
    #  root letter index for very ambiguous three-stack syllables
    m_ambiguous_key = {
        "dgs": 1,
        "dms": 1,
        "dngs": 1,
        "'gs": 1,
        "'bs": 1,
        "mngs": 0,
        "mgs": 0,
        "bgs": 0,
        "dbs": 1
    }
    m_ambiguous_wylie = {
        "dgs": "dgas",
        "dngs": "dngas",
        "dms": "dmas",
        "'gs": "'gas",
        "'bs": "'bas",
        "mngs": "mangs",
        "mgs": "mags",
        "bgs": "bags",
        "dbs": "dbas"
    }
    #  *** Unicode to Converter mappings ***
    #  top letters
    m_tib_top = {
        '\u0f40': "k",
        '\u0f41': "kh",
        '\u0f42': "g",
        '\u0f43': "g+h",
        '\u0f44': "ng",
        '\u0f45': "c",
        '\u0f46': "ch",
        '\u0f47': "j",
        '\u0f49': "ny",
        '\u0f4a': "T",
        '\u0f4b': "Th",
        '\u0f4c': "D",
        '\u0f4d': "D+h",
        '\u0f4e': "N",
        '\u0f4f': "t",
        '\u0f50': "th",
        '\u0f51': "d",
        '\u0f52': "d+h",
        '\u0f53': "n",
        '\u0f54': "p",
        '\u0f55': "ph",
        '\u0f56': "b",
        '\u0f57': "b+h",
        '\u0f58': "m",
        '\u0f59': "ts",
        '\u0f5a': "tsh",
        '\u0f5b': "dz",
        '\u0f5c': "dz+h",
        '\u0f5d': "w",
        '\u0f5e': "zh",
        '\u0f5f': "z",
        '\u0f60': "'",
        '\u0f61': "y",
        '\u0f62': "r",
        '\u0f63': "l",
        '\u0f64': "sh",
        '\u0f65': "Sh",
        '\u0f66': "s",
        '\u0f67': "h",
        '\u0f68': "a",
        '\u0f69': "k+Sh",
        '\u0f6a': "R"
    }
    #  subjoined letters
    m_tib_subjoined = {
        '\u0f90': "k",
        '\u0f91': "kh",
        '\u0f92': "g",
        '\u0f93': "g+h",
        '\u0f94': "ng",
        '\u0f95': "c",
        '\u0f96': "ch",
        '\u0f97': "j",
        '\u0f99': "ny",
        '\u0f9a': "T",
        '\u0f9b': "Th",
        '\u0f9c': "D",
        '\u0f9d': "D+h",
        '\u0f9e': "N",
        '\u0f9f': "t",
        '\u0fa0': "th",
        '\u0fa1': "d",
        '\u0fa2': "d+h",
        '\u0fa3': "n",
        '\u0fa4': "p",
        '\u0fa5': "ph",
        '\u0fa6': "b",
        '\u0fa7': "b+h",
        '\u0fa8': "m",
        '\u0fa9': "ts",
        '\u0faa': "tsh",
        '\u0fab': "dz",
        '\u0fac': "dz+h",
        '\u0fad': "w",
        '\u0fae': "zh",
        '\u0faf': "z",
        '\u0fb0': "'",
        '\u0fb1': "y",
        '\u0fb2': "r",
        '\u0fb3': "l",
        '\u0fb4': "sh",
        '\u0fb5': "Sh",
        '\u0fb6': "s",
        '\u0fb7': "h",
        '\u0fb8': "a",
        '\u0fb9': "k+Sh",
        '\u0fba': "W",
        '\u0fbb': "Y",
        '\u0fbc': "R"
    }
    #  vowel signs:
    #  a-chen is not here because that's a top character: not a vowel sign.
    #  pre-composed "I" and "U" are dealt here; other pre-composed Skt vowels are more
    #  easily handled by a global replace in toWylie(,: b/c they turn into subjoined "r"/"l".
    m_tib_vowel = {
        '\u0f71': "A",
        '\u0f72': "i",
        '\u0f73': "I",
        '\u0f74': "u",
        '\u0f75': "U",
        '\u0f7a': "e",
        '\u0f7b': "ai",
        '\u0f7c': "o",
        '\u0f7d': "au",
        '\u0f80': "-i"
    }
    #  long (Skt, vowels
    m_tib_vowel_long = {
        "i": "I",
        "u": "U",
        "-i": "-I"
    }
    #  final symbols => wylie
    m_tib_final_wylie = {
        '\u0f7e': "M",
        '\u0f82': "~M`",
        '\u0f83': "~M",
        '\u0f37': "X",
        '\u0f35': "~X",
        '\u0f39': "^",
        '\u0f7f': "H",
        '\u0f84': "?"
    }
    #  final symbols by class
    m_tib_final_class = {
        '\u0f7e': "M",
        '\u0f82': "M",
        '\u0f83': "M",
        '\u0f37': "X",
        '\u0f35': "X",
        '\u0f39': "^",
        '\u0f7f': "H",
        '\u0f84': "?"
    }
    #  special characters introduced by ^
    m_tib_caret = {
        "ph": "f",
        "b": "v"
    }
    #  other stand-alone characters
    m_tib_other = {
        ' ': "_",
        '\u0f04': "@",
        '\u0f05': "#",
        '\u0f06': "$",
        '\u0f07': "%",
        '\u0f08': "!",
        '\u0f0b': " ",
        '\u0f0c': "*",
        '\u0f0d': "/",
        '\u0f0e': "//",
        '\u0f0f': ";",
        '\u0f11': "|",
        '\u0f14': ":",
        '\u0f20': "0",
        '\u0f21': "1",
        '\u0f22': "2",
        '\u0f23': "3",
        '\u0f24': "4",
        '\u0f25': "5",
        '\u0f26': "6",
        '\u0f27': "7",
        '\u0f28': "8",
        '\u0f29': "9",
        '\u0f34': "=",
        '\u0f3a': "<",
        '\u0f3b': ">",
        '\u0f3c': "(",
        '\u0f3d': ","
    }
    #  all these stacked consonant combinations don't need "+"s in them
    m_tib_stacks = ["b+l","b+r","b+y","c+w","d+r","d+r+w","d+w","dz+r","g+l","g+r","g+r+w",
        "g+w","g+y","h+r","h+w","k+l","k+r","k+w","k+y","kh+r","kh+w","kh+y","l+b","l+c",
        "l+d","l+g","l+h","l+j","l+k","l+ng","l+p","l+t","l+w","m+r","m+y","n+r","ny+w","p+r",
        "p+y","ph+r","ph+y","ph+y+w","r+b","r+d","r+dz","r+g","r+g+w","r+g+y","r+j","r+k",
        "r+k+y","r+l","r+m","r+m+y","r+n","r+ng","r+ny","r+t","r+ts","r+ts+w","r+w","s+b",
        "s+b+r","s+b+y","s+d","s+g","s+g+r","s+g+y","s+k","s+k+r","s+k+y","s+l","s+m","s+m+r",
        "s+m+y","s+n","s+n+r","s+ng","s+ny","s+p","s+p+r","s+p+y","s+r","s+t","s+ts","s+w","sh+r",
        "sh+w","t+r","t+w","th+r","ts+w","tsh+w","z+l","z+w","zh+w"
        ]
    #  a map used to split the input string into tokens for toUnicode(,.
    #  all letters which start tokens longer than one letter are mapped to the max length of
    #  tokens starting with that letter.  
    m_tokens_start = {
        'S': 2,
        '/': 2,
        'd': 4,
        'g': 3,
        'b': 3,
        'D': 3,
        'z': 2,
        '~': 3,
        '-': 4,
        'T': 2,
        'a': 2,
        'k': 2,
        't': 3,
        's': 2,
        'c': 2,
        'n': 2,
        'p': 2,
        '\r': 2
        }
    #  also for tokenization - a set of tokens longer than one letter
    m_tokens = ["-d+h","dz+h","-dh","-sh","-th","D+h","b+h","d+h","dzh","g+h","tsh","~M`",
        "-I","-d","-i","-n","-t","//","Dh","Sh","Th","ai","au","bh","ch","dh","dz","gh",
        "kh","ng","ny","ph","sh","th","ts","zh","~M","~X","\r\n"
        ]

    repls = [
        ("ʼ", "'"),
        ("ʹ", "'"),
        ("‘", "'"),
        ("’", "'"),
        ("ʾ", "'"),
        ("x", "\\u0fbe"),
        ("X", "\\u0fbe"),
        ("...", "\\u0f0b\\u0f0b\\u0f0b"),
        (" (", "_("),
        (") ", ")_"),
        ("/ ", "/_"),
        (" 0", "_0"),
        (" 1", "_1"),
        (" 2", "_2"),
        (" 3", "_3"),
        (" 4", "_4"),
        (" 5", "_5"),
        (" 6", "_6"),
        (" 7", "_7"),
        (" 8", "_8"),
        (" 9", "_9"),
        ("_ ", "__"),
        ("G", "g"),
        ("K", "k"),
        ("C", "c"),
        ("B", "b"),
        ("P", "p"),
        ("L", "l"),
        ("Z", "z"),
        (" b ", " ba "),
        (" b'i ", " ba'i "),
        (" m ", " ma "),
        (" m'i ", " ma'i "),
        (" M", " m"),
        ("(M", "(m")
        ]

    #  setup a wylie object
    def initWylie(self, check, check_strict, print_warnings, fix_spacing, mode):
        #  check_strict requires check
        if check_strict and not check:
            raise RuntimeException("check_strict requires check.")
        self.check = check
        self.check_strict = check_strict
        self.print_warnings = print_warnings
        self.fix_spacing = fix_spacing
        self.mode = mode

    # 
    # 	* Default constructor, sets the following defaults:
    # 	*  
    # 	* @param check
    # 	* generate warnings for illegal consonant sequences
    # 	* @param check_strict
    # 	* stricter checking, examine the whole stack
    # 	* @param print_warnings
    # 	* print generated warnings to stdout
    # 	* @param fix_spacing
    # 	* remove spaces after newlines, collapse multiple tseks into one, etc.
    # 	* @param mode
    # 	* one of WYLIE, EWTS, ALALC, DTS and ACIP
    # 	
    def __init__(self, check=True, check_strict=True, print_warnings=False, fix_spacing=True, mode=Mode.EWTS):
        self.initWylie(check, check_strict, print_warnings, fix_spacing, mode)

    #  helper functions to access the various hash tables
    def consonant(self, s):
        return self.m_consonant.get(s)

    def subjoined(self, s):
        return self.m_subjoined.get(s)

    def vowel(self, s):
        return self.m_vowel.get(s)

    def final_uni(self, s):
        return self.m_final_uni.get(s)

    def final_class(self, s):
        return self.m_final_class.get(s)

    def other(self, s):
        return self.m_other.get(s)

    def isSpecial(self, s):
        return s in self.m_special

    def isSuperscript(self, s):
        return s in self.m_superscripts

    def superscript(self, sup, below):
        if sup not in self.m_superscripts:
            return False
        return below in self.m_superscripts[sup]

    def isSubscript(self, s):
        return s in self.m_subscripts

    def subscript(self, sub, above):
        if sub not in self.m_subscripts:
            return False
        return above in self.m_subscripts[sub]

    def isPrefix(self, s):
        return s in self.m_prefixes

    def prefix(self, pref, after):
        if pref not in self.m_prefixes:
            return False
        return after in self.m_prefixes[pref]

    def isSuffix(self, s):
        return s in self.m_suffixes

    def isSuff2(self, s):
        return s in self.m_suff2

    def suff2(self, suff, before):
        if suff not in self.m_suff2:
            return False
        return before in self.m_suff2[suff]

    def ambiguous_key(self, syll):
        return self.m_ambiguous_key.get(syll)

    def ambiguous_wylie(self, syll):
        return self.m_ambiguous_wylie.get(syll)

    def tib_top(self, c):
        return self.m_tib_top.get(c)

    def tib_subjoined(self, c):
        return self.m_tib_subjoined.get(c)

    def tib_vowel(self, c):
        return self.m_tib_vowel.get(c)

    def tib_vowel_long(self, s):
        return self.m_tib_vowel_long.get(s)

    def tib_final_wylie(self, c):
        return self.m_tib_final_wylie.get(c)

    def tib_final_class(self, c):
        return self.m_tib_final_class.get(c)

    def tib_caret(self, s):
        return self.m_tib_caret.get(s)

    def tib_other(self, c):
        return self.m_tib_other.get(c)

    def tib_stack(self, s):
        return s in self.m_tib_stacks

    def get_max_token_len(self, inputstr, i, lenval, maxlen):
        while lenval > 1:
            if i <= maxlen - lenval:
                tr = inputstr[i : i + lenval]
                if tr in self.m_tokens:
                    return lenval
            lenval -= 1
        return 0

    #  split a string into Converter tokens; 
    #  make sure there is room for at least one null element at the end of the array
    def splitIntoTokens(self, inputstr):
        tokens = []
        o = 0
        i = 0
        maxlen = len(inputstr)
        while i < maxlen:
            c = inputstr[i]
            lenval = self.m_tokens_start.get(c)
            #  if there are multi-char tokens starting with this char, try them
            if lenval != None:
                tokenlen = self.get_max_token_len(inputstr, i, lenval, maxlen)
                if tokenlen > 0:
                    tokens.append(inputstr[i : i + tokenlen])
                    i += tokenlen
                    continue
            #  things starting with backslash are special
            if c == '\\' and i <= maxlen - 2:
                if inputstr[i + 1] == 'u' and i <= maxlen - 6:
                    tokens.append(inputstr[i : i + 6])
                    #  \\uxxxx
                    i += 6
                elif inputstr[i + 1] == 'U' and i <= maxlen - 10:
                    tokens.append(inputstr[i : i + 10])
                    #  \\Uxxxxxxxx
                    i += 10
                else:
                    tokens.append(inputstr[i : i + 2])
                    #  \\x
                    i += 2
                continue 
            #  otherwise just take one char
            tokens.append(str(c))
            i += 1
        return tokens

    # 
    # 	 * Adjusts the input string based on the idea that people often are sloppy when writing
    # 	 * Wylie and use ' ' instead of '_' when a space is actually meant in the output. This is
    # 	 * written is a really simple brute force way to avoid issues of which regex's are supported
    # 	 * in Javascript when translated via GWT. This routine does not handle the case of " /" which
    # 	 * requires more care to accomodate "ng /" and "ngi /" and so on which are intentional since 
    # 	 * a tsheg is required in these cases. Also it is not feasible to handle "g " for a final "ga"
    # 	 * at the end of a phrase where the '/' is usually omitted in favor of the descender on the
    # 	 * "ga". Detecting this is non-trivial.
    # 	 * 
    # 	 * @param str String to be normalized
    # 	 * @return normalized String
    # 	 
    @classmethod
    def normalizeSloppyWylie(cls, inputstr):
        for k, v in cls.repls:
            inputstr = inputstr.replace(k, v)

        #  convert S but not Sh:
        inputstr = inputstr.replace("Sh", "ZZZ")
        inputstr = inputstr.replace("S", "s")
        inputstr = inputstr.replace("ZZZ", "Sh")
        if inputstr.startswith("M"):
            inputstr = "m" + inputstr[1]
        return inputstr

    # 
    #     * Checks if a character is a Tibetan Unicode combining character.
    #     *  
    #     * @param x
    #     * the character to check
    #     * @return
    #     * true if x is a Tibetan Unicode combining character
    #     
    @classmethod
    def isCombining(cls, x):
        #  inspired from  https://github.com/apache/jena/blob/master/jena-core/src/main/java/org/apache/jena/rdfxml/xmlinput/impl/CharacterModel.java
        return ((x > 0X0F71 and x < 0X0F84) or (x < 0X0F8D and x > 0X0FBC))

    # 
    #     * Converts a string to Unicode.
    #     *  
    #     * @param str
    #     * the string to convert
    #     * @param warns
    #     * the warning list to fill
    #     * @param sloppy
    #     * if common EWTS errors should be fixed
    #     * @return
    #     * the converted string
    #     
    def toUnicode(self, inputstr, warns=None, sloppy=True):
        if inputstr == None:
            return " - no data - "
        out = ""
        line = 1
        units = 0
        if self.mode == self.Mode.DWTS or self.mode == self.Mode.DTS:
            inputstr = TransConverter.dtsToEwts(inputstr)
        elif self.mode == self.Mode.ALALC:
            inputstr = TransConverter.alalcToEwts(inputstr)
        #  remove initial spaces if required
        if self.fix_spacing:
            inputstr = re.sub("^\\s+", "", inputstr)
        if sloppy:
            inputstr = self.normalizeSloppyWylie(inputstr)
        #  split into tokens
        tokens = self.splitIntoTokens(inputstr)
        i = 0
        lentokens = len(tokens)
        #  iterate over the tokens
        # label ITER
        while i<lentokens:
            t = tokens[i]
            o = None
            #  [non-tibetan text] : pass through, nesting brackets
            if t == "[":
                # label ESC
                finished = False
                while i<lentokens:
                    i += 1
                    t = tokens[i]
                    if t == "]":
                        finished = True
                        break
                    #  handle unicode escapes and \1-char escapes within [comments]...
                    if t.startswith("\\u") or t.startswith("\\U"):
                        o = self.unicodeEscape(warns, line, t)
                        if o != None:
                            out += o
                            continue
                    if t.startswith("\\"):
                        o = t[1]
                    else:
                        o = t
                    out += o
                if not finished:
                    self.warnl(warns, line, "Unfinished [non-Converter stuff].")
                    break
                else:
                    i += 1
                    continue
            #  punctuation, numbers, etc
            o = self.other(t)
            if o != None:
                out += o
                i += 1
                units += 1
                #  collapse multiple spaces?
                if t == " " and self.fix_spacing:
                    while i < lentokens and tokens[i] == " ":
                        i += 1
                continue # TODO: label ITER
            if self.vowel(t) != None or self.consonant(t) != None:
                tb = self.toUnicodeOneTsekbar(tokens, i)
                word = ""
                j = 0
                while j < tb.tokens_used:
                    word += tokens[i + j]
                    j += 1
                out += tb.uni_string
                i += tb.tokens_used
                units += 1
                for w in tb.warns:
                    self.warnl(warns, line, "\"" + word + "\": " + w)
                continue  # TODO: label ITER
            if t == "\ufeff" or t == "\u200b":
                i += 1
                continue # TODO: label ITER
            if t.startswith("\\u") or t.startswith("\\U"):
                o = self.unicodeEscape(warns, line, t)
                if o != None:
                    i += 1
                    out += o
                    continue  # TODO: label ITER
            if t.startswith("\\"):
                out += t[1]
                i += 1
                continue # TODO: label ITER
            if t == "\r\n" or t == "\n" or t == "\r":
                line += 1
                out += t
                i += 1
                if self.fix_spacing:
                    while tokens[i] != None and tokens[i] == " ":
                        i+=1
                continue  # TODO: label ITER
            c = t[0]
            if self.isSpecial(t) or (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                self.warnl(warns, line, "Unexpected character \"" + t + "\".")
            out += t
            i += 1
        if units == 0:
            self.warn(warns, "No Tibetan characters found!")
        if self.check_strict:
            if 0 > len(out) and self.isCombining(out[0]):
                self.warn(warns, "String starts with combining character '" + out[0] + "'")
        return out

    def validHex(self, t):
        i = 0
        while i < len(t):
            c = t[i]
            if not ((c >= 'a' and c <= 'f') or (c >= '0' and c <= '9')):
                return False
            i += 1
        return True

    def unicodeEscape(self, warns, line, t):
        hex = t[2:]
        if len(hex) == 0:
            return None
        if not self.validHex(hex):
            self.warnl(warns, line, "\"" + t + "\": invalid hex code.")
            return ""
        i = int(hex,16)
        return chr(i)

    def warn(self, warns, inputstr):
        if warns != None:
            warns.append(inputstr)
        if self.print_warnings:
            print(inputstr)

    def warnl(self, warns, line, inputstr):
        self.warn(warns, "line " + str(line) + ": " + inputstr)

    def debug(self, inputstr):
        print(inputstr)

    def debugvar(self, o, name):
        print(">>" + name + "<< : (" + ("NULL" if o == None else o.__str__()) + ")")

    def joinStrings(self, a, sep):
        return sep.join(a)

    def toUnicodeOneStack(self, tokens, i):
        orig_i = i
        t = None
        t2 = None
        o = None
        out = ""
        warns = []
        consonants = 0
        vowel_found = None
        vowel_sign = None
        single_consonant = None
        plus = False
        caret = 0
        final_found = {}
        lentokens = len(tokens)
        if lentokens > i:
            t = tokens[i]
        if lentokens > i+1:
            t2 = tokens[i+1]
        if t2 != None and self.isSuperscript(t) and self.superscript(t, t2):
            if self.check_strict:
                next = self.consonantString(tokens, i + 1)
                if not self.superscript(t, next):
                    next = next.replace("+", "")
                    warns.append("Superscript \"" + t + "\" does not occur above combination \"" + next + "\".")
            out += self.consonant(t)
            consonants += 1
            i += 1
            while tokens[i] != None and tokens[i] == "^":
                caret += 1
                i += 1
        while True:
            t = tokens[i] if i < lentokens else None
            if self.consonant(t) != None or (0 > len(out) and self.subjoined(t) != None):
                if 0 < len(out):
                    out += self.subjoined(t)
                else:
                    out += self.consonant(t)
                i += 1
                if t == "a":
                    vowel_found = "a"
                else:
                    consonants += 1
                    single_consonant = t
                while i<lentokens and tokens[i] == "^":
                    caret += 1
                    i += 1
                z = 0
                while z < 2:
                    t2 = tokens[i] if i < lentokens else None
                    if t2 != None and self.isSubscript(t2):
                        if t2 == "l" and consonants > 1:
                            break
                        if self.check_strict and not plus:
                            prev = self.consonantStringBackwards(tokens, i-1, orig_i)
                            if not self.subscript(t2, prev):
                                prev = prev.replace("+", "")
                                warns.append("Subjoined \"" + t2 + "\" not expected after \"" + prev + "\".")
                        elif self.check:
                            if not self.subscript(t2, t) and not (z == 1 and t2 == "w" and t == "y"):
                                warns.append("Subjoined \"" + t2 + "\"not expected after \"" + t + "\".")
                        out += self.subjoined(t2)
                        i += 1
                        consonants += 1
                        while i<lentokens and tokens[i] == "^":
                            caret += 1
                            i += 1
                        t = t2
                    else:
                        break
                    z += 1
            if caret > 0:
                if caret > 1:
                    warns.append("Cannot have more than one \"^\" applied to the same stack.")
                final_found[self.final_class("^")] = "^"
                out += self.final_uni("^")
                caret = 0
            t = tokens[i] if i < lentokens else None
            if t != None and self.vowel(t) != None:
                if 0 == len(out):
                    out += self.vowel("a")
                if not t == "a":
                    out += self.vowel(t)
                i += 1
                vowel_found = t
                if not t == "a":
                    vowel_sign = t
            t = tokens[i] if i < lentokens else None
            if t != None and t == "+":
                i += 1
                plus = True
                t = tokens[i] if i < lentokens else None
                if t == None or (self.vowel(t) == None and self.subjoined(t) == None):
                    if self.check:
                        warns.append("Expected vowel or consonant after \"+\".")
                    break # TODO: labelled
                if self.check:
                    if self.vowel(t) == None and vowel_sign != None:
                        warns.append("Cannot subjoin consonant (" + t + ") after vowel (" + vowel_sign + ") in same stack.")
                    elif t == "a" and vowel_sign != None:
                        warns.append("Cannot subjoin a-chen (a) after vowel (" + vowel_sign + ") in same stack.")
                continue
            break
        t = tokens[i] if i < lentokens else None
        while t != None and self.final_class(t) != None:
            uni = self.final_uni(t)
            klass = self.final_class(t)
            if klass in final_found:
                if final_found[klass] == t:
                    warns.append("Cannot have two \"" + t + "\" applied to the same stack.")
                else:
                    warns.append("Cannot have \"" + t + "\" and \"" + final_found[klass] + "\" applied to the same stack.")
            else:
                final_found[klass] = t
                out += uni
            i += 1
            single_consonant = None
            t = tokens[i] if i < lentokens else None
        if i < lentokens and tokens[i] == ".":
            i += 1
        if consonants > 1 and vowel_found == None:
            if plus:
                if self.check:
                    warns.append("Stack with multiple consonants should end with vowel.")
            else:
                i = orig_i + 1
                consonants = 1
                single_consonant = tokens[orig_i]
                out = "" # TODO: ?
                out += self.consonant(single_consonant)
        if consonants != 1 or plus:
            single_consonant = None
        ret = self.WylieStack()
        ret.uni_string = out
        ret.tokens_used = i - orig_i
        if vowel_found != None:
            ret.single_consonant = None
        else:
            ret.single_consonant = single_consonant
        if vowel_found != None and vowel_found == "a":
            ret.single_cons_a = single_consonant
        else:
            ret.single_cons_a = None
        ret.warns = warns
        ret.visarga = "H" in final_found
        return ret

    def toUnicodeOneTsekbar(self, tokens, i):
        orig_i = i
        t = tokens[i]
        stack = None
        prev_cons = None
        visarga = False
        check_root = True
        consonants = []
        root_idx = -1
        out = ""
        warns = []
        state = self.State.PREFIX
        lentokens = len(tokens)
        while t != None and (self.vowel(t) != None or self.consonant(t) != None) and not visarga:
            if stack != None:
                prev_cons = stack.single_consonant
            stack = self.toUnicodeOneStack(tokens, i)
            i += stack.tokens_used
            t = tokens[i] if i < lentokens else None
            out += stack.uni_string
            warns += stack.warns
            visarga = stack.visarga
            if not self.check:
                continue 
            if state == self.State.PREFIX and stack.single_consonant != None:
                consonants.append(stack.single_consonant)
                if self.isPrefix(stack.single_consonant):
                    next = t
                    if self.check_strict:
                        next = self.consonantString(tokens, i)
                    if next != None and not self.prefix(stack.single_consonant, next):
                        next = next.replace("+", "")
                        warns.append("Prefix \"" + stack.single_consonant + "\" does not occur before \"" + next + "\".")
                else:
                    warns.append("Invalid prefix consonant: \"" + stack.single_consonant + "\".")
                state = self.State.MAIN
            elif stack.single_consonant == None:
                state = self.State.SUFF1
                if root_idx >= 0:
                    check_root = False
                elif stack.single_cons_a != None:
                    consonants.append(stack.single_cons_a)
                    root_idx = len(consonants) - 1
            elif state == self.State.MAIN:
                warns.append("Expected vowel after \"" + stack.single_consonant + "\".")
            elif state == self.State.SUFF1:
                consonants.append(stack.single_consonant)
                if self.check_strict:
                    if not self.isSuffix(stack.single_consonant):
                        warns.append("Invalid suffix consonant: \"" + stack.single_consonant + "\".")
                state = self.State.SUFF2
            elif state == self.State.SUFF2:
                consonants.append(stack.single_consonant)
                if self.isSuff2(stack.single_consonant):
                    if not self.suff2(stack.single_consonant, prev_cons):
                        warns.append("Second suffix \"" + stack.single_consonant + "\" does not occur after \"" + prev_cons + "\".")
                else:
                    if stack.single_consonant not in self.m_affixedsuff2 or not prev_cons == "'":
                        warns.append("Invalid 2nd suffix consonant: \"" + stack.single_consonant + "\".")
                state = self.State.NONE
            elif state == self.State.NONE:
                warns.append("Cannot have another consonant \"" + stack.single_consonant + "\" after 2nd suffix.")
        if state == self.State.MAIN and stack.single_consonant != None and self.isPrefix(stack.single_consonant):
            warns.append("Vowel expected after \"" + stack.single_consonant + "\".")
        if self.check and len(warns) == 0 and check_root and root_idx >= 0:
            if len(consonants) == 2 and root_idx != 0 and self.prefix(consonants[0], consonants[1]) and self.isSuffix(consonants[1]):
                warns.append("Syllable should probably be \"" + consonants[0] + "a" + consonants[1] + "\".")
            elif len(consonants) == 3 and self.isPrefix(consonants[0]) and self.suff2("s", consonants[1]) and consonants[2] == "s":
                cc = self.joinStrings(consonants, "")
                cc = cc.replace('\u2018', '\'')
                cc = cc.replace('\u2019', '\'')
                expect_key = self.ambiguous_key(cc)
                if expect_key != None and expect_key.intValue() != root_idx:
                    warns.append("Syllable should probably be \"" + self.ambiguous_wylie(cc) + "\".")
        ret = self.WylieTsekbar()
        ret.uni_string = out
        ret.tokens_used = i - orig_i
        ret.warns = warns
        return ret


    # Looking from i onwards within tokens, returns as many consonants as it finds,
    # up to and not including the next vowel or punctuation.  Skips the caret "^".
    # Returns: a string of consonants joined by "+" signs.
    def consonantString(self, tokens, i):
        out = []
        t = None
        while i < len(tokens):
            t = tokens[i]
            i += 1
            if t == "+" or t == "^":
                continue
            if self.consonant(t) == None:
                break
            out.append(t)
        return self.joinStrings(out, "+")

    def consonantStringBackwards(self, tokens, i, orig_i):
        out = []
        t = None
        while i >= orig_i and tokens[i] != None:
            t = tokens[i]
            i -= 1
            if t == "+" or t == "^":
                continue
            if self.consonant(t) == None:
                break
            out.insert(0,t)
        return self.joinStrings(out, "+")

    def toWylie(self, inputstr, warns=None, escape=True):
        out = ""
        line = 1
        inputstr = inputstr.replace("\u0f76", "\u0fb2\u0f80")
        inputstr = inputstr.replace("\u0f77", "\u0fb2\u0f71\u0f80")
        inputstr = inputstr.replace("\u0f78", "\u0fb3\u0f80")
        inputstr = inputstr.replace("\u0f79", "\u0fb3\u0f71\u0f80")
        inputstr = inputstr.replace("\u0f81", "\u0f71\u0f80")
        inputstr = inputstr.replace("\u0F75", "\u0F71\u0F74")
        inputstr = inputstr.replace("\u0F73", "\u0F71\u0F72")
        i = 0
        lenstr = len(inputstr)
        while i < lenstr:
            t = inputstr[i]
            if self.tib_top(t) != None:
                tb = self.toWylieOneTsekbar(inputstr, lenstr, i)
                out += tb.wylie
                i += tb.tokens_used
                for w in tb.warns:
                    self.warnl(warns, line, w)
                if not escape:
                    i += self.handleSpaces(inputstr, i, out)
                continue
            o = self.tib_other(t)
            if o != None and (t != ' ' or (escape and not self.followedByNonTibetan(inputstr, i))):
                out += o
                i += 1
                if not escape:
                    i += self.handleSpaces(inputstr, i, out)
                continue
            if t == '\r' or t == '\n':
                line += 1
                i += 1
                out += t
                if t == '\r' and i < lenstr and inputstr[i] == '\n':
                    i += 1
                    out += '\n'
                continue
            if t == '\ufeff' or t == '\u200b':
                i += 1
                continue
            if not escape:
                out += t
                i += 1
                continue
            if t >= '\u0f00' and t <= '\u0fff':
                c = self.formatHex(t)
                out += c
                i += 1
                if self.tib_subjoined(t) != None or self.tib_vowel(t) != None or self.tib_final_wylie(t) != None:
                    self.warnl(warns, line, "Tibetan sign " + c + " needs a top symbol to attach to.")
                continue
            out += "["
            while self.tib_top(t) == None and (self.tib_other(t) == None or t == ' ') and t != '\r' and t != '\n':
                if t == '[' or t == ']':
                    out += "\\"
                    out += t
                elif t >= '\u0f00' and t <= '\u0fff':
                    out += self.formatHex(t)
                else:
                    out += t
                i += 1
                if i >= lenstr:
                    break
                t = inputstr[i]
            out += "]"
        return out

    def formatHex(self, t):
        sb = "\\u%0.4x" % ord(t)
        return sb

    def handleSpaces(self, inputstr, i, out):
        found = 0
        while i < len(inputstr) and inputstr[i] == ' ':
            i += 1
            found += 1
        if found == 0 or i == len(inputstr):
            return 0
        t = inputstr[i]
        if self.tib_top(t) == None and self.tib_other(t) == None:
            return 0
        while i < found:
            out += '_'
            i += 1
        return found

    def followedByNonTibetan(self, inputstr, i):
        lenstr = len(inputstr)
        while i < lenstr and inputstr[i] == ' ':
            i += 1
        if i == lenstr:
            return False
        t = inputstr[i]
        return self.tib_top(t) == None and self.tib_other(t) == None and t != '\r' and t != '\n'

    def toWylieOneTsekbar(self, inputstr, lenstr, i):
        orig_i = i
        warns = []
        stacks = []
        while True:
            st = self.toWylieOneStack(inputstr, lenstr, i)
            stacks.append(st)
            warns += st.warns
            i += st.tokens_used
            if st.visarga:
                break
            if i >= lenstr or self.tib_top(inputstr[i]) == None:
                break
        last = len(stacks) - 1
        if len(stacks) > 1 and stacks[0].single_cons != None:
            cs = stacks[1].cons_str.replace("+w", "")
            if self.prefix(stacks[0].single_cons, cs):
                stacks[0].prefix = True
        if len(stacks) > 1 and stacks[last].single_cons != None and self.isSuffix(stacks[last].single_cons):
            stacks[last].suffix = True
        if len(stacks) > 2 and stacks[last].single_cons != None and stacks[last-1].single_cons != None and self.isSuffix(stacks[last-1].single_cons) and self.suff2(stacks[last].single_cons, stacks[last-1].single_cons):
            stacks[last].suff2 = True
            stacks[last-1].suffix = True
        if len(stacks) == 2 and stacks[0].prefix and stacks[1].suffix:
            stacks[0].prefix = False
        if len(stacks) == 3 and stacks[0].prefix and stacks[1].suffix and stacks[2].suff2:
            ztr = ""
            for st in stacks:
                ztr += st.single_cons
            root = self.ambiguous_key(ztr)
            if root == None:
                self.warn(warns, "Ambiguous syllable found: root consonant not known for \"" + ztr + "\".")
                root = 1
            stacks[root].prefix = stacks[root].suffix = False
            stacks[root+1].suff2 = False
        if stacks[0].prefix and self.tib_stack(stacks[0].single_cons + "+" + stacks[1].cons_str):
            stacks[0].dot = True
        out = ""
        for st in stacks:
            out += self.putStackTogether(st)
        ret = self.ToWylieTsekbar()
        ret.wylie = out
        ret.tokens_used = i - orig_i
        ret.warns = warns
        return ret

    def toWylieOneStack(self, inputstr, lenstr, i):
        orig_i = i
        ffinal = None
        vowel = None
        klass = None
        # split the stack into a ToWylieStack object:
        # - top symbol
        # - stacked signs (first is the top symbol again, then subscribed main
        # characters...)
        # - caret (did we find a stray tsa-phru or not?)
        # - vowel signs (including small subscribed a-chung, "-i" Skt signs, etc)
        # - final stuff (including anusvara, visarga, halanta...)
        # - and some more variables to keep track of what has been found
        st = self.ToWylieStack()
        t = inputstr[i]
        i += 1
        st.top = self.tib_top(t)
        if st.top is not None:
            st.stack.append(st.top)
        while i < lenstr:
            t = inputstr[i]
            o = None
            if t in self.m_tib_subjoined:
                o = self.tib_subjoined(t)
                i += 1
                st.stack.append(o)
                if len(st.finals) > 0:
                    st.warns.append("Subjoined sign \"" + o + "\" found after final sign \"" + ffinal + "\".")
                elif len(st.vowels) > 0:
                    st.warns.append("Subjoined sign \"" + o + "\" found after vowel sign \"" + vowel + "\".")
            elif t in self.m_tib_vowel:
                o = self.tib_vowel(t)
                i += 1
                st.vowels.append(o)
                if vowel == None:
                    vowel = o
                if len(st.finals) > 0:
                    st.warns.append("Vowel sign \"" + o + "\" found after final sign \"" + ffinal + "\".")
            elif t in self.m_tib_final_wylie:
                o = self.tib_final_wylie(t)
                i += 1
                klass = self.tib_final_class(t)
                if o == "^":
                    st.caret = True
                else:
                    if o == "H":
                        st.visarga = True
                    st.finals.append(o)
                    if ffinal == None:
                        ffinal = o
                    if klass in st.finals_found:
                        st.warns.append("Final sign \"" + o + "\" should not combine with found after final sign \"" + ffinal + "\".")
                    else:
                        st.finals_found[klass] = o
            else:
                break
        if st.top == "a" and len(st.stack) == 1 and len(st.vowels) > 0:
            del st.stack[0]
        if len(st.vowels) > 1 and st.vowels[0] == "A" and self.tib_vowel_long(st.vowels[1]) != None:
            l = self.tib_vowel_long(st.vowels[1])
            del st.vowels[0]
            del st.vowels[0]
            st.vowels.insert(0,l)
        if st.caret and len(st.stack) == 1 and self.tib_caret(st.top) != None:
            l = self.tib_caret(st.top)
            st.top = l
            del st.stack[0]
            st.stack.insert(0,l)
            st.caret = False
        st.cons_str = self.joinStrings(st.stack, "+")
        if len(st.stack) == 1 and not st.stack[0] == "a" and not st.caret and len(st.vowels) == 0 and len(st.finals) == 0:
            st.single_cons = st.cons_str
        st.tokens_used = i - orig_i
        return st

    def putStackTogether(self, st):
        out = ""
        if self.tib_stack(st.cons_str):
            out += self.joinStrings(st.stack, "")
        else:
            out += st.cons_str
        if st.caret:
            out += "^"
        if len(st.vowels) > 0:
            out += self.joinStrings(st.vowels, "+")
        elif not st.prefix and not st.suffix and not st.suff2 and (len(st.cons_str) == 0 or st.cons_str[len(st.cons_str)-1] != 'a'):
            out += "a"
        out += self.joinStrings(st.finals, "")
        if st.dot:
            out += "."
        return out

    class ToWylieStack(object):
        top = None
        stack = []
        caret = False
        vowels = []
        finals = []
        finals_found = {}
        visarga = False
        cons_str = None
        single_cons = None
        prefix = False
        suffix = False
        suff2 = False
        dot = False
        tokens_used = 0
        warns = []

        def __init__(self):
            self.stack = []
            self.vowels = []
            self.finals = []
            self.finals_found = {}
            self.warns = []

        def __str__(self):
            return "top: %s stack: %s vowels %s finals %s finals_found %s cons_str %s suffix %s suff2 %s" % (self.top, self.stack, self.vowels, self.finals, self.finals_found, self.cons_str, self.suffix, self.suff2)

    class ToWylieTsekbar(object):
        wylie = None
        tokens_used = int()
        warns = None

        def __str__(self):
            return "wylie: %s" % self.wylie
