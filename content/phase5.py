from core import problem

PH = 5


def rand_word(r, alpha="abcdefghijklmnopqrstuvwxyz", lo=1, hi=50):
    return "".join(r.choice(alpha) for _ in range(r.randint(lo, hi)))


@problem(phase=PH, title="Defang an IP", returns="str", concepts=["building a new string"],
         statement="""
         Replace every `.` in an IPv4 address with `[.]` and return the result.

         Build the result yourself with a StringBuilder (Java) or a list of characters (Python) instead of `replace`.

         **Constraints:** a valid IPv4 address
         """,
         params=[("address", "str")],
         tests=[("1.1.1.1",), ("255.100.50.0",), ("0.0.0.0",), ("192.168.1.10",), ("10.0.0.255",)],
         hints=["Walk the string one character at a time. What do you append for a normal character?",
                "What do you append instead when the character is '.'?",
                "Java: StringBuilder sb; sb.append(c == '.' ? \"[.]\" : String.valueOf(c))."],
         practice=("LeetCode 1108: Defanging an IP Address", "https://leetcode.com/problems/defanging-an-ip-address/"))
def defang(address):
    return address.replace(".", "[.]")


@problem(phase=PH, title="To Lower Case", returns="str", concepts=["char arithmetic"],
         statement="""
         Return `s` with every uppercase letter changed to lowercase, **without** `toLowerCase` / `lower()`.

         **Constraints:** 1 ≤ s.length ≤ 100, printable ASCII
         """,
         params=[("s", "str")],
         tests=[("Hello",), ("here",), ("LOVELY",), ("Mixed 123 CASE!",), ("@[`{",)],
         hints=["What is the numeric distance between 'A' and 'a'?",
                "Which characters should you leave untouched?",
                "If 'A' <= c <= 'Z', use (char)(c + 32). Python: chr(ord(c) + 32)."],
         practice=("LeetCode 709: To Lower Case", "https://leetcode.com/problems/to-lower-case/"))
def to_lower(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


@problem(phase=PH, title="Jewels and Stones", returns="int", concepts=["membership check"],
         statement="""
         Each character in `jewels` is a type of jewel. Return how many characters in `stones` are jewels.
         Letters are case-sensitive.

         **Constraints:** 1 ≤ jewels.length, stones.length ≤ 50, letters only, jewels are distinct
         """,
         params=[("jewels", "str"), ("stones", "str")],
         tests=[("aA", "aAAbbbb"), ("z", "ZZ"), ("abc", "abc"), ("x", "xxxxx"), ("AbC", "abcABC")],
         hints=["For one stone, how do you decide whether it is a jewel?",
                "Nested loops over the two strings work fine at this size.",
                "Bonus: a boolean[128] lookup table makes the check O(1)."],
         practice=("LeetCode 771: Jewels and Stones", "https://leetcode.com/problems/jewels-and-stones/"))
def jewels(jewels, stones):
    return sum(1 for c in stones if c in jewels)


@problem(phase=PH, title="Balanced Halves", returns="bool", concepts=["counting vowels"],
         statement="""
         Split `s` (even length) into two halves. Return `true` if both halves contain the same number of vowels
         (a, e, i, o, u, upper or lower case).

         **Constraints:** 2 ≤ s.length ≤ 1000, even length, letters only
         """,
         params=[("s", "str")],
         tests=[("book",), ("textbook",), ("AbCdEfGh",), ("aa",), ("ab",)],
         gen=lambda r: (rand_word(r, "aeiouAEIOUbcdxyzBCD", 1, 500) * 2,), gen_count=2,
         hints=["Write an isVowel(c) helper first.",
                "Which indexes belong to the first half?",
                "Count vowels in [0, n/2) and [n/2, n) and compare."],
         practice=("LeetCode 1704: Determine if String Halves Are Alike",
                   "https://leetcode.com/problems/determine-if-string-halves-are-alike/"))
def halves(s):
    v = set("aeiouAEIOU")
    h = len(s) // 2
    return sum(c in v for c in s[:h]) == sum(c in v for c in s[h:])


@problem(phase=PH, title="Reverse Each Word", returns="str", concepts=["word boundaries"],
         statement="""
         Reverse the characters of every word while keeping the word order and single spaces.

         **Constraints:** 1 ≤ s.length ≤ 5·10^4, words separated by exactly one space, no leading/trailing spaces
         """,
         params=[("s", "str")],
         tests=[("Let's take LeetCode contest",), ("Mr Ding",), ("a",), ("ab cd ef",), ("racecar level",)],
         hints=["How do you find where a word starts and ends?",
                "Once you know a word's start and end index, you already know how to reverse it.",
                "Loop with i; find j = end of word; reverse s[i..j−1]; continue from j + 1."],
         practice=("LeetCode 557: Reverse Words in a String III",
                   "https://leetcode.com/problems/reverse-words-in-a-string-iii/"))
def rev_each(s):
    return " ".join(w[::-1] for w in s.split(" "))


@problem(phase=PH, title="Valid Palindrome", returns="bool", concepts=["two pointers", "skipping characters"],
         statement="""
         Ignoring case and every non-alphanumeric character, return `true` if `s` reads the same both ways.
         Solve it with two pointers, without building a cleaned copy.

         **Constraints:** 1 ≤ s.length ≤ 2·10^5
         """,
         params=[("s", "str")],
         tests=[("A man, a plan, a canal: Panama",), ("race a car",), (" ",), ("0P",), ("Madam, I'm Adam",), (".,",)],
         hints=["Put one pointer at each end. When should a pointer skip a character?",
                "After skipping, compare the two characters case-insensitively.",
                "while l < r: skip non-alnum on both sides; if they differ return false; l++, r--."],
         practice=("LeetCode 125: Valid Palindrome", "https://leetcode.com/problems/valid-palindrome/"))
def valid_palin(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]


@problem(phase=PH, title="Length of Last Word", returns="int", concepts=["scanning from the end"],
         statement="""
         `s` contains words and spaces (possibly trailing spaces). Return the length of the last word.

         **Constraints:** 1 ≤ s.length ≤ 10^4, at least one word
         """,
         params=[("s", "str")],
         tests=[("Hello World",), ("   fly me   to   the moon  ",), ("luffy is still joyboy",), ("a",), ("a ",), ("  ab",)],
         hints=["Which end of the string is the last word closer to?",
                "What do you skip first when scanning from the end?",
                "i = n−1; skip spaces; then count non-spaces."],
         practice=("LeetCode 58: Length of Last Word", "https://leetcode.com/problems/length-of-last-word/"))
def last_word(s):
    return len(s.split()[-1])


@problem(phase=PH, title="Detect Capital", returns="bool", concepts=["counting categories"],
         statement="""
         A word uses capitals correctly if it is all caps (`USA`), all lowercase (`leetcode`),
         or only the first letter is capital (`Google`). Return `true` if `word` is correct.

         **Constraints:** 1 ≤ word.length ≤ 100, letters only
         """,
         params=[("word", "str")],
         tests=[("USA",), ("FlaG",), ("leetcode",), ("Google",), ("g",), ("G",), ("gOOGLE",)],
         hints=["What one number describes each valid shape?",
                "Count the uppercase letters.",
                "Valid if count == 0, count == n, or (count == 1 and word[0] is uppercase)."],
         practice=("LeetCode 520: Detect Capital", "https://leetcode.com/problems/detect-capital/"))
def detect_capital(word):
    return word.isupper() or word.islower() or (word[0].isupper() and word[1:].islower()) or len(word) == 1


@problem(phase=PH, title="Pangram", returns="bool", concepts=["frequency array"],
         statement="""
         Return `true` if the lowercase sentence uses every letter a–z at least once.

         **Constraints:** 1 ≤ sentence.length ≤ 1000, lowercase letters only
         """,
         params=[("sentence", "str")],
         tests=[("thequickbrownfoxjumpsoverthelazydog",), ("leetcode",), ("abcdefghijklmnopqrstuvwxyz",),
                ("abcdefghijklmnopqrstuvwxy",), ("zyxwvutsrqponmlkjihgfedcbaa",)],
         hints=["How can you remember which letters you have seen?",
                "`c - 'a'` turns a letter into an index 0..25.",
                "boolean[26] seen; mark each letter; check all 26 are true."],
         practice=("LeetCode 1832: Check if the Sentence Is Pangram",
                   "https://leetcode.com/problems/check-if-the-sentence-is-pangram/"))
def pangram(sentence):
    return len(set(sentence)) == 26


@problem(phase=PH, title="Valid Anagram", returns="bool", concepts=["frequency array"],
         statement="""
         Return `true` if `t` is a rearrangement of `s`. Do not sort.

         **Constraints:** 1 ≤ s.length, t.length ≤ 5·10^4, lowercase letters
         """,
         params=[("s", "str"), ("t", "str")],
         tests=[("anagram", "nagaram"), ("rat", "car"), ("a", "ab"), ("ab", "ba"), ("aacc", "ccac")],
         gen=lambda r: (lambda w: (w, "".join(r.sample(w, len(w)))))(rand_word(r, "abc", 1000, 50000)), gen_count=1,
         hints=["If the lengths differ, can they be anagrams?",
                "Count each letter of s, then 'un-count' each letter of t.",
                "int[26] count; count[s[i]-'a']++, count[t[i]-'a']--; all zero means anagram."],
         practice=("LeetCode 242: Valid Anagram", "https://leetcode.com/problems/valid-anagram/"))
def anagram(s, t):
    return sorted(s) == sorted(t)


@problem(phase=PH, title="First Unique Character", returns="int", concepts=["two passes with counts"],
         statement="""
         Return the index of the first character that appears exactly once in `s`, or −1.

         **Constraints:** 1 ≤ s.length ≤ 10^5, lowercase letters
         """,
         params=[("s", "str")],
         tests=[("leetcode",), ("loveleetcode",), ("aabb",), ("z",), ("aabbc",)],
         gen=lambda r: (rand_word(r, "abcdefghijklmnopqrstuvwxy", 10**4, 10**5) * 2 + "z",), gen_count=1,
         hints=["Can you know a character is unique before you have seen the whole string?",
                "First pass: count. Second pass: find.",
                "int[26] freq; then return the first i with freq[s[i]-'a'] == 1."],
         practice=("LeetCode 387: First Unique Character in a String",
                   "https://leetcode.com/problems/first-unique-character-in-a-string/"))
def first_unique(s):
    from collections import Counter
    c = Counter(s)
    for i, ch in enumerate(s):
        if c[ch] == 1:
            return i
    return -1


@problem(phase=PH, title="Ransom Note", returns="bool", concepts=["frequency array"],
         statement="""
         Return `true` if `note` can be built from the letters of `magazine`, each letter used at most once.

         **Constraints:** 1 ≤ lengths ≤ 10^5, lowercase letters
         """,
         params=[("note", "str"), ("magazine", "str")],
         tests=[("a", "b"), ("aa", "ab"), ("aa", "aab"), ("abc", "cba"), ("zzz", "zz")],
         hints=["Which string's letters are the 'supply'?",
                "Count the supply, then spend from it.",
                "If any count goes below zero, return false."],
         practice=("LeetCode 383: Ransom Note", "https://leetcode.com/problems/ransom-note/"))
def ransom(note, magazine):
    from collections import Counter
    return not (Counter(note) - Counter(magazine))


@problem(phase=PH, title="Reverse Only Vowels", returns="str", concepts=["two pointers"],
         statement="""
         Reverse only the vowels of `s` (a e i o u, both cases); everything else stays in place.

         **Constraints:** 1 ≤ s.length ≤ 3·10^5, printable ASCII
         """,
         params=[("s", "str")],
         tests=[("hello",), ("leetcode",), ("aA",), ("xyz",), ("IceCreAm",)],
         hints=["Which two characters swap first?",
                "Move each pointer until it lands on a vowel.",
                "Convert to a char array; swap when both pointers are on vowels; move inward."],
         practice=("LeetCode 345: Reverse Vowels of a String", "https://leetcode.com/problems/reverse-vowels-of-a-string/"))
def rev_vowels(s):
    v = [c for c in s if c in "aeiouAEIOU"]
    return "".join(v.pop() if c in "aeiouAEIOU" else c for c in s)


@problem(phase=PH, title="Is Subsequence", returns="bool", concepts=["two indexes"],
         statement="""
         Return `true` if `s` can be obtained from `t` by deleting some characters without reordering.
         `s` may be empty.

         **Constraints:** 0 ≤ s.length ≤ 100, 0 ≤ t.length ≤ 10^4, lowercase letters
         """,
         params=[("s", "str"), ("t", "str")],
         tests=[("abc", "ahbgdc"), ("axc", "ahbgdc"), ("", "abc"), ("abc", "abc"), ("aaa", "aa")],
         hints=["Walk through t. When do you move forward in s?",
                "When is the answer known to be true?",
                "i over s, j over t; if s[i] == t[j] then i++; always j++. True if i reaches s.length."],
         practice=("LeetCode 392: Is Subsequence", "https://leetcode.com/problems/is-subsequence/"))
def is_subseq(s, t):
    it = iter(t)
    return all(c in it for c in s)


@problem(phase=PH, title="Longest Common Prefix", returns="str", concepts=["column scan"],
         statement="""
         Return the longest prefix shared by every string in `strs` (may be empty).

         **Constraints:** 1 ≤ strs.length ≤ 200, 0 ≤ strs[i].length ≤ 200
         """,
         params=[("strs", "str[]")],
         tests=[(["flower", "flow", "flight"],), (["dog", "racecar", "car"],), (["alone"],), (["ab", "a"],),
                (["interview", "internet", "interval"],)],
         hints=["Compare the strings column by column. Which column comes first?",
                "When must you stop?",
                "For i = 0..: if any string is too short or differs at i, return the prefix so far."],
         practice=("LeetCode 14: Longest Common Prefix", "https://leetcode.com/problems/longest-common-prefix/"))
def lcp(strs):
    import os
    return os.path.commonprefix(strs)


@problem(phase=PH, title="Find the Substring", returns="int", concepts=["nested loops on strings"],
         statement="""
         Return the first index where `needle` occurs in `haystack`, or −1. No `indexOf` / `find`.

         **Constraints:** 1 ≤ lengths ≤ 10^4
         """,
         params=[("haystack", "str"), ("needle", "str")],
         tests=[("sadbutsad", "sad"), ("leetcode", "leeto"), ("a", "a"), ("abc", "c"), ("aaa", "aaaa"), ("mississippi", "issip")],
         hints=["At which starting positions could needle possibly fit?",
                "For one start position, how do you check a match?",
                "for i in 0..n−m: compare needle[j] with haystack[i + j] for all j."],
         practice=("LeetCode 28: Find the Index of the First Occurrence in a String",
                   "https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/"))
def strstr(haystack, needle):
    return haystack.find(needle)


@problem(phase=PH, title="Rotate String", returns="bool", concepts=["modulo indexing"],
         statement="""
         A shift moves the first character of `s` to the end. Return `true` if `s` can become `goal`
         after some number of shifts.

         **Constraints:** 1 ≤ lengths ≤ 100
         """,
         params=[("s", "str"), ("goal", "str")],
         tests=[("abcde", "cdeab"), ("abcde", "abced"), ("a", "a"), ("ab", "abc"), ("aa", "aa")],
         hints=["How many different shifts are there?",
                "For a shift by k, which character of s lands at position i?",
                "Try every k: goal[i] == s[(i + k) % n] for all i. (Bonus: think about s + s.)"],
         practice=("LeetCode 796: Rotate String", "https://leetcode.com/problems/rotate-string/"))
def rotate_str(s, goal):
    return len(s) == len(goal) and goal in s + s


@problem(phase=PH, title="Isomorphic Strings", difficulty="medium", returns="bool", concepts=["mapping arrays"],
         statement="""
         Two strings are isomorphic if each character of `s` can be replaced to get `t`, where every occurrence
         maps the same way and no two characters map to the same character.

         **Constraints:** 1 ≤ s.length == t.length ≤ 5·10^4, printable ASCII
         """,
         params=[("s", "str"), ("t", "str")],
         tests=[("egg", "add"), ("foo", "bar"), ("paper", "title"), ("badc", "baba"), ("a", "b")],
         hints=["What goes wrong in foo → bar? What goes wrong in badc → baba?",
                "One mapping s→t is not enough. Why?",
                "Keep two char arrays of size 128: mapST and mapTS; check both directions at each index."],
         practice=("LeetCode 205: Isomorphic Strings", "https://leetcode.com/problems/isomorphic-strings/"))
def isomorphic(s, t):
    return len(set(s)) == len(set(t)) == len(set(zip(s, t)))


@problem(phase=PH, title="Roman to Integer", returns="int", concepts=["look-ahead"],
         statement="""
         Convert a Roman numeral to an integer. I=1, V=5, X=10, L=50, C=100, D=500, M=1000.
         A smaller value before a larger one is subtracted (IV = 4, CM = 900).

         **Constraints:** valid numerals for 1 to 3999
         """,
         params=[("s", "str")],
         tests=[("III",), ("LVIII",), ("MCMXCIV",), ("IV",), ("MMMCMXCIX",), ("XLII",)],
         hints=["Write value(c) using a switch.",
                "When do you subtract a symbol instead of adding it?",
                "If value(s[i]) < value(s[i+1]) subtract it, else add it."],
         practice=("LeetCode 13: Roman to Integer", "https://leetcode.com/problems/roman-to-integer/"))
def roman_to_int(s):
    v = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and v[c] < v[s[i + 1]]:
            total -= v[c]
        else:
            total += v[c]
    return total


@problem(phase=PH, title="Add Binary", difficulty="medium", returns="str", concepts=["carry", "from the right"],
         statement="""
         Return the sum of two binary strings as a binary string. Do not convert them to numbers:
         they can be 10^4 digits long.

         **Constraints:** 1 ≤ a.length, b.length ≤ 10^4, no leading zeros except "0"
         """,
         params=[("a", "str"), ("b", "str")],
         tests=[("11", "1"), ("1010", "1011"), ("0", "0"), ("1", "111"), ("1" * 100, "1")],
         gen=lambda r: ("1" + rand_word(r, "01", 5000, 9999), "1" + rand_word(r, "01", 1, 9999)), gen_count=1,
         hints=["Which digits do you add first?",
                "What three values go into each column's sum?",
                "i, j from the ends; sum = carry + bits; append sum % 2; carry = sum / 2; reverse at the end."],
         practice=("LeetCode 67: Add Binary", "https://leetcode.com/problems/add-binary/"))
def add_binary(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]


@problem(phase=PH, title="Reverse the Words", difficulty="medium", returns="str", concepts=["splitting manually"],
         statement="""
         Reverse the order of the words. The input may have leading, trailing or multiple spaces;
         the output must have single spaces only.

         **Constraints:** 1 ≤ s.length ≤ 10^4, at least one word
         """,
         params=[("s", "str")],
         tests=[("the sky is blue",), ("  hello world  ",), ("a good   example",), ("x",), ("  one  ",)],
         hints=["First collect the words. How do you know where one ends?",
                "Then join them in reverse order.",
                "Scan from the end: skip spaces, take a word, append it with a separator."],
         practice=("LeetCode 151: Reverse Words in a String", "https://leetcode.com/problems/reverse-words-in-a-string/"))
def rev_words(s):
    return " ".join(reversed(s.split()))


@problem(phase=PH, title="String Compression", difficulty="medium", returns="str", concepts=["run-length counting"],
         statement="""
         Compress runs of the same character: `aabcccccaaa` → `a2bc5a3`. A run of length 1 is written
         as just the character; runs of 10 or more write all digits (`b12`). Return the compressed string.

         **Constraints:** 1 ≤ s.length ≤ 2000, printable ASCII without spaces
         """,
         params=[("s", "str")],
         tests=[("aabcccccaaa",), ("a",), ("abbbbbbbbbbbb",), ("abc",), ("zzzzzzzzzz",)],
         gen=lambda r: ("".join(r.choice("ab") * r.randint(1, 15) for _ in range(r.randint(1, 120))),), gen_count=1,
         hints=["How do you know where a run ends?",
                "After a run ends, what do you append?",
                "Inner while j < n and s[j] == s[i]; append s[i] and (j − i if > 1); i = j."],
         practice=("LeetCode 443: String Compression", "https://leetcode.com/problems/string-compression/"))
def compress(s):
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(s[i] + (str(j - i) if j - i > 1 else ""))
        i = j
    return "".join(out)
