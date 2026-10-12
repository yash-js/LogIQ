from core import problem

PH = 3
NOTE = "\n\nSolve it with recursion: no `for` / `while` loops."


@problem(phase=PH, title="Count Up, Count Down", mode="print", returns="lines", concepts=["base case", "call order"],
         statement="""
         Without any loop, print 1 to `n` on the first line and `n` to 1 on the second line, space separated.

         Hint of the phase: the only difference between the two is **where** you print relative to the recursive call.

         **Constraints:** 1 ≤ n ≤ 500
         """,
         params=[("n", "int")],
         tests=[(5,), (1,), (2,), (9,), (500,)],
         hints=["What is the smallest n for which you know the answer immediately? That is your base case.",
                "If `printUp(n - 1)` prints 1..n−1, what is left to do for n?",
                "Print after the recursive call for counting up, before it for counting down. Then print a newline between."])
def count_up_down(n):
    return [" ".join(map(str, range(1, n + 1))), " ".join(map(str, range(n, 0, -1)))]


@problem(phase=PH, title="Sum to N", returns="int", concepts=["return values"],
         statement="""
         Return 1 + 2 + ... + `n`.""" + NOTE + """

         **Constraints:** 1 ≤ n ≤ 1000
         """,
         params=[("n", "int")],
         tests=[(5,), (1,), (2,), (100,), (1000,)],
         hints=["If you already knew sum(n − 1), how would you get sum(n)?",
                "Which n has an answer you know without any work?",
                "sum(n) = n + sum(n - 1), with sum(1) = 1."])
def sum_to_n(n):
    return n * (n + 1) // 2


@problem(phase=PH, title="Recursive Factorial", returns="long", concepts=["return values"],
         statement="""
         Return `n!`.""" + NOTE + """

         **Constraints:** 0 ≤ n ≤ 20
         """,
         params=[("n", "int")],
         tests=[(5,), (0,), (1,), (10,), (20,)],
         hints=["What is the smaller version of n! ?",
                "Is the base case n == 1 enough? What about n == 0?",
                "fact(n) = n * fact(n - 1), with fact(0) = 1. Use long."])
def rec_fact(n):
    f = 1
    for i in range(2, n + 1):
        f *= i
    return f


@problem(phase=PH, title="Recursive Fibonacci", returns="int", concepts=["two recursive calls"],
         statement="""
         Return F(n) where F(0) = 0, F(1) = 1, F(n) = F(n−1) + F(n−2).""" + NOTE + """

         After it works, draw the call tree for n = 5 and count how many times F(2) is computed.

         **Constraints:** 0 ≤ n ≤ 30
         """,
         params=[("n", "int")],
         tests=[(0,), (1,), (2,), (10,), (20,), (30,)],
         hints=["How many base cases does this recurrence need?",
                "The formula is already recursive. Translate it directly.",
                "if n <= 1 return n; return fib(n-1) + fib(n-2)."],
         practice=("LeetCode 509: Fibonacci Number", "https://leetcode.com/problems/fibonacci-number/"))
def rec_fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@problem(phase=PH, title="Count Digits", returns="int", concepts=["shrinking the input"],
         statement="""
         Return the number of digits in `n` (0 has one digit).""" + NOTE + """

         **Constraints:** 0 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(12345,), (0,), (7,), (10,), (2147483647,), (1000000,)],
         hints=["How do you make n one digit shorter?",
                "When does the number have exactly one digit?",
                "if n < 10 return 1; return 1 + count(n / 10)."])
def count_digits(n):
    return len(str(n))


@problem(phase=PH, title="Recursive Digital Root", returns="int", concepts=["recursion calling recursion"],
         statement="""
         Return the digital root of `n` (keep summing digits until one digit remains).""" + NOTE + """

         You may write two recursive functions: one for the digit sum and one for the root.

         **Constraints:** 0 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(38,), (0,), (9,), (2147483647,), (99999,), (10,)],
         hints=["Split it into two problems: digitSum(n) and root(n).",
                "digitSum(n) = last digit + digitSum(rest). Base case?",
                "root(n) = n if n < 10, else root(digitSum(n))."],
         practice=("LeetCode 258: Add Digits", "https://leetcode.com/problems/add-digits/"))
def rec_root(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


@problem(phase=PH, title="Recursive Reverse Number", difficulty="medium", returns="int", concepts=["helper parameters"],
         statement="""
         Return the digits of `n` reversed (trailing zeros disappear: 120 → 21).""" + NOTE + """

         **Constraints:** 0 ≤ n ≤ 999999999
         """,
         params=[("n", "int")],
         tests=[(1234,), (120,), (0,), (5,), (999999999,), (1000000,), (907,)],
         hints=["Returning the answer alone makes this hard. What extra information would help?",
                "Add a second parameter that carries the reversed-so-far value.",
                "helper(n, rev): if n == 0 return rev; return helper(n / 10, rev * 10 + n % 10)."])
def rec_rev(n):
    return int(str(n)[::-1])


@problem(phase=PH, title="Recursive GCD", returns="int", concepts=["Euclid"],
         statement="""
         Return the greatest common divisor of `a` and `b`.""" + NOTE + """

         **Constraints:** 1 ≤ a, b ≤ 10^9
         """,
         params=[("a", "int"), ("b", "int")],
         tests=[(12, 18), (17, 5), (1, 1), (1000000000, 999999999), (48, 180), (7, 7)],
         hints=["Euclid's rule from Phase 2 is already recursive in disguise.",
                "What is gcd(a, 0)?",
                "gcd(a, b) = b == 0 ? a : gcd(b, a % b)."])
def rec_gcd(a, b):
    while b:
        a, b = b, a % b
    return a


@problem(phase=PH, title="Recursive Power of Two", returns="bool", concepts=["multiple base cases"],
         statement="""
         Return `true` if `n` is a power of two.""" + NOTE + """

         **Constraints:** −2^31 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(1,), (16,), (6,), (0,), (-4,), (1073741824,), (2147483647,)],
         hints=["List the cases where you can answer immediately.",
                "If n is even, which smaller question has the same answer?",
                "n == 1 → true; n <= 0 or odd → false; else recurse on n / 2."],
         practice=("LeetCode 231: Power of Two", "https://leetcode.com/problems/power-of-two/"))
def rec_pow2(n):
    return n > 0 and (n & (n - 1)) == 0


@problem(phase=PH, title="Power of Three", returns="bool", concepts=["multiple base cases"],
         statement="""
         Return `true` if `n` is a power of three.""" + NOTE + """

         **Constraints:** −2^31 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(27,), (0,), (-1,), (9,), (45,), (1,), (1162261467,), (1162261466,)],
         hints=["Same shape as the power-of-two problem. What changes?",
                "When is n definitely not a power of three?",
                "n == 1 → true; n <= 0 or n % 3 != 0 → false; else recurse on n / 3."],
         practice=("LeetCode 326: Power of Three", "https://leetcode.com/problems/power-of-three/"))
def pow3(n):
    if n <= 0:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


@problem(phase=PH, title="Power of Four", returns="bool", concepts=["multiple base cases"],
         statement="""
         Return `true` if `n` is a power of four.""" + NOTE + """

         **Constraints:** −2^31 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(16,), (5,), (1,), (8,), (0,), (1073741824,), (-16,)],
         hints=["Is 8 a power of four? Your solution must say no.",
                "Reuse the pattern from the last two problems.",
                "n == 1 → true; n <= 0 or n % 4 != 0 → false; else recurse on n / 4."],
         practice=("LeetCode 342: Power of Four", "https://leetcode.com/problems/power-of-four/"))
def pow4(n):
    if n <= 0:
        return False
    while n % 4 == 0:
        n //= 4
    return n == 1


@problem(phase=PH, title="Fast Power", difficulty="medium", returns="double", concepts=["halving the problem"],
         statement="""
         Return `x` raised to the power `n` without `Math.pow` / `**`. Answers within a relative error of 10^-5 are accepted.

         Try to make it fast: x^10 = (x^5)², so you never need 10 multiplications.

         **Constraints:** 0.5 ≤ |x| ≤ 2.0, −60 ≤ n ≤ 60
         """,
         params=[("x", "double"), ("n", "int")],
         tests=[(2.0, 10), (2.1, 3), (2.0, -2), (1.5, 0), (-2.0, 3), (0.5, 60), (-1.5, -7), (1.9, 60)],
         hints=["If you know x^(n/2), how do you get x^n when n is even? When n is odd?",
                "What should x^(negative n) become?",
                "half = pow(x, n/2); result = half*half (times x if n is odd). For n < 0 use 1 / pow(x, -n)."],
         practice=("LeetCode 50: Pow(x, n)", "https://leetcode.com/problems/powx-n/"))
def fast_pow(x, n):
    return x ** n


@problem(phase=PH, title="Decimal to Binary", returns="str", concepts=["building strings recursively"],
         statement="""
         Return the binary representation of `n` as a string (no leading zeros; 0 → "0").""" + NOTE + """

         **Constraints:** 0 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(10,), (0,), (1,), (2,), (255,), (2147483647,), (1024,)],
         hints=["`n % 2` is the last bit. Which recursive call produces all the bits before it?",
                "Should the last bit go before or after the result of the recursive call?",
                "if n < 2 return \"\" + n; return toBinary(n / 2) + (n % 2)."])
def to_binary(n):
    return bin(n)[2:]


@problem(phase=PH, title="Array Sum and Max", returns="long_list", concepts=["recursion over an index"],
         statement="""
         Return the sum and the maximum of `arr`.""" + NOTE + """

         **Constraints:** 1 ≤ arr.length ≤ 1000, −10^6 ≤ arr[i] ≤ 10^6
         """,
         params=[("arr", "int[]")],
         tests=[([1, 2, 3, 4],), ([5],), ([-3, -1, -7],), ([0, 0, 0],), (list(range(-500, 500)),), ([10**6] * 1000,)],
         hints=["Arrays do not shrink. What can you pass to the function instead to represent \"the rest of the array\"?",
                "Add an index parameter i. What is the answer when i is the last index?",
                "sum(i) = arr[i] + sum(i + 1); max(i) = larger of arr[i] and max(i + 1)."])
def arr_sum_max(arr):
    return [sum(arr), max(arr)]


@problem(phase=PH, title="Is Array Sorted", returns="bool", concepts=["recursion over an index"],
         statement="""
         Return `true` if `arr` is sorted in non-decreasing order.""" + NOTE + """

         **Constraints:** 0 ≤ arr.length ≤ 1000
         """,
         params=[("arr", "int[]")],
         tests=[([1, 2, 2, 3],), ([3, 2, 1],), ([],), ([7],), ([1, 3, 2],), (list(range(1000)),), ([5, 5, 5, 4],)],
         hints=["Which pair of elements should you compare at each step?",
                "When have you checked enough pairs to say true?",
                "sorted(i): if i >= n - 1 return true; return arr[i] <= arr[i+1] && sorted(i + 1)."])
def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


@problem(phase=PH, title="Recursive Reverse String", returns="str", concepts=["two pointers via recursion"],
         statement="""
         Return the string `s` reversed.""" + NOTE + """ No built-in reverse either.

         **Constraints:** 1 ≤ s.length ≤ 1000
         """,
         params=[("s", "str")],
         tests=[("hello",), ("a",), ("ab",), ("racecar",), ("Hello World",), ("x" * 499 + "y" * 501,)],
         hints=["What smaller string is the rest of the problem?",
                "Option 1: reverse(rest) + first char. Option 2: swap the two ends of a char array and recurse inward.",
                "Swap version: helper(chars, l, r): if l >= r stop; swap chars[l], chars[r]; helper(chars, l+1, r-1)."],
         practice=("LeetCode 344: Reverse String", "https://leetcode.com/problems/reverse-string/"))
def rec_reverse(s):
    return s[::-1]


@problem(phase=PH, title="Recursive Palindrome", returns="bool", concepts=["two pointers via recursion"],
         statement="""
         Return `true` if `s` is a palindrome after converting to lowercase and keeping only letters and digits.""" + NOTE + """

         **Constraints:** 1 ≤ s.length ≤ 1000
         """,
         params=[("s", "str")],
         tests=[("A man, a plan, a canal: Panama",), ("race a car",), (" ",), ("aa",), ("0P",), ("No 'x' in Nixon",), ("ab",)],
         hints=["Clean the string first in a separate step. Then the recursion only compares characters.",
                "Compare the outermost pair. What smaller problem is left?",
                "check(l, r): if l >= r return true; if c[l] != c[r] return false; return check(l+1, r-1)."],
         practice=("LeetCode 125: Valid Palindrome", "https://leetcode.com/problems/valid-palindrome/"))
def rec_palin(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]


@problem(phase=PH, title="Climbing Stairs", difficulty="medium", returns="long", concepts=["memoisation"],
         statement="""
         You can climb 1 or 2 steps at a time. Return how many distinct ways there are to reach step `n`.

         Plain recursion will be too slow for n = 80. Store answers you have already computed.

         **Constraints:** 1 ≤ n ≤ 80
         """,
         params=[("n", "int")],
         tests=[(2,), (3,), (1,), (5,), (45,), (80,)],
         hints=["What was your very last move to reach step n?",
                "ways(n) = ways(n−1) + ways(n−2). Which famous sequence is that?",
                "Keep a `long[] memo`; return memo[n] if already filled before recursing."],
         practice=("LeetCode 70: Climbing Stairs", "https://leetcode.com/problems/climbing-stairs/"))
def stairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@problem(phase=PH, title="Tower of Hanoi", difficulty="medium", mode="print", returns="lines", concepts=["trusting the recursion"],
         statement="""
         Move `n` disks from rod A to rod C using rod B, never placing a larger disk on a smaller one.
         Disks are numbered 1 (smallest) to n.

         Print every move as `Move disk d from X to Y`, then a final line `Total moves: k`.

         **Constraints:** 1 ≤ n ≤ 10
         """,
         params=[("n", "int")],
         tests=[(1,), (2,), (3,), (5,), (10,)],
         hints=["To move the biggest disk to C, where must all the other n − 1 disks be?",
                "Assume `hanoi(n-1, from, to, via)` already works. Write hanoi(n) using it twice.",
                "hanoi(n, A, C, B): hanoi(n-1, A, B, C); move disk n A→C; hanoi(n-1, B, C, A)."])
def hanoi(n):
    out = []

    def go(k, src, dst, via):
        if k == 0:
            return
        go(k - 1, src, via, dst)
        out.append(f"Move disk {k} from {src} to {dst}")
        go(k - 1, via, dst, src)

    go(n, "A", "C", "B")
    out.append(f"Total moves: {len(out)}")
    return out
