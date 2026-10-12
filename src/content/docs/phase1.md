# Phase 1 · Conditional Logic

Every program makes decisions. This phase teaches you to turn a sentence like *"if the number is divisible by both 3 and 5, say Both"* into code that is correct for **every** input, including the awkward ones.

## 1. How a LogicQuest problem looks

You only write the body of `solve(...)`. Reading input and printing the answer are already done for you below the dotted line.

```java
static String solve(int n) {
    if (n > 0) return "Positive";
    if (n < 0) return "Negative";
    return "Zero";
}
```

```python
def solve(n):
    if n > 0:
        return "Positive"
    if n < 0:
        return "Negative"
    return "Zero"
```

```javascript
function solve(n) {
  if (n > 0) return "Positive";
  if (n < 0) return "Negative";
  return "Zero";
}
```

**Run** checks the examples you can see. **Submit** checks hidden tests too, and that is where edge cases live.

## 2. if / else if / else

A chain is checked **top to bottom** and the first true branch wins. Order matters.

```java
if (n % 15 == 0) result = "Both";      // most specific first
else if (n % 3 == 0) result = "Three";
else if (n % 5 == 0) result = "Five";
else result = "Neither";
```

```python
if n % 15 == 0:
    result = "Both"        # most specific first
elif n % 3 == 0:
    result = "Three"
elif n % 5 == 0:
    result = "Five"
else:
    result = "Neither"
```

```javascript
if (n % 15 === 0) result = "Both";      // most specific first
else if (n % 3 === 0) result = "Three";
else if (n % 5 === 0) result = "Five";
else result = "Neither";
```

> **Rule of thumb:** put the most specific condition first. If `n % 3 == 0` came first, 15 would print "Three".

## 3. Combining conditions

| Meaning | Java | Python | JavaScript |
| --- | --- | --- | --- |
| and | `a && b` | `a and b` | `a && b` |
| or | `a \|\| b` | `a or b` | `a \|\| b` |
| not | `!a` | `not a` | `!a` |
| equal | `a == b` | `a == b` | `a === b` (always three `=`) |

Leap years combine all three: divisible by 400, **or** (divisible by 4 **and not** divisible by 100).

## 4. The modulo trap

`%` gives the remainder.

:::only java
The sign of the result follows the **left** number, so `-7 % 2` is `-1`. Integer division truncates toward zero: `-7 / 2` is `-3`.
:::

:::only python
The sign of the result follows the **divisor**, so `-7 % 2` is `1`. Floor division rounds down: `-7 // 2` is `-4`.
:::

:::only javascript
The sign of the result follows the **left** number, so `-7 % 2` is `-1`. `/` keeps decimals (`-7 / 2` is `-3.5`); `Math.trunc(-7 / 2)` drops them toward zero and gives `-3`.
:::

```java
System.out.println(-7 % 2);  // -1, not 1!
```

```python
print(-7 % 2)   # 1 (the sign follows the divisor)
print(-7 // 2)  # -4 (floor division rounds down)
```

```javascript
console.log(-7 % 2);             // -1, not 1
console.log(Math.trunc(-7 / 2)); // -3: "/" gives -3.5, so drop the decimals yourself
```

:::only java
So `n % 2 == 1` breaks for negative odd numbers. Use `n % 2 != 0` or `n % 2 == 0` instead.
:::

:::only python
`n % 2 == 1` is safe for negative odd numbers, because the remainder is never negative. When a problem instead wants truncation toward zero, do not use `//`. Use `int(a / b)`, and take the remainder as `a - b * int(a / b)`.
:::

:::only javascript
So `n % 2 === 1` breaks for negative odd numbers. Use `n % 2 !== 0` or `n % 2 === 0` instead.
:::

## 5. Characters are numbers

Every character has a code: `'A'` is 65, `'a'` is 97, `'0'` is 48. Letters and digits are consecutive, so range checks work:

```java
boolean upper = ch >= 'A' && ch <= 'Z';
int digitValue = ch - '0';           // '7' -> 7
char lower = (char) (ch + 32);       // 'A' -> 'a'
```

```python
upper = "A" <= ch <= "Z"
digit_value = ord(ch) - ord("0")     # '7' -> 7
lower = chr(ord(ch) + 32)            # 'A' -> 'a'
```

```javascript
const upper = ch >= "A" && ch <= "Z";
const digitValue = ch.charCodeAt(0) - 48;              // '7' -> 7
const lower = String.fromCharCode(ch.charCodeAt(0) + 32); // 'A' -> 'a'
```

## 6. switch for one value, many cases

:::only java
`switch` picks one branch from a single value. When you `return` immediately, you do not need `break`.
:::

:::only python
`match` (3.10 and later) picks one branch from a single value. An `if` / `elif` chain does the same thing on older versions.
:::

:::only javascript
`switch` picks one branch from a single value, comparing with `===`. When you `return` immediately, you do not need `break`.
:::

```java
switch (op) {
    case '+': return String.valueOf(a + b);
    case '-': return String.valueOf(a - b);
    default:  return "Error";
}
```

```python
match op:              # 3.10+; an if/elif chain works on older versions
    case "+":
        return str(a + b)
    case "-":
        return str(a - b)
    case _:
        return "Error"
```

```javascript
switch (op) {
  case "+": return String(a + b);
  case "-": return String(a - b);
  default:  return "Error";
}
```

## 7. Overflow

:::only java
An `int` holds about ±2.1 billion. `100000 * 100000 * 100000` does not fit, and the result silently wraps to a wrong number. Use `long` when a product can get big. A `long` holds about ±9 × 10^18.
:::

:::only python
Integers grow as large as you need; they never overflow. Some problems still ask you to *detect* when a value leaves the 32-bit range (about ±2.1 billion) and clamp it or return 0.
:::

:::only javascript
Numbers stay exact only up to 2^53 (about 9 × 10^15). Past that, the value silently loses precision. Use `BigInt` (`10n`, `BigInt(x)`) when an answer can exceed that. The starter code tells you when.
:::

## 8. Shortcuts and the Pure challenge

Library helpers like `sort`, `Set`, `max()` or `reverse()` do the thinking for you, and this course is about doing the thinking yourself. You can still use them: a correct answer is accepted and earns XP. But LogicQuest notices them and opens a **Pure challenge** for that problem: solve it again with only loops, conditions, arrays and strings for **+50% bonus XP**. The editor shows which shortcuts it spotted while you type.

## 9. A habit to keep

Before you code, write down 3–4 inputs and their answers: a normal one, zero, a negative, and the boundary (like exactly 38 marks, or exactly 100 units). Most wrong answers in this phase come from boundaries.
