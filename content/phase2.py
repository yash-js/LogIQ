from core import problem

PH = 2


@problem(phase=PH, title="Counting Up and Down", mode="print", returns="lines", concepts=["for loop"],
         statement="""
         Print the numbers 1 to `n` on the first line and `n` down to 1 on the second line,
         separated by single spaces.

         **Constraints:** 1 ≤ n ≤ 1000
         """,
         params=[("n", "int")],
         tests=[(5,), (1,), (2,), (10,), (37,), (1000,)],
         hints=["Which three parts does a for-loop have? What should each be here?",
                "How do you print on the same line without a newline after each number?",
                {"java": "Loop i from 1 to n, printing each i and a space, then a newline, then loop i from n down to 1.",
                 "python": "Loop i from 1 to n with print(i, end=' '), then a newline, then loop i from n down to 1.",
                 "javascript": "Build each line in a string and log it once. One line is 1..n, the next is n..1."}])
def counting(n):
    return [" ".join(str(i) for i in range(1, n + 1)), " ".join(str(i) for i in range(n, 0, -1))]


@problem(phase=PH, title="Multiplication Table", mode="print", returns="lines", concepts=["for loop", "formatting"],
         statement="""
         Print the multiplication table of `n` from 1 to 10, one line per row, in exactly this format:

         ```
         n x i = result
         ```

         **Constraints:** 1 ≤ n ≤ 10^4
         """,
         params=[("n", "int")],
         tests=[(2,), (9,), (1,), (13,), (10000,)],
         hints=["Which part of each line changes, and which part stays the same?",
                "Your loop variable runs from 1 to 10. What do you print in each iteration?",
                {"java": "Print n + \" x \" + i + \" = \" + (n * i). The brackets multiply before the pieces are joined.",
                 "python": "Print an f-string: f\"{n} x {i} = {n * i}\".",
                 "javascript": "Log n + \" x \" + i + \" = \" + (n * i). The brackets multiply before the pieces are joined."}],
         practice=("HackerRank: Java Loops I", "https://www.hackerrank.com/challenges/java-loops-i/problem"))
def table(n):
    return [f"{n} x {i} = {n * i}" for i in range(1, 11)]


@problem(phase=PH, title="Three Sums", returns="long_list", concepts=["accumulator"],
         statement="""
         For the numbers 1 to `n`, return three values: the sum of all numbers, the sum of even numbers,
         and the sum of odd numbers.

         **Constraints:** 1 ≤ n ≤ 10^6

         :::only java
         The sums may not fit in an `int`. Accumulate in a `long`.
         :::
         :::only python
         The sums can be large. An integer grows to hold them.
         :::
         :::only javascript
         The sums stay exact in a normal number.
         :::
         """,
         params=[("n", "int")],
         tests=[(5,), (1,), (2,), (10,), (999,), (1000000,)],
         hints=["What variable do you need before the loop to collect a sum?",
                "Can one loop update all three sums at once?",
                {"java": "Use three long accumulators. Add i to the even or odd one depending on i % 2.",
                 "python": "Use three accumulators. Add i to the even or odd one depending on i % 2. Integers will not overflow.",
                 "javascript": "Use three accumulators. Add i to the even or odd one depending on i % 2. These sums stay exact."}])
def three_sums(n):
    total = n * (n + 1) // 2
    evens = sum(range(2, n + 1, 2))
    return [total, evens, total - evens]


@problem(phase=PH, title="Fizz Buzz", mode="print", returns="lines", concepts=["loop + conditions"],
         statement="""
         For every number from 1 to `n`, print on its own line:

         - `FizzBuzz` if it is divisible by 3 and 5
         - `Fizz` if divisible by 3 only
         - `Buzz` if divisible by 5 only
         - the number itself otherwise

         **Constraints:** 1 ≤ n ≤ 10^4
         """,
         params=[("n", "int")],
         tests=[(15,), (1,), (5,), (3,), (30,), (100,)],
         hints=["You solved the single-number version in Phase 1. What changes now?",
                "Put that same if-else chain inside a loop.",
                "Check divisibility by 15 first, then 3, then 5, else print the number."],
         practice=("LeetCode 412: Fizz Buzz", "https://leetcode.com/problems/fizz-buzz/"))
def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        out.append("FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i))
    return out


@problem(phase=PH, title="Digits That Divide", returns="int", concepts=["digit extraction"],
         statement="""
         Return how many digits of `n` divide `n` exactly. Count repeated digits each time they appear.
         `n` contains no zero digits.

         **Constraints:** 1 ≤ n ≤ 10^9, `n` has no digit 0
         """,
         params=[("n", "int")],
         tests=[(7,), (121,), (1248,), (111,), (987654321,), (22,), (35,)],
         hints=["How do you get the last digit of a number? How do you remove it?",
                "You need the original `n` for the divisibility check. What happens if you modify `n` itself?",
                {"java": "Copy n into temp; while temp > 0: d = temp % 10, check n % d, then temp /= 10.",
                 "python": "Copy n into temp; while temp > 0: d = temp % 10, check n % d, then temp //= 10.",
                 "javascript": "Copy n into temp; while temp > 0: d = temp % 10, check n % d, then temp = Math.floor(temp / 10)."}],
         practice=("LeetCode 2520: Count the Digits That Divide a Number",
                   "https://leetcode.com/problems/count-the-digits-that-divide-a-number/"))
def digits_divide(n):
    return sum(1 for d in str(n) if n % int(d) == 0)


@problem(phase=PH, title="Product Minus Sum", returns="int", concepts=["digit extraction"],
         statement="""
         Return (product of the digits of `n`) − (sum of the digits of `n`).

         **Constraints:** 1 ≤ n ≤ 10^5
         """,
         params=[("n", "int")],
         tests=[(234,), (4421,), (1,), (10,), (99999,), (100000,)],
         hints=["What should the product start at? What should the sum start at?",
                {"java": "Use the same % 10 and / 10 loop as before.",
                 "python": "Use the same % 10 and // 10 loop as before.",
                 "javascript": "Use the same % 10 and Math.floor(n / 10) loop as before."},
                "product = 1, sum = 0; update both for each digit; return product - sum."],
         practice=("LeetCode 1281: Subtract the Product and Sum of Digits",
                   "https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/"))
def prod_minus_sum(n):
    p, s = 1, 0
    for d in str(n):
        p *= int(d)
        s += int(d)
    return p - s


@problem(phase=PH, title="Digital Root", returns="int", concepts=["nested loops", "while"],
         statement="""
         Repeatedly replace `n` with the sum of its digits until a single digit remains. Return it.

         Use loops (the one-line math trick is for later).

         **Constraints:** 0 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(38,), (0,), (9,), (10,), (2147483647,), (999999999,), (123456789,)],
         hints=["When should the outer loop stop?",
                "Inside it, you need the digit-sum loop you already know.",
                "while n >= 10: compute s = digit sum of n; n = s."],
         practice=("LeetCode 258: Add Digits", "https://leetcode.com/problems/add-digits/"))
def digital_root(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


@problem(phase=PH, title="Reverse Integer", difficulty="medium", returns="int", concepts=["digit building", "overflow"],
         statement="""
         Reverse the digits of `x`, keeping its sign. If the result does not fit in a 32-bit signed integer
         (−2^31 to 2^31 − 1), return 0.

         **Constraints:** −2^31 ≤ x ≤ 2^31 − 1
         """,
         params=[("x", "int")],
         tests=[(123,), (-123,), (120,), (0,), (1534236469,), (-2147483648,), (2147483647,), (1463847412,), (-10,)],
         hints=["How do you build a number one digit at a time? Think `rev = rev * 10 + digit`.",
                "How can you detect that `rev * 10 + digit` would go past 2^31 − 1 before it happens?",
                {"java": "Work in a long, or stop early when rev > Integer.MAX_VALUE / 10.",
                 "python": "Integers never overflow. After reversing, return 0 if the result is outside -2147483648 .. 2147483647.",
                 "javascript": "Reversing a 32-bit value stays exact. Return 0 if the result is outside -2147483648 .. 2147483647."}],
         practice=("LeetCode 7: Reverse Integer", "https://leetcode.com/problems/reverse-integer/"))
def reverse_int(x):
    sign = -1 if x < 0 else 1
    r = sign * int(str(abs(x))[::-1])
    return r if -2**31 <= r <= 2**31 - 1 else 0


@problem(phase=PH, title="Palindrome Number", returns="bool", concepts=["digit building"],
         statement="""
         Return `true` if `x` reads the same forwards and backwards. Solve it **without** converting `x` to a string.

         **Constraints:** −2^31 ≤ x ≤ 2^31 − 1
         """,
         params=[("x", "int")],
         tests=[(121,), (-121,), (10,), (0,), (1221,), (12321,), (2147447412,), (1000021,)],
         hints=["Can a negative number be a palindrome?",
                "Reverse the number with the loop from the last problem and compare.",
                {"java": "Build the reversed value in a long so it cannot overflow an int.",
                 "python": "Reversing cannot overflow. Compare the rebuilt number with the original.",
                 "javascript": "Reversing a 32-bit value stays exact. Compare the rebuilt number with the original."}],
         practice=("LeetCode 9: Palindrome Number", "https://leetcode.com/problems/palindrome-number/"))
def palin_num(x):
    return x >= 0 and str(x) == str(x)[::-1]


@problem(phase=PH, title="Armstrong Number", returns="bool", concepts=["two passes over digits"],
         statement="""
         An Armstrong number equals the sum of its digits, each raised to the power of the number of digits.
         Example: 153 = 1³ + 5³ + 3³.

         Return `true` if `n` is an Armstrong number.

         **Constraints:** 0 ≤ n ≤ 10^9
         """,
         params=[("n", "int")],
         tests=[(153,), (370,), (9474,), (9475,), (0,), (7,), (10,), (548834,), (100,)],
         hints=["You need the number of digits before you can compute any power. How many passes over the digits is that?",
                "First loop: count digits. Second loop: add each digit^count.",
                "Write your own power loop: multiply the digit by itself `count` times."])
def armstrong(n):
    k = len(str(n))
    return sum(int(d) ** k for d in str(n)) == n


@problem(phase=PH, title="Factorial and Trailing Zeroes", returns="long_list", concepts=["product loop", "long"],
         statement="""
         Return `n!` and the number of trailing zeroes in `n!`.

         **Constraints:** 0 ≤ n ≤ 20

         :::only java
         20! still fits in a `long`.
         :::
         :::only python
         An integer holds 20! exactly.
         :::
         :::only javascript
         20! is larger than 2^53, so build it with `BigInt` or the digits will not be exact.
         :::
         """,
         params=[("n", "int")],
         tests=[(5,), (0,), (1,), (10,), (15,), (20,), (4,)],
         hints=["What is 0! ? What should the product start at?",
                "Trailing zeroes: how do you check whether the last digit of a number is 0? How do you drop it?",
                {"java": "Compute f in a long loop; then while f % 10 == 0, count one and do f /= 10.",
                 "python": "Compute f in a loop; then while f % 10 == 0, count one and do f //= 10.",
                 "javascript": "20! exceeds 2^53, so compute f with BigInt; then while f % 10n === 0n, count one and do f /= 10n."}],
         practice=("LeetCode 172: Factorial Trailing Zeroes", "https://leetcode.com/problems/factorial-trailing-zeroes/"))
def fact_zeros(n):
    f = 1
    for i in range(2, n + 1):
        f *= i
    z, t = 0, f
    while t % 10 == 0:
        z += 1
        t //= 10
    return [f, z]


@problem(phase=PH, title="Fibonacci Number", returns="long", concepts=["two variables moving together"],
         statement="""
         F(0) = 0, F(1) = 1, and F(n) = F(n−1) + F(n−2). Return F(n) using a loop.

         **Constraints:** 0 ≤ n ≤ 90

         :::only java
         F(90) fits in a `long`, not in an `int`.
         :::
         :::only python
         An integer holds F(90) exactly.
         :::
         :::only javascript
         F(90) is larger than 2^53. Use `BigInt`.
         :::
         """,
         params=[("n", "int")],
         tests=[(0,), (1,), (2,), (10,), (30,), (50,), (90,)],
         hints=["To compute the next term, which values do you need to remember?",
                "Keep `a` and `b` for the last two terms. How do they shift each step?",
                {"java": "next = a + b; a = b; b = next. Keep them in long, because F(90) does not fit in an int.",
                 "python": "next = a + b; a = b; b = next. An integer grows to hold F(90).",
                 "javascript": "next = a + b; a = b; b = next. F(90) exceeds 2^53, so use BigInt."}],
         practice=("LeetCode 509: Fibonacci Number", "https://leetcode.com/problems/fibonacci-number/"))
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@problem(phase=PH, title="Count Primes", difficulty="medium", returns="int", concepts=["nested loops", "early exit"],
         statement="""
         Return how many prime numbers are **strictly less** than `n`.

         **Constraints:** 0 ≤ n ≤ 20000
         """,
         params=[("n", "int")],
         tests=[(10,), (0,), (1,), (2,), (3,), (100,), (20000,), (7919,)],
         hints=["Write `isPrime(x)` first. Which divisors do you actually need to try?",
                "If x has a divisor bigger than √x, it also has one smaller than √x. So where can the loop stop?",
                "Loop d from 2 while d*d <= x. Then count primes for x in [2, n)."],
         practice=("LeetCode 204: Count Primes", "https://leetcode.com/problems/count-primes/"))
def count_primes(n):
    c = 0
    for x in range(2, n):
        d, ok = 2, True
        while d * d <= x:
            if x % d == 0:
                ok = False
                break
            d += 1
        c += ok
    return c


@problem(phase=PH, title="GCD and LCM", returns="long_list", concepts=["Euclid's method"],
         statement="""
         Return the greatest common divisor and the least common multiple of `a` and `b`.

         **Constraints:** 1 ≤ a, b ≤ 10^6

         :::only java
         The LCM may not fit in an `int`. Use a `long`, and divide before you multiply.
         :::
         :::only python
         Divide before you multiply. An integer will not overflow either way.
         :::
         :::only javascript
         Divide before you multiply. These values stay below 2^53, so a normal number is exact.
         :::
         """,
         params=[("a", "int"), ("b", "int")],
         tests=[(12, 18), (7, 13), (1, 1), (100, 10), (1000000, 999999), (48, 180), (17, 17)],
         hints=["A slow way: try every number from min(a, b) down to 1. Can you do better?",
                "Euclid: gcd(a, b) = gcd(b, a % b). When does it stop?",
                {"java": "lcm = a / gcd * b (divide first so the product fits in a long).",
                 "python": "lcm = a // gcd * b (divide first). An integer will not overflow.",
                 "javascript": "lcm = Math.floor(a / gcd) * b (divide first). These values stay exact."}],
         practice=("LeetCode 1979: Find Greatest Common Divisor of Array",
                   "https://leetcode.com/problems/find-greatest-common-divisor-of-array/"))
def gcd_lcm(a, b):
    x, y = a, b
    while y:
        x, y = y, x % y
    return [x, a // x * b]


@problem(phase=PH, title="Perfect Number", returns="bool", concepts=["divisor loop"],
         statement="""
         A perfect number equals the sum of its positive divisors excluding itself (6 = 1 + 2 + 3).
         Return `true` if `n` is perfect.

         **Constraints:** 1 ≤ n ≤ 10^8
         """,
         params=[("n", "int")],
         tests=[(28,), (6,), (7,), (1,), (496,), (8128,), (33550336,), (100000000,)],
         hints=["Looping all the way to n is too slow for 10^8. Where can you stop?",
                "If d divides n, then n / d also divides n. Add both.",
                "Loop d from 2 while d*d <= n; add d and n/d (once if equal). Start the sum at 1 and handle n = 1."],
         practice=("LeetCode 507: Perfect Number", "https://leetcode.com/problems/perfect-number/"))
def perfect(n):
    if n == 1:
        return False
    s, d = 1, 2
    while d * d <= n:
        if n % d == 0:
            s += d
            if d != n // d:
                s += n // d
        d += 1
    return s == n


@problem(phase=PH, title="Power of Two", returns="bool", concepts=["repeated division"],
         statement="""
         Return `true` if `n` is a power of two (1, 2, 4, 8, ...).

         **Constraints:** −2^31 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(1,), (16,), (3,), (0,), (-8,), (1073741824,), (2147483647,), (6,)],
         hints=["Which values can never be a power of two?",
                "If n is even, divide it by 2. What should be left at the end?",
                {"java": "Return false for n <= 0; while n % 2 == 0, do n /= 2; return n == 1.",
                 "python": "Return False for n <= 0; while n % 2 == 0, do n //= 2; return n == 1.",
                 "javascript": "Return false for n <= 0; while n % 2 === 0, do n = Math.floor(n / 2); return n === 1."}],
         practice=("LeetCode 231: Power of Two", "https://leetcode.com/problems/power-of-two/"))
def pow2(n):
    return n > 0 and (n & (n - 1)) == 0


@problem(phase=PH, title="Happy Number", returns="bool", concepts=["loops that may not end"],
         statement="""
         Replace `n` by the sum of the squares of its digits, again and again.
         If it reaches 1, `n` is happy. If it loops forever without reaching 1, it is not.

         Return `true` if `n` is happy.

         **Constraints:** 1 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(19,), (2,), (1,), (7,), (4,), (100,), (2147483647,), (1111111,)],
         hints=["Trace n = 2 by hand. What happens after a few steps?",
                "Every unhappy number eventually enters the same cycle. Which number appears in it?",
                "Loop while n != 1 and n != 4 (4 is in the only cycle). Or remember seen values."],
         practice=("LeetCode 202: Happy Number", "https://leetcode.com/problems/happy-number/"))
def happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1


@problem(phase=PH, title="Ugly Number", returns="bool", concepts=["repeated division"],
         statement="""
         An ugly number is a positive number whose only prime factors are 2, 3 and 5. Return `true` if `n` is ugly.
         (1 counts as ugly.)

         **Constraints:** −2^31 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(6,), (1,), (14,), (0,), (-30,), (2147483647,), (1000000000,), (49,)],
         hints=["What happens to 30 if you keep dividing by 2, then 3, then 5?",
                "What value is left when the number had only those factors?",
                {"java": "For each f in {2, 3, 5}: while n % f == 0, do n /= f. Ugly if n == 1 (and n > 0 at the start).",
                 "python": "For each f in {2, 3, 5}: while n % f == 0, do n //= f. Ugly if n == 1 (and n > 0 at the start).",
                 "javascript": "For each f in {2, 3, 5}: while n % f === 0, do n = Math.floor(n / f). Ugly if n === 1 (and n > 0 at the start)."}],
         practice=("LeetCode 263: Ugly Number", "https://leetcode.com/problems/ugly-number/"))
def ugly(n):
    if n <= 0:
        return False
    for f in (2, 3, 5):
        while n % f == 0:
            n //= f
    return n == 1


@problem(phase=PH, title="Steps to Zero", returns="int", concepts=["while loop"],
         statement="""
         In one step: if `n` is even, halve it; otherwise subtract 1. Return the number of steps to reach 0.

         **Constraints:** 0 ≤ n ≤ 10^6
         """,
         params=[("n", "int")],
         tests=[(14,), (8,), (0,), (1,), (123,), (1000000,)],
         hints=["What is the loop condition?",
                "Inside the loop, which two actions are possible?",
                {"java": "while (n > 0) { n = (n % 2 == 0) ? n / 2 : n - 1; steps++; }",
                 "python": "while n > 0: n = n // 2 if n % 2 == 0 else n - 1; then steps += 1.",
                 "javascript": "while (n > 0) { n = n % 2 === 0 ? Math.floor(n / 2) : n - 1; steps++; }"}],
         practice=("LeetCode 1342: Number of Steps to Reduce a Number to Zero",
                   "https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/"))
def steps_zero(n):
    s = 0
    while n:
        n = n // 2 if n % 2 == 0 else n - 1
        s += 1
    return s


@problem(phase=PH, title="Count Set Bits", returns="int", concepts=["binary", "% 2"],
         statement="""
         Return how many 1s appear in the binary form of `n`.

         **Constraints:** 0 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(11,), (128,), (0,), (1,), (2147483647,), (255,), (1024,)],
         hints=["How do you get the last digit of a number in base 10? What is the base-2 version?",
                {"java": "n % 2 is the last bit; n / 2 removes it.",
                 "python": "n % 2 is the last bit; n // 2 removes it.",
                 "javascript": "n % 2 is the last bit; Math.floor(n / 2) removes it."},
                {"java": "Loop while n > 0, add n % 2 to a counter, then n /= 2.",
                 "python": "Loop while n > 0, add n % 2 to a counter, then n //= 2.",
                 "javascript": "Loop while n > 0, add n % 2 to a counter, then n = Math.floor(n / 2)."}],
         practice=("LeetCode 191: Number of 1 Bits", "https://leetcode.com/problems/number-of-1-bits/"))
def set_bits(n):
    return bin(n).count("1")


@problem(phase=PH, title="Integer Square Root", returns="int", concepts=["overflow", "loop bound"],
         statement="""
         Return the square root of `x` rounded down.

         :::only java
         Do not use `Math.sqrt`.
         :::
         :::only python
         Do not use `math.sqrt` or `** 0.5`.
         :::
         :::only javascript
         Do not use `Math.sqrt` or `** 0.5`.
         :::

         **Constraints:** 0 ≤ x ≤ 2^31 − 1
         """,
         params=[("x", "int")],
         tests=[(4,), (8,), (0,), (1,), (2147483647,), (2147395600,), (99,), (100,)],
         hints=["Start from 1 and go up. When should you stop?",
                {"java": "What happens to i * i in an int when i is around 46341?",
                 "python": "i * i is always exact. When should the loop stop?",
                 "javascript": "i * i stays exact for a 32-bit x. When should the loop stop?"},
                {"java": "Loop while (long) i * i <= x; the answer is the last i that passed.",
                 "python": "Loop while i * i <= x; the answer is the last i that passed.",
                 "javascript": "Loop while i * i <= x; the answer is the last i that passed."}],
         practice=("LeetCode 69: Sqrt(x)", "https://leetcode.com/problems/sqrtx/"))
def isqrt(x):
    import math
    return math.isqrt(x)


@problem(phase=PH, title="Star Triangles", mode="print", returns="lines", strict=True, concepts=["nested loops", "patterns"],
         statement="""
         Print a right-angled triangle of `*` with `n` rows, then the same triangle upside down.
         No spaces between stars. For n = 3:

         ```
         *
         **
         ***
         ***
         **
         *
         ```

         **Constraints:** 1 ≤ n ≤ 50
         """,
         params=[("n", "int")],
         tests=[(3,), (1,), (2,), (5,), (50,)],
         hints=["How many stars are in row i? Write it as a formula of i.",
                "The outer loop picks the row; what does the inner loop do?",
                "Row i (1-based) has i stars in the first half and n - i + 1 in the second half."])
def star_triangles(n):
    return ["*" * i for i in range(1, n + 1)] + ["*" * i for i in range(n, 0, -1)]


@problem(phase=PH, title="Staircase", mode="print", returns="lines", strict=True, concepts=["spaces + symbols"],
         statement="""
         Print a right-aligned staircase of `#` with `n` rows. For n = 4:

         ```
            #
           ##
          ###
         ####
         ```

         Leading spaces matter; trailing spaces are ignored.

         **Constraints:** 1 ≤ n ≤ 100
         """,
         params=[("n", "int")],
         tests=[(4,), (1,), (2,), (6,), (100,)],
         hints=["Each row has two parts. What are they?",
                "In row i, how many spaces come before the #s?",
                "Row i: (n - i) spaces, then i #s."],
         practice=("HackerRank: Staircase", "https://www.hackerrank.com/challenges/staircase/problem"))
def staircase(n):
    return [" " * (n - i) + "#" * i for i in range(1, n + 1)]


@problem(phase=PH, title="Diamond", difficulty="medium", mode="print", returns="lines", strict=True,
         concepts=["patterns", "symmetry"],
         statement="""
         Print a diamond of `*` made of a pyramid with `n` rows followed by an upside-down pyramid of `n − 1` rows.
         For n = 3:

         ```
           *
          ***
         *****
          ***
           *
         ```

         **Constraints:** 1 ≤ n ≤ 50
         """,
         params=[("n", "int")],
         tests=[(3,), (1,), (2,), (4,), (50,)],
         hints=["Solve the top pyramid alone first. How many spaces and stars are in row i?",
                "Stars in row i of the pyramid: 1, 3, 5, ... What formula is that?",
                "Row i: (n - i) spaces + (2i - 1) stars. Then repeat for i = n-1 down to 1."])
def diamond(n):
    rows = [" " * (n - i) + "*" * (2 * i - 1) for i in range(1, n + 1)]
    return rows + rows[-2::-1]


@problem(phase=PH, title="Floyd's Triangle", mode="print", returns="lines", concepts=["counter across loops"],
         statement="""
         Print Floyd's triangle with `n` rows: consecutive numbers starting at 1, row i containing i numbers,
         separated by spaces. For n = 4:

         ```
         1
         2 3
         4 5 6
         7 8 9 10
         ```

         **Constraints:** 1 ≤ n ≤ 100
         """,
         params=[("n", "int")],
         tests=[(4,), (1,), (2,), (7,), (100,)],
         hints=["Does the number restart in each row?",
                "Declare the counter outside both loops.",
                {"java": "Print counter, then add 1, i times in row i. counter++ does both.",
                 "python": "Print the counter, then add 1, i times in row i.",
                 "javascript": "Log the counter, then add 1, i times in row i. counter++ does both."}])
def floyd(n):
    out, c = [], 1
    for i in range(1, n + 1):
        out.append(" ".join(str(c + k) for k in range(i)))
        c += i
    return out


@problem(phase=PH, title="Pascal's Triangle", difficulty="medium", returns="int_list_2d", concepts=["rows from previous rows"],
         statement="""
         Return the first `n` rows of Pascal's triangle. Each number is the sum of the two numbers above it.

         ```
         1
         1 1
         1 2 1
         1 3 3 1
         ```

         **Constraints:** 1 ≤ n ≤ 30
         """,
         params=[("n", "int")],
         tests=[(1,), (2,), (5,), (10,), (30,)],
         hints=["What are the first and last numbers of every row?",
                "Row i, position j: which two numbers from row i−1 make it?",
                "row[j] = prev[j-1] + prev[j] for 0 < j < i; ends are 1."],
         practice=("LeetCode 118: Pascal's Triangle", "https://leetcode.com/problems/pascals-triangle/"))
def pascal(n):
    rows = [[1]]
    for _ in range(n - 1):
        prev = rows[-1]
        rows.append([1] + [prev[j - 1] + prev[j] for j in range(1, len(prev))] + [1])
    return rows
