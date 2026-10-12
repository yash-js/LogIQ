# Phase 2 · Loops, Repetition & Patterns

Loops let one piece of code handle a thousand inputs. This phase covers three loop skills you will use in every later problem: **accumulating**, **pulling digits apart**, and **nested loops**.

## 1. The three loop shapes

```java
for (int i = 1; i <= n; i++) { ... }   // you know how many times
while (n > 0) { ... }                   // you know when to stop
do { ... } while (cond);                // runs at least once
```

```python
for i in range(1, n + 1):   # 1..n inclusive
    ...
while n > 0:
    ...
```

```javascript
for (let i = 1; i <= n; i++) { ... }   // you know how many times
while (n > 0) { ... }                   // you know when to stop
do { ... } while (cond);                // runs at least once
```

A loop that runs n times goes either from 1 to n or from 0 to n − 1. Mixing the two up is the most common off-by-one bug.

:::only java
Write `i <= n` to include n, and `i < n` to stop just before it.
:::

:::only python
`range(a, b)` stops **before** `b`, so `range(1, n + 1)` is 1 through n.
:::

:::only javascript
Write `i <= n` to include n, and `i < n` to stop just before it.
:::

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

```javascript
let sum = 0;
for (let i = 1; i <= n; i++) sum += i;
```

## 3. Pulling digits apart

`% 10` gives the last digit. Dividing by 10 drops it. This one loop powers digit sums, reversing numbers, palindromes and Armstrong numbers.

:::only java
`temp /= 10` removes the last digit. `/` on whole numbers truncates toward zero.
:::

:::only python
`temp //= 10` removes the last digit. `/` would leave a float; `//` is floor division, which for a positive digit is the drop you want.
:::

:::only javascript
`temp = Math.floor(temp / 10)` removes the last digit. `/` alone keeps the decimals.
:::

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

```javascript
let temp = n;
while (temp > 0) {
  const d = temp % 10;
  // use d
  temp = Math.floor(temp / 10);   // "/" alone keeps the decimals
}
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

```javascript
for (let d = 2; d * d <= x; d++) {
  if (x % d === 0) return false;
}
return true;
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

```javascript
for (let i = 1; i <= n; i++) {
  let row = "";
  for (let s = 0; s < n - i; s++) row += " ";
  for (let k = 0; k < 2 * i - 1; k++) row += "*";
  console.log(row);
}
```

## 6. Print vs return

Pattern problems use **print mode**: `solve` prints directly and does not return the lines.

:::only java
`System.out.print` stays on the line. `System.out.println` ends it. Returning a string is not the same as printing it.
:::

:::only python
`print(x, end=" ")` stays on the line. A plain `print(x)` ends it. Returning a string is not the same as printing it.
:::

:::only javascript
Every `console.log` ends the line, so build the row in a string first and log it once. Returning a string is not the same as printing it.
:::

## 7. Loops that might never end

Happy Number can cycle forever. Whenever your loop condition depends on a value that can repeat, ask: *what guarantees this stops?* If nothing does, track what you have seen or find the cycle.
