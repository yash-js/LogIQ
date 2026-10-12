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

> **Rule of thumb:** put the most specific condition first. If `n % 3 == 0` came first, 15 would print "Three".

## 3. Combining conditions

| Meaning | Java | Python |
| --- | --- | --- |
| and | `a && b` | `a and b` |
| or | `a \|\| b` | `a or b` |
| not | `!a` | `not a` |

Leap years combine all three: divisible by 400, **or** (divisible by 4 **and not** divisible by 100).

## 4. The modulo trap

`%` gives the remainder. In Java the sign of the result follows the **left** number:

```java
System.out.println(-7 % 2);  // -1, not 1!
```

```python
print(-7 % 2)   # 1 (Python follows the right number)
print(-7 // 2)  # -4 (floor division rounds DOWN, Java's -7 / 2 is -3)
```

So `n % 2 == 1` breaks for negative odd numbers in Java. Use `n % 2 != 0` or `n % 2 == 0` instead.

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

## 6. switch for one value, many cases

```java
switch (op) {
    case '+': return String.valueOf(a + b);
    case '-': return String.valueOf(a - b);
    default:  return "Error";
}
```

```python
match op:              # Python 3.10+; an if/elif chain works everywhere
    case "+":
        return str(a + b)
    case "-":
        return str(a - b)
    case _:
        return "Error"
```

## 7. Overflow

A Java `int` holds about ±2.1 billion. `100000 * 100000 * 100000` does not fit, and Java will silently give a wrong number. Use `long` when a product can get big. Python integers never overflow, but the problem may still ask you to *detect* when a value leaves the 32-bit range.

## 8. A habit to keep

Before you code, write down 3–4 inputs and their answers: a normal one, zero, a negative, and the boundary (like exactly 38 marks, or exactly 100 units). Most wrong answers in this phase come from boundaries.
