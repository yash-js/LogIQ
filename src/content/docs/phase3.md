# Phase 3 · Recursive Thinking

A recursive function solves a problem by calling itself on a **smaller** version of the same problem. It feels like magic until you learn to trust two rules.

## 1. The two rules

1. **Base case:** an input so small you know the answer immediately.
2. **Recursive step:** turn the problem into a smaller one, assume that smaller call works, and finish the job.

```java
static long fact(int n) {
    if (n == 0) return 1;           // base case
    return n * fact(n - 1);         // smaller problem
}
```

```python
def fact(n):
    if n == 0:
        return 1                    # base case
    return n * fact(n - 1)          # smaller problem
```

```javascript
function fact(n) {
  if (n === 0) return 1;          // base case
  return n * fact(n - 1);         // smaller problem
}
```

The hardest habit to build: **do not trace every call in your head.** Assume `fact(n - 1)` is correct and only check that your step is right.

## 2. What happens in memory

Each call gets its own box (a stack frame) with its own `n`. `fact(3)` waits for `fact(2)`, which waits for `fact(1)`, which waits for `fact(0)`. Then the answers flow back up: 1 → 1 → 2 → 6.

No base case, or a step that does not shrink the input, means infinite calls. Every call uses a stack frame, and endless calls exhaust the stack.

:::only java
The error is **StackOverflowError**.
:::

:::only python
The error is **RecursionError**.
:::

:::only javascript
The error is **RangeError** (`Maximum call stack size exceeded`).
:::

## 3. Before or after the call?

Where you put the work changes the order:

```java
static void up(int n) {      // prints 1 2 3 ... n
    if (n == 0) return;
    up(n - 1);
    System.out.print(n + " ");
}

static void down(int n) {    // prints n ... 3 2 1
    if (n == 0) return;
    System.out.print(n + " ");
    down(n - 1);
}
```

```python
def up(n):          # prints 1 2 3 ... n
    if n == 0:
        return
    up(n - 1)
    print(n, end=" ")

def down(n):        # prints n ... 3 2 1
    if n == 0:
        return
    print(n, end=" ")
    down(n - 1)
```

```javascript
let out = "";
function up(n) {     // 1 2 3 ... n
  if (n === 0) return;
  up(n - 1);
  out += n + " ";
}
function down(n) {   // n ... 3 2 1
  if (n === 0) return;
  out += n + " ";
  down(n - 1);
}
```

## 4. Helper parameters

Sometimes the function needs extra information. Write a helper with more parameters and call it from `solve`.

```java
static int reverse(int n, int rev) {
    if (n == 0) return rev;
    return reverse(n / 10, rev * 10 + n % 10);
}
// solve(n) returns reverse(n, 0)
```

```python
def reverse(n, rev):
    if n == 0:
        return rev
    return reverse(n // 10, rev * 10 + n % 10)
# solve(n) returns reverse(n, 0)
```

```javascript
function reverse(n, rev) {
  if (n === 0) return rev;
  return reverse(Math.floor(n / 10), rev * 10 + (n % 10));
}
// solve(n) returns reverse(n, 0)
```

For arrays, pass an **index** instead of shrinking the array: `sum(arr, i) = arr[i] + sum(arr, i + 1)`.

## 5. Halving makes it fast

x^64 by multiplying 64 times is slow. But x^64 = (x^32)², x^32 = (x^16)², … only 6 steps.

```java
static double pow(double x, int n) {
    if (n == 0) return 1;
    double half = pow(x, n / 2);
    return (n % 2 == 0) ? half * half : half * half * x;
}
```

```python
def power(x, n):
    if n == 0:
        return 1.0
    half = power(x, n // 2)
    return half * half if n % 2 == 0 else half * half * x
```

```javascript
function power(x, n) {
  if (n === 0) return 1;
  const half = power(x, Math.trunc(n / 2));
  return n % 2 === 0 ? half * half : half * half * x;
}
```

Careful with negative `n`: handle it once at the top with `1 / pow(x, -n)`.

## 6. Repeated work and memoisation

`fib(n) = fib(n-1) + fib(n-2)` recomputes the same values again and again: `fib(40)` makes over 300 million calls. Remember answers you already have:

```java
static long[] memo = new long[100];
static long ways(int n) {
    if (n <= 1) return 1;
    if (memo[n] != 0) return memo[n];
    return memo[n] = ways(n - 1) + ways(n - 2);
}
```

```python
memo = {}
def ways(n):
    if n <= 1:
        return 1
    if n not in memo:
        memo[n] = ways(n - 1) + ways(n - 2)
    return memo[n]
```

```javascript
const memo = new Array(100).fill(0);
function ways(n) {
  if (n <= 1) return 1;
  if (memo[n] !== 0) return memo[n];
  return (memo[n] = ways(n - 1) + ways(n - 2));
}
```

## 7. Recursion limits

:::only java
Several thousand nested calls are allowed. LogicQuest runs your program with a larger stack, and the tests in this phase stay inside that limit.
:::

:::only python
About 1000 nested calls are allowed by default. The tests in this phase stay below that. If you ever need more, import `sys` and raise `sys.setrecursionlimit`.
:::

:::only javascript
Several thousand nested calls are allowed. LogicQuest runs your program with a larger stack, and the tests in this phase stay inside that limit.
:::

## 8. The leap of faith

Tower of Hanoi looks impossible until you say: *"to move n disks to C, move n−1 disks out of the way to B, move the big one, then move the n−1 disks onto it."* You never think about disk 3 of 7. That is recursive thinking.
