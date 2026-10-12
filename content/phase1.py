from core import problem

PH = 1


@problem(phase=PH, title="Number Identity", concepts=["if-else"],
         statement="""
         Given an integer `n`, return `"Positive"`, `"Negative"` or `"Zero"`.

         **Constraints:** -10^9 ≤ n ≤ 10^9
         """,
         params=[("n", "int")], returns="str",
         tests=[(5,), (-3,), (0,), (1,), (-1,), (1000000000,), (-1000000000,)],
         hints=["How many different answers are possible? Each one needs its own branch.",
                "Which single comparison separates Positive from everything else?",
                "Check `n > 0` first, then `n < 0`; whatever is left must be zero."])
def number_identity(n):
    if n > 0:
        return "Positive"
    if n < 0:
        return "Negative"
    return "Zero"


@problem(phase=PH, title="Odd or Even", concepts=["modulo", "negative numbers"],
         statement="""
         Given an integer `n`, return `"Even"` if it is even and `"Odd"` otherwise.

         Watch out: `n` can be negative.

         **Constraints:** -10^9 ≤ n ≤ 10^9
         """,
         params=[("n", "int")], returns="str",
         tests=[(4,), (7,), (0,), (-7,), (-8,), (999999999,), (-1,)],
         hints=["What does the remainder after dividing by 2 tell you?",
                {"java": "What is `-7 % 2`? Try it. Is it 1?",
                 "python": "What is `-7 % 2`? Try it. And what is `-7 // 2`?",
                 "javascript": "What is `-7 % 2`? Try it. Is it 1?"},
                "Compare the remainder with 0 instead of 1, so negative numbers work too."],
         practice=("HackerRank: Java If-Else", "https://www.hackerrank.com/challenges/java-if-else/problem"))
def odd_even(n):
    return "Even" if n % 2 == 0 else "Odd"


@problem(phase=PH, title="Divisibility Check", concepts=["modulo", "order of conditions"],
         statement="""
         Given a positive integer `n`, return:

         - `"Both"` if it is divisible by 3 **and** 5
         - `"Three"` if it is divisible only by 3
         - `"Five"` if it is divisible only by 5
         - `"Neither"` otherwise

         **Constraints:** 1 ≤ n ≤ 10^9
         """,
         params=[("n", "int")], returns="str",
         tests=[(15,), (9,), (10,), (7,), (30,), (1,), (3,), (5,), (999999990,)],
         hints=["If 15 is divisible by 3, why should the answer not be \"Three\"?",
                "Which condition is the most specific? Where should it go in your if-else chain?",
                "Test the \"Both\" case first, then the single cases, then the fallback."])
def divisibility(n):
    if n % 15 == 0:
        return "Both"
    if n % 3 == 0:
        return "Three"
    if n % 5 == 0:
        return "Five"
    return "Neither"


@problem(phase=PH, title="Largest of Three", concepts=["comparison", "nested if"],
         statement="""
         Given three integers `a`, `b` and `c` (one per line), return the largest.

         :::only java
         Do not use `Math.max`. Build the comparisons yourself.
         :::
         :::only python
         Do not use `max()`. Build the comparisons yourself.
         :::
         :::only javascript
         Do not use `Math.max`. Build the comparisons yourself.
         :::

         **Constraints:** -10^9 ≤ a, b, c ≤ 10^9
         """,
         params=[("a", "int"), ("b", "int"), ("c", "int")], returns="int",
         tests=[(1, 2, 3), (3, 2, 1), (2, 3, 1), (5, 5, 5), (-1, -5, -3), (7, 7, 2), (0, -1, 0)],
         hints=["What must be true about `a` for it to be the answer?",
                "What happens when two values are equal? Does `>` or `>=` matter?",
                "Keep a variable `best = a`, then compare it with `b` and with `c`."])
def largest_of_three(a, b, c):
    best = a
    if b > best:
        best = b
    if c > best:
        best = c
    return best


@problem(phase=PH, title="Leap Year", concepts=["compound conditions", "&&", "||"],
         statement="""
         Return `true` if `year` is a leap year, otherwise `false`.

         A year is a leap year if it is divisible by 4, **except** years divisible by 100,
         which are leap years only if they are also divisible by 400.

         **Constraints:** 1 ≤ year ≤ 10^5
         """,
         params=[("year", "int")], returns="bool",
         tests=[(2024,), (2023,), (1900,), (2000,), (2100,), (2400,), (4,), (1,)],
         hints=["Is 1900 a leap year? Is 2000? What rule separates them?",
                "Write the rule as three separate if-statements first, from most specific to least.",
                "One-line form: divisible by 400, OR (divisible by 4 AND not divisible by 100)."],
         practice=("LeetCode 1154: Day of the Year", "https://leetcode.com/problems/day-of-the-year/"))
def leap_year(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


@problem(phase=PH, title="Grade Rounding", concepts=["modulo", "rounding rules"],
         statement="""
         A college rounds marks like this:

         - If the difference between `marks` and the **next multiple of 5** is less than 3,
           round `marks` up to that multiple.
         - Marks below 38 are failing and are never rounded.

         Return the final marks.

         **Constraints:** 0 ≤ marks ≤ 100
         """,
         params=[("marks", "int")], returns="int",
         tests=[(84,), (29,), (57,), (38,), (37,), (73,), (67,), (100,), (40,), (0,)],
         hints=["For 84, what is the next multiple of 5? How did you calculate it?",
                "`marks % 5` tells you how far you are past the previous multiple. How far to the next one?",
                "next = marks + (5 - marks % 5). Round only if marks ≥ 38 and next - marks < 3."],
         practice=("HackerRank: Grading Students", "https://www.hackerrank.com/challenges/grading/problem"))
def grade_rounding(marks):
    if marks < 38:
        return marks
    nxt = marks + (5 - marks % 5)
    return nxt if nxt - marks < 3 else marks


@problem(phase=PH, title="Vowel or Consonant", concepts=["char comparison", "switch"],
         statement="""
         Given a single character `ch`, return `"Vowel"`, `"Consonant"` or `"Not a letter"`.

         Vowels are a, e, i, o, u in either uppercase or lowercase.

         **Constraints:** `ch` is a printable, non-space ASCII character.
         """,
         params=[("ch", "char")], returns="str",
         tests=[("a",), ("E",), ("z",), ("B",), ("5",), ("#",), ("u",), ("Y",)],
         hints=["Before checking vowels, how do you know it is a letter at all?",
                "Characters are numbers underneath. What range do 'a'..'z' and 'A'..'Z' cover?",
                "Convert to lowercase first, then compare against the five vowels."])
def vowel_consonant(ch):
    if not ("a" <= ch <= "z" or "A" <= ch <= "Z"):
        return "Not a letter"
    return "Vowel" if ch.lower() in "aeiou" else "Consonant"


@problem(phase=PH, title="Character Type", concepts=["char ranges"],
         statement="""
         Given a character `ch`, return `"Uppercase"`, `"Lowercase"`, `"Digit"` or `"Special"`.

         :::only java
         Do not use `Character.isDigit` or `Character.isLetter`. Compare ranges yourself.
         :::
         :::only python
         Do not use `str.isdigit` or `str.isalpha`. Compare ranges yourself.
         :::
         :::only javascript
         Do not use a character-class test. Compare ranges yourself.
         :::

         **Constraints:** `ch` is a printable, non-space ASCII character.
         """,
         params=[("ch", "char")], returns="str",
         tests=[("A",), ("z",), ("0",), ("9",), ("@",), ("M",), ("[",), ("`",)],
         hints=["Characters are ordered. What can you say about every character between 'A' and 'Z'?",
                "Write one range check per category.",
                {"java": "`ch >= 'A' && ch <= 'Z'` is uppercase; do the same for 'a'..'z' and '0'..'9'.",
                 "python": "`'A' <= ch <= 'Z'` is uppercase; do the same for 'a'..'z' and '0'..'9'.",
                 "javascript": "`ch >= 'A' && ch <= 'Z'` is uppercase; do the same for 'a'..'z' and '0'..'9'."}])
def char_type(ch):
    if "A" <= ch <= "Z":
        return "Uppercase"
    if "a" <= ch <= "z":
        return "Lowercase"
    if "0" <= ch <= "9":
        return "Digit"
    return "Special"


@problem(phase=PH, title="Simple Calculator", concepts=["switch", "edge cases"],
         statement="""
         Given integers `a` and `b` and an operator `op` (one of `+ - * / %`), return the result as a string.

         :::only java
         Division truncates toward zero: `-7 / 2` is `-3`. The remainder follows the left operand: `-7 % 2` is `-1`.
         :::
         :::only python
         Division must truncate toward zero. `//` does not: `-7 // 2` is `-4`, and `-7 % 2` is `1`. Use `int(a / b)` for the quotient. The matching remainder is `a - b * int(a / b)`.
         :::
         :::only javascript
         Division must truncate toward zero: `Math.trunc(a / b)`. The remainder follows the left operand: `-7 % 2` is `-1`. A plain `/` keeps the decimals.
         :::

         If `op` is `/` or `%` and `b` is 0, return `"Error"`.

         **Constraints:** -10^4 ≤ a, b ≤ 10^4
         """,
         params=[("a", "int"), ("op", "char"), ("b", "int")], returns="str",
         tests=[(6, "+", 3), (6, "-", 9), (7, "*", -3), (7, "/", 2), (-7, "/", 2), (7, "%", 3),
                (-7, "%", 2), (5, "/", 0), (5, "%", 0), (0, "/", 5)],
         hints=["Which statement lets you pick one branch out of five based on a single value?",
                "Which two operators can fail? What should happen before you divide?",
                {"java": "Check `b == 0` before `/` or `%`. `/` truncates toward zero, and `%` follows the left operand.",
                 "python": "Check `b == 0` first. The quotient is `int(a / b)` and the remainder is `a - b * int(a / b)`. Do not use `//`.",
                 "javascript": "Check `b === 0` before `/` or `%`. The quotient is `Math.trunc(a / b)`; `%` already follows the left operand."}])
def calculator(a, op, b):
    if op in "/%" and b == 0:
        return "Error"
    if op == "+":
        return str(a + b)
    if op == "-":
        return str(a - b)
    if op == "*":
        return str(a * b)
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    if op == "/":
        return str(q)
    return str(a - q * b)


@problem(phase=PH, title="Quadrant Finder", concepts=["nested conditions"],
         statement="""
         Given a point `(x, y)`, return `"Q1"`, `"Q2"`, `"Q3"` or `"Q4"` for the quadrant.

         If the point lies on an axis, return `"X-axis"` or `"Y-axis"`; for `(0, 0)` return `"Origin"`.

         **Constraints:** -10^9 ≤ x, y ≤ 10^9
         """,
         params=[("x", "int"), ("y", "int")], returns="str",
         tests=[(3, 4), (-3, 4), (-3, -4), (3, -4), (0, 5), (5, 0), (0, 0), (0, -2), (-2, 0)],
         hints=["Which cases are special and should be handled before the quadrants?",
                "A point on the X-axis has which coordinate equal to zero?",
                "Handle Origin, then the axes, then use the signs of x and y for the four quadrants."])
def quadrant(x, y):
    if x == 0 and y == 0:
        return "Origin"
    if y == 0:
        return "X-axis"
    if x == 0:
        return "Y-axis"
    if x > 0:
        return "Q1" if y > 0 else "Q4"
    return "Q2" if y > 0 else "Q3"


@problem(phase=PH, title="Electricity Bill", concepts=["slabs", "arithmetic"],
         statement="""
         Compute an electricity bill for `units` consumed:

         | Units | Rate |
         | --- | --- |
         | first 100 | ₹5 per unit |
         | next 100 (101–200) | ₹7 per unit |
         | above 200 | ₹10 per unit |

         A fixed meter charge of ₹50 is always added. Return the total.

         **Constraints:** 0 ≤ units ≤ 10^5
         """,
         params=[("units", "int")], returns="int",
         tests=[(0,), (50,), (100,), (150,), (200,), (250,), (101,), (1000,)],
         hints=["Work out 250 units by hand. How many units fall in each slab?",
                "How many units are charged at ₹5 when units = 70? When units = 170?",
                "Slab 1 = min(units, 100); slab 2 = min(max(units-100, 0), 100); slab 3 = max(units-200, 0)."])
def electricity_bill(units):
    s1 = min(units, 100)
    s2 = min(max(units - 100, 0), 100)
    s3 = max(units - 200, 0)
    return 50 + 5 * s1 + 7 * s2 + 10 * s3


@problem(phase=PH, title="Triangle Type", concepts=["validity check", "classification"],
         statement="""
         Given three side lengths, return `"None"` if they cannot form a triangle,
         otherwise `"Equilateral"`, `"Isosceles"` or `"Scalene"`.

         Sides form a triangle only if the sum of every two sides is **greater** than the third.

         **Constraints:** 1 ≤ a, b, c ≤ 10^4
         """,
         params=[("a", "int"), ("b", "int"), ("c", "int")], returns="str",
         tests=[(3, 3, 3), (3, 4, 5), (3, 4, 4), (1, 2, 3), (1, 1, 5), (5, 5, 8), (2, 3, 4), (10, 1, 10)],
         hints=["Why must the validity check come before the classification?",
                "How many pairs need the sum check? Write all of them.",
                "Equilateral: all equal. Isosceles: any two equal. Scalene: the rest."],
         practice=("LeetCode 3024: Type of Triangle", "https://leetcode.com/problems/type-of-triangle/"))
def triangle_type(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return "None"
    if a == b == c:
        return "Equilateral"
    if a == b or b == c or a == c:
        return "Isosceles"
    return "Scalene"


@problem(phase=PH, title="Temperature Conversion", concepts=["doubles", "formulas"],
         statement="""
         Convert `celsius` to Kelvin and Fahrenheit. Return both, Kelvin first.

         - Kelvin = Celsius + 273.15
         - Fahrenheit = Celsius × 1.80 + 32.00

         Answers within 10^-5 of the expected value are accepted.

         **Constraints:** 0 ≤ celsius ≤ 1000
         """,
         params=[("celsius", "double")], returns="double_list",
         tests=[(36.5,), (122.11,), (0.0,), (100.0,), (37.0,), (1000.0,)],
         hints=["Which data type keeps the decimal part?",
                {"java": "What does `9 / 5` evaluate to when both values are ints? Why might that drop the decimal?",
                 "python": "What does `9 / 5` evaluate to? What does `9 // 5` evaluate to, and which one does the formula need?",
                 "javascript": "What does `9 / 5` evaluate to? Does it keep the decimal?"},
                "Use the formulas exactly as given, and keep the fractional part."],
         practice=("LeetCode 2469: Convert the Temperature", "https://leetcode.com/problems/convert-the-temperature/"))
def temperature(celsius):
    return [celsius + 273.15, celsius * 1.8 + 32.0]


@problem(phase=PH, title="Smallest Even Multiple", concepts=["parity"],
         statement="""
         Return the smallest positive number that is a multiple of both 2 and `n`.

         **Constraints:** 1 ≤ n ≤ 150
         """,
         params=[("n", "int")], returns="int",
         tests=[(5,), (6,), (1,), (2,), (150,), (149,)],
         hints=["Try n = 5 and n = 6 on paper. What is different?",
                "If n is already even, is n itself a multiple of 2?",
                "Even n: answer is n. Odd n: answer is 2n."],
         practice=("LeetCode 2413: Smallest Even Multiple", "https://leetcode.com/problems/smallest-even-multiple/"))
def smallest_even_multiple(n):
    return n if n % 2 == 0 else 2 * n


@problem(phase=PH, title="Count Odds in a Range", concepts=["math instead of loops"],
         statement="""
         Return how many odd numbers lie between `low` and `high`, both inclusive.

         Solve it **without a loop**.

         **Constraints:** 0 ≤ low ≤ high ≤ 10^9
         """,
         params=[("low", "int"), ("high", "int")], returns="int",
         tests=[(3, 7), (8, 10), (0, 0), (1, 1), (2, 2), (0, 1000000000), (1, 1000000000), (7, 8)],
         hints=["How many odd numbers are there from 0 up to some number x?",
                "Count odds in [0, high] and subtract odds in [0, low - 1].",
                {"java": "Odds in [0, x] = (x + 1) / 2, with integer division.",
                 "python": "Odds in [0, x] = (x + 1) // 2.",
                 "javascript": "Odds in [0, x] = Math.floor((x + 1) / 2)."}],
         practice=("LeetCode 1523: Count Odd Numbers in an Interval Range",
                   "https://leetcode.com/problems/count-odd-numbers-in-an-interval-range/"))
def count_odds(low, high):
    return (high + 1) // 2 - low // 2


@problem(phase=PH, title="Circle Cuts", concepts=["case analysis"],
         statement="""
         A cut is a straight line through the centre of a circle. It can either touch the edge at two points
         (a full diameter) or at one point (a radius).

         Return the minimum number of cuts needed to split the circle into `n` equal slices.

         **Constraints:** 1 ≤ n ≤ 100
         """,
         params=[("n", "int")], returns="int",
         tests=[(4,), (3,), (1,), (2,), (6,), (7,), (100,), (99,)],
         hints=["Draw n = 4 and n = 3. How many cuts did each need?",
                "A full diameter makes two slices at once. When can you use only diameters?",
                "n = 1 needs 0 cuts. Even n needs n/2. Odd n needs n."],
         practice=("LeetCode 2481: Minimum Cuts to Divide a Circle",
                   "https://leetcode.com/problems/minimum-cuts-to-divide-a-circle/"))
def circle_cuts(n):
    if n == 1:
        return 0
    return n // 2 if n % 2 == 0 else n


@problem(phase=PH, title="Box Category", concepts=["overflow", "multiple flags"],
         statement="""
         A box has `length`, `width`, `height` and `mass`.

         - It is **Bulky** if any dimension is ≥ 10^4, or its volume is ≥ 10^9.
         - It is **Heavy** if mass ≥ 100.

         Return `"Both"`, `"Bulky"`, `"Heavy"` or `"Neither"`.

         :::only java
         The volume can exceed an `int`. Multiply in a `long`.
         :::
         :::only python
         The volume fits in an ordinary integer.
         :::
         :::only javascript
         The largest volume here is 10^15, which is still exact in a normal number.
         :::

         **Constraints:** 1 ≤ length, width, height ≤ 10^5, 1 ≤ mass ≤ 10^3
         """,
         params=[("length", "int"), ("width", "int"), ("height", "int"), ("mass", "int")], returns="str",
         tests=[(1000, 35, 700, 300), (200, 50, 800, 50), (10000, 1, 1, 1), (1000, 1000, 1000, 100),
                (100000, 100000, 100000, 1000), (1, 1, 1, 99), (999, 999, 999, 100)],
         hints=["Compute two booleans separately: isBulky and isHeavy.",
                {"java": "What is the largest possible volume? Does it fit in an int?",
                 "python": "What is the largest possible volume? An integer can hold it. Which comparison uses it?",
                 "javascript": "What is the largest possible volume? Is 10^15 still exact in a normal number?"},
                {"java": "Multiply into a long, then combine the two flags.",
                 "python": "Multiply the three dimensions, then combine the two flags.",
                 "javascript": "Multiply the three dimensions (10^15 is still exact), then combine the two flags."}],
         practice=("LeetCode 2525: Categorize Box According to Criteria",
                   "https://leetcode.com/problems/categorize-box-according-to-criteria/"))
def box_category(length, width, height, mass):
    bulky = max(length, width, height) >= 10**4 or length * width * height >= 10**9
    heavy = mass >= 100
    if bulky and heavy:
        return "Both"
    if bulky:
        return "Bulky"
    if heavy:
        return "Heavy"
    return "Neither"


@problem(phase=PH, title="Rectangle Overlap", concepts=["thinking in negatives"],
         statement="""
         Each rectangle is given as `x1 y1 x2 y2` on one line: bottom-left corner `(x1, y1)` and
         top-right corner `(x2, y2)`.

         Return `true` if the two rectangles overlap with a **positive area**. Touching only at an edge
         or a corner does not count.

         **Constraints:** -10^9 ≤ coordinates ≤ 10^9, x1 < x2, y1 < y2
         """,
         params=[("r1", "int[4]"), ("r2", "int[4]")], returns="bool",
         tests=[([0, 0, 2, 2], [1, 1, 3, 3]), ([0, 0, 1, 1], [1, 0, 2, 1]), ([0, 0, 1, 1], [2, 2, 3, 3]),
                ([0, 0, 5, 5], [1, 1, 2, 2]), ([0, 0, 2, 2], [0, 2, 2, 4]), ([-3, -3, 3, 3], [-1, -10, 1, 10]),
                ([0, 0, 1, 1], [0, 0, 1, 1])],
         hints=["It is easier to describe when two rectangles do NOT overlap. When is one fully to the left of the other?",
                "List the four ways they can be apart: left, right, above, below.",
                "Overlap = not (r1 left of r2 or r1 right of r2 or r1 below r2 or r1 above r2). Use <= for touching."],
         practice=("LeetCode 836: Rectangle Overlap", "https://leetcode.com/problems/rectangle-overlap/"))
def rect_overlap(r1, r2):
    return not (r1[2] <= r2[0] or r2[2] <= r1[0] or r1[3] <= r2[1] or r2[3] <= r1[1])


@problem(phase=PH, title="Valid Boomerang", concepts=["geometry with integers"],
         statement="""
         Three points are given, each as `x y` on its own line.

         Return `true` if they are all distinct and **not** on one straight line.

         **Constraints:** 0 ≤ x, y ≤ 100
         """,
         params=[("p1", "int[2]"), ("p2", "int[2]"), ("p3", "int[2]")], returns="bool",
         tests=[([1, 1], [2, 3], [3, 2]), ([1, 1], [2, 2], [3, 3]), ([0, 0], [0, 0], [1, 1]),
                ([0, 0], [0, 5], [0, 9]), ([0, 0], [1, 0], [0, 1]), ([2, 4], [4, 8], [6, 12])],
         hints=["Three points are on one line when the slopes p1→p2 and p1→p3 are equal.",
                "Dividing to get a slope can give decimals or divide-by-zero. Can you compare without dividing?",
                "Cross-multiply: (y2-y1)*(x3-x1) != (y3-y1)*(x2-x1). Duplicate points also make this equal."],
         practice=("LeetCode 1037: Valid Boomerang", "https://leetcode.com/problems/valid-boomerang/"))
def boomerang(p1, p2, p3):
    return (p2[1] - p1[1]) * (p3[0] - p1[0]) != (p3[1] - p1[1]) * (p2[0] - p1[0])


@problem(phase=PH, title="Clock Angle", difficulty="medium", concepts=["formulas", "doubles"],
         statement="""
         Given `hour` and `minutes` on an analog clock, return the **smaller** angle (in degrees)
         between the hour hand and the minute hand.

         The hour hand moves continuously, so at 3:30 it is halfway between 3 and 4.
         Answers within 10^-5 are accepted.

         **Constraints:** 1 ≤ hour ≤ 12, 0 ≤ minutes ≤ 59
         """,
         params=[("hour", "int"), ("minutes", "int")], returns="double",
         tests=[(12, 30), (3, 30), (3, 15), (4, 50), (12, 0), (6, 0), (9, 45), (1, 59)],
         hints=["How many degrees does the minute hand move per minute? The hour hand per hour?",
                "How far does the hour hand move in one minute?",
                "minuteAngle = 6*m; hourAngle = 30*(h % 12) + 0.5*m; answer = min(diff, 360 - diff)."],
         practice=("LeetCode 1344: Angle Between Hands of a Clock",
                   "https://leetcode.com/problems/angle-between-hands-of-a-clock/"))
def clock_angle(hour, minutes):
    diff = abs(30 * (hour % 12) + 0.5 * minutes - 6 * minutes)
    return min(diff, 360 - diff)
