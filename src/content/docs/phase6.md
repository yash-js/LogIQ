# Phase 6 · Combining Logic & Problem Solving

No new syntax in this phase. Every problem combines things you already know: a condition inside a loop, digits inside a string, a grid walked with boundaries. What changes is the **process** you use before typing.

## 1. A five-step routine

1. **Restate** the problem in one sentence of your own.
2. **Examples by hand:** do 2–3 inputs on paper, including the smallest possible one.
3. **Name the state:** what variables would you need to do it by hand? (Counts? Position? Direction? Carry?)
4. **Write the steps in plain words**, then translate each line to code.
5. **Hunt edge cases:** empty, one element, all the same, the largest value, negatives.

If you are stuck for more than 10 minutes, go back to step 2 with a smaller example.

## 2. Simulation problems

Many problems say "do exactly what the story says". Keep the state small and update it each step.

```java
int x = 0, y = 0;
for (char m : moves.toCharArray()) {
    switch (m) {
        case 'U': y++; break;
        case 'D': y--; break;
        case 'L': x--; break;
        case 'R': x++; break;
    }
}
return x == 0 && y == 0;
```

```python
x = y = 0
for m in moves:
    if m == "U":
        y += 1
    elif m == "D":
        y -= 1
    elif m == "L":
        x -= 1
    else:
        x += 1
return x == 0 and y == 0
```

Robot moves, lemonade change, zigzag rows and tic-tac-toe are all this shape.

## 3. Base conversion, one more time

Any base b: `digit = n % b`, `n = n / b`, digits come out reversed. Excel columns are base 26 **without a zero digit**, which is why you subtract 1 before each step.

## 4. Look-ahead parsing

When a token's meaning depends on the next character (Roman numerals, `()` vs `(al)`), look at `s[i + 1]` and advance `i` by the token's length instead of 1. Always check `i + 1 < n` first.

## 5. Grids with boundaries

For spiral order, keep four walls and move them inward after each side:

```java
int top = 0, bottom = rows - 1, left = 0, right = cols - 1;
while (top <= bottom && left <= right) {
    for (int j = left; j <= right; j++) out.add(m[top][j]);
    top++;
    for (int i = top; i <= bottom; i++) out.add(m[i][right]);
    right--;
    if (top <= bottom) { for (int j = right; j >= left; j--) out.add(m[bottom][j]); bottom--; }
    if (left <= right) { for (int i = bottom; i >= top; i--) out.add(m[i][left]); left++; }
}
```

```python
top, bottom, left, right = 0, rows - 1, 0, cols - 1
while top <= bottom and left <= right:
    for j in range(left, right + 1):
        out.append(m[top][j])
    top += 1
    for i in range(top, bottom + 1):
        out.append(m[i][right])
    right -= 1
    if top <= bottom:
        for j in range(right, left - 1, -1):
            out.append(m[bottom][j])
        bottom -= 1
    if left <= right:
        for i in range(bottom, top - 1, -1):
            out.append(m[i][left])
        left += 1
```

The two `if` checks handle single rows and single columns, the edge cases that break most first attempts.

## 6. Clamping and overflow

`atoi` and similar problems must stay inside 32-bit limits. Build the number in a `long`, and as soon as it passes `Integer.MAX_VALUE`, clamp and stop reading. Python has no overflow, so you must clamp yourself with `max(-2**31, min(2**31 - 1, value))`.

## 7. Stretch problems

The last four problems are harder on purpose. Use all three hints if you need them; there is no shame in it. Then come back a week later and solve it again without hints. That second solve is when it actually sticks.

## 8. What comes next

Finishing this phase means you can turn a problem statement into working code on your own. That is exactly what DSA assumes. When you start DSA, you will learn faster *tools* (hash maps, stacks, sorting, binary search). The thinking you built here is what you will use them with.
