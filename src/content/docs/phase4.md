# Phase 4 · Array Fundamentals

An array is a row of boxes, each with an index starting at 0. Almost every problem in this phase is one of five moves: **walk**, **track**, **compare pairs**, **swap**, or **write into position**.

## 1. Creating and walking

```java
int[] a = new int[5];          // five zeros
int[] b = {3, 1, 4};
for (int i = 0; i < b.length; i++) System.out.println(b[i]);
for (int x : b) System.out.println(x);   // when you don't need i
```

```python
a = [0] * 5
b = [3, 1, 4]
for i in range(len(b)):
    print(b[i])
for x in b:            # when you don't need i
    print(x)
```

```javascript
const a = new Array(5).fill(0);
const b = [3, 1, 4];
for (let i = 0; i < b.length; i++) console.log(b[i]);
for (const x of b) console.log(x);   // when you don't need i
```

The last valid index is one less than the length.

:::only java
That index is `a.length - 1`. Reading `a[a.length]` throws **ArrayIndexOutOfBoundsException**.
:::

:::only python
That index is `len(a) - 1`. Reading past the end throws **IndexError**.
:::

:::only javascript
That index is `a.length - 1`. Reading `a[a.length]` silently gives `undefined`, and the bug shows up later as `NaN`.
:::

## 2. Track a value while you walk

Many "find" problems are one loop plus one or two variables:

```java
int best = arr[0];
for (int i = 1; i < arr.length; i++) {
    if (arr[i] > best) best = arr[i];
}
```

```python
best = arr[0]
for x in arr[1:]:
    if x > best:
        best = x
```

```javascript
let best = arr[0];
for (let i = 1; i < arr.length; i++) {
  if (arr[i] > best) best = arr[i];
}
```

The same idea gives you: minimum so far (stock prices), current streak + best streak (consecutive ones), running total (prefix sums).

## 3. Every pair

To compare every pair once, start the inner loop **after** the outer index:

```java
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        if (nums[i] == nums[j]) count++;
```

```python
for i in range(n):
    for j in range(i + 1, n):
        if nums[i] == nums[j]:
            count += 1
```

```javascript
for (let i = 0; i < n; i++)
  for (let j = i + 1; j < n; j++)
    if (nums[i] === nums[j]) count++;
```

This is O(n²): fine for a few thousand elements. DSA will teach faster tools; here, correct comes first.

## 4. Two pointers and swapping

Reversing in place: one pointer at each end, swap, move inward.

```java
int l = 0, r = arr.length - 1;
while (l < r) {
    int t = arr[l]; arr[l] = arr[r]; arr[r] = t;
    l++; r--;
}
```

```python
l, r = 0, len(arr) - 1
while l < r:
    arr[l], arr[r] = arr[r], arr[l]
    l += 1
    r -= 1
```

```javascript
let l = 0, r = arr.length - 1;
while (l < r) {
  const t = arr[l]; arr[l] = arr[r]; arr[r] = t;
  l++; r--;
}
```

## 5. The write pointer

To keep only some elements, walk with `i` and write with `k`:

```java
int k = 0;
for (int i = 0; i < n; i++) {
    if (nums[i] != 0) nums[k++] = nums[i];
}
while (k < n) nums[k++] = 0;      // move zeroes
```

```python
k = 0
for i in range(n):
    if nums[i] != 0:
        nums[k] = nums[i]
        k += 1
while k < n:                       # move zeroes
    nums[k] = 0
    k += 1
```

```javascript
let k = 0;
for (let i = 0; i < n; i++) {
  if (nums[i] !== 0) nums[k++] = nums[i];
}
while (k < n) nums[k++] = 0;   // move zeroes
```

## 6. Index arithmetic

Ask *"where does element i go?"* and write it as a formula:

- Rotate right by k → `(i + k) % n`
- Shuffle halves → x_i goes to `2i`, y_i goes to `2i + 1`
- Transpose → `[i][j]` goes to `[j][i]`
- Other diagonal of an n×n matrix → `[i][n − 1 − i]`

`%` wraps an index around the end, and it also turns a huge `k` into a small one.

## 7. 2D arrays

```java
int[][] m = new int[rows][cols];
for (int i = 0; i < m.length; i++)
    for (int j = 0; j < m[i].length; j++)
        total += m[i][j];
```

```python
m = [[0] * cols for _ in range(rows)]   # NOT [[0] * cols] * rows
for i in range(len(m)):
    for j in range(len(m[i])):
        total += m[i][j]
```

```javascript
const m = Array.from({ length: rows }, () => new Array(cols).fill(0)); // NOT new Array(rows).fill([])
for (let i = 0; i < m.length; i++)
  for (let j = 0; j < m[i].length; j++)
    total += m[i][j];
```

:::only java
`new int[rows][cols]` already gives each row its own array.
:::

:::only python
`[[0] * cols] * rows` makes every row the **same** list, so changing one row changes all of them. Build each row on its own: `[[0] * cols for _ in range(rows)]`.
:::

:::only javascript
`new Array(rows).fill([])` stores the **same** row over and over, so changing one row changes all of them. Build each row on its own: `Array.from({ length: rows }, () => new Array(cols).fill(0))`.
:::

## 8. Returning arrays

Some problems say "in place" and also ask you to return the array. Modify the input array and return that same array. The tests can't see whether you made a copy, but the habit matters for interviews.
