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

```javascript
const s = "hello";
const c = s[0];            // "h" (a one-letter string)
const n = s.length;        // property, no ()
const arr = s.split("");   // when you need to modify
```

## 2. Strings are immutable

You cannot change a character inside a string. Every `s = s + c` creates a whole new string, which gets slow inside a loop. Build with:

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

```javascript
let result = "";
for (const c of s) {
  if (c !== " ") result += c;   // fine in modern JS engines; an array + join("") also works
}
```

## 3. Comparing strings

:::only java
`==` compares **references**, not text. Always use `a.equals(b)`. For a single `char`, `==` is fine because a `char` is a number.
:::

:::only python
`==` compares the characters. `"hi" == "hi"` is true.
:::

:::only javascript
`===` compares the characters, so `a === b` is the comparison to use. `==` coerces types; prefer `===`.
:::

```java
if (word.equals("Google")) ...       // correct
if (word == "Google") ...            // bug that sometimes "works"
```

## 4. Character arithmetic

| Task | Java | Python | JavaScript |
| --- | --- | --- | --- |
| letter → 0..25 | `c - 'a'` | `ord(c) - ord('a')` | `c.charCodeAt(0) - 97` |
| 0..25 → letter | `(char)('a' + i)` | `chr(ord('a') + i)` | `String.fromCharCode(97 + i)` |
| digit char → int | `c - '0'` | `int(c)` | `c.charCodeAt(0) - 48` |
| upper → lower | `(char)(c + 32)` | `chr(ord(c) + 32)` | `String.fromCharCode(c.charCodeAt(0) + 32)` |

## 5. Frequency arrays

Counting characters is the single most useful string trick. For lowercase letters, an array of 26 counters is all you need:

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

```javascript
const freq = new Array(26).fill(0);
for (const c of s) freq[c.charCodeAt(0) - 97]++;
```

:::only java
For any character in the ASCII range, use size 128 and index directly with the `char`.
:::

:::only python
For any character in the ASCII range, use size 128 and index with `ord(c)`.
:::

:::only javascript
For any character in the ASCII range, use size 128 and index with `c.charCodeAt(0)`.
:::

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

```javascript
const ok = (c) => /[a-z0-9]/i.test(c);   // or compare character codes yourself
while (l < r) {
  while (l < r && !ok(s[l])) l++;
  while (l < r && !ok(s[r])) r--;
  if (s[l].toLowerCase() !== s[r].toLowerCase()) return false;
  l++; r--;
}
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

```javascript
let i = 0;
while (i < n) {
  let j = i;
  while (j < n && s[j] === s[i]) j++;
  // the run is s.slice(i, j), length j - i
  i = j;
}
```

## 8. Grade-school arithmetic on strings

Adding binary or decimal strings: start from the **right**, keep a carry, append the remainder, carry the quotient, and reverse at the end. Phase 6 builds on this for multiplication.

:::only java
The digit you append is `sum % base` and the carry is `sum / base`.
:::

:::only python
The digit you append is `sum % base` and the carry is `sum // base`.
:::

:::only javascript
The digit you append is `sum % base` and the carry is `Math.floor(sum / base)`.
:::
