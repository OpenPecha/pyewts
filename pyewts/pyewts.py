#!/usr/bin/env python3
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
# 
class pyewts(object):
    #  various options for Converter conversion
    check = bool()
    check_strict = bool()
    print_warnings = bool()
    fix_spacing = bool()

    #  constant hashes and sets to help with the conversion
    m_consonant = None
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
    base = [None] * 36
    repl = [None] * 36

    class Mode:
        WYLIE = u'WYLIE'
        EWTS = u'EWTS'
        DWTS = u'DWTS'
        DTS = u'DTS'
        ALALC = u'ALALC'
        ACIP = u'ACIP'

    mode = Mode.EWTS

    #  EWTS by default
    #  initialize all the hashes with the correspondences between Converter and Unicode.  
    #  this gets called from a 'static section' to initialize the hashes the moment the
    #  class gets loaded.
    @classmethod
    def initHashes(cls):
        tmpSet = None
        #  mappings auto-generated from the Perl code
        #  *** Converter to Unicode mappings ***
        #  list of wylie consonant => unicode
        cls.m_consonant = HashMap()
        cls.m_consonant.put("k", "\u0f40")
        cls.m_consonant.put("kh", "\u0f41")
        cls.m_consonant.put("g", "\u0f42")
        cls.m_consonant.put("gh", "\u0f42\u0fb7")
        cls.m_consonant.put("g+h", "\u0f42\u0fb7")
        cls.m_consonant.put("ng", "\u0f44")
        cls.m_consonant.put("c", "\u0f45")
        cls.m_consonant.put("ch", "\u0f46")
        cls.m_consonant.put("j", "\u0f47")
        cls.m_consonant.put("ny", "\u0f49")
        cls.m_consonant.put("T", "\u0f4a")
        cls.m_consonant.put("-t", "\u0f4a")
        cls.m_consonant.put("Th", "\u0f4b")
        cls.m_consonant.put("-th", "\u0f4b")
        cls.m_consonant.put("D", "\u0f4c")
        cls.m_consonant.put("-d", "\u0f4c")
        cls.m_consonant.put("Dh", "\u0f4c\u0fb7")
        cls.m_consonant.put("D+h", "\u0f4c\u0fb7")
        cls.m_consonant.put("-dh", "\u0f4c\u0fb7")
        cls.m_consonant.put("-d+h", "\u0f4c\u0fb7")
        cls.m_consonant.put("N", "\u0f4e")
        cls.m_consonant.put("-n", "\u0f4e")
        cls.m_consonant.put("t", "\u0f4f")
        cls.m_consonant.put("th", "\u0f50")
        cls.m_consonant.put("d", "\u0f51")
        cls.m_consonant.put("dh", "\u0f51\u0fb7")
        cls.m_consonant.put("d+h", "\u0f51\u0fb7")
        cls.m_consonant.put("n", "\u0f53")
        cls.m_consonant.put("p", "\u0f54")
        cls.m_consonant.put("ph", "\u0f55")
        cls.m_consonant.put("b", "\u0f56")
        cls.m_consonant.put("bh", "\u0f56\u0fb7")
        cls.m_consonant.put("b+h", "\u0f56\u0fb7")
        cls.m_consonant.put("m", "\u0f58")
        cls.m_consonant.put("ts", "\u0f59")
        cls.m_consonant.put("tsh", "\u0f5a")
        cls.m_consonant.put("dz", "\u0f5b")
        cls.m_consonant.put("dzh", "\u0f5b\u0fb7")
        cls.m_consonant.put("dz+h", "\u0f5b\u0fb7")
        cls.m_consonant.put("w", "\u0f5d")
        cls.m_consonant.put("zh", "\u0f5e")
        cls.m_consonant.put("z", "\u0f5f")
        cls.m_consonant.put("'", "\u0f60")
        cls.m_consonant.put("y", "\u0f61")
        cls.m_consonant.put("r", "\u0f62")
        cls.m_consonant.put("l", "\u0f63")
        cls.m_consonant.put("sh", "\u0f64")
        cls.m_consonant.put("Sh", "\u0f65")
        cls.m_consonant.put("-sh", "\u0f65")
        cls.m_consonant.put("s", "\u0f66")
        cls.m_consonant.put("h", "\u0f67")
        cls.m_consonant.put("W", "\u0f5d")
        cls.m_consonant.put("Y", "\u0f61")
        cls.m_consonant.put("R", "\u0f6a")
        cls.m_consonant.put("f", "\u0f55\u0f39")
        cls.m_consonant.put("v", "\u0f56\u0f39")
        #  subjoined letters
        cls.m_subjoined = HashMap()
        cls.m_subjoined.put("k", "\u0f90")
        cls.m_subjoined.put("kh", "\u0f91")
        cls.m_subjoined.put("g", "\u0f92")
        cls.m_subjoined.put("gh", "\u0f92\u0fb7")
        cls.m_subjoined.put("g+h", "\u0f92\u0fb7")
        cls.m_subjoined.put("ng", "\u0f94")
        cls.m_subjoined.put("c", "\u0f95")
        cls.m_subjoined.put("ch", "\u0f96")
        cls.m_subjoined.put("j", "\u0f97")
        cls.m_subjoined.put("ny", "\u0f99")
        cls.m_subjoined.put("T", "\u0f9a")
        cls.m_subjoined.put("-t", "\u0f9a")
        cls.m_subjoined.put("Th", "\u0f9b")
        cls.m_subjoined.put("-th", "\u0f9b")
        cls.m_subjoined.put("D", "\u0f9c")
        cls.m_subjoined.put("-d", "\u0f9c")
        cls.m_subjoined.put("Dh", "\u0f9c\u0fb7")
        cls.m_subjoined.put("D+h", "\u0f9c\u0fb7")
        cls.m_subjoined.put("-dh", "\u0f9c\u0fb7")
        cls.m_subjoined.put("-d+h", "\u0f9c\u0fb7")
        cls.m_subjoined.put("N", "\u0f9e")
        cls.m_subjoined.put("-n", "\u0f9e")
        cls.m_subjoined.put("t", "\u0f9f")
        cls.m_subjoined.put("th", "\u0fa0")
        cls.m_subjoined.put("d", "\u0fa1")
        cls.m_subjoined.put("dh", "\u0fa1\u0fb7")
        cls.m_subjoined.put("d+h", "\u0fa1\u0fb7")
        cls.m_subjoined.put("n", "\u0fa3")
        cls.m_subjoined.put("p", "\u0fa4")
        cls.m_subjoined.put("ph", "\u0fa5")
        cls.m_subjoined.put("b", "\u0fa6")
        cls.m_subjoined.put("bh", "\u0fa6\u0fb7")
        cls.m_subjoined.put("b+h", "\u0fa6\u0fb7")
        cls.m_subjoined.put("m", "\u0fa8")
        cls.m_subjoined.put("ts", "\u0fa9")
        cls.m_subjoined.put("tsh", "\u0faa")
        cls.m_subjoined.put("dz", "\u0fab")
        cls.m_subjoined.put("dzh", "\u0fab\u0fb7")
        cls.m_subjoined.put("dz+h", "\u0fab\u0fb7")
        cls.m_subjoined.put("w", "\u0fad")
        cls.m_subjoined.put("zh", "\u0fae")
        cls.m_subjoined.put("z", "\u0faf")
        cls.m_subjoined.put("'", "\u0fb0")
        cls.m_subjoined.put("y", "\u0fb1")
        cls.m_subjoined.put("r", "\u0fb2")
        cls.m_subjoined.put("l", "\u0fb3")
        cls.m_subjoined.put("sh", "\u0fb4")
        cls.m_subjoined.put("Sh", "\u0fb5")
        cls.m_subjoined.put("-sh", "\u0fb5")
        cls.m_subjoined.put("s", "\u0fb6")
        cls.m_subjoined.put("h", "\u0fb7")
        cls.m_subjoined.put("a", "\u0fb8")
        cls.m_subjoined.put("W", "\u0fba")
        cls.m_subjoined.put("Y", "\u0fbb")
        cls.m_subjoined.put("R", "\u0fbc")
        #  vowels
        cls.m_vowel = HashMap()
        cls.m_vowel.put("a", "\u0f68")
        cls.m_vowel.put("A", "\u0f71")
        cls.m_vowel.put("i", "\u0f72")
        cls.m_vowel.put("I", "\u0f71\u0f72")
        cls.m_vowel.put("u", "\u0f74")
        cls.m_vowel.put("U", "\u0f71\u0f74")
        cls.m_vowel.put("e", "\u0f7a")
        cls.m_vowel.put("ai", "\u0f7b")
        cls.m_vowel.put("o", "\u0f7c")
        cls.m_vowel.put("au", "\u0f7d")
        cls.m_vowel.put("-i", "\u0f80")
        cls.m_vowel.put("-I", "\u0f71\u0f80")
        #  final symbols to unicode
        cls.m_final_uni = HashMap()
        cls.m_final_uni.put("M", "\u0f7e")
        cls.m_final_uni.put("~M`", "\u0f82")
        cls.m_final_uni.put("~M", "\u0f83")
        cls.m_final_uni.put("X", "\u0f37")
        cls.m_final_uni.put("~X", "\u0f35")
        cls.m_final_uni.put("H", "\u0f7f")
        cls.m_final_uni.put("?", "\u0f84")
        cls.m_final_uni.put("^", "\u0f39")
        #  final symbols organized by class
        cls.m_final_class = HashMap()
        cls.m_final_class.put("M", "M")
        cls.m_final_class.put("~M`", "M")
        cls.m_final_class.put("~M", "M")
        cls.m_final_class.put("X", "X")
        cls.m_final_class.put("~X", "X")
        cls.m_final_class.put("H", "H")
        cls.m_final_class.put("?", "?")
        cls.m_final_class.put("^", "^")
        #  other stand-alone symbols
        cls.m_other = HashMap()
        cls.m_other.put("0", "\u0f20")
        cls.m_other.put("1", "\u0f21")
        cls.m_other.put("2", "\u0f22")
        cls.m_other.put("3", "\u0f23")
        cls.m_other.put("4", "\u0f24")
        cls.m_other.put("5", "\u0f25")
        cls.m_other.put("6", "\u0f26")
        cls.m_other.put("7", "\u0f27")
        cls.m_other.put("8", "\u0f28")
        cls.m_other.put("9", "\u0f29")
        cls.m_other.put(" ", "\u0f0b")
        cls.m_other.put("*", "\u0f0c")
        cls.m_other.put("/", "\u0f0d")
        cls.m_other.put("//", "\u0f0e")
        cls.m_other.put(";", "\u0f0f")
        cls.m_other.put("|", "\u0f11")
        cls.m_other.put("!", "\u0f08")
        cls.m_other.put(":", "\u0f14")
        cls.m_other.put("_", " ")
        cls.m_other.put("=", "\u0f34")
        cls.m_other.put("<", "\u0f3a")
        cls.m_other.put(">", "\u0f3b")
        cls.m_other.put("(", "\u0f3c")
        cls.m_other.put(")", "\u0f3d")
        cls.m_other.put("@", "\u0f04")
        cls.m_other.put("#", "\u0f05")
        cls.m_other.put("$", "\u0f06")
        cls.m_other.put("%", "\u0f07")
        #  special characters: flag those if they occur out of context
        cls.m_special = HashSet()
        cls.m_special.add(".")
        cls.m_special.add("+")
        cls.m_special.add("-")
        cls.m_special.add("~")
        cls.m_special.add("^")
        cls.m_special.add("?")
        cls.m_special.add("`")
        cls.m_special.add("]")
        #  superscripts: hashmap of superscript => set of letters or stacks below
        cls.m_superscripts = HashMap()
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("g")
        tmpSet.add("ng")
        tmpSet.add("j")
        tmpSet.add("ny")
        tmpSet.add("t")
        tmpSet.add("d")
        tmpSet.add("n")
        tmpSet.add("b")
        tmpSet.add("m")
        tmpSet.add("ts")
        tmpSet.add("dz")
        tmpSet.add("k+y")
        tmpSet.add("g+y")
        tmpSet.add("m+y")
        tmpSet.add("b+w")
        tmpSet.add("ts+w")
        tmpSet.add("g+w")
        cls.m_superscripts.put("r", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("g")
        tmpSet.add("ng")
        tmpSet.add("c")
        tmpSet.add("j")
        tmpSet.add("t")
        tmpSet.add("d")
        tmpSet.add("p")
        tmpSet.add("b")
        tmpSet.add("h")
        cls.m_superscripts.put("l", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("g")
        tmpSet.add("ng")
        tmpSet.add("ny")
        tmpSet.add("t")
        tmpSet.add("d")
        tmpSet.add("n")
        tmpSet.add("p")
        tmpSet.add("b")
        tmpSet.add("m")
        tmpSet.add("ts")
        tmpSet.add("k+y")
        tmpSet.add("g+y")
        tmpSet.add("p+y")
        tmpSet.add("b+y")
        tmpSet.add("m+y")
        tmpSet.add("k+r")
        tmpSet.add("g+r")
        tmpSet.add("p+r")
        tmpSet.add("b+r")
        tmpSet.add("m+r")
        tmpSet.add("n+r")
        cls.m_superscripts.put("s", tmpSet)
        #  subscripts => set of letters above
        cls.m_subscripts = HashMap()
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("kh")
        tmpSet.add("g")
        tmpSet.add("p")
        tmpSet.add("ph")
        tmpSet.add("b")
        tmpSet.add("m")
        tmpSet.add("r+k")
        tmpSet.add("r+g")
        tmpSet.add("r+m")
        tmpSet.add("s+k")
        tmpSet.add("s+g")
        tmpSet.add("s+p")
        tmpSet.add("s+b")
        tmpSet.add("s+m")
        cls.m_subscripts.put("y", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("kh")
        tmpSet.add("g")
        tmpSet.add("t")
        tmpSet.add("th")
        tmpSet.add("d")
        tmpSet.add("n")
        tmpSet.add("p")
        tmpSet.add("ph")
        tmpSet.add("b")
        tmpSet.add("m")
        tmpSet.add("sh")
        tmpSet.add("s")
        tmpSet.add("h")
        tmpSet.add("dz")
        tmpSet.add("s+k")
        tmpSet.add("s+g")
        tmpSet.add("s+p")
        tmpSet.add("s+b")
        tmpSet.add("s+m")
        tmpSet.add("s+n")
        cls.m_subscripts.put("r", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("g")
        tmpSet.add("b")
        tmpSet.add("r")
        tmpSet.add("s")
        tmpSet.add("z")
        cls.m_subscripts.put("l", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("kh")
        tmpSet.add("g")
        tmpSet.add("c")
        tmpSet.add("ny")
        tmpSet.add("t")
        tmpSet.add("d")
        tmpSet.add("ts")
        tmpSet.add("tsh")
        tmpSet.add("zh")
        tmpSet.add("z")
        tmpSet.add("r")
        tmpSet.add("l")
        tmpSet.add("sh")
        tmpSet.add("s")
        tmpSet.add("h")
        tmpSet.add("g+r")
        tmpSet.add("d+r")
        tmpSet.add("ph+y")
        tmpSet.add("r+g")
        tmpSet.add("r+ts")
        cls.m_subscripts.put("w", tmpSet)
        #  prefixes => set of consonants or stacks after
        cls.m_prefixes = HashMap()
        tmpSet = HashSet()
        tmpSet.add("c")
        tmpSet.add("ny")
        tmpSet.add("t")
        tmpSet.add("d")
        tmpSet.add("n")
        tmpSet.add("ts")
        tmpSet.add("zh")
        tmpSet.add("z")
        tmpSet.add("y")
        tmpSet.add("sh")
        tmpSet.add("s")
        cls.m_prefixes.put("g", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("g")
        tmpSet.add("ng")
        tmpSet.add("p")
        tmpSet.add("b")
        tmpSet.add("m")
        tmpSet.add("k+y")
        tmpSet.add("g+y")
        tmpSet.add("p+y")
        tmpSet.add("b+y")
        tmpSet.add("m+y")
        tmpSet.add("k+r")
        tmpSet.add("g+r")
        tmpSet.add("p+r")
        tmpSet.add("b+r")
        cls.m_prefixes.put("d", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("k")
        tmpSet.add("g")
        tmpSet.add("c")
        tmpSet.add("t")
        tmpSet.add("d")
        tmpSet.add("ts")
        tmpSet.add("zh")
        tmpSet.add("z")
        tmpSet.add("sh")
        tmpSet.add("s")
        tmpSet.add("r")
        tmpSet.add("l")
        tmpSet.add("k+y")
        tmpSet.add("g+y")
        tmpSet.add("k+r")
        tmpSet.add("g+r")
        tmpSet.add("r+l")
        tmpSet.add("s+l")
        tmpSet.add("r+k")
        tmpSet.add("r+g")
        tmpSet.add("r+ng")
        tmpSet.add("r+j")
        tmpSet.add("r+ny")
        tmpSet.add("r+t")
        tmpSet.add("r+d")
        tmpSet.add("r+n")
        tmpSet.add("r+ts")
        tmpSet.add("r+dz")
        tmpSet.add("s+k")
        tmpSet.add("s+g")
        tmpSet.add("s+ng")
        tmpSet.add("s+ny")
        tmpSet.add("s+t")
        tmpSet.add("s+d")
        tmpSet.add("s+n")
        tmpSet.add("s+ts")
        tmpSet.add("r+k+y")
        tmpSet.add("r+g+y")
        tmpSet.add("s+k+y")
        tmpSet.add("s+g+y")
        tmpSet.add("s+k+r")
        tmpSet.add("s+g+r")
        tmpSet.add("l+d")
        tmpSet.add("l+t")
        tmpSet.add("k+l")
        tmpSet.add("s+r")
        tmpSet.add("z+l")
        tmpSet.add("s+w")
        cls.m_prefixes.put("b", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("kh")
        tmpSet.add("g")
        tmpSet.add("ng")
        tmpSet.add("ch")
        tmpSet.add("j")
        tmpSet.add("ny")
        tmpSet.add("th")
        tmpSet.add("d")
        tmpSet.add("n")
        tmpSet.add("tsh")
        tmpSet.add("dz")
        tmpSet.add("kh+y")
        tmpSet.add("g+y")
        tmpSet.add("kh+r")
        tmpSet.add("g+r")
        cls.m_prefixes.put("m", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("kh")
        tmpSet.add("g")
        tmpSet.add("ch")
        tmpSet.add("j")
        tmpSet.add("th")
        tmpSet.add("d")
        tmpSet.add("ph")
        tmpSet.add("b")
        tmpSet.add("tsh")
        tmpSet.add("dz")
        tmpSet.add("kh+y")
        tmpSet.add("g+y")
        tmpSet.add("ph+y")
        tmpSet.add("b+y")
        tmpSet.add("kh+r")
        tmpSet.add("g+r")
        tmpSet.add("d+r")
        tmpSet.add("ph+r")
        tmpSet.add("b+r")
        cls.m_prefixes.put("'", tmpSet)
        #  set of suffix letters
        #  also included are some Skt letters b/c they occur often in suffix position in Skt words
        cls.m_suffixes = HashSet()
        cls.m_suffixes.add("'")
        cls.m_suffixes.add("g")
        cls.m_suffixes.add("ng")
        cls.m_suffixes.add("d")
        cls.m_suffixes.add("n")
        cls.m_suffixes.add("b")
        cls.m_suffixes.add("m")
        cls.m_suffixes.add("r")
        cls.m_suffixes.add("l")
        cls.m_suffixes.add("s")
        cls.m_suffixes.add("N")
        cls.m_suffixes.add("T")
        cls.m_suffixes.add("-n")
        cls.m_suffixes.add("-t")
        #  suffix2 => set of letters before
        cls.m_suff2 = HashMap()
        tmpSet = HashSet()
        tmpSet.add("g")
        tmpSet.add("ng")
        tmpSet.add("b")
        tmpSet.add("m")
        cls.m_suff2.put("s", tmpSet)
        tmpSet = HashSet()
        tmpSet.add("n")
        tmpSet.add("r")
        tmpSet.add("l")
        cls.m_suff2.put("d", tmpSet)
        cls.m_affixedsuff2 = HashSet()
        cls.m_affixedsuff2.add("ng")
        cls.m_affixedsuff2.add("m")
        #  root letter index for very ambiguous three-stack syllables
        cls.m_ambiguous_key = HashMap()
        cls.m_ambiguous_key.put("dgs", 1)
        cls.m_ambiguous_key.put("dms", 1)
        cls.m_ambiguous_key.put("dngs", 1)
        cls.m_ambiguous_key.put("'gs", 1)
        cls.m_ambiguous_key.put("'bs", 1)
        cls.m_ambiguous_key.put("mngs", 0)
        cls.m_ambiguous_key.put("mgs", 0)
        cls.m_ambiguous_key.put("bgs", 0)
        cls.m_ambiguous_key.put("dbs", 1)
        cls.m_ambiguous_wylie = HashMap()
        cls.m_ambiguous_wylie.put("dgs", "dgas")
        cls.m_ambiguous_wylie.put("dngs", "dngas")
        cls.m_ambiguous_wylie.put("dms", "dmas")
        cls.m_ambiguous_wylie.put("'gs", "'gas")
        cls.m_ambiguous_wylie.put("'bs", "'bas")
        cls.m_ambiguous_wylie.put("mngs", "mangs")
        cls.m_ambiguous_wylie.put("mgs", "mags")
        cls.m_ambiguous_wylie.put("bgs", "bags")
        cls.m_ambiguous_wylie.put("dbs", "dbas")
        #  *** Unicode to Converter mappings ***
        #  top letters
        cls.m_tib_top = HashMap()
        cls.m_tib_top.put('\u0f40', "k")
        cls.m_tib_top.put('\u0f41', "kh")
        cls.m_tib_top.put('\u0f42', "g")
        cls.m_tib_top.put('\u0f43', "g+h")
        cls.m_tib_top.put('\u0f44', "ng")
        cls.m_tib_top.put('\u0f45', "c")
        cls.m_tib_top.put('\u0f46', "ch")
        cls.m_tib_top.put('\u0f47', "j")
        cls.m_tib_top.put('\u0f49', "ny")
        cls.m_tib_top.put('\u0f4a', "T")
        cls.m_tib_top.put('\u0f4b', "Th")
        cls.m_tib_top.put('\u0f4c', "D")
        cls.m_tib_top.put('\u0f4d', "D+h")
        cls.m_tib_top.put('\u0f4e', "N")
        cls.m_tib_top.put('\u0f4f', "t")
        cls.m_tib_top.put('\u0f50', "th")
        cls.m_tib_top.put('\u0f51', "d")
        cls.m_tib_top.put('\u0f52', "d+h")
        cls.m_tib_top.put('\u0f53', "n")
        cls.m_tib_top.put('\u0f54', "p")
        cls.m_tib_top.put('\u0f55', "ph")
        cls.m_tib_top.put('\u0f56', "b")
        cls.m_tib_top.put('\u0f57', "b+h")
        cls.m_tib_top.put('\u0f58', "m")
        cls.m_tib_top.put('\u0f59', "ts")
        cls.m_tib_top.put('\u0f5a', "tsh")
        cls.m_tib_top.put('\u0f5b', "dz")
        cls.m_tib_top.put('\u0f5c', "dz+h")
        cls.m_tib_top.put('\u0f5d', "w")
        cls.m_tib_top.put('\u0f5e', "zh")
        cls.m_tib_top.put('\u0f5f', "z")
        cls.m_tib_top.put('\u0f60', "'")
        cls.m_tib_top.put('\u0f61', "y")
        cls.m_tib_top.put('\u0f62', "r")
        cls.m_tib_top.put('\u0f63', "l")
        cls.m_tib_top.put('\u0f64', "sh")
        cls.m_tib_top.put('\u0f65', "Sh")
        cls.m_tib_top.put('\u0f66', "s")
        cls.m_tib_top.put('\u0f67', "h")
        cls.m_tib_top.put('\u0f68', "a")
        cls.m_tib_top.put('\u0f69', "k+Sh")
        cls.m_tib_top.put('\u0f6a', "R")
        #  subjoined letters
        cls.m_tib_subjoined = HashMap()
        cls.m_tib_subjoined.put('\u0f90', "k")
        cls.m_tib_subjoined.put('\u0f91', "kh")
        cls.m_tib_subjoined.put('\u0f92', "g")
        cls.m_tib_subjoined.put('\u0f93', "g+h")
        cls.m_tib_subjoined.put('\u0f94', "ng")
        cls.m_tib_subjoined.put('\u0f95', "c")
        cls.m_tib_subjoined.put('\u0f96', "ch")
        cls.m_tib_subjoined.put('\u0f97', "j")
        cls.m_tib_subjoined.put('\u0f99', "ny")
        cls.m_tib_subjoined.put('\u0f9a', "T")
        cls.m_tib_subjoined.put('\u0f9b', "Th")
        cls.m_tib_subjoined.put('\u0f9c', "D")
        cls.m_tib_subjoined.put('\u0f9d', "D+h")
        cls.m_tib_subjoined.put('\u0f9e', "N")
        cls.m_tib_subjoined.put('\u0f9f', "t")
        cls.m_tib_subjoined.put('\u0fa0', "th")
        cls.m_tib_subjoined.put('\u0fa1', "d")
        cls.m_tib_subjoined.put('\u0fa2', "d+h")
        cls.m_tib_subjoined.put('\u0fa3', "n")
        cls.m_tib_subjoined.put('\u0fa4', "p")
        cls.m_tib_subjoined.put('\u0fa5', "ph")
        cls.m_tib_subjoined.put('\u0fa6', "b")
        cls.m_tib_subjoined.put('\u0fa7', "b+h")
        cls.m_tib_subjoined.put('\u0fa8', "m")
        cls.m_tib_subjoined.put('\u0fa9', "ts")
        cls.m_tib_subjoined.put('\u0faa', "tsh")
        cls.m_tib_subjoined.put('\u0fab', "dz")
        cls.m_tib_subjoined.put('\u0fac', "dz+h")
        cls.m_tib_subjoined.put('\u0fad', "w")
        cls.m_tib_subjoined.put('\u0fae', "zh")
        cls.m_tib_subjoined.put('\u0faf', "z")
        cls.m_tib_subjoined.put('\u0fb0', "'")
        cls.m_tib_subjoined.put('\u0fb1', "y")
        cls.m_tib_subjoined.put('\u0fb2', "r")
        cls.m_tib_subjoined.put('\u0fb3', "l")
        cls.m_tib_subjoined.put('\u0fb4', "sh")
        cls.m_tib_subjoined.put('\u0fb5', "Sh")
        cls.m_tib_subjoined.put('\u0fb6', "s")
        cls.m_tib_subjoined.put('\u0fb7', "h")
        cls.m_tib_subjoined.put('\u0fb8', "a")
        cls.m_tib_subjoined.put('\u0fb9', "k+Sh")
        cls.m_tib_subjoined.put('\u0fba', "W")
        cls.m_tib_subjoined.put('\u0fbb', "Y")
        cls.m_tib_subjoined.put('\u0fbc', "R")
        #  vowel signs:
        #  a-chen is not here because that's a top character, not a vowel sign.
        #  pre-composed "I" and "U" are dealt here; other pre-composed Skt vowels are more
        #  easily handled by a global replace in toWylie(), b/c they turn into subjoined "r"/"l".
        cls.m_tib_vowel = HashMap()
        cls.m_tib_vowel.put('\u0f71', "A")
        cls.m_tib_vowel.put('\u0f72', "i")
        cls.m_tib_vowel.put('\u0f73', "I")
        cls.m_tib_vowel.put('\u0f74', "u")
        cls.m_tib_vowel.put('\u0f75', "U")
        cls.m_tib_vowel.put('\u0f7a', "e")
        cls.m_tib_vowel.put('\u0f7b', "ai")
        cls.m_tib_vowel.put('\u0f7c', "o")
        cls.m_tib_vowel.put('\u0f7d', "au")
        cls.m_tib_vowel.put('\u0f80', "-i")
        #  long (Skt) vowels
        cls.m_tib_vowel_long = HashMap()
        cls.m_tib_vowel_long.put("i", "I")
        cls.m_tib_vowel_long.put("u", "U")
        cls.m_tib_vowel_long.put("-i", "-I")
        #  final symbols => wylie
        cls.m_tib_final_wylie = HashMap()
        cls.m_tib_final_wylie.put('\u0f7e', "M")
        cls.m_tib_final_wylie.put('\u0f82', "~M`")
        cls.m_tib_final_wylie.put('\u0f83', "~M")
        cls.m_tib_final_wylie.put('\u0f37', "X")
        cls.m_tib_final_wylie.put('\u0f35', "~X")
        cls.m_tib_final_wylie.put('\u0f39', "^")
        cls.m_tib_final_wylie.put('\u0f7f', "H")
        cls.m_tib_final_wylie.put('\u0f84', "?")
        #  final symbols by class
        cls.m_tib_final_class = HashMap()
        cls.m_tib_final_class.put('\u0f7e', "M")
        cls.m_tib_final_class.put('\u0f82', "M")
        cls.m_tib_final_class.put('\u0f83', "M")
        cls.m_tib_final_class.put('\u0f37', "X")
        cls.m_tib_final_class.put('\u0f35', "X")
        cls.m_tib_final_class.put('\u0f39', "^")
        cls.m_tib_final_class.put('\u0f7f', "H")
        cls.m_tib_final_class.put('\u0f84', "?")
        #  special characters introduced by ^
        cls.m_tib_caret = HashMap()
        cls.m_tib_caret.put("ph", "f")
        cls.m_tib_caret.put("b", "v")
        #  other stand-alone characters
        cls.m_tib_other = HashMap()
        cls.m_tib_other.put(' ', "_")
        cls.m_tib_other.put('\u0f04', "@")
        cls.m_tib_other.put('\u0f05', "#")
        cls.m_tib_other.put('\u0f06', "$")
        cls.m_tib_other.put('\u0f07', "%")
        cls.m_tib_other.put('\u0f08', "!")
        cls.m_tib_other.put('\u0f0b', " ")
        cls.m_tib_other.put('\u0f0c', "*")
        cls.m_tib_other.put('\u0f0d', "/")
        cls.m_tib_other.put('\u0f0e', "//")
        cls.m_tib_other.put('\u0f0f', ";")
        cls.m_tib_other.put('\u0f11', "|")
        cls.m_tib_other.put('\u0f14', ":")
        cls.m_tib_other.put('\u0f20', "0")
        cls.m_tib_other.put('\u0f21', "1")
        cls.m_tib_other.put('\u0f22', "2")
        cls.m_tib_other.put('\u0f23', "3")
        cls.m_tib_other.put('\u0f24', "4")
        cls.m_tib_other.put('\u0f25', "5")
        cls.m_tib_other.put('\u0f26', "6")
        cls.m_tib_other.put('\u0f27', "7")
        cls.m_tib_other.put('\u0f28', "8")
        cls.m_tib_other.put('\u0f29', "9")
        cls.m_tib_other.put('\u0f34', "=")
        cls.m_tib_other.put('\u0f3a', "<")
        cls.m_tib_other.put('\u0f3b', ">")
        cls.m_tib_other.put('\u0f3c', "(")
        cls.m_tib_other.put('\u0f3d', ")")
        #  all these stacked consonant combinations don't need "+"s in them
        cls.m_tib_stacks = HashSet()
        cls.m_tib_stacks.add("b+l")
        cls.m_tib_stacks.add("b+r")
        cls.m_tib_stacks.add("b+y")
        cls.m_tib_stacks.add("c+w")
        cls.m_tib_stacks.add("d+r")
        cls.m_tib_stacks.add("d+r+w")
        cls.m_tib_stacks.add("d+w")
        cls.m_tib_stacks.add("dz+r")
        cls.m_tib_stacks.add("g+l")
        cls.m_tib_stacks.add("g+r")
        cls.m_tib_stacks.add("g+r+w")
        cls.m_tib_stacks.add("g+w")
        cls.m_tib_stacks.add("g+y")
        cls.m_tib_stacks.add("h+r")
        cls.m_tib_stacks.add("h+w")
        cls.m_tib_stacks.add("k+l")
        cls.m_tib_stacks.add("k+r")
        cls.m_tib_stacks.add("k+w")
        cls.m_tib_stacks.add("k+y")
        cls.m_tib_stacks.add("kh+r")
        cls.m_tib_stacks.add("kh+w")
        cls.m_tib_stacks.add("kh+y")
        cls.m_tib_stacks.add("l+b")
        cls.m_tib_stacks.add("l+c")
        cls.m_tib_stacks.add("l+d")
        cls.m_tib_stacks.add("l+g")
        cls.m_tib_stacks.add("l+h")
        cls.m_tib_stacks.add("l+j")
        cls.m_tib_stacks.add("l+k")
        cls.m_tib_stacks.add("l+ng")
        cls.m_tib_stacks.add("l+p")
        cls.m_tib_stacks.add("l+t")
        cls.m_tib_stacks.add("l+w")
        cls.m_tib_stacks.add("m+r")
        cls.m_tib_stacks.add("m+y")
        cls.m_tib_stacks.add("n+r")
        cls.m_tib_stacks.add("ny+w")
        cls.m_tib_stacks.add("p+r")
        cls.m_tib_stacks.add("p+y")
        cls.m_tib_stacks.add("ph+r")
        cls.m_tib_stacks.add("ph+y")
        cls.m_tib_stacks.add("ph+y+w")
        cls.m_tib_stacks.add("r+b")
        cls.m_tib_stacks.add("r+d")
        cls.m_tib_stacks.add("r+dz")
        cls.m_tib_stacks.add("r+g")
        cls.m_tib_stacks.add("r+g+w")
        cls.m_tib_stacks.add("r+g+y")
        cls.m_tib_stacks.add("r+j")
        cls.m_tib_stacks.add("r+k")
        cls.m_tib_stacks.add("r+k+y")
        cls.m_tib_stacks.add("r+l")
        cls.m_tib_stacks.add("r+m")
        cls.m_tib_stacks.add("r+m+y")
        cls.m_tib_stacks.add("r+n")
        cls.m_tib_stacks.add("r+ng")
        cls.m_tib_stacks.add("r+ny")
        cls.m_tib_stacks.add("r+t")
        cls.m_tib_stacks.add("r+ts")
        cls.m_tib_stacks.add("r+ts+w")
        cls.m_tib_stacks.add("r+w")
        cls.m_tib_stacks.add("s+b")
        cls.m_tib_stacks.add("s+b+r")
        cls.m_tib_stacks.add("s+b+y")
        cls.m_tib_stacks.add("s+d")
        cls.m_tib_stacks.add("s+g")
        cls.m_tib_stacks.add("s+g+r")
        cls.m_tib_stacks.add("s+g+y")
        cls.m_tib_stacks.add("s+k")
        cls.m_tib_stacks.add("s+k+r")
        cls.m_tib_stacks.add("s+k+y")
        cls.m_tib_stacks.add("s+l")
        cls.m_tib_stacks.add("s+m")
        cls.m_tib_stacks.add("s+m+r")
        cls.m_tib_stacks.add("s+m+y")
        cls.m_tib_stacks.add("s+n")
        cls.m_tib_stacks.add("s+n+r")
        cls.m_tib_stacks.add("s+ng")
        cls.m_tib_stacks.add("s+ny")
        cls.m_tib_stacks.add("s+p")
        cls.m_tib_stacks.add("s+p+r")
        cls.m_tib_stacks.add("s+p+y")
        cls.m_tib_stacks.add("s+r")
        cls.m_tib_stacks.add("s+t")
        cls.m_tib_stacks.add("s+ts")
        cls.m_tib_stacks.add("s+w")
        cls.m_tib_stacks.add("sh+r")
        cls.m_tib_stacks.add("sh+w")
        cls.m_tib_stacks.add("t+r")
        cls.m_tib_stacks.add("t+w")
        cls.m_tib_stacks.add("th+r")
        cls.m_tib_stacks.add("ts+w")
        cls.m_tib_stacks.add("tsh+w")
        cls.m_tib_stacks.add("z+l")
        cls.m_tib_stacks.add("z+w")
        cls.m_tib_stacks.add("zh+w")
        #  a map used to split the input string into tokens for toUnicode().
        #  all letters which start tokens longer than one letter are mapped to the max length of
        #  tokens starting with that letter.  
        cls.m_tokens_start = HashMap()
        cls.m_tokens_start.put('S', 2)
        cls.m_tokens_start.put('/', 2)
        cls.m_tokens_start.put('d', 4)
        cls.m_tokens_start.put('g', 3)
        cls.m_tokens_start.put('b', 3)
        cls.m_tokens_start.put('D', 3)
        cls.m_tokens_start.put('z', 2)
        cls.m_tokens_start.put('~', 3)
        cls.m_tokens_start.put('-', 4)
        cls.m_tokens_start.put('T', 2)
        cls.m_tokens_start.put('a', 2)
        cls.m_tokens_start.put('k', 2)
        cls.m_tokens_start.put('t', 3)
        cls.m_tokens_start.put('s', 2)
        cls.m_tokens_start.put('c', 2)
        cls.m_tokens_start.put('n', 2)
        cls.m_tokens_start.put('p', 2)
        cls.m_tokens_start.put('\r', 2)
        #  also for tokenization - a set of tokens longer than one letter
        cls.m_tokens = HashSet()
        cls.m_tokens.add("-d+h")
        cls.m_tokens.add("dz+h")
        cls.m_tokens.add("-dh")
        cls.m_tokens.add("-sh")
        cls.m_tokens.add("-th")
        cls.m_tokens.add("D+h")
        cls.m_tokens.add("b+h")
        cls.m_tokens.add("d+h")
        cls.m_tokens.add("dzh")
        cls.m_tokens.add("g+h")
        cls.m_tokens.add("tsh")
        cls.m_tokens.add("~M`")
        cls.m_tokens.add("-I")
        cls.m_tokens.add("-d")
        cls.m_tokens.add("-i")
        cls.m_tokens.add("-n")
        cls.m_tokens.add("-t")
        cls.m_tokens.add("//")
        cls.m_tokens.add("Dh")
        cls.m_tokens.add("Sh")
        cls.m_tokens.add("Th")
        cls.m_tokens.add("ai")
        cls.m_tokens.add("au")
        cls.m_tokens.add("bh")
        cls.m_tokens.add("ch")
        cls.m_tokens.add("dh")
        cls.m_tokens.add("dz")
        cls.m_tokens.add("gh")
        cls.m_tokens.add("kh")
        cls.m_tokens.add("ng")
        cls.m_tokens.add("ny")
        cls.m_tokens.add("ph")
        cls.m_tokens.add("sh")
        cls.m_tokens.add("th")
        cls.m_tokens.add("ts")
        cls.m_tokens.add("zh")
        cls.m_tokens.add("~M")
        cls.m_tokens.add("~X")
        cls.m_tokens.add("\r\n")

    @classmethod
    def initSloppyRepl(cls):
        i = 0
        cls.base[i] = "ʼ"
        cls.repl[i] = "'"
        i += 1
        #  0x02BC
        cls.base[i] = "ʹ"
        cls.repl[i] = "'"
        i += 1
        #  0x02B9
        cls.base[i] = "‘"
        cls.repl[i] = "'"
        i += 1
        #  0x2018
        cls.base[i] = "’"
        cls.repl[i] = "'"
        i += 1
        #  0x2019
        cls.base[i] = "ʾ"
        cls.repl[i] = "'"
        i += 1
        #  0x02BE
        cls.base[i] = "x"
        cls.repl[i] = "\\u0fbe"
        i += 1
        cls.base[i] = "X"
        cls.repl[i] = "\\u0fbe"
        i += 1
        cls.base[i] = "..."
        cls.repl[i] = "\\u0f0b\\u0f0b\\u0f0b"
        i += 1
        cls.base[i] = " ("
        cls.repl[i] = "_("
        i += 1
        cls.base[i] = ") "
        cls.repl[i] = ")_"
        i += 1
        cls.base[i] = "/ "
        cls.repl[i] = "/_"
        i += 1
        cls.base[i] = " 0"
        cls.repl[i] = "_0"
        i += 1
        cls.base[i] = " 1"
        cls.repl[i] = "_1"
        i += 1
        cls.base[i] = " 2"
        cls.repl[i] = "_2"
        i += 1
        cls.base[i] = " 3"
        cls.repl[i] = "_3"
        i += 1
        cls.base[i] = " 4"
        cls.repl[i] = "_4"
        i += 1
        cls.base[i] = " 5"
        cls.repl[i] = "_5"
        i += 1
        cls.base[i] = " 6"
        cls.repl[i] = "_6"
        i += 1
        cls.base[i] = " 7"
        cls.repl[i] = "_7"
        i += 1
        cls.base[i] = " 8"
        cls.repl[i] = "_8"
        i += 1
        cls.base[i] = " 9"
        cls.repl[i] = "_9"
        i += 1
        cls.base[i] = "_ "
        cls.repl[i] = "__"
        i += 1
        cls.base[i] = "G"
        cls.repl[i] = "g"
        i += 1
        cls.base[i] = "K"
        cls.repl[i] = "k"
        i += 1
        cls.base[i] = "G."
        cls.repl[i] = "g."
        i += 1
        cls.base[i] = "C"
        cls.repl[i] = "c"
        i += 1
        cls.base[i] = "B"
        cls.repl[i] = "b"
        i += 1
        cls.base[i] = " b "
        cls.repl[i] = " ba "
        i += 1
        cls.base[i] = " m "
        cls.repl[i] = " ma "
        i += 1
        cls.base[i] = " m'i "
        cls.repl[i] = " ma'i "
        i += 1
        cls.base[i] = " b'i "
        cls.repl[i] = " ba'i "
        i += 1
        cls.base[i] = "P"
        cls.repl[i] = "p"
        i += 1
        cls.base[i] = "L"
        cls.repl[i] = "l"
        i += 1
        cls.base[i] = " M"
        cls.repl[i] = " m"
        i += 1
        cls.base[i] = "(M"
        cls.repl[i] = "(m"
        i += 1
        cls.base[i] = "Z"
        cls.repl[i] = "z"
        i += 1

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
    # 	* remove spaces after newlines, collapse multiple tseks into one, etc
    # 	
    @overloaded
    def __init__(self, check, check_strict, print_warnings, fix_spacing):
        self.initWylie(check, check_strict, print_warnings, fix_spacing, self.Mode.EWTS)

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
    @__init__.register(object, bool, bool, bool, bool, self.Mode)
    def __init___0(self, check, check_strict, print_warnings, fix_spacing, mode):
        self.initWylie(check, check_strict, print_warnings, fix_spacing, mode)

    # 
    #     * Default constructor, sets the following defaults:
    #     * <ul>
    #     *   <li>check: true</li>
    #     *   <li>check_strict: true</li>
    #     *   <li>print_warning: false</li>
    #     *   <li>fix_spacing: true</li>
    #     * </ul> 
    #     
    @__init__.register(object)
    def __init___1(self):
        self.initWylie(True, True, False, True, self.Mode.EWTS)

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
        return self.m_special.contains(s)

    def isSuperscript(self, s):
        return self.m_superscripts.containsKey(s)

    def superscript(self, sup, below):
        tmpSet = self.m_superscripts.get(sup)
        if tmpSet == None:
            return False
        return tmpSet.contains(below)

    def isSubscript(self, s):
        return self.m_subscripts.containsKey(s)

    def subscript(self, sub, above):
        tmpSet = self.m_subscripts.get(sub)
        if tmpSet == None:
            return False
        return tmpSet.contains(above)

    def isPrefix(self, s):
        return self.m_prefixes.containsKey(s)

    def prefix(self, pref, after):
        tmpSet = self.m_prefixes.get(pref)
        if tmpSet == None:
            return False
        return tmpSet.contains(after)

    def isSuffix(self, s):
        return self.m_suffixes.contains(s)

    def isSuff2(self, s):
        return self.m_suff2.containsKey(s)

    def suff2(self, suff, before):
        tmpSet = self.m_suff2.get(suff)
        if tmpSet == None:
            return False
        return tmpSet.contains(before)

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
        return self.m_tib_stacks.contains(s)

    #  split a string into Converter tokens; 
    #  make sure there is room for at least one null element at the end of the array
    def splitIntoTokens(self, inputstr):
        tokens = [None] * 2 + len(inputstr)
        o = 0
        i = 0
        maxlen = len(inputstr)
        while i < maxlen:
            c = inputstr.charAt(i)
            mlo = self.m_tokens_start.get(c)
            #  if there are multi-char tokens starting with this char, try them
            if mlo != None:
                len = mlo.intValue()
                while len > 1:
                    if i <= maxlen - len:
                        tr = inputstr.substring(i, i + len)
                        if self.m_tokens.contains(tr):
                            o += 1
                            tokens[o] = tr
                            i += len
                            len -= 1
                            continue # TODO: was a named continue
                    len -= 1
            #  things starting with backslash are special
            if c == '\\' and i <= maxlen - 2:
                if inputstr.charAt(i + 1) == 'u' and i <= maxlen - 6:
                    o += 1
                    tokens[o] = inputstr.substring(i, i + 6)
                    #  \\uxxxx
                    i += 6
                elif inputstr.charAt(i + 1) == 'U' and i <= maxlen - 10:
                    o += 1
                    tokens[o] = inputstr.substring(i, i + 10)
                    #  \\Uxxxxxxxx
                    i += 10
                else:
                    o += 1
                    tokens[o] = inputstr.substring(i, i + 2)
                    #  \\x
                    i += 2
                continue 
            #  otherwise just take one char
            o += 1
            tokens[o] = Character.toString(c)
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
        inputstr = StringUtils.replaceEach(inputstr, cls.base, cls.repl)
        #  convert S but not Sh:
        inputstr = inputstr.replace("Sh", "ZZZ")
        inputstr = inputstr.replace("S", "s")
        inputstr = inputstr.replace("ZZZ", "Sh")
        if inputstr.startsWith("M"):
            inputstr = "m" + inputstr.substring(1)
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
    #     * Converts a string to Unicode, fixes common EWTS errors.
    #     *  
    #     * @param str
    #     * the string to convert
    #     * @return
    #     * the converted string
    #     
    @overloaded
    def toUnicode(self, inputstr):
        return self.toUnicode(inputstr, None, True)

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
    @toUnicode.register(object, str, List, bool)
    def toUnicode_0(self, inputstr, warns, sloppy):
        if inputstr == None:
            return " - no data - "
        out = StringBuilder()
        line = 1
        units = 0
        if self.mode == self.Mode.DWTS or self.mode == self.Mode.DTS:
            inputstr = TransConverter.dtsToEwts(inputstr)
        elif self.mode == self.Mode.ALALC:
            inputstr = TransConverter.alalcToEwts(inputstr)
        #  remove initial spaces if required
        if self.fix_spacing:
            inputstr = inputstr.replaceFirst("^\\s+", "")
        if sloppy:
            inputstr = self.normalizeSloppyWylie(inputstr)
        #  split into tokens
        tokens = self.splitIntoTokens(inputstr)
        i = 0
        #  iterate over the tokens
        __i_5 = i
        i += 1
        while tokens[i] != None:
            t = tokens[i]
            o = None
            #  [non-tibetan text] : pass through, nesting brackets
            if t == "[":
                nesting = 1
                i += 1
                while tokens[i] != None:
                    t = tokens[__i_5]
                    if t == "[":
                        nesting += 1
                    if t == "]":
                        nesting -= 1
                    if nesting == 0:
                        continue # TODO: named
                    #  handle unicode escapes and \1-char escapes within [comments]...
                    if t.startsWith("\\u") or t.startsWith("\\U"):
                        o = unicodeEscape(warns, line, t)
                        if o != None:
                            out.append(o)
                            continue  # TODO: named
                    if t.startsWith("\\"):
                        o = t.substring(1)
                    else:
                        o = t
                    out.append(o)
                warnl(warns, line, "Unfinished [non-Converter stuff].")
                break # TODO: labelled
            #  punctuation, numbers, etc
            o = self.other(t)
            if o != None:
                out.append(o)
                i += 1
                units += 1
                #  collapse multiple spaces?
                if t == " " and self.fix_spacing:
                    while tokens[i] != None and tokens[i] == " ":
                continue # TODO: labelled
            if self.vowel(t) != None or self.consonant(t) != None:
                tb = toUnicodeOneTsekbar(tokens, i)
                word = StringBuilder()
                j = 0
                while j < tb.tokens_used:
                    word.append(tokens[i + j])
                    j += 1
                out.append(tb.uni_string)
                i += tb.tokens_used
                units += 1
                for w in tb.warns:
                    warnl(warns, line, "\"" + word.__str__() + "\": " + w)
                continue  # TODO: named
            if t == "\ufeff" or t == "\u200b":
                i += 1
                continue # TODO: labelled
            if t.startsWith("\\u") or t.startsWith("\\U"):
                o = unicodeEscape(warns, line, t)
                if o != None:
                    i += 1
                    out.append(o)
                    continue  # TODO: named
            if t.startsWith("\\"):
                out.append(t.substring(1))
                i += 1
                continue # TODO: labelled
            if t == "\r\n" or t == "\n" or t == "\r":
                line += 1
                out.append(t)
                i += 1
                if self.fix_spacing:
                    while tokens[i] != None and tokens[i] == " ":
                continue  # TODO: named
            c = t.charAt(0)
            if self.isSpecial(t) or (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                warnl(warns, line, "Unexpected character \"" + t + "\".")
            out.append(t)
            i += 1
        if units == 0:
            warn(warns, "No Tibetan characters found!")
        if self.check_strict:
            if 0 > len(out) and self.isCombining(out.charAt(0)):
                warn(warns, "String starts with combining character '" + out.charAt(0) + "'")
        return out.__str__()

    def validHex(self, t):
        i = 0
        while i < len(t):
            c = t.charAt(i)
            if not ((c >= 'a' and c <= 'f') or (c >= '0' and c <= '9')):
                return False
            i += 1
        return True

    def unicodeEscape(self, warns, line, t):
        hex = t.substring(2)
        if hex.isEmpty():
            return None
        if not self.validHex(hex):
            warnl(warns, line, "\"" + t + "\": invalid hex code.")
            return ""
        return Character.valueOf(str(Integer.parseInt(hex, 16))).__str__()

    def warn(self, warns, inputstr):
        if warns != None:
            warns.add(inputstr)
        if self.print_warnings:
            print(inputstr)

    def warnl(self, warns, line, inputstr):
        self.warn(warns, "line " + line + ": " + inputstr)

    @SuppressWarnings("unused")
    def debug(self, inputstr):
        print(inputstr)

    @SuppressWarnings("unused")
    def debugvar(self, o, name):
        print(">>" + name + "<< : (" + ("NULL" if o == None else o.__str__()) + ")")

    def joinStrings(self, a, sep):
        out = StringBuilder()
        len = len(a)
        i = 0
        for v in a:
            out.append(v)
            if sep != None and i < len - 1:
                out.append(sep)
            i += 1
        return out.__str__()

    @SuppressWarnings("unused")
    def toUnicodeOneStack(self, tokens, i):
        orig_i = i
        t = None
        t2 = None
        o = None
        out = StringBuilder()
        warns = ArrayList()
        consonants = 0
        vowel_found = None
        vowel_sign = None
        single_consonant = None
        plus = False
        caret = 0
        final_found = HashMap()
        t = tokens[i]
        t2 = tokens[i + 1]
        if t2 != None and self.isSuperscript(t) and self.superscript(t, t2):
            if self.check_strict:
                next = consonantString(tokens, i + 1)
                if not self.superscript(t, next):
                    next = next.replace("+", "")
                    warns.add("Superscript \"" + t + "\" does not occur above combination \"" + next + "\".")
            out.append(self.consonant(t))
            consonants += 1
            i += 1
            while tokens[i] != None and tokens[i] == "^":
                caret += 1
                i += 1
        while True:
            t = tokens[i]
            if self.consonant(t) != None or (0 > len(out) and self.subjoined(t) != None):
                if 0 > len(out):
                    out.append(self.subjoined(t))
                else:
                    out.append(self.consonant(t))
                i += 1
                if t == "a":
                    vowel_found = "a"
                else:
                    consonants += 1
                    single_consonant = t
                while tokens[i] != None and tokens[i] == "^":
                    caret += 1
                    i += 1
                z = 0
                while z < 2:
                    t2 = tokens[i]
                    if t2 != None and self.isSubscript(t2):
                        if t2 == "l" and consonants > 1:
                            break
                        if self.check_strict and not plus:
                            prev = consonantStringBackwards(tokens, i - 1, orig_i)
                            if not self.subscript(t2, prev):
                                prev = prev.replace("+", "")
                                warns.add("Subjoined \"" + t2 + "\" not expected after \"" + prev + "\".")
                        elif self.check:
                            if not self.subscript(t2, t) and not (z == 1 and t2 == "w" and t == "y"):
                                warns.add("Subjoined \"" + t2 + "\"not expected after \"" + t + "\".")
                        out.append(self.subjoined(t2))
                        i += 1
                        consonants += 1
                        while tokens[i] != None and tokens[i] == "^":
                            caret += 1
                            i += 1
                        t = t2
                    else:
                        break
                    z += 1
            if caret > 0:
                if caret > 1:
                    warns.add("Cannot have more than one \"^\" applied to the same stack.")
                final_found.put(self.final_class("^"), "^")
                out.append(self.final_uni("^"))
                caret = 0
            t = tokens[i]
            if t != None and self.vowel(t) != None:
                if 0 == len(out):
                    out.append(self.vowel("a"))
                if not t == "a":
                    out.append(self.vowel(t))
                i += 1
                vowel_found = t
                if not t == "a":
                    vowel_sign = t
            t = tokens[i]
            if t != None and t == "+":
                i += 1
                plus = True
                t = tokens[i]
                if t == None or (self.vowel(t) == None and self.subjoined(t) == None):
                    if self.check:
                        warns.add("Expected vowel or consonant after \"+\".")
                    break # TODO: labelled
                if self.check:
                    if self.vowel(t) == None and vowel_sign != None:
                        warns.add("Cannot subjoin consonant (" + t + ") after vowel (" + vowel_sign + ") in same stack.")
                    elif t == "a" and vowel_sign != None:
                        warns.add("Cannot subjoin a-chen (a) after vowel (" + vowel_sign + ") in same stack.")
                continue # TODO: labelled
            break # TODO: labelled
        t = tokens[i]
        while t != None and self.final_class(t) != None:
            uni = self.final_uni(t)
            klass = self.final_class(t)
            if final_found.containsKey(klass):
                if final_found.get(klass) == t:
                    warns.add("Cannot have two \"" + t + "\" applied to the same stack.")
                else:
                    warns.add("Cannot have \"" + t + "\" and \"" + final_found.get(klass) + "\" applied to the same stack.")
            else:
                final_found.put(klass, t)
                out.append(uni)
            i += 1
            single_consonant = None
            t = tokens[i]
        if tokens[i] != None and tokens[i] == ".":
            i += 1
        if consonants > 1 and vowel_found == None:
            if plus:
                if self.check:
                    warns.add("Stack with multiple consonants should end with vowel.")
            else:
                i = orig_i + 1
                consonants = 1
                single_consonant = tokens[orig_i]
                out.setLength(0)
                out.append(self.consonant(single_consonant))
        if consonants != 1 or plus:
            single_consonant = None
        ret = WylieStack()
        ret.uni_string = out.__str__()
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
        ret.visarga = final_found.containsKey("H")
        return ret

    @SuppressWarnings("unused")
    def toUnicodeOneTsekbar(self, tokens, i):
        orig_i = i
        t = tokens[i]
        stack = None
        prev_cons = None
        visarga = False
        check_root = True
        consonants = ArrayList()
        root_idx = -1
        out = StringBuilder()
        warns = ArrayList()
        state = State.PREFIX
        while t != None and (self.vowel(t) != None or self.consonant(t) != None) and not visarga:
            if stack != None:
                prev_cons = stack.single_consonant
            stack = self.toUnicodeOneStack(tokens, i)
            i += stack.tokens_used
            t = tokens[i]
            out.append(stack.uni_string)
            warns.addAll(stack.warns)
            visarga = stack.visarga
            if not self.check:
                continue 
            if state == State.PREFIX and stack.single_consonant != None:
                consonants.add(stack.single_consonant)
                if self.isPrefix(stack.single_consonant):
                    next = t
                    if self.check_strict:
                        next = consonantString(tokens, i)
                    if next != None and not self.prefix(stack.single_consonant, next):
                        next = next.replace("+", "")
                        warns.add("Prefix \"" + stack.single_consonant + "\" does not occur before \"" + next + "\".")
                else:
                    warns.add("Invalid prefix consonant: \"" + stack.single_consonant + "\".")
                state = State.MAIN
            elif stack.single_consonant == None:
                state = State.SUFF1
                if root_idx >= 0:
                    check_root = False
                elif stack.single_cons_a != None:
                    consonants.add(stack.single_cons_a)
                    root_idx = len(consonants) - 1
            elif state == State.MAIN:
                warns.add("Expected vowel after \"" + stack.single_consonant + "\".")
            elif state == State.SUFF1:
                consonants.add(stack.single_consonant)
                if self.check_strict:
                    if not self.isSuffix(stack.single_consonant):
                        warns.add("Invalid suffix consonant: \"" + stack.single_consonant + "\".")
                state = State.SUFF2
            elif state == State.SUFF2:
                consonants.add(stack.single_consonant)
                if self.isSuff2(stack.single_consonant):
                    if not self.suff2(stack.single_consonant, prev_cons):
                        warns.add("Second suffix \"" + stack.single_consonant + "\" does not occur after \"" + prev_cons + "\".")
                else:
                    if not self.m_affixedsuff2.contains(stack.single_consonant) or not prev_cons == "'":
                        warns.add("Invalid 2nd suffix consonant: \"" + stack.single_consonant + "\".")
                state = State.NONE
            elif state == State.NONE:
                warns.add("Cannot have another consonant \"" + stack.single_consonant + "\" after 2nd suffix.")
        if state == State.MAIN and stack.single_consonant != None and self.isPrefix(stack.single_consonant):
            warns.add("Vowel expected after \"" + stack.single_consonant + "\".")
        if self.check and len(warns) == 0 and check_root and root_idx >= 0:
            if len(consonants) == 2 and root_idx != 0 and self.prefix(consonants.get(0), consonants.get(1)) and self.isSuffix(consonants.get(1)):
                warns.add("Syllable should probably be \"" + consonants.get(0) + "a" + consonants.get(1) + "\".")
            elif len(consonants) == 3 and self.isPrefix(consonants.get(0)) and self.suff2("s", consonants.get(1)) and consonants.get(2) == "s":
                cc = self.joinStrings(consonants, "")
                cc = cc.replace('\u2018', '\'')
                cc = cc.replace('\u2019', '\'')
                expect_key = self.ambiguous_key(cc)
                if expect_key != None and expect_key.intValue() != root_idx:
                    warns.add("Syllable should probably be \"" + self.ambiguous_wylie(cc) + "\".")
        ret = WylieTsekbar()
        ret.uni_string = out.__str__()
        ret.tokens_used = i - orig_i
        ret.warns = warns
        return ret

    def consonantString(self, tokens, i):
        out = ArrayList()
        t = None
        __i_6 = i
        i += 1
        while tokens[i] != None:
            t = tokens[__i_6]
            if t == "+" or t == "^":
                continue 
            if self.consonant(t) == None:
                break
            out.add(t)
        return self.joinStrings(out, "+")

    def consonantStringBackwards(self, tokens, i, orig_i):
        out = LinkedList()
        t = None
        __i_7 = i
        i -= 1
        while i >= orig_i and tokens[i] != None:
            t = tokens[__i_7]
            if t == "+" or t == "^":
                continue 
            if self.consonant(t) == None:
                break
            out.addFirst(t)
        return self.joinStrings(out, "+")

    @overloaded
    def toWylie(self, inputstr):
        return self.toWylie(inputstr, None, True)

    @toWylie.register(object, str, List, bool)
    def toWylie_0(self, inputstr, warns, escape):
        out = StringBuilder()
        line = 1
        inputstr = inputstr.replace("\u0f76", "\u0fb2\u0f80")
        inputstr = inputstr.replace("\u0f77", "\u0fb2\u0f71\u0f80")
        inputstr = inputstr.replace("\u0f78", "\u0fb3\u0f80")
        inputstr = inputstr.replace("\u0f79", "\u0fb3\u0f71\u0f80")
        inputstr = inputstr.replace("\u0f81", "\u0f71\u0f80")
        inputstr = inputstr.replace("\u0F75", "\u0F71\u0F74")
        inputstr = inputstr.replace("\u0F73", "\u0F71\u0F72")
        i = 0
        len = len(inputstr)
        i += 1
        while i < len:
            t = inputstr.charAt(i)
            if self.tib_top(t) != None:
                tb = toWylieOneTsekbar(inputstr, len, i)
                out.append(tb.wylie)
                i += tb.tokens_used
                for w in tb.warns:
                    self.warnl(warns, line, w)
                if not escape:
                    i += handleSpaces(inputstr, i, out)
                continue # TODO: labelled
            o = self.tib_other(t)
            if o != None and (t != ' ' or (escape and not followedByNonTibetan(inputstr, i))):
                out.append(o)
                i += 1
                if not escape:
                    i += handleSpaces(inputstr, i, out)
                continue # TODO: labelled
            if t == '\r' or t == '\n':
                line += 1
                i += 1
                out.append(t)
                if t == '\r' and i < len and inputstr.charAt(i) == '\n':
                    i += 1
                    out.append('\n')
                continue # TODO: labelled
            if t == '\ufeff' or t == '\u200b':
                i += 1
                continue # TODO: labelled
            if not escape:
                out.append(t)
                i += 1
                continue # TODO: labelled
            if t >= '\u0f00' and t <= '\u0fff':
                c = formatHex(t)
                out.append(c)
                i += 1
                if self.tib_subjoined(t) != None or self.tib_vowel(t) != None or self.tib_final_wylie(t) != None:
                    self.warnl(warns, line, "Tibetan sign " + c + " needs a top symbol to attach to.")
                continue # TODO: labelled
            out.append("[")
            while self.tib_top(t) == None and (self.tib_other(t) == None or t == ' ') and t != '\r' and t != '\n':
                if t == '[' or t == ']':
                    out.append("\\")
                    out.append(t)
                elif t >= '\u0f00' and t <= '\u0fff':
                    out.append(formatHex(t))
                else:
                    out.append(t)
                if i >= len:
                    break
                t = inputstr.charAt(i)
            out.append("]")
        return out.__str__()

    def formatHex(self, t):
        sb = StringBuilder()
        sb.append("\\u")
        s = Integer.toHexString(int(t))
        i = len(s)
        while i < 4:
            sb.append('0')
            i += 1
        sb.append(s)
        return sb.__str__()

    def handleSpaces(self, inputstr, i, out):
        found = 0
        orig_i = i
        while i < len(inputstr) and inputstr.charAt(i) == ' ':
            i += 1
            found += 1
        if found == 0 or i == len(inputstr):
            return 0
        t = inputstr.charAt(i)
        if self.tib_top(t) == None and self.tib_other(t) == None:
            return 0
        while i < found:
            out.append('_')
            i += 1
        return found

    def followedByNonTibetan(self, inputstr, i):
        len = len(inputstr)
        while i < len and inputstr.charAt(i) == ' ':
            i += 1
        if i == len:
            return False
        t = inputstr.charAt(i)
        return self.tib_top(t) == None and self.tib_other(t) == None and t != '\r' and t != '\n'

    def toWylieOneTsekbar(self, inputstr, len, i):
        orig_i = i
        warns = ArrayList()
        stacks = ArrayList()
        while True:
            st = toWylieOneStack(inputstr, len, i)
            stacks.add(st)
            warns.addAll(st.warns)
            i += st.tokens_used
            if st.visarga:
                break
            if i >= len or self.tib_top(inputstr.charAt(i)) == None:
                break
        last = len(stacks) - 1
        if len(stacks) > 1 and stacks.get(0).single_cons != None:
            cs = stacks.get(1).cons_str.replace("+w", "")
            if self.prefix(stacks.get(0).single_cons, cs):
                stacks.get(0).prefix = True
        if len(stacks) > 1 and stacks.get(last).single_cons != None and self.isSuffix(stacks.get(last).single_cons):
            stacks.get(last).suffix = True
        if len(stacks) > 2 and stacks.get(last).single_cons != None and stacks.get(last - 1).single_cons != None and self.isSuffix(stacks.get(last - 1).single_cons) and self.suff2(stacks.get(last).single_cons, stacks.get(last - 1).single_cons):
            stacks.get(last).suff2 = True
            stacks.get(last - 1).suffix = True
        if len(stacks) == 2 and stacks.get(0).prefix and stacks.get(1).suffix:
            stacks.get(0).prefix = False
        if len(stacks) == 3 and stacks.get(0).prefix and stacks.get(1).suffix and stacks.get(2).suff2:
            strb = StringBuilder()
            for st in stacks:
                strb.append(st.single_cons)
            ztr = strb.__str__()
            root = self.ambiguous_key(ztr)
            if root == None:
                warns.add("Ambiguous syllable found: root consonant not known for \"" + ztr + "\".")
                root = 1
            stacks.get(root).prefix = stacks.get(root).suffix = False
            stacks.get(root + 1).suff2 = False
        if stacks.get(0).prefix and self.tib_stack(stacks.get(0).single_cons + "+" + stacks.get(1).cons_str):
            stacks.get(0).dot = True
        out = StringBuilder()
        for st in stacks:
            out.append(putStackTogether(st))
        ret = ToWylieTsekbar()
        ret.wylie = out.__str__()
        ret.tokens_used = i - orig_i
        ret.warns = warns
        return ret

    def toWylieOneStack(self, inputstr, len, i):
        orig_i = i
        ffinal = None
        vowel = None
        klass = None
        st = ToWylieStack()
        __i_9 = i
        i += 1
        t = inputstr.charAt(__i_9)
        st.top = self.tib_top(t)
        st.stack.add(self.tib_top(t))
        while i < len:
            t = inputstr.charAt(i)
            o = None
            if (o = self.tib_subjoined(t)) != None:
                i += 1
                st.stack.add(o)
                if not st.finals.isEmpty():
                    st.warns.add("Subjoined sign \"" + o + "\" found after final sign \"" + ffinal + "\".")
                elif not st.vowels.isEmpty():
                    st.warns.add("Subjoined sign \"" + o + "\" found after vowel sign \"" + vowel + "\".")
            elif (o = self.tib_vowel(t)) != None:
                i += 1
                st.vowels.add(o)
                if vowel == None:
                    vowel = o
                if not st.finals.isEmpty():
                    st.warns.add("Vowel sign \"" + o + "\" found after final sign \"" + ffinal + "\".")
            elif (o = self.tib_final_wylie(t)) != None:
                i += 1
                klass = self.tib_final_class(t)
                if o == "^":
                    st.caret = True
                else:
                    if o == "H":
                        st.visarga = True
                    st.finals.add(o)
                    if ffinal == None:
                        ffinal = o
                    if st.finals_found.containsKey(klass):
                        st.warns.add("Final sign \"" + o + "\" should not combine with found after final sign \"" + ffinal + "\".")
                    else:
                        st.finals_found.put(klass, o)
            else:
                break
        if st.top == "a" and len(st.stack) == 1 and not st.vowels.isEmpty():
            st.stack.removeFirst()
        if len(st.vowels) > 1 and st.vowels.get(0) == "A" and self.tib_vowel_long(st.vowels.get(1)) != None:
            l = self.tib_vowel_long(st.vowels.get(1))
            st.vowels.removeFirst()
            st.vowels.removeFirst()
            st.vowels.addFirst(l)
        if st.caret and len(st.stack) == 1 and self.tib_caret(st.top) != None:
            l = self.tib_caret(st.top)
            st.top = l
            st.stack.removeFirst()
            st.stack.addFirst(l)
            st.caret = False
        st.cons_str = self.joinStrings(st.stack, "+")
        if len(st.stack) == 1 and not st.stack.get(0) == "a" and not st.caret and st.vowels.isEmpty() and st.finals.isEmpty():
            st.single_cons = st.cons_str
        st.tokens_used = i - orig_i
        return st

    def putStackTogether(self, st):
        out = StringBuilder()
        if self.tib_stack(st.cons_str):
            out.append(self.joinStrings(st.stack, ""))
        else:
            out.append(st.cons_str)
        if st.caret:
            out.append("^")
        if not st.vowels.isEmpty():
            out.append(self.joinStrings(st.vowels, "+"))
        elif not st.prefix and not st.suffix and not st.suff2 and (st.cons_str.isEmpty() or st.cons_str.charAt(1 - len(length)) != 'a'):
            out.append("a")
        out.append(self.joinStrings(st.finals, ""))
        if st.dot:
            out.append(".")
        return out.__str__()

    class State:
        PREFIX = u'PREFIX'
        MAIN = u'MAIN'
        SUFF1 = u'SUFF1'
        SUFF2 = u'SUFF2'
        NONE = u'NONE'

    class WylieStack(object):
        uni_string = None
        tokens_used = int()
        single_consonant = None
        single_cons_a = None
        warns = None
        visarga = bool()

    class WylieTsekbar(object):
        uni_string = None
        tokens_used = int()
        warns = None

    class ToWylieStack(object):
        top = None
        stack = None
        caret = bool()
        vowels = None
        finals = None
        finals_found = None
        visarga = bool()
        cons_str = None
        single_cons = None
        prefix = bool()
        suffix = bool()
        suff2 = bool()
        dot = bool()
        tokens_used = int()
        warns = None

        def __init__(self):
                self.stack = LinkedList()
            self.vowels = LinkedList()
            self.finals = ArrayList()
            self.finals_found = HashMap()
            self.warns = ArrayList()

    class ToWylieTsekbar(object):
        wylie = None
        tokens_used = int()
        warns = None
