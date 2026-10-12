# Phase 2 · Loops, Repetition & Patterns

Loops let one piece of code handle a thousand inputs. This phase covers three loop skills you will use in every later problem: **accumulating**, **pulling digits apart**, and **nested loops**.

## 1. The three loop shapes

```java
for (int i = 1; i <= n; i++) { ... }     // you know how many times
while (n > 0) { ... }                      // you know when to stop
do { ... } while (cond);                   // runs at least once
```

```python
for i in range(1, n + 1):   # 1..n inclusive
    ...
while n > 0:
    ...
```

`range(a, b)` stops **before** `b`. Most off-by-one bugs come from forgetting that.

## 2. Accumulators

Decide what the variable means **before** the loop, and give it the right starting value.

| Goal | Start value |
| --- | --- |
| sum | 0 |
| product | 1 |
| count | 0 |
| max | the first element (not 0!) |

```java
long sum = 0;
for (int i = 1; i <= n; i++) sum += i;
```

```python
total = 0
for i in range(1, n + 1):
    total += i
```

## 3. Pulling digits apart

`% 10` gives the last digit, `/ 10` removes it. This one loop powers digit sums, reversing numbers, palindromes and Armstrong numbers.

```java
int temp = n;
while (temp > 0) {
    int d = temp % 10;
    // use d
    temp /= 10;
}
```

```python
temp = n
while temp > 0:
    d = temp % 10
    # use d
    temp //= 10
```

Work on a **copy** (`temp`) when you still need the original `n` later.

To **build** a number digit by digit: `rev = rev * 10 + d`.

## 4. Stopping early

`break` leaves the loop, `continue` skips to the next round. For primes, you can stop at √x:

```java
for (int d = 2; (long) d * d <= x; d++) {
    if (x % d == 0) return false;
}
return true;
```

```python
d = 2
while d * d <= x:
    if x % d == 0:
        return False
    d += 1
return True
```

## 5. Nested loops and patterns

The outer loop picks the **row**, the inner loop draws what is **in** that row. Before coding a pattern, fill this table for n = 4:

| row i | spaces | stars |
| --- | --- | --- |
| 1 | 3 | 1 |
| 2 | 2 | 3 |
| 3 | 1 | 5 |
| 4 | 0 | 7 |

Now you can read the formulas: spaces = n − i, stars = 2i − 1.

```java
for (int i = 1; i <= n; i++) {
    StringBuilder row = new StringBuilder();
    for (int s = 0; s < n - i; s++) row.append(' ');
    for (int k = 0; k < 2 * i - 1; k++) row.append('*');
    System.out.println(row);
}
```

```python
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))
```

## 6. Print vs return

Pattern problems use **print mode**: `solve` prints directly. In Java, `System.out.print` stays on the line and `System.out.println` ends it. In Python, `print(x, end=" ")` stays on the line.

## 7. Loops that might never end

Happy Number can cycle forever. Whenever your loop condition depends on a value that can repeat, ask: *what guarantees this stops?* If nothing does, track what you have seen or find the cycle.
