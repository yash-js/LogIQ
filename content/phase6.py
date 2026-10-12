from core import problem

PH = 6


@problem(phase=PH, title="Self Dividing Numbers", returns="int_list", concepts=["loop + digit check"],
         statement="""
         A self-dividing number is divisible by every one of its digits and contains no zero.
         Return all self-dividing numbers from `left` to `right` inclusive, in increasing order.

         **Constraints:** 1 ≤ left ≤ right ≤ 10^4 (the range always contains at least one answer)
         """,
         params=[("left", "int"), ("right", "int")],
         tests=[(1, 22), (47, 85), (1, 1), (9999, 10000), (100, 130), (1, 10000)],
         hints=["Write isSelfDividing(n) on its own first.",
                "What should happen as soon as a digit is 0?",
                "Loop over the range and collect numbers that pass the check."],
         practice=("LeetCode 728: Self Dividing Numbers", "https://leetcode.com/problems/self-dividing-numbers/"))
def self_dividing(left, right):
    return [x for x in range(left, right + 1) if all(d != "0" and x % int(d) == 0 for d in str(x))]


@problem(phase=PH, title="Base 7", returns="str", concepts=["base conversion"],
         statement="""
         Return the base-7 representation of `num` as a string (with `-` for negatives).

         **Constraints:** −10^7 ≤ num ≤ 10^7
         """,
         params=[("num", "int")],
         tests=[(100,), (-7,), (0,), (6,), (10000000,), (-10000000,), (49,)],
         hints=["You converted to base 2 in Phase 3. What changes for base 7?",
                "Handle the sign separately.",
                {"java": "Repeatedly take n % 7 and n /= 7; the digits come out reversed. Take the sign off first.",
                 "python": "Repeatedly take n % 7 and n //= 7; the digits come out reversed. Take the sign off first.",
                 "javascript": "Repeatedly take n % 7 and n = Math.floor(n / 7); the digits come out reversed. Take the sign off first, because floor division rounds the wrong way for negatives."}],
         practice=("LeetCode 504: Base 7", "https://leetcode.com/problems/base-7/"))
def base7(num):
    if num == 0:
        return "0"
    n, out = abs(num), ""
    while n:
        out = str(n % 7) + out
        n //= 7
    return ("-" if num < 0 else "") + out


@problem(phase=PH, title="Number Complement", returns="int", concepts=["binary digits"],
         statement="""
         Flip every bit of `num`'s binary form (no leading zeros) and return the resulting number.
         Example: 5 = 101 → 010 = 2.

         **Constraints:** 1 ≤ num ≤ 2^31 − 1
         """,
         params=[("num", "int")],
         tests=[(5,), (1,), (2,), (7,), (10,), (2147483647,), (1073741824,)],
         hints=["How do you read the bits one by one?",
                "Each flipped bit has a place value. Which power of 2 belongs to bit i?",
                {"java": "For each bit b at position i, add (1 - b) times 2^i. Keep the place value in a long.",
                 "python": "For each bit b at position i, add (1 - b) times 2**i. An integer will not overflow.",
                 "javascript": "For each bit b at position i, add (1 - b) times 2**i. These values fit exactly in a normal number."}],
         practice=("LeetCode 476: Number Complement", "https://leetcode.com/problems/number-complement/"))
def complement(num):
    return num ^ ((1 << num.bit_length()) - 1)


@problem(phase=PH, title="Excel Column Number", returns="int", concepts=["base 26"],
         statement="""
         Spreadsheet columns go A, B, …, Z, AA, AB, …. Return the column number for `title` (A = 1).

         **Constraints:** 1 ≤ title.length ≤ 6, uppercase letters
         """,
         params=[("title", "str")],
         tests=[("A",), ("AB",), ("ZY",), ("Z",), ("AAA",), ("FXSHRX",)],
         hints=["Is this like converting a number from some base? Which base?",
                "What value does each letter have?",
                "result = result * 26 + (c − 'A' + 1) for each letter."],
         practice=("LeetCode 171: Excel Sheet Column Number", "https://leetcode.com/problems/excel-sheet-column-number/"))
def excel_number(title):
    r = 0
    for c in title:
        r = r * 26 + ord(c) - 64
    return r


@problem(phase=PH, title="Excel Column Title", difficulty="medium", returns="str", concepts=["base 26 without zero"],
         statement="""
         The reverse of the previous problem: return the column title for `n`.

         **Constraints:** 1 ≤ n ≤ 2^31 − 1
         """,
         params=[("n", "int")],
         tests=[(1,), (28,), (701,), (26,), (52,), (2147483647,), (27,)],
         hints=["Try the normal base-26 loop on n = 26. What goes wrong?",
                "There is no digit for zero here. How can you shift values so that A..Z become 0..25?",
                {"java": "n--; the digit is (char)('A' + n % 26); then n /= 26. Repeat while n > 0, then reverse.",
                 "python": "n -= 1; the digit is chr(ord('A') + n % 26); then n //= 26. Repeat while n > 0, then reverse.",
                 "javascript": "n--; the digit is String.fromCharCode(65 + (n % 26)); then n = Math.floor(n / 26). Repeat while n > 0, then reverse."}],
         practice=("LeetCode 168: Excel Sheet Column Title", "https://leetcode.com/problems/excel-sheet-column-title/"))
def excel_title(n):
    out = ""
    while n:
        n -= 1
        out = chr(65 + n % 26) + out
        n //= 26
    return out


@problem(phase=PH, title="Add Strings", difficulty="medium", returns="str", concepts=["grade-school addition"],
         statement="""
         Return the sum of two non-negative numbers given as strings. Do not convert them to integers
         (they can have 10^4 digits).

         **Constraints:** 1 ≤ lengths ≤ 10^4, no leading zeros except "0"
         """,
         params=[("num1", "str"), ("num2", "str")],
         tests=[("11", "123"), ("456", "77"), ("0", "0"), ("999", "1"), ("1", "9" * 50)],
         gen=lambda r: ("1" + "".join(r.choice("0123456789") for _ in range(9000)),
                        str(r.randint(1, 9)) + "".join(r.choice("0123456789") for _ in range(r.randint(0, 9999)))), gen_count=1,
         hints=["You did this with binary strings in Phase 5. What changes for base 10?",
                "What is the largest possible column sum, and what is the carry then?",
                "Add from the right with carry; append sum % 10; reverse at the end."],
         practice=("LeetCode 415: Add Strings", "https://leetcode.com/problems/add-strings/"))
def add_strings(num1, num2):
    import sys
    sys.set_int_max_str_digits(0)
    return str(int(num1) + int(num2))


@problem(phase=PH, title="Add to Array-Form", difficulty="medium", returns="int[]", concepts=["carry with an int"],
         statement="""
         `num` is a number stored as digits (most significant first). Return the digits of `num + k`.

         **Constraints:** 1 ≤ num.length ≤ 10^4, 1 ≤ k ≤ 10^4
         """,
         params=[("num", "int[]"), ("k", "int")],
         tests=[([1, 2, 0, 0], 34), ([2, 7, 4], 181), ([2, 1, 5], 806), ([0], 10000), ([9, 9, 9, 9], 1)],
         hints=["Can k itself act as the carry?",
                "Add k to the last digit. What do you keep, and what moves left?",
                {"java": "From the right: k += num[i]; the digit is k % 10; then k /= 10. Continue while k > 0 after the array ends.",
                 "python": "From the right: k += num[i]; the digit is k % 10; then k //= 10. Continue while k > 0 after the array ends.",
                 "javascript": "From the right: k += num[i]; the digit is k % 10; then k = Math.floor(k / 10). Continue while k > 0 after the array ends."}],
         practice=("LeetCode 989: Add to Array-Form of Integer", "https://leetcode.com/problems/add-to-array-form-of-integer/"))
def array_form(num, k):
    return [int(c) for c in str(int("".join(map(str, num))) + k)]


@problem(phase=PH, title="Day of the Week", difficulty="medium", returns="str", concepts=["counting days", "leap years"],
         statement="""
         Return the weekday name (`Sunday`, `Monday`, …, `Saturday`) for a date between 1971 and 2100.
         1 January 1971 was a Friday.

         **Constraints:** valid dates from 1971-01-01 to 2100-12-31
         """,
         params=[("day", "int"), ("month", "int"), ("year", "int")],
         tests=[(31, 8, 2019), (18, 7, 1999), (15, 8, 1993), (1, 1, 1971), (31, 12, 2100), (29, 2, 2000), (11, 10, 2026)],
         hints=["How many days have passed since 1 January 1971?",
                "Add full years first (365 or 366), then full months, then days.",
                "Reuse your leap-year check from Phase 1. Then weekday = (Friday + days) % 7."],
         practice=("LeetCode 1185: Day of the Week", "https://leetcode.com/problems/day-of-the-week/"))
def weekday(day, month, year):
    import datetime
    return datetime.date(year, month, day).strftime("%A")


@problem(phase=PH, title="Robot Return", returns="bool", concepts=["simulation"],
         statement="""
         A robot starts at (0, 0) and follows `moves`: U, D, L, R move one step. Return `true` if it ends at the origin.

         **Constraints:** 1 ≤ moves.length ≤ 2·10^4
         """,
         params=[("moves", "str")],
         tests=[("UD",), ("LL",), ("RRDDLULU",), ("U",), ("LRUDLRUD",)],
         gen=lambda r: ("".join(r.choice("UDLR") for _ in range(r.randint(1, 20000))),), gen_count=1,
         hints=["What state do you need to track?",
                "How does each letter change that state?",
                "Track x and y, one branch per letter. Return whether both are back at 0."],
         practice=("LeetCode 657: Robot Return to Origin", "https://leetcode.com/problems/robot-return-to-origin/"))
def robot(moves):
    return moves.count("U") == moves.count("D") and moves.count("L") == moves.count("R")


@problem(phase=PH, title="Attendance Award", returns="bool", concepts=["counting + streaks"],
         statement="""
         A record uses `A` (absent), `L` (late), `P` (present). A student gets an award if they were absent
         fewer than 2 days in total **and** were never late 3 or more days in a row.

         **Constraints:** 1 ≤ s.length ≤ 1000
         """,
         params=[("s", "str")],
         tests=[("PPALLP",), ("PPALLL",), ("AA",), ("P",), ("LALL",), ("LLPLLPA",)],
         hints=["Which two things do you need to track?",
                "One is a total, the other is a streak. How does each update?",
                {"java": "absent++ on 'A'; late = (c == 'L') ? late + 1 : 0; fail if absent >= 2 or late >= 3.",
                 "python": "absent += 1 on 'A'; late = late + 1 if c == 'L' else 0; fail if absent >= 2 or late >= 3.",
                 "javascript": "absent++ on 'A'; late = (c === 'L') ? late + 1 : 0; fail if absent >= 2 or late >= 3."}],
         practice=("LeetCode 551: Student Attendance Record I", "https://leetcode.com/problems/student-attendance-record-i/"))
def attendance(s):
    return s.count("A") < 2 and "LLL" not in s


@problem(phase=PH, title="Goal Parser", returns="str", concepts=["look-ahead parsing"],
         statement="""
         `command` is made of `G`, `()` and `(al)`. Interpret `G` as "G", `()` as "o" and `(al)` as "al",
         and return the result.

         **Constraints:** 1 ≤ command.length ≤ 100
         """,
         params=[("command", "str")],
         tests=[("G()(al)",), ("G()()()()(al)",), ("(al)G(al)()()G",), ("G",), ("()",)],
         hints=["When you see '(', how do you know which token it starts?",
                "Look at the next character.",
                "If s[i] == 'G' take G, i += 1; if s[i+1] == ')' take o, i += 2; else take al, i += 4."],
         practice=("LeetCode 1678: Goal Parser Interpretation", "https://leetcode.com/problems/goal-parser-interpretation/"))
def goal_parser(command):
    return command.replace("()", "o").replace("(al)", "al")


@problem(phase=PH, title="Reverse in Chunks", returns="str", concepts=["stepping by 2k"],
         statement="""
         For every block of `2k` characters, reverse the first `k`. If fewer than k remain, reverse them all;
         if between k and 2k remain, reverse the first k.

         **Constraints:** 1 ≤ s.length ≤ 10^4, 1 ≤ k ≤ 10^4
         """,
         params=[("s", "str"), ("k", "int")],
         tests=[("abcdefg", 2), ("abcd", 2), ("a", 5), ("abcdefgh", 3), ("abcdefghij", 1)],
         hints=["Where does each block start?",
                "Where does the part to reverse end? Careful at the end of the string.",
                "for start = 0; start < n; start += 2k: reverse [start, min(start + k, n) − 1]."],
         practice=("LeetCode 541: Reverse String II", "https://leetcode.com/problems/reverse-string-ii/"))
def rev_chunks(s, k):
    a = list(s)
    for i in range(0, len(a), 2 * k):
        a[i:i + k] = reversed(a[i:i + k])
    return "".join(a)


@problem(phase=PH, title="Lemonade Change", returns="bool", concepts=["greedy simulation"],
         statement="""
         Lemonade costs ₹5. Customers pay with ₹5, ₹10 or ₹20 notes in the order given. You start with no change.
         Return `true` if you can give every customer correct change.

         **Constraints:** 1 ≤ bills.length ≤ 10^5
         """,
         params=[("bills", "int[]")],
         tests=[([5, 5, 5, 10, 20],), ([5, 5, 10, 10, 20],), ([10],), ([5, 5, 5, 20],), ([5, 10, 5, 20],)],
         gen=lambda r: ([5] * 50 + [r.choice([5, 10, 20]) for _ in range(r.randint(1, 10**4))],), gen_count=1,
         hints=["Which notes do you need to remember?",
                "For a ₹20, which way of giving ₹15 change is smarter, and why?",
                "Prefer one 10 plus one 5; otherwise three 5s; otherwise the answer is no."],
         practice=("LeetCode 860: Lemonade Change", "https://leetcode.com/problems/lemonade-change/"))
def lemonade(bills):
    five = ten = 0
    for b in bills:
        if b == 5:
            five += 1
        elif b == 10:
            if not five:
                return False
            five -= 1
            ten += 1
        else:
            if ten and five:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True


@problem(phase=PH, title="Plant the Flowers", returns="bool", concepts=["neighbour checks"],
         statement="""
         `bed` has 0 (empty) and 1 (planted). Flowers cannot be planted in adjacent plots.
         Return `true` if `n` new flowers can be planted.

         **Constraints:** 1 ≤ bed.length ≤ 2·10^4, no two adjacent 1s at the start, 0 ≤ n ≤ bed.length
         """,
         params=[("bed", "int[]"), ("n", "int")],
         tests=[([1, 0, 0, 0, 1], 1), ([1, 0, 0, 0, 1], 2), ([0], 1), ([0, 0, 1, 0, 0], 2), ([1], 0), ([0, 0], 2)],
         hints=["When is plot i plantable?",
                "What about the first and last plots, which have only one neighbour?",
                "Treat outside the array as empty; plant greedily and count."],
         practice=("LeetCode 605: Can Place Flowers", "https://leetcode.com/problems/can-place-flowers/"))
def flowers(bed, n):
    b = list(bed)
    c = 0
    for i in range(len(b)):
        if b[i] == 0 and (i == 0 or b[i - 1] == 0) and (i == len(b) - 1 or b[i + 1] == 0):
            b[i] = 1
            c += 1
    return c >= n


@problem(phase=PH, title="Mountain Array", returns="bool", concepts=["walking phases"],
         statement="""
         Return `true` if `arr` strictly increases to a peak and then strictly decreases.
         The peak cannot be the first or last element.

         **Constraints:** 1 ≤ arr.length ≤ 10^4
         """,
         params=[("arr", "int[]")],
         tests=[([2, 1],), ([3, 5, 5],), ([0, 3, 2, 1],), ([1, 2, 3],), ([3, 2, 1],), ([1, 3, 2],), ([1],)],
         hints=["Walk up as far as you can. Where did you stop?",
                "Is that stopping point allowed to be index 0 or n − 1?",
                "Climb while increasing, check the peak position, descend while decreasing, check you reached the end."],
         practice=("LeetCode 941: Valid Mountain Array", "https://leetcode.com/problems/valid-mountain-array/"))
def mountain(arr):
    n, i = len(arr), 0
    while i + 1 < n and arr[i] < arr[i + 1]:
        i += 1
    if i == 0 or i == n - 1:
        return False
    while i + 1 < n and arr[i] > arr[i + 1]:
        i += 1
    return i == n - 1


@problem(phase=PH, title="Summary Ranges", returns="str_list", concepts=["grouping runs"],
         statement="""
         `nums` is sorted with distinct values. Print each run of consecutive numbers on its own line as
         `a->b`, or just `a` if the run has one number.

         **Constraints:** 1 ≤ nums.length ≤ 20
         """,
         params=[("nums", "int[]")],
         tests=[([0, 1, 2, 4, 5, 7],), ([0, 2, 3, 4, 6, 8, 9],), ([5],), ([-3, -2, -1],), ([1, 3, 5],)],
         hints=["How do you know a run has ended?",
                "Same run-detection idea as String Compression.",
                "Remember the run start; when nums[i+1] != nums[i] + 1 (or at the end), output the run."],
         practice=("LeetCode 228: Summary Ranges", "https://leetcode.com/problems/summary-ranges/"))
def ranges(nums):
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}")
        i = j + 1
    return out


@problem(phase=PH, title="Tic-Tac-Toe Winner", difficulty="medium", returns="str", concepts=["grid simulation"],
         statement="""
         Players A (X) and B (O) take turns on a 3×3 grid; A moves first. Each row of `moves` is `row col`.
         Return `A` or `B` for the winner, `Draw` if the board is full with no winner, or `Pending` otherwise.

         **Constraints:** 1 ≤ moves.length ≤ 9, all moves valid, play stops when someone wins
         """,
         params=[("moves", "int[][]")],
         tests=[([[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]],), ([[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]],),
                ([[0, 0], [1, 1], [2, 0], [1, 0], [1, 2], [2, 1], [0, 1], [0, 2], [2, 2]],), ([[0, 0], [1, 1]],),
                ([[1, 1]],), ([[0, 2], [0, 0], [1, 1], [1, 0], [2, 0]],)],
         hints=["Replay the moves onto a 3×3 char grid first.",
                "How many lines can a player win on? List them.",
                "Check 3 rows, 3 columns, 2 diagonals; if no winner: 9 moves → Draw, else Pending."],
         practice=("LeetCode 1275: Find Winner on a Tic Tac Toe Game",
                   "https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game/"))
def tictactoe(moves):
    g = [[""] * 3 for _ in range(3)]
    for i, (r, c) in enumerate(moves):
        g[r][c] = "A" if i % 2 == 0 else "B"
    lines = [[(r, c) for c in range(3)] for r in range(3)] + [[(r, c) for r in range(3)] for c in range(3)]
    lines += [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]
    for ln in lines:
        vals = {g[r][c] for r, c in ln}
        if len(vals) == 1 and "" not in vals:
            return vals.pop()
    return "Draw" if len(moves) == 9 else "Pending"


@problem(phase=PH, title="Pascal Row", returns="long_list", concepts=["update a row in place"],
         statement="""
         Return row `k` (0-indexed) of Pascal's triangle using only one array of size k + 1.

         **Constraints:** 0 ≤ k ≤ 33
         """,
         params=[("k", "int")],
         tests=[(3,), (0,), (1,), (10,), (33,)],
         hints=["If you update the row from left to right, what value do you lose?",
                "Try updating from right to left instead.",
                "row[j] += row[j−1] for j from i down to 1, for each new row i."],
         practice=("LeetCode 119: Pascal's Triangle II", "https://leetcode.com/problems/pascals-triangle-ii/"))
def pascal_row(k):
    row = [1]
    for _ in range(k):
        row = [1] + [row[j - 1] + row[j] for j in range(1, len(row))] + [1]
    return row


@problem(phase=PH, title="Count and Say", difficulty="medium", returns="str", concepts=["run-length on a sequence"],
         statement="""
         Term 1 is `1`. Each next term describes the previous one by runs: `1` → "one 1" → `11` → "two 1s" → `21`
         → `1211` → `111221` …. Return term `n`.

         **Constraints:** 1 ≤ n ≤ 30
         """,
         params=[("n", "int")],
         tests=[(1,), (4,), (5,), (2,), (10,), (30,)],
         hints=["You already wrote run-length compression. How is this different?",
                "Here the count comes before the digit.",
                {"java": "Start with \"1\" and apply the describe step n - 1 times, appending into a StringBuilder.",
                 "python": "Start with \"1\" and apply the describe step n - 1 times, collecting characters in a list and joining.",
                 "javascript": "Start with \"1\" and apply the describe step n - 1 times, building the next string as you go."}],
         practice=("LeetCode 38: Count and Say", "https://leetcode.com/problems/count-and-say/"))
def count_say(n):
    s = "1"
    for _ in range(n - 1):
        out, i = [], 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            out.append(f"{j - i}{s[i]}")
            i = j
        s = "".join(out)
    return s


@problem(phase=PH, title="Integer to Roman", difficulty="medium", returns="str", concepts=["value table"],
         statement="""
         Convert `num` to a Roman numeral using the subtractive forms IV, IX, XL, XC, CD and CM.

         **Constraints:** 1 ≤ num ≤ 3999
         """,
         params=[("num", "int")],
         tests=[(3,), (58,), (1994,), (3999,), (4,), (944,), (1000,)],
         hints=["Which symbol do you write first for 1994?",
                "Treat the subtractive forms as symbols of their own.",
                "Table values 1000, 900, 500, 400, … 1; while num >= value, append the symbol and subtract."],
         practice=("LeetCode 12: Integer to Roman", "https://leetcode.com/problems/integer-to-roman/"))
def int_to_roman(num):
    table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
             (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = ""
    for v, sym in table:
        while num >= v:
            out += sym
            num -= v
    return out


@problem(phase=PH, title="String to Integer", difficulty="medium", returns="int", concepts=["parsing", "overflow", "edge cases"],
         statement="""
         Convert `s` to a 32-bit signed integer like C's `atoi`:

         1. Skip leading spaces.
         2. Read an optional `+` or `-`.
         3. Read digits until a non-digit or the end.
         4. No digits read → 0. Clamp the result to [−2^31, 2^31 − 1].

         :::only java
         Build the number in a `long` and clamp as soon as it leaves the `int` range.
         :::
         :::only python
         Integers do not overflow, so compare with 2147483647 and -2147483648 and clamp yourself.
         :::
         :::only javascript
         The value stays exact while you read it. Clamp to 2147483647 and -2147483648 before you return.
         :::

         **Constraints:** 1 ≤ s.length ≤ 200, letters, digits, spaces, `+ - .`
         """,
         params=[("s", "str")],
         tests=[("42",), ("   -042",), ("1337c0d3",), ("0-1",), ("words and 987",), ("-91283472332",),
                ("+1",), ("+-12",), ("2147483648",), ("   ",)],
         hints=["Follow the four steps literally, each with its own small loop or check.",
                "When can the number overflow, and how do you notice before it does?",
                {"java": "Build in a long and clamp as soon as it passes Integer.MAX_VALUE or Integer.MIN_VALUE.",
                 "python": "Integers never overflow, so compare with 2147483647 and -2147483648 and clamp yourself.",
                 "javascript": "A normal number stays exact past the 32-bit range. Compare with 2147483647 and -2147483648 and clamp."}],
         practice=("LeetCode 8: String to Integer (atoi)", "https://leetcode.com/problems/string-to-integer-atoi/"))
def atoi(s):
    i, n = 0, len(s)
    while i < n and s[i] == " ":
        i += 1
    sign = 1
    if i < n and s[i] in "+-":
        sign = -1 if s[i] == "-" else 1
        i += 1
    v = 0
    while i < n and s[i].isdigit():
        v = v * 10 + int(s[i])
        i += 1
    return max(-2**31, min(2**31 - 1, sign * v))


@problem(phase=PH, title="Zigzag Conversion", difficulty="medium", returns="str", concepts=["simulating movement"],
         statement="""
         Write `s` in a zigzag over `rows` rows (down, then diagonally up, repeat), then read row by row.
         "PAYPALISHIRING" with 3 rows reads "PAHNAPLSIIGYIR".

         **Constraints:** 1 ≤ s.length ≤ 1000, 1 ≤ rows ≤ 1000
         """,
         params=[("s", "str"), ("rows", "int")],
         tests=[("PAYPALISHIRING", 3), ("PAYPALISHIRING", 4), ("A", 1), ("AB", 1), ("ABCDE", 10), ("ABCDEFG", 2)],
         hints=[{"java": "Keep one StringBuilder per row. Which row does each character go to?",
                 "python": "Keep one list of characters per row. Which row does each character go to?",
                 "javascript": "Keep one string per row. Which row does each character go to?"},
                "When does the direction flip?",
                "row += dir; flip dir at row 0 and row rows−1. Special-case rows == 1."],
         practice=("LeetCode 6: Zigzag Conversion", "https://leetcode.com/problems/zigzag-conversion/"))
def zigzag(s, rows):
    if rows == 1:
        return s
    out = [""] * rows
    r, d = 0, 1
    for c in s:
        out[r] += c
        if r == 0:
            d = 1
        elif r == rows - 1:
            d = -1
        r += d
    return "".join(out)


@problem(phase=PH, title="Multiply Strings", difficulty="stretch", returns="str", concepts=["long multiplication"],
         statement="""
         Return the product of two non-negative numbers given as strings, without converting them to numbers.

         **Constraints:** 1 ≤ lengths ≤ 200, no leading zeros except "0"
         """,
         params=[("num1", "str"), ("num2", "str")],
         tests=[("2", "3"), ("123", "456"), ("0", "52"), ("999", "999"), ("9" * 200, "9" * 200), ("1", "1")],
         hints=["How long can the product be?",
                "Digit i of num1 times digit j of num2 lands in which position of the result?",
                {"java": "int[] res of size m + n; res[i + j + 1] += a * b; then fix carries from the right; strip leading zeros.",
                 "python": "res = [0] * (m + n); res[i + j + 1] += a * b; then fix carries from the right; strip leading zeros.",
                 "javascript": "res = new Array(m + n).fill(0); res[i + j + 1] += a * b; then fix carries from the right; strip leading zeros."}],
         practice=("LeetCode 43: Multiply Strings", "https://leetcode.com/problems/multiply-strings/"))
def multiply(num1, num2):
    return str(int(num1) * int(num2))


@problem(phase=PH, title="Spiral Order", difficulty="stretch", returns="int_list", concepts=["boundaries"],
         statement="""
         Return all elements of `matrix` in clockwise spiral order, starting at the top-left.

         **Constraints:** 1 ≤ rows, cols ≤ 10
         """,
         params=[("matrix", "int[][]")],
         tests=[([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],), ([[7]],),
                ([[1], [2], [3]],), ([[1, 2, 3]],)],
         gen=lambda r: ([[r.randint(-100, 100) for _ in range(c)] for c in [r.randint(1, 10)] for _ in range(r.randint(1, 10))],),
         gen_count=2,
         hints=["Keep four boundaries: top, bottom, left, right.",
                "After walking the top row, which boundary moves?",
                "Loop while top <= bottom and left <= right; check the boundaries again before the bottom row and left column."],
         practice=("LeetCode 54: Spiral Matrix", "https://leetcode.com/problems/spiral-matrix/"))
def spiral(matrix):
    m = [row[:] for row in matrix]
    out = []
    while m:
        out += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]
    return out


@problem(phase=PH, title="Rotate the Image", difficulty="stretch", returns="int[][]", concepts=["transpose + reverse"],
         statement="""
         Rotate the square `matrix` 90 degrees clockwise **in place** and return it.

         **Constraints:** 1 ≤ n ≤ 20
         """,
         params=[("matrix", "int[][]")],
         tests=[([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],),
                ([[1]],), ([[1, 2], [3, 4]],)],
         gen=lambda r: ((lambda n: [[r.randint(-99, 99) for _ in range(n)] for _ in range(n)])(r.randint(1, 20)),),
         gen_count=1,
         hints=["Where does matrix[0][0] go? matrix[0][n−1]?",
                "Two operations you already know combine into a rotation.",
                "Transpose in place (swap [i][j] with [j][i] for j > i), then reverse each row."],
         practice=("LeetCode 48: Rotate Image", "https://leetcode.com/problems/rotate-image/"))
def rotate_image(matrix):
    return [list(r) for r in zip(*matrix[::-1])]


@problem(phase=PH, title="Valid Sudoku", difficulty="stretch", returns="bool", concepts=["3 checks, plain arrays"],
         statement="""
         `board` has 9 lines of 9 characters (`1`–`9` or `.` for empty). Return `true` if no row, column or
         3×3 box contains a repeated digit. The board does not need to be solvable.

         **Constraints:** exactly 9 rows of 9 characters
         """,
         params=[("board", "str[]")],
         tests=[(["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"],),
                (["83..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"],),
                (["........."] * 9,),
                (["1........", ".........", ".........", ".........", ".........", ".........", ".........", ".........", "1........"],),
                (["1........", ".1.......", ".........", ".........", ".........", ".........", ".........", ".........", "........."],),
                (["123456789", "456789123", "789123456", "214365897", "365897214", "897214365", "531642978", "642978531", "978531642"],)],
         hints=[{"java": "Start with only the rows. How do you detect a repeat with a boolean[10]?",
                 "python": "Start with only the rows. How do you detect a repeat with a list of 10 flags?",
                 "javascript": "Start with only the rows. How do you detect a repeat with an array of 10 flags?"},
                "Columns are the same idea with i and j swapped.",
                {"java": "Box index = (i / 3) * 3 + j / 3. Keep boolean[9][10] for rows, columns and boxes.",
                 "python": "Box index = (i // 3) * 3 + j // 3. Keep three lists of nine lists of ten flags: rows, columns and boxes.",
                 "javascript": "Box index = Math.floor(i / 3) * 3 + Math.floor(j / 3). Keep a 9 by 10 array of flags for rows, columns and boxes."}],
         practice=("LeetCode 36: Valid Sudoku", "https://leetcode.com/problems/valid-sudoku/"))
def sudoku(board):
    seen = set()
    for i in range(9):
        for j in range(9):
            c = board[i][j]
            if c == ".":
                continue
            keys = {("r", i, c), ("c", j, c), ("b", i // 3, j // 3, c)}
            if keys & seen:
                return False
            seen |= keys
    return True
