from bc import unit

L = "javascript"

READ = 'const lines = require("fs").readFileSync(0, "utf8").split("\\n");'

# 1 ---------------------------------------------------------------- output
u = unit(L, "Hello, output", """
`console.log(x)` prints `x` and then moves to a new line. A JavaScript file runs from top to bottom.

`console.log(a, b)` puts a space between values. There is no "print without newline" in `console.log`;
build the whole line as a string first, then log it once.
""")
u.predict("""
console.log("Hello");
console.log("World");
""", "Each `console.log` ends its line, so the words land on two lines.")
u.predict("""
let line = "Lo";
line += "g";
line += "IQ";
console.log(line);
""", "Build the string first, then log it once.")
u.choice("What does `console.log(\"a\", \"b\", \"c\")` show?", ["abc", "a b c", "a,b,c", "[ 'a', 'b', 'c' ]"], 1,
         "Separate arguments are printed with one space between them.")
u.blank("Print `1-2-3` using one console.log.", """
console.log([1, 2, 3].___("-"));
""", [["join"]], "`join(sep)` turns an array into one string with `sep` between items.")
u.predict("""
console.log("2 + 3");
console.log(2 + 3);
console.log("2" + 3);
""", "In quotes it's text. Numbers add. But a string `+` a number **joins** them: \"23\".")
u.fix("This should print `Ready` but crashes. Fix it.", """
Console.log("Ready");
""", """
console.log("Ready");
""", "JavaScript is case-sensitive. The error says `ReferenceError: Console is not defined`.")

# 2 ---------------------------------------------------------------- variables
u = unit(L, "Variables and types", """
Declare with `let` (can change) or `const` (can't be reassigned). Never use the old `var`.

```js
let age = 21;          // number
const price = 9.5;     // number too: JS has one number type
const name = "Yash";   // string
let done = true;       // boolean
```

`typeof x` tells you the type.
""")
u.predict("""
let x = 10;
x = x + 5;
console.log(x);
""", "`x = x + 5` reads 10, adds 5, and stores 15 back in `x`.")
u.choice("What happens with `const n = 1; n = 2;`?", ["n becomes 2", "TypeError: Assignment to constant variable", "n stays 1 silently", "n becomes undefined"], 1,
         "`const` can't be reassigned. Use `let` for values that change.")
u.predict("""
const first = "Log";
const second = "IQ";
console.log(first + second);
console.log(`${first} ${second}`);
""", "Template strings in backticks put values inside `${...}`.")
u.blank("Swap `a` and `b` in one line.", """
let a = 1;
let b = 2;
[a, b] = [___, ___];
console.log(a, b);
""", [["b"], ["a"]], "Array destructuring: the right side is built first, then unpacked into a and b.")
u.order("Arrange the lines so the program prints `20`.", """
const a = 4;
const b = 5;
const product = a * b;
console.log(product);
""", "A `const` must be declared before it's used.")
u.fix("Print `Age: 21` and then update the age to 22 and print `Age: 22`. It crashes. Fix it.", """
const age = 21;
console.log("Age: " + age);
age = 22;
console.log("Age: " + age);
""", """
let age = 21;
console.log("Age: " + age);
age = 22;
console.log("Age: " + age);
""", "A value that changes must be declared with `let`.")

# 3 ---------------------------------------------------------------- operators
u = unit(L, "Operators", """
`/` always gives a decimal: `7 / 2` is `3.5`. For whole-number division use `Math.trunc(7 / 2)` (or `Math.floor` for non-negative numbers).
`%` is the remainder, `**` is power.

`x += 3` is short for `x = x + 3`, `x++` adds 1. Compare with `===` and `!==`; avoid `==`.
""")
u.predict("""
console.log(7 / 2);
console.log(Math.trunc(7 / 2));
console.log(7 % 2);
console.log(2 ** 5);
""", "`/` → 3.5, truncated → 3, `%` → 1, `**` → 32.")
u.predict("""
let x = 5;
x += 3;
x *= 2;
x--;
console.log(x);
""", "5 → 8 → 16 → 15.")
u.choice("What is `\"5\" == 5` versus `\"5\" === 5`?", ["true, true", "true, false", "false, false", "false, true"], 1,
         "`==` converts types before comparing; `===` doesn't. Always use `===`.")
u.predict("""
console.log(-7 % 2);
console.log(Math.trunc(-7 / 2));
console.log(Math.floor(-7 / 2));
""", "`%` keeps the sign of the left number (-1). `trunc` cuts toward zero (-3); `floor` rounds down (-4).")
u.blank("Print the last digit of `n`, then `n` without its last digit.", """
const n = 1234;
console.log(n ___ 10);
console.log(Math.___(n / 10));
""", [["%"], ["floor", "trunc"]], "`% 10` is the last digit. `n / 10` is 123.4, so drop the decimals.")
u.fix("This should print `5`, the number of full boxes of 4 you can fill from 22 eggs, but prints `5.5`.", """
const eggs = 22;
console.log(eggs / 4);
""", """
const eggs = 22;
console.log(Math.floor(eggs / 4));
""", "Full boxes is whole-number division: `Math.floor(eggs / 4)`.")

# 4 ---------------------------------------------------------------- strings
u = unit(L, "Strings and characters", """
A string is text. A single character is a string of length 1.

- `s.length` → number of characters (a property, no brackets)
- `s[i]` → character at index `i` (from 0); `s[s.length - 1]` is the last
- `s.charCodeAt(i)` → code number, `String.fromCharCode(98)` → `"b"`
- Compare text with `===`.
""")
u.predict("""
const s = "quest";
console.log(s.length);
console.log(s[0]);
console.log(s[s.length - 1]);
""", "Indexes run from 0 to length − 1.")
u.predict("""
const c = "a";
console.log(c.charCodeAt(0) + 1);
console.log(String.fromCharCode(c.charCodeAt(0) + 1));
""", "`charCodeAt` gives 97; adding 1 and converting back gives \"b\".")
u.choice("What is `\"abc\"[3]`?", ["\"c\"", "an error", "undefined", "\"\""], 2,
         "Reading past the end doesn't throw in JavaScript; it gives `undefined`. That's why off-by-one bugs hide.")
u.blank("Print every character of `word` on its own line.", """
const word = "abc";
for (let i = 0; i < word.___; i++) {
  console.log(word[___]);
}
""", [["length"], ["i"]], "`length` is a property; `word[i]` reads one character.")
u.predict("""
let s = "Hi";
s = s + "!";
console.log(s.repeat(2));
""", "`+` joins strings, and `repeat(2)` repeats the string twice.")
u.write("Read a word and print its first and last character separated by a space. For `logic` print `l c`.", READ + """
const w = lines[0].trim();
// print first and last character
""", READ + """
const w = lines[0].trim();
console.log(w[0] + " " + w[w.length - 1]);
""", ["logic\n", "a\n", "script\n"], "First is `w[0]`, last is `w[w.length - 1]`.")

# 5 ---------------------------------------------------------------- input
u = unit(L, "Reading input", """
Node reads everything the user typed (stdin) at once. Split it into lines, then convert:

```js
const lines = require("fs").readFileSync(0, "utf8").split("\\n");
const n = Number(lines[0]);                       // one number
const [a, b] = lines[1].split(" ").map(Number);   // two numbers on one line
```

In LogIQ's problems the input is read for you, but you'll need this everywhere else.
""")
u.predict(READ + """
const [a, b] = lines[0].split(" ").map(Number);
console.log(a * b);
""", "The two numbers 6 and 7 come from the input, so it prints 42.", stdin="6 7\n",
          prompt="The input is `6 7`. What does this print?")
u.choice("What type is `lines[0]` after reading stdin?", ["number", "string", "array", "It depends on what was typed"], 1,
         "Always a string. `Number(...)` converts it.")
u.blank("Read a name and greet it: input `Ana` → `Hello, Ana`.", READ + """
const name = lines[___].trim();
console.log("Hello, " + name);
""", [["0"]], "The first line is `lines[0]`. `trim()` removes the trailing newline or spaces.", stdin="Ana\n")
u.order("Arrange the lines to read two numbers (one per line) and print their sum.", READ + """
const x = Number(lines[0]);
const y = Number(lines[1]);
const total = x + y;
console.log(total);
""", "Read the input before using it.", stdin="3\n4\n")
u.write("Read an integer `n` and print `n` squared.", READ + """
// read n and print n * n
""", READ + """
const n = Number(lines[0]);
console.log(n * n);
""", ["5\n", "0\n", "-3\n", "12\n"], "`Number(lines[0])`, then print `n * n`.")
u.fix("Read two numbers and print their sum. It prints `57` for input `5 7`. Fix it.", READ + """
const [a, b] = lines[0].split(" ");
console.log(a + b);
""", READ + """
const [a, b] = lines[0].split(" ").map(Number);
console.log(a + b);
""", "`split` gives strings, and `+` joins strings. Convert with `.map(Number)`.", stdin="5 7\n")

# 6 ---------------------------------------------------------------- conditions
u = unit(L, "Conditions", """
```js
if (n > 0) {
  console.log("positive");
} else if (n < 0) {
  console.log("negative");
} else {
  console.log("zero");
}
```

Compare with `=== !== < > <= >=`. Combine with `&&` (and), `||` (or), `!` (not).
""")
u.predict("""
const n = 15;
if (n % 3 === 0 && n % 5 === 0) {
  console.log("both");
} else if (n % 3 === 0) {
  console.log("three");
} else {
  console.log("other");
}
""", "The first true branch wins. 15 is divisible by both.")
u.choice("Which condition is true when `age` is between 13 and 19, inclusive?",
         ["age > 13 || age < 19", "age >= 13 && age <= 19", "13 <= age <= 19", "age >= 13 and age <= 19"], 1,
         "`13 <= age <= 19` runs but is wrong in JS: it compares `true`/`false` with 19. Use `&&`.")
u.predict("""
const a = 4, b = 9;
const bigger = a > b ? "a" : "b";
console.log(bigger);
""", "`cond ? x : y` picks `x` when true. 4 > 9 is false.")
u.blank("Print `even` or `odd`.", """
const n = 8;
if (n % 2 ___ 0) {
  console.log("even");
} ___ {
  console.log("odd");
}
""", [["===", "=="], ["else"]], "Compare with `===`.")
u.fix("It should print `adult` for 18 and above. For 18 it prints `minor`.", """
const age = 18;
if (age > 18) {
  console.log("adult");
} else {
  console.log("minor");
}
""", """
const age = 18;
if (age >= 18) {
  console.log("adult");
} else {
  console.log("minor");
}
""", "\"18 and above\" includes 18, so the check is `>=`.")
u.write("Read a number and print `big` if it is greater than 100, otherwise `small`.", READ + """
const n = Number(lines[0]);
// your if / else here
""", READ + """
const n = Number(lines[0]);
if (n > 100) {
  console.log("big");
} else {
  console.log("small");
}
""", ["150\n", "100\n", "7\n", "101\n"], "Exactly 100 is not greater than 100, so it's `small`.")

# 7 ---------------------------------------------------------------- loops
u = unit(L, "Loops", """
```js
for (let i = 1; i <= 5; i++) {   // start; keep going while; step
  console.log(i);
}

let n = 10;
while (n > 0) {
  n = Math.floor(n / 2);
}

for (const x of [4, 8, 15]) { ... }   // each value of an array
```

`break` leaves the loop, `continue` jumps to the next round.
""")
u.predict("""
let out = "";
for (let i = 0; i < 3; i++) {
  out += i + " ";
}
console.log(out.trim());
""", "Starts at 0 and stops before 3: 0, 1, 2.")
u.predict("""
let sum = 0;
for (let i = 1; i <= 4; i++) {
  sum += i;
}
console.log(sum);
""", "1 + 2 + 3 + 4 = 10.")
u.predict("""
let n = 20;
let steps = 0;
while (n > 1) {
  n = Math.floor(n / 2);
  steps++;
}
console.log(steps);
""", "20 → 10 → 5 → 2 → 1: four halvings. Without `Math.floor`, n would never become a whole number.")
u.blank("Print 5, 4, 3, 2, 1 on separate lines.", """
for (let i = 5; i ___ 1; i___) {
  console.log(i);
}
""", [[">="], ["--"]], "Count down while `i >= 1`, decreasing with `i--`.")
u.order("Arrange the lines to print only the odd numbers from 1 to 5.", """
for (let i = 1; i <= 5; i++) {
  if (i % 2 === 0) {
    continue;
  }
  console.log(i);
}
""", "`continue` skips the log for even numbers.")
u.fix("It should print 1 to 5 but stops at 4. Fix the loop.", """
for (let i = 1; i < 5; i++) {
  console.log(i);
}
""", """
for (let i = 1; i <= 5; i++) {
  console.log(i);
}
""", "`i < 5` stops before 5. Use `<=` to include it.")

# 8 ---------------------------------------------------------------- arrays
u = unit(L, "Arrays", """
```js
const nums = [4, 8, 15];
const zeros = new Array(5).fill(0);   // five zeros
nums[0];          // first
nums.length;      // 3
nums.push(16);    // add to the end
```

`const` stops you from reassigning `nums`, but you can still change what's inside.
""")
u.predict("""
const a = [3, 6, 9];
console.log(a.length);
console.log(a[1]);
a[1] = 100;
console.log(a[0] + a[1]);
""", "Index 1 is the second element. After changing it, 3 + 100 = 103.")
u.predict("""
const a = new Array(4).fill(0);
a[2] = 7;
console.log(a.join(" "));
""", "`new Array(4).fill(0)` is four zeros; only index 2 changed.")
u.choice("For `const a = [5, 6, 7];`, what is `a[3] + 1`?", ["8", "an error", "NaN", "undefined"], 2,
         "`a[3]` is `undefined`, and `undefined + 1` is `NaN`. JavaScript doesn't stop you, so check your indexes.")
u.blank("Find the largest value without `Math.max`.", """
const a = [4, 11, 2, 9];
let best = a[0];
for (let i = 1; i < a.___; i++) {
  if (a[i] ___ best) {
    best = a[i];
  }
}
console.log(best);
""", [["length"], [">"]], "Walk the array and keep the biggest value seen so far.")
u.order("Arrange the lines to print the sum of the array without `reduce`.", """
const a = [1, 2, 3, 4];
let sum = 0;
for (const x of a) {
  sum += x;
}
console.log(sum);
""", "Create the array and the accumulator before the loop, log after it.")
u.write("Read `n`, then a line of `n` numbers. Print how many of them are negative.", READ + """
const n = Number(lines[0]);
const a = lines[1].trim().split(" ").map(Number);
// count the negatives
""", READ + """
const n = Number(lines[0]);
const a = lines[1].trim().split(" ").map(Number);
let count = 0;
for (const x of a) {
  if (x < 0) count++;
}
console.log(count);
""", ["5\n1 -2 3 -4 -5\n", "1\n7\n", "3\n-1 -1 -1\n"], "Loop over the array and count values below zero.")

# 9 ---------------------------------------------------------------- functions
u = unit(L, "Functions", """
```js
function square(x) {
  return x * x;
}

console.log(square(4));   // 16
```

A function without `return` gives back `undefined`. In LogIQ problems you write `solve`.
""")
u.predict("""
function twice(x) {
  return x * 2;
}

const a = twice(5);
console.log(a + twice(1));
""", "twice(5) is 10, twice(1) is 2, so 12.")
u.predict("""
function shout(word) {
  console.log(word + "!");
}

const result = shout("hey");
console.log(result);
""", "`shout` logs, but returns nothing, so `result` is `undefined`.")
u.blank("Complete the function that returns the larger of two numbers.", """
___ max2(a, b) {
  if (a > b) {
    ___ a;
  }
  return b;
}

console.log(max2(3, 8));
""", [["function"], ["return"]], "`function` declares it; `return` sends the value back.")
u.choice("What does a JavaScript function return if it has no `return`?", ["0", "null", "undefined", "It's an error"], 2,
         "It returns `undefined`.")
u.fix("`isEven(4)` should print `true`, but it prints `undefined`. Fix it.", """
function isEven(n) {
  if (n % 2 === 0) {
    console.log(true);
  }
}

console.log(isEven(4));
""", """
function isEven(n) {
  return n % 2 === 0;
}

console.log(isEven(4));
""", "Logging inside a function isn't returning. Use `return`.")
u.write("Complete `cube` so it returns `n * n * n`. The program reads `n` and prints `cube(n)`.", READ + """
function cube(n) {
  return 0;
}

console.log(cube(Number(lines[0])));
""", READ + """
function cube(n) {
  return n * n * n;
}

console.log(cube(Number(lines[0])));
""", ["3\n", "0\n", "-2\n", "100\n"], "Replace `return 0` with the real calculation.")

# 10 --------------------------------------------------------------- errors
u = unit(L, "Reading errors", """
Node prints the error type and a stack trace. Read the **first line** and the `main.js:LINE` location.

- `ReferenceError: x is not defined` → typo, or used before declaring
- `TypeError: ... is not a function` / `Cannot read properties of undefined` → wrong value, often from a bad index
- `SyntaxError` → missing bracket, quote or comma
- Silent bugs: `undefined` and `NaN` in your output usually mean an index or conversion went wrong.
""")
u.choice("`ReferenceError: totl is not defined` most likely means…",
         ["Node is broken", "A typo or a variable used before it was declared", "The array is empty", "You need to import something"], 1,
         "JavaScript doesn't know `totl`; usually a typo of `total`.")
u.choice("Your output shows `NaN`. What's a likely cause?",
         ["Adding a number to `undefined` (e.g. reading past the end of an array)", "A missing semicolon", "Using `let`", "The number is too small"], 0,
         "`undefined + 1` is `NaN`. Check indexes and `Number(...)` conversions.")
u.fix("Fix the typo so it prints `30`.", """
let total = 10;
total = totl + 20;
console.log(total);
""", """
let total = 10;
total = total + 20;
console.log(total);
""", "`ReferenceError: totl is not defined`. Match the name you declared.")
u.fix("The average prints `NaN` when there are no items. Print `0` in that case instead.", """
const sum = 0;
const count = 0;
console.log(sum / count);
""", """
const sum = 0;
const count = 0;
if (count === 0) {
  console.log(0);
} else {
  console.log(sum / count);
}
""", "0 / 0 is `NaN` in JavaScript (no crash!). Check `count === 0` first.")
u.fix("`TypeError: Cannot read properties of undefined`. It should print each word's first letter: `L Q`.", """
const words = ["Loop", "Queue"];
let out = "";
for (let i = 0; i <= words.length; i++) {
  out += words[i][0] + " ";
}
console.log(out.trim());
""", """
const words = ["Loop", "Queue"];
let out = "";
for (let i = 0; i < words.length; i++) {
  out += words[i][0] + " ";
}
console.log(out.trim());
""", "`i <= words.length` reaches index 2, which is `undefined`. Use `<`.")
u.choice("Your loop prints one value too few. What's the most likely cause?",
         ["Using `<` where you needed `<=`", "Missing semicolon", "Using const", "JavaScript skipped a line"], 0,
         "Off-by-one: check where the loop starts and whether the end should be included.")
