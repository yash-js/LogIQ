# Phase 5 · Working with Strings

A string is an array of characters with a few extra rules. Everything from Phase 4 applies, plus three new tools: **character arithmetic**, **frequency arrays**, and **building strings efficiently**.

## 1. Reading characters

```java
String s = "hello";
char c = s.charAt(0);          // 'h'
int n = s.length();            // method, with ()
char[] arr = s.toCharArray();  // when you need to modify
```

```python
s = "hello"
c = s[0]          # 'h'
n = len(s)
arr = list(s)     # when you need to modify
```

## 2. Strings are immutable

You cannot change a character inside a Java `String` or Python `str`. Every `s = s + c` creates a whole new string, which gets slow inside a loop. Build with:

```java
StringBuilder sb = new StringBuilder();
for (char c : s.toCharArray()) {
    if (c != ' ') sb.append(c);
}
String result = sb.toString();
```

```python
parts = []
for c in s:
    if c != " ":
        parts.append(c)
result = "".join(parts)
```

## 3. Comparing strings

In Java, `==` compares **references**, not text. Always use `a.equals(b)`. For single characters, `==` is fine because `char` is a number.

```java
if (word.equals("Google")) ...       // correct
if (word == "Google") ...            // bug that sometimes "works"
```

## 4. Character arithmetic

| Task | Java | Python |
| --- | --- | --- |
| letter → 0..25 | `c - 'a'` | `ord(c) - ord('a')` |
| 0..25 → letter | `(char)('a' + i)` | `chr(ord('a') + i)` |
| digit char → int | `c - '0'` | `int(c)` |
| upper → lower | `(char)(c + 32)` | `chr(ord(c) + 32)` |

## 5. Frequency arrays

Counting characters is the single most useful string trick. For lowercase letters, an `int[26]` is all you need:

```java
int[] freq = new int[26];
for (char c : s.toCharArray()) freq[c - 'a']++;
// anagram check: count s up, count t down, all zeros at the end
```

```python
freq = [0] * 26
for c in s:
    freq[ord(c) - ord("a")] += 1
```

For any ASCII character, use size 128 and index directly with `c`.

## 6. Two pointers on strings

Palindromes and reversing vowels use the same pattern as reversing an array, with an extra rule for which characters a pointer is allowed to stop on:

```java
while (l < r) {
    while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
    while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
    if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r))) return false;
    l++; r--;
}
```

```python
while l < r:
    while l < r and not s[l].isalnum():
        l += 1
    while l < r and not s[r].isalnum():
        r -= 1
    if s[l].lower() != s[r].lower():
        return False
    l += 1
    r -= 1
```

## 7. Runs and words

To process a run (same character repeated, or a word between spaces), use an inner loop that finds where it ends:

```java
int i = 0;
while (i < n) {
    int j = i;
    while (j < n && s.charAt(j) == s.charAt(i)) j++;
    // the run is s[i..j-1], length j - i
    i = j;
}
```

```python
i = 0
while i < n:
    j = i
    while j < n and s[j] == s[i]:
        j += 1
    # the run is s[i:j], length j - i
    i = j
```

## 8. Grade-school arithmetic on strings

Adding binary or decimal strings: start from the **right**, keep a carry, append `sum % base`, carry `sum / base`, and reverse at the end. Phase 6 builds on this for multiplication.
