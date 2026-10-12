from bc import unit

L = "java"

# 1 ---------------------------------------------------------------- output
u = unit(L, "Hello, output", """
Every Java program starts in `main`. In Basecamp you only see the lines **inside** `main`;
LogicQuest wraps them in `public class Main { public static void main(String[] args) { ... } }` for you.

`System.out.println(x)` prints `x` and then moves to a new line. `System.out.print(x)` stays on the same line.
Every statement ends with a semicolon `;`.
""")
u.predict("""
System.out.println("Hello");
System.out.println("World");
""", "Each `println` ends its line, so the words land on two lines.")
u.predict("""
System.out.print("Log");
System.out.print("ic");
System.out.println("Quest");
""", "`print` doesn't add a newline, so the three pieces join into one word.")
u.choice("Which line prints `Hi` and moves to the next line?",
         ["System.out.print(\"Hi\");", "System.out.println(\"Hi\");", "print(\"Hi\");", "System.println(\"Hi\");"], 1,
         "`println` = print + line break. `print` keeps the cursor on the same line.")
u.blank("Make it print `5 apples` on one line.", """
System.out.___("5 ");
System.out.println("apples");
""", [["print"]], "`print` keeps `5 ` and `apples` on the same line.")
u.predict("""
System.out.println("2 + 3");
System.out.println(2 + 3);
""", "Inside quotes it's text and printed as-is. Without quotes Java does the maths first.")
u.fix("This should print `Ready` but doesn't compile. Fix it.", """
System.out.println("Ready")
""", """
System.out.println("Ready");
""", "Every Java statement ends with `;`. The compiler error says `';' expected`.")

# 2 ---------------------------------------------------------------- variables
u = unit(L, "Variables and types", """
A variable is a named box with a fixed **type**: `int` for whole numbers, `long` for big whole numbers,
`double` for decimals, `boolean` for `true`/`false`, `char` for one character in single quotes, and
`String` for text in double quotes.

```java
int age = 21;
double price = 9.5;
String name = "Yash";
```
""")
u.predict("""
int x = 10;
x = x + 5;
System.out.println(x);
""", "`x = x + 5` reads the old value (10), adds 5, and stores 15 back in `x`.")
u.choice("Which type should hold the value `3.75`?", ["int", "double", "boolean", "char"], 1,
         "Decimals need `double`. Putting 3.75 in an `int` won't even compile.")
u.predict("""
String first = "Logic";
String second = "Quest";
System.out.println(first + second);
System.out.println(first + " " + second);
""", "`+` joins Strings. Spaces only appear where you add them.")
u.blank("Declare a `boolean` called `done` set to true.", """
___ done = ___;
System.out.println(done);
""", [["boolean"], ["true"]], "`boolean` holds exactly `true` or `false`, written in lowercase.")
u.order("Arrange the lines so the program prints `20`.", """
int a = 4;
int b = 5;
int product = a * b;
System.out.println(product);
""", "A variable must be declared before it is used, so declarations come first.")
u.fix("Swap the values so it prints `2 1`.", """
int a = 1;
int b = 2;
a = b;
b = a;
System.out.println(a + " " + b);
""", """
int a = 1;
int b = 2;
int temp = a;
a = b;
b = temp;
System.out.println(a + " " + b);
""", "After `a = b`, the old value of `a` is gone. Keep it in a `temp` variable first.")

# 3 ---------------------------------------------------------------- operators
u = unit(L, "Operators", """
`+ - * /` work as you'd expect, with one catch: **int / int gives an int**. `7 / 2` is `3`, the decimal part is dropped.
`%` gives the remainder: `7 % 2` is `1`.

`x += 3` is short for `x = x + 3`, and `x++` adds 1.
""")
u.predict("""
System.out.println(7 / 2);
System.out.println(7 % 2);
System.out.println(7.0 / 2);
""", "Two ints → integer division (3). One double makes the result a double (3.5).")
u.predict("""
int x = 5;
x += 3;
x *= 2;
x--;
System.out.println(x);
""", "5 → 8 → 16 → 15.")
u.choice("What is `2 + 3 * 4` in Java?", ["20", "14", "24", "9"], 1,
         "`*` happens before `+`, just like in maths: 3 × 4 = 12, then 2 + 12.")
u.predict("""
System.out.println(-7 % 2);
System.out.println(-7 / 2);
""", "Java keeps the sign of the left number for `%` and drops the decimals for `/`, so you get -1 and -3.")
u.blank("Print the last digit of `n`.", """
int n = 1234;
System.out.println(n ___ 10);
""", [["%"]], "The remainder after dividing by 10 is always the last digit.")
u.fix("This should print the average `2.5`, but prints `2.0`. Fix the calculation.", """
int a = 2, b = 3;
double avg = (a + b) / 2;
System.out.println(avg);
""", """
int a = 2, b = 3;
double avg = (a + b) / 2.0;
System.out.println(avg);
""", "`(a + b) / 2` is int / int = 2 before it is stored. Dividing by `2.0` makes it a decimal division.")

# 4 ---------------------------------------------------------------- strings
u = unit(L, "Strings and chars", """
A `String` is text; a `char` is one character in single quotes, like `'a'`.

- `s.length()` → number of characters
- `s.charAt(i)` → the character at index `i` (starting from 0)
- Compare text with `a.equals(b)`, never `==`.
- A `char` is a number underneath: `'b' - 'a'` is `1`.
""")
u.predict("""
String s = "quest";
System.out.println(s.length());
System.out.println(s.charAt(0));
System.out.println(s.charAt(s.length() - 1));
""", "Indexes run from 0 to length − 1, so the last character is at `length() - 1`.")
u.predict("""
char c = 'a';
System.out.println(c + 1);
System.out.println((char) (c + 1));
""", "`'a' + 1` is the number 98. Casting back to `char` turns it into `'b'`.")
u.choice("How do you check if String `a` has the same text as String `b`?", ["a == b", "a.equals(b)", "a = b", "a.same(b)"], 1,
         "`==` checks if they are the same object in memory. `.equals` compares the characters.")
u.blank("Print every character of `word` on its own line.", """
String word = "abc";
for (int i = 0; i < word.___(); i++) {
    System.out.println(word.___(i));
}
""", [["length"], ["charAt"]], "`length()` gives the count; `charAt(i)` reads one character.")
u.predict("""
String s = "Hi";
s = s + '!';
System.out.println(s + s.length());
""", "Adding a char to a String appends it. Then `+ 3` turns the length into text too.")
u.write("Print the first and last character of the word you read, separated by a space. For `logic` print `l c`.", """
Scanner sc = new Scanner(System.in);
String w = sc.next();
// print first and last character
""", """
Scanner sc = new Scanner(System.in);
String w = sc.next();
System.out.println(w.charAt(0) + " " + w.charAt(w.length() - 1));
""", ["logic\n", "a\n", "java\n"], "First is `charAt(0)`, last is `charAt(w.length() - 1)`.")

# 5 ---------------------------------------------------------------- input
u = unit(L, "Reading input", """
`Scanner` reads what the user types (stdin):

```java
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();      // next whole number
String w = sc.next();      // next word
String line = sc.nextLine(); // rest of the line
```

In LogicQuest's problems the input is read for you, but you'll need this everywhere else.
""")
u.predict("""
Scanner sc = new Scanner(System.in);
int a = sc.nextInt();
int b = sc.nextInt();
System.out.println(a * b);
""", "The two numbers 6 and 7 come from the input, so it prints 42.", stdin="6 7\n",
          prompt="The input is `6 7`. What does this print?")
u.choice("Which Scanner method reads the next whole number?", ["sc.next()", "sc.nextInt()", "sc.readInt()", "sc.nextLine()"], 1,
         "`nextInt()` reads an int. `next()` reads a word as a String.")
u.blank("Read a name and greet it: input `Ana` → `Hello, Ana`.", """
Scanner sc = new ___(System.in);
String name = sc.___();
System.out.println("Hello, " + name);
""", [["Scanner"], ["next", "nextLine"]], "Create a `Scanner` on `System.in`, then `next()` reads one word.", stdin="Ana\n")
u.order("Arrange the lines to read two numbers and print their sum.", """
Scanner sc = new Scanner(System.in);
int x = sc.nextInt();
int y = sc.nextInt();
System.out.println(x + y);
""", "Create the Scanner before reading, and read before printing.", stdin="3 4\n")
u.write("Read an integer `n` and print `n` squared.", """
Scanner sc = new Scanner(System.in);
// read n and print n * n
""", """
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
System.out.println(n * n);
""", ["5\n", "0\n", "-3\n", "12\n"], "`sc.nextInt()` then print `n * n`.")
u.fix("Read two numbers and print their sum. It prints `57` for input `5 7`. Fix it.", """
Scanner sc = new Scanner(System.in);
String a = sc.next();
String b = sc.next();
System.out.println(a + b);
""", """
Scanner sc = new Scanner(System.in);
int a = sc.nextInt();
int b = sc.nextInt();
System.out.println(a + b);
""", "`+` on Strings joins them. Read numbers with `nextInt()` so `+` adds.", stdin="5 7\n")

# 6 ---------------------------------------------------------------- conditions
u = unit(L, "Conditions", """
```java
if (n > 0) {
    System.out.println("positive");
} else if (n < 0) {
    System.out.println("negative");
} else {
    System.out.println("zero");
}
```

Compare with `== != < > <= >=`. Combine with `&&` (and), `||` (or), `!` (not).
""")
u.predict("""
int n = 15;
if (n % 3 == 0 && n % 5 == 0) {
    System.out.println("both");
} else if (n % 3 == 0) {
    System.out.println("three");
} else {
    System.out.println("other");
}
""", "The first true branch wins. 15 is divisible by both, so `both` prints and the rest is skipped.")
u.choice("Which condition is true when `age` is between 13 and 19, inclusive?",
         ["age > 13 || age < 19", "age >= 13 && age <= 19", "13 <= age <= 19", "age >= 13 & age"], 1,
         "Both limits must hold, so use `&&`. Java doesn't allow the chained `13 <= age <= 19`.")
u.predict("""
int a = 4, b = 9;
String bigger = (a > b) ? "a" : "b";
System.out.println(bigger);
""", "`cond ? x : y` picks `x` when true, `y` when false. 4 > 9 is false.")
u.blank("Print `even` or `odd`.", """
int n = 8;
if (n % 2 ___ 0) {
    System.out.println("even");
} ___ {
    System.out.println("odd");
}
""", [["=="], ["else"]], "`==` compares; `=` would assign and not compile here.")
u.fix("It should print `adult` for 18 and above. For 18 it prints `minor`.", """
int age = 18;
if (age > 18) {
    System.out.println("adult");
} else {
    System.out.println("minor");
}
""", """
int age = 18;
if (age >= 18) {
    System.out.println("adult");
} else {
    System.out.println("minor");
}
""", "\"18 and above\" includes 18, so the check is `>=`.")
u.write("Read a number and print `big` if it is greater than 100, otherwise `small`.", """
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
// your if / else here
""", """
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
if (n > 100) {
    System.out.println("big");
} else {
    System.out.println("small");
}
""", ["150\n", "100\n", "7\n", "101\n"], "Exactly 100 is not greater than 100, so it's `small`.")

# 7 ---------------------------------------------------------------- loops
u = unit(L, "Loops", """
```java
for (int i = 1; i <= 5; i++) {   // start; keep going while; step
    System.out.println(i);
}

int n = 10;
while (n > 0) {
    n = n / 2;
}
```

`break` leaves the loop. `continue` jumps to the next round.
""")
u.predict("""
for (int i = 0; i < 3; i++) {
    System.out.print(i + " ");
}
System.out.println();
""", "Starts at 0 and stops before 3: 0, 1, 2.")
u.predict("""
int sum = 0;
for (int i = 1; i <= 4; i++) {
    sum += i;
}
System.out.println(sum);
""", "1 + 2 + 3 + 4 = 10.")
u.predict("""
int n = 20;
int steps = 0;
while (n > 1) {
    n = n / 2;
    steps++;
}
System.out.println(steps);
""", "20 → 10 → 5 → 2 → 1: four halvings.")
u.blank("Print the numbers 5, 4, 3, 2, 1 on separate lines.", """
for (int i = 5; i ___ 1; i___) {
    System.out.println(i);
}
""", [[">="], ["--"]], "Count down: keep going while `i >= 1`, and decrease with `i--`.")
u.order("Arrange the lines to print only the odd numbers from 1 to 5.", """
for (int i = 1; i <= 5; i++) {
    if (i % 2 == 0) {
        continue;
    }
    System.out.println(i);
}
""", "`continue` skips the print for even numbers.")
u.fix("It should print 1 to 5 but stops at 4. Fix the loop.", """
for (int i = 1; i < 5; i++) {
    System.out.println(i);
}
""", """
for (int i = 1; i <= 5; i++) {
    System.out.println(i);
}
""", "`i < 5` stops before 5. Use `<=` to include it. This off-by-one is the most common loop bug.")

# 8 ---------------------------------------------------------------- arrays
u = unit(L, "Arrays", """
An array holds a fixed number of values of one type:

```java
int[] nums = {4, 8, 15};
int[] zeros = new int[5];   // five zeros
nums[0]          // first element
nums.length      // 3, no brackets
```
""")
u.predict("""
int[] a = {3, 6, 9};
System.out.println(a.length);
System.out.println(a[1]);
a[1] = 100;
System.out.println(a[0] + a[1]);
""", "Index 1 is the second element. After changing it to 100, 3 + 100 = 103.")
u.predict("""
int[] a = new int[4];
a[2] = 7;
for (int x : a) {
    System.out.print(x + " ");
}
System.out.println();
""", "`new int[4]` starts as four zeros; only index 2 changed.")
u.choice("For `int[] a = {5, 6, 7};`, which is the last element?", ["a[3]", "a[a.length]", "a[a.length - 1]", "a.last()"], 2,
         "Indexes go 0..length − 1. `a[3]` throws ArrayIndexOutOfBoundsException.")
u.blank("Find the largest value.", """
int[] a = {4, 11, 2, 9};
int best = a[0];
for (int i = 1; i < a.___; i++) {
    if (a[i] ___ best) {
        best = a[i];
    }
}
System.out.println(best);
""", [["length"], [">"]], "Walk the array and keep the biggest value seen so far.")
u.order("Arrange the lines to print the sum of the array.", """
int[] a = {1, 2, 3, 4};
int sum = 0;
for (int x : a) {
    sum += x;
}
System.out.println(sum);
""", "Create the array and the accumulator before the loop, print after it.")
u.write("Read `n`, then `n` numbers. Print how many of them are negative.", """
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
int[] a = new int[n];
// fill the array, then count the negatives
""", """
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();
int[] a = new int[n];
for (int i = 0; i < n; i++) a[i] = sc.nextInt();
int count = 0;
for (int x : a) if (x < 0) count++;
System.out.println(count);
""", ["5\n1 -2 3 -4 -5\n", "1\n7\n", "3\n-1 -1 -1\n"], "Read with a loop into `a[i]`, then count with a second loop.")

# 9 ---------------------------------------------------------------- functions
u = unit(L, "Methods (functions)", """
A method packs logic under a name. In LogicQuest problems you write `solve`:

```java
static int square(int x) {   // return type, name, parameters
    return x * x;
}
```

`static` lets `main` call it directly. `void` means it returns nothing.
""")
u.predict("""
public class Main {
    static int twice(int x) {
        return x * 2;
    }

    public static void main(String[] args) {
        int a = twice(5);
        System.out.println(a + twice(1));
    }
}
""", "twice(5) is 10, twice(1) is 2, so 12.", full=True)
u.choice("A method that only prints and gives nothing back has which return type?", ["int", "void", "null", "String"], 1,
         "`void` means no return value.")
u.blank("Complete the method that returns the larger of two ints.", """
public class Main {
    static ___ max2(int a, int b) {
        if (a > b) {
            ___ a;
        }
        return b;
    }

    public static void main(String[] args) {
        System.out.println(max2(3, 8));
    }
}
""", [["int"], ["return"]], "The method gives back an int, and `return` sends the value out.", full=True)
u.predict("""
public class Main {
    static void greet(String name) {
        System.out.println("Hi " + name);
    }

    public static void main(String[] args) {
        greet("Ana");
        greet("Ravi");
    }
}
""", "Each call runs the method body once with a different `name`.", full=True)
u.fix("`isEven(4)` should return true, but this doesn't compile. Fix the method.", """
public class Main {
    static boolean isEven(int n) {
        if (n % 2 == 0) {
            return true;
        }
    }

    public static void main(String[] args) {
        System.out.println(isEven(4));
    }
}
""", """
public class Main {
    static boolean isEven(int n) {
        if (n % 2 == 0) {
            return true;
        }
        return false;
    }

    public static void main(String[] args) {
        System.out.println(isEven(4));
    }
}
""", "Every path must return something. Java reports `missing return statement`.", full=True)
u.write("Complete `cube` so it returns `n * n * n`. The program reads `n` and prints `cube(n)`.", """
import java.util.*;

public class Main {
    static long cube(long n) {
        return 0;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println(cube(sc.nextLong()));
    }
}
""", """
import java.util.*;

public class Main {
    static long cube(long n) {
        return n * n * n;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println(cube(sc.nextLong()));
    }
}
""", ["3\n", "0\n", "-2\n", "100\n"], "Replace `return 0;` with the real calculation.", full=True)

# 10 --------------------------------------------------------------- errors
u = unit(L, "Reading errors", """
Errors are messages, not failures. Read the **first line** and the **line number**.

- **Compile errors** (before running): `';' expected`, `cannot find symbol` (typo or undeclared variable),
  `incompatible types` (wrong type).
- **Runtime exceptions** (while running): `ArrayIndexOutOfBoundsException`, `ArithmeticException: / by zero`,
  `NullPointerException`.
""")
u.choice("`error: cannot find symbol  symbol: variable totl` most likely means…",
         ["Java is broken", "You misspelled a variable name or didn't declare it", "The file is too long", "You need more memory"], 1,
         "Java doesn't know `totl`. Usually a typo of `total`.")
u.choice("Which line throws `ArrayIndexOutOfBoundsException`?", ["int[] a = new int[3];", "a[2] = 1;", "a[3] = 1;", "int x = a.length;"], 2,
         "An array of 3 has indexes 0, 1, 2. Index 3 is outside.", code="int[] a = new int[3];")
u.fix("Fix the typo so it prints `30`.", """
int total = 10;
total = totl + 20;
System.out.println(total);
""", """
int total = 10;
total = total + 20;
System.out.println(total);
""", "`cannot find symbol: totl`. Match the name you declared.")
u.fix("This crashes with `/ by zero` when there are no items. Print `0` in that case instead.", """
int sum = 0;
int count = 0;
System.out.println(sum / count);
""", """
int sum = 0;
int count = 0;
if (count == 0) {
    System.out.println(0);
} else {
    System.out.println(sum / count);
}
""", "Guard the division: check `count == 0` before dividing.")
u.fix("`incompatible types: String cannot be converted to int`. Fix it so it prints `8`.", """
String s = "5";
int n = s;
System.out.println(n + 3);
""", """
String s = "5";
int n = Integer.parseInt(s);
System.out.println(n + 3);
""", "Text isn't a number until you convert it: `Integer.parseInt(s)`.")
u.choice("Your loop prints one value too few. What's the most likely cause?",
         ["Using `<` where you needed `<=`", "Missing semicolon", "Wrong variable type", "Java skipped a line"], 0,
         "Off-by-one: check where the loop starts and whether the end should be included.")
