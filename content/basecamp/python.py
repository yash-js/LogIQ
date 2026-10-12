from bc import unit

L = "python"

# 1 ---------------------------------------------------------------- output
u = unit(L, "Hello, output", """
`print(x)` shows `x` and then moves to a new line. No semicolons, no `main` needed:
a Python file simply runs from top to bottom.

`print(a, b)` puts a space between the values. `print(x, end="")` stays on the same line.
""")
u.predict("""
print("Hello")
print("World")
""", "Each `print` ends with a newline, so the words land on two lines.")
u.predict("""
print("Log", end="")
print("ic", end="")
print("Quest")
""", "`end=\"\"` replaces the newline with nothing, so the pieces join.")
u.choice("What does `print(\"a\", \"b\", \"c\")` show?", ["abc", "a b c", "a,b,c", "('a', 'b', 'c')"], 1,
         "Commas in `print` separate values with one space by default.")
u.blank("Print `1-2-3` using one print call.", """
print(1, 2, 3, sep=___)
""", [['"-"', "'-'"]], "`sep` sets what goes between the values (a space by default).")
u.predict("""
print("2 + 3")
print(2 + 3)
""", "Inside quotes it's text and printed as-is. Without quotes Python does the maths first.")
u.fix("This should print `Ready` but crashes. Fix it.", """
Print("Ready")
""", """
print("Ready")
""", "Python is case-sensitive. The error says `NameError: name 'Print' is not defined`.")

# 2 ---------------------------------------------------------------- variables
u = unit(L, "Variables and types", """
A variable is a name pointing at a value. No type keyword is needed; Python works it out:

```python
age = 21          # int
price = 9.5       # float
name = "Yash"     # str
done = True       # bool (capital T)
```

`type(x)` tells you what you have.
""")
u.predict("""
x = 10
x = x + 5
print(x)
""", "`x = x + 5` reads 10, adds 5, and stores 15 back in `x`.")
u.choice("Which value is a `bool` in Python?", ["true", "\"True\"", "True", "1.0"], 2,
         "Booleans are `True` and `False`, capitalised. `\"True\"` in quotes is a string.")
u.predict("""
first = "Logic"
second = "Quest"
print(first + second)
print(first, second)
""", "`+` joins strings with no space; a comma in `print` adds one.")
u.blank("Swap `a` and `b` in one line.", """
a = 1
b = 2
a, b = ___, ___
print(a, b)
""", [["b"], ["a"]], "Python evaluates the right side first, then assigns: a gets old b, b gets old a.")
u.order("Arrange the lines so the program prints `20`.", """
a = 4
b = 5
product = a * b
print(product)
""", "A name must have a value before you use it.")
u.fix("This should print `Age: 21` but crashes with a TypeError. Fix it.", """
age = 21
print("Age: " + age)
""", """
age = 21
print("Age: " + str(age))
""", "You can't `+` a string and an int. Convert with `str(age)` (or use `print(\"Age:\", age)`).")

# 3 ---------------------------------------------------------------- operators
u = unit(L, "Operators", """
`/` always gives a float: `7 / 2` is `3.5`. Use `//` for whole-number division: `7 // 2` is `3`.
`%` is the remainder, `**` is power.

`x += 3` is short for `x = x + 3`. There is no `x++` in Python.
""")
u.predict("""
print(7 / 2)
print(7 // 2)
print(7 % 2)
print(2 ** 5)
""", "`/` → 3.5, `//` → 3, `%` → 1, `**` → 32.")
u.predict("""
x = 5
x += 3
x *= 2
x -= 1
print(x)
""", "5 → 8 → 16 → 15.")
u.choice("What is `2 + 3 * 4` in Python?", ["20", "14", "24", "9"], 1,
         "`*` happens before `+`: 3 × 4 = 12, then 2 + 12.")
u.predict("""
print(-7 % 2)
print(-7 // 2)
""", "Python's `//` rounds **down** (to -4) and `%` follows the sign of the right number (1). Java and JavaScript give -1 and -3.")
u.blank("Print the last digit of `n`, then `n` without its last digit.", """
n = 1234
print(n ___ 10)
print(n ___ 10)
""", [["%"], ["//"]], "`% 10` gives the last digit; `// 10` removes it. `/ 10` would give 123.4.")
u.fix("This should print `5`, the number of full boxes of 4 you can fill from 22 eggs, but prints `5.5`.", """
eggs = 22
print(eggs / 4)
""", """
eggs = 22
print(eggs // 4)
""", "Full boxes is whole-number division: `//`.")

# 4 ---------------------------------------------------------------- strings
u = unit(L, "Strings and characters", """
A `str` is text. A single character is just a string of length 1.

- `len(s)` → number of characters
- `s[i]` → character at index `i` (from 0); `s[-1]` is the last one
- `ord("a")` → 97, `chr(98)` → `"b"`
- Compare text with `==`.
""")
u.predict("""
s = "quest"
print(len(s))
print(s[0])
print(s[-1])
""", "Negative indexes count from the end: `s[-1]` is the last character.")
u.predict("""
c = "a"
print(ord(c) + 1)
print(chr(ord(c) + 1))
""", "`ord` turns a character into its code (97); `chr` turns a code back into a character.")
u.choice("Which expression is True when `s` is `\"abc\"`?", ["s[3] == \"c\"", "s[len(s) - 1] == \"c\"", "s.length == 3", "s[1] == \"a\""], 1,
         "Indexes go 0..len − 1. `s[3]` raises IndexError and strings have no `.length`.")
u.blank("Print every character of `word` on its own line.", """
word = "abc"
for i in range(___(word)):
    print(word[___])
""", [["len"], ["i"]], "`range(len(word))` gives the indexes 0, 1, 2.")
u.predict("""
s = "Hi"
s = s + "!"
print(s * 2)
""", "`+` joins strings, and `* 2` repeats the string twice.")
u.write("Read a word and print its first and last character separated by a space. For `logic` print `l c`.", """
w = input()
# print first and last character
""", """
w = input()
print(w[0], w[-1])
""", ["logic\n", "a\n", "python\n"], "First is `w[0]`, last is `w[-1]`.")

# 5 ---------------------------------------------------------------- input
u = unit(L, "Reading input", """
`input()` reads one line as a **string**. Convert it to use it as a number:

```python
n = int(input())                    # one number
a, b = map(int, input().split())    # two numbers on one line
```

In LogicQuest's problems the input is read for you, but you'll need this everywhere else.
""")
u.predict("""
a, b = map(int, input().split())
print(a * b)
""", "The two numbers 6 and 7 come from the input, so it prints 42.", stdin="6 7\n",
          prompt="The input is `6 7`. What does this print?")
u.choice("What type does `input()` return?", ["int", "str", "float", "It depends on what you type"], 1,
         "Always a string. `int(...)` converts it.")
u.blank("Read a name and greet it: input `Ana` → `Hello, Ana`.", """
name = ___()
print("Hello, " + name)
""", [["input"]], "`input()` reads the line the user typed.", stdin="Ana\n")
u.order("Arrange the lines to read two numbers (one per line) and print their sum.", """
x = int(input())
y = int(input())
total = x + y
print(total)
""", "Read both numbers before adding.", stdin="3\n4\n")
u.write("Read an integer `n` and print `n` squared.", """
# read n and print n * n
""", """
n = int(input())
print(n * n)
""", ["5\n", "0\n", "-3\n", "12\n"], "`int(input())`, then print `n * n`.")
u.fix("Read two numbers and print their sum. It prints `57` for input `5 7`. Fix it.", """
a, b = input().split()
print(a + b)
""", """
a, b = map(int, input().split())
print(a + b)
""", "`split()` gives strings, and `+` joins strings. Convert with `map(int, ...)`.", stdin="5 7\n")

# 6 ---------------------------------------------------------------- conditions
u = unit(L, "Conditions", """
```python
if n > 0:
    print("positive")
elif n < 0:
    print("negative")
else:
    print("zero")
```

The colon `:` and the **indentation** (4 spaces) mark the block. Combine conditions with `and`, `or`, `not`.
""")
u.predict("""
n = 15
if n % 3 == 0 and n % 5 == 0:
    print("both")
elif n % 3 == 0:
    print("three")
else:
    print("other")
""", "The first true branch wins. 15 is divisible by both.")
u.choice("Which condition is True when `age` is between 13 and 19, inclusive?",
         ["age > 13 or age < 19", "13 <= age <= 19", "age >= 13 && age <= 19", "13 < age < 19"], 1,
         "Python allows chained comparisons. `&&` is not Python syntax; use `and`.")
u.predict("""
a, b = 4, 9
bigger = "a" if a > b else "b"
print(bigger)
""", "`x if cond else y` picks `x` when the condition is true. 4 > 9 is false.")
u.blank("Print `even` or `odd`.", """
n = 8
if n % 2 ___ 0:
    print("even")
___:
    print("odd")
""", [["=="], ["else"]], "`==` compares. `else:` needs its colon too.")
u.fix("It should print `adult` for 18 and above. For 18 it prints `minor`.", """
age = 18
if age > 18:
    print("adult")
else:
    print("minor")
""", """
age = 18
if age >= 18:
    print("adult")
else:
    print("minor")
""", "\"18 and above\" includes 18, so the check is `>=`.")
u.write("Read a number and print `big` if it is greater than 100, otherwise `small`.", """
n = int(input())
# your if / else here
""", """
n = int(input())
if n > 100:
    print("big")
else:
    print("small")
""", ["150\n", "100\n", "7\n", "101\n"], "Exactly 100 is not greater than 100, so it's `small`.")

# 7 ---------------------------------------------------------------- loops
u = unit(L, "Loops", """
```python
for i in range(1, 6):     # 1, 2, 3, 4, 5  (stops BEFORE 6)
    print(i)

n = 10
while n > 0:
    n = n // 2
```

`range(5)` is 0..4, `range(a, b)` is a..b−1, `range(a, b, step)` jumps by step. `break` and `continue` work as usual.
""")
u.predict("""
for i in range(3):
    print(i, end=" ")
print()
""", "`range(3)` is 0, 1, 2.")
u.predict("""
total = 0
for i in range(1, 5):
    total += i
print(total)
""", "1 + 2 + 3 + 4 = 10. The 5 is not included.")
u.predict("""
n = 20
steps = 0
while n > 1:
    n = n // 2
    steps += 1
print(steps)
""", "20 → 10 → 5 → 2 → 1: four halvings.")
u.blank("Print 5, 4, 3, 2, 1 on separate lines.", """
for i in range(5, ___, ___):
    print(i)
""", [["0"], ["-1"]], "Count down with step −1. The stop value 0 is not included.")
u.order("Arrange the lines to print only the odd numbers from 1 to 5.", """
for i in range(1, 6):
    if i % 2 == 0:
        continue
    print(i)
""", "`continue` skips the print for even numbers.")
u.fix("It should print 1 to 5 but stops at 4. Fix the loop.", """
for i in range(1, 5):
    print(i)
""", """
for i in range(1, 6):
    print(i)
""", "`range` stops before its end value. To include 5, the end must be 6.")

# 8 ---------------------------------------------------------------- lists
u = unit(L, "Lists", """
A list holds values in order:

```python
nums = [4, 8, 15]
zeros = [0] * 5       # five zeros
nums[0]               # first
nums[-1]              # last
len(nums)             # 3
nums.append(16)       # add to the end
```
""")
u.predict("""
a = [3, 6, 9]
print(len(a))
print(a[1])
a[1] = 100
print(a[0] + a[1])
""", "Index 1 is the second element. After changing it, 3 + 100 = 103.")
u.predict("""
a = [0] * 4
a[2] = 7
for x in a:
    print(x, end=" ")
print()
""", "`[0] * 4` is four zeros; only index 2 changed.")
u.choice("For `a = [5, 6, 7]`, which expression raises IndexError?", ["a[-1]", "a[2]", "a[3]", "a[0]"], 2,
         "Valid indexes are 0, 1, 2 (and −1, −2, −3). 3 is outside.")
u.blank("Find the largest value without using `max()`.", """
a = [4, 11, 2, 9]
best = a[0]
for x in ___:
    if x ___ best:
        best = x
print(best)
""", [["a"], [">"]], "Walk the list and keep the biggest value seen so far.")
u.order("Arrange the lines to print the sum of the list without `sum()`.", """
a = [1, 2, 3, 4]
total = 0
for x in a:
    total += x
print(total)
""", "Create the list and the accumulator before the loop, print after it.")
u.write("Read `n`, then a line of `n` numbers. Print how many of them are negative.", """
n = int(input())
a = list(map(int, input().split()))
# count the negatives
""", """
n = int(input())
a = list(map(int, input().split()))
count = 0
for x in a:
    if x < 0:
        count += 1
print(count)
""", ["5\n1 -2 3 -4 -5\n", "1\n7\n", "3\n-1 -1 -1\n"], "Loop over the list and add 1 for each value below zero.")

# 9 ---------------------------------------------------------------- functions
u = unit(L, "Functions", """
```python
def square(x):
    return x * x

print(square(4))   # 16
```

A function without `return` gives back `None`. In LogicQuest problems you write `solve`.
""")
u.predict("""
def twice(x):
    return x * 2

a = twice(5)
print(a + twice(1))
""", "twice(5) is 10, twice(1) is 2, so 12.")
u.predict("""
def shout(word):
    print(word + "!")

result = shout("hey")
print(result)
""", "`shout` prints, but it doesn't return anything, so `result` is `None`.")
u.blank("Complete the function that returns the larger of two numbers.", """
___ max2(a, b):
    if a > b:
        ___ a
    return b

print(max2(3, 8))
""", [["def"], ["return"]], "`def` starts a function; `return` sends the value back.")
u.choice("What does a Python function return if it has no `return` statement?", ["0", "None", "False", "It's an error"], 1,
         "It returns `None`.")
u.fix("`is_even(4)` should print `True`, but it prints `None`. Fix it.", """
def is_even(n):
    if n % 2 == 0:
        print(True)

print(is_even(4))
""", """
def is_even(n):
    return n % 2 == 0

print(is_even(4))
""", "Printing inside a function isn't returning. Use `return`.")
u.write("Complete `cube` so it returns `n * n * n`. The program reads `n` and prints `cube(n)`.", """
def cube(n):
    return 0

print(cube(int(input())))
""", """
def cube(n):
    return n * n * n

print(cube(int(input())))
""", ["3\n", "0\n", "-2\n", "100\n"], "Replace `return 0` with the real calculation.")

# 10 --------------------------------------------------------------- errors
u = unit(L, "Reading errors", """
Python prints a **traceback**. Read the **last line** first: it names the error. The line above shows where.

- `NameError` → a name doesn't exist (typo, or used before defining)
- `TypeError` → wrong type for the operation (e.g. `"a" + 1`)
- `IndexError` → index outside the list or string
- `ZeroDivisionError`, `ValueError` (e.g. `int("abc")`)
- `IndentationError` → the spaces at the start of a line don't line up
""")
u.choice("`NameError: name 'totl' is not defined` most likely means…",
         ["Python is broken", "A typo or a variable used before it was created", "The list is empty", "You need an import"], 1,
         "Python doesn't know `totl`; usually a typo of `total`.")
u.choice("Which line raises `IndexError`?", ["a = [0] * 3", "a[2] = 1", "a[3] = 1", "a[-3] = 1"], 2,
         "A list of 3 has indexes 0, 1, 2 (and −1..−3). 3 is outside.", code="a = [0] * 3")
u.fix("Fix the typo so it prints `30`.", """
total = 10
total = totl + 20
print(total)
""", """
total = 10
total = total + 20
print(total)
""", "`NameError: name 'totl' is not defined`. Match the name you created.")
u.fix("This crashes with `ZeroDivisionError` when there are no items. Print `0` in that case instead.", """
total = 0
count = 0
print(total // count)
""", """
total = 0
count = 0
if count == 0:
    print(0)
else:
    print(total // count)
""", "Check `count == 0` before dividing.")
u.fix("`IndentationError: expected an indented block`. Fix it so it prints 1, 2, 3.", """
for i in range(1, 4):
print(i)
""", """
for i in range(1, 4):
    print(i)
""", "The body of a loop must be indented (4 spaces).")
u.choice("Your loop prints one value too few. What's the most likely cause?",
         ["`range(1, n)` where you needed `range(1, n + 1)`", "Missing colon", "Wrong variable type", "Python skipped a line"], 0,
         "`range` stops before its end value.")
