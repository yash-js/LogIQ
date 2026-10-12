from bc import oop_unit

L = "java"

# 1 ---------------------------------------------------------------- classes and objects
u = oop_unit(L, "Classes and objects", """
A class is a blueprint. An object is one built thing, with its own fields and methods.

```java
class Dog {
    String name;
    void bark() {
        System.out.println(name + " says woof");
    }
}
```

`new Dog()` builds an object. A second `new Dog()` is a different object: writing one `name` leaves the other alone.
""")
u.predict("""
class Counter {
    int n = 0;
    void add() { n++; }
}

public class Main {
    public static void main(String[] args) {
        Counter a = new Counter();
        Counter b = new Counter();
        a.add();
        a.add();
        b.add();
        System.out.println(a.n);
        System.out.println(b.n);
    }
}
""", "Each `new Counter()` has its own `n`. `a` is incremented twice, `b` once.", full=True)
u.choice("What does `new Dog()` do?",
         ["It renames the Dog class", "It builds one Dog object from the class", "It runs the program", "It deletes a Dog"], 1,
         "`new` builds an object. The class itself is only the blueprint.")
u.blank("Two dogs, two names. Print both.", """
class Dog { String name; }

public class Main {
    public static void main(String[] args) {
        Dog a = ___ Dog();
        a.name = "Rex";
        Dog b = new Dog();
        b.___ = "Milo";
        System.out.println(a.name);
        System.out.println(b.name);
    }
}
""", [["new"], ["name"]], "`new` builds the object. `name` is that object's own field.", full=True)
u.order("Arrange the lines so the program prints `Rex`.", """
class Dog { String name; }
public class Main {
    public static void main(String[] args) {
        Dog d = new Dog();
        d.name = "Rex";
        System.out.println(d.name);
    }
}
""", "Declare the class, build an object, set the field, then print it.", full=True)
u.fix("Both lines should show different names, `Rex` then `Milo`. They don't.", """
class Dog { String name; }

public class Main {
    public static void main(String[] args) {
        Dog a = new Dog();
        Dog b = a;
        a.name = "Rex";
        b.name = "Milo";
        System.out.println(a.name);
        System.out.println(b.name);
    }
}
""", """
class Dog { String name; }

public class Main {
    public static void main(String[] args) {
        Dog a = new Dog();
        Dog b = new Dog();
        a.name = "Rex";
        b.name = "Milo";
        System.out.println(a.name);
        System.out.println(b.name);
    }
}
""", "`b = a` makes both names point at one object. `new Dog()` builds a second one.", full=True)
u.write("Read a name and an age. Store them on a `Person` and print `name is age`. Input `Ana` then `21` prints `Ana is 21`.", """
import java.util.*;

class Person { String name; int age; }

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Person p = new Person();
        p.name = sc.next();
        p.age = sc.nextInt();
        System.out.println(p.name);
    }
}
""", """
import java.util.*;

class Person { String name; int age; }

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Person p = new Person();
        p.name = sc.next();
        p.age = sc.nextInt();
        System.out.println(p.name + " is " + p.age);
    }
}
""", ["Ana\n21\n", "Bo\n0\n", "Ravi\n7\n"], "The object holds both fields. Print them in one sentence.", full=True)

# 2 ---------------------------------------------------------------- constructors and this
u = oop_unit(L, "Constructors and this", """
A constructor runs when `new` builds the object. Its name matches the class, and it has no return type.
You can write several, as long as the parameter lists differ.

```java
class Box {
    int w;
    Box(int w) { this.w = w; }
}
```

`this.w` is the field. The bare `w` is the parameter. `w = w` stores the parameter in itself and leaves the field at 0.
""")
u.predict("""
class Greeter {
    Greeter() { System.out.println("hi"); }
    Greeter(String name) { System.out.println("hi " + name); }
}

public class Main {
    public static void main(String[] args) {
        new Greeter();
        new Greeter("Ana");
    }
}
""", "Java picks the constructor whose parameters match the `new` call.", full=True)
u.choice("The field and the parameter are both named `w`. Which line stores the parameter on the object?",
         ["w = w;", "this.w = w;", "w = this.w;", "Box.w = this;"], 1,
         "`this.w` is the field. The `w` on the right is the parameter.")
u.blank("A square box uses the two-argument constructor.", """
class Box {
    int w;
    int h;
    Box(int side) { ___(side, side); }
    Box(int w, int h) { this.w = w; ___.h = h; }
}

public class Main {
    public static void main(String[] args) {
        Box b = new Box(4);
        System.out.println(b.w * b.h);
    }
}
""", [["this"], ["this"]], "`this(...)` calls another constructor. `this.h` is the field.", full=True)
u.order("Arrange the lines so the program prints `10`.", """
class Box { int w; int h; Box(int w, int h) { this.w = w; this.h = h; } }
public class Main {
    public static void main(String[] args) {
        Box b = new Box(2, 5);
        System.out.println(b.w * b.h);
    }
}
""", "Build the box with `new`, then read the fields the constructor stored.", full=True)
u.fix("`show` should print `4`, the value passed to `new`. It prints `0`.", """
class Point {
    int x;
    Point(int x) { x = x; }
    void show() { System.out.println(x); }
}

public class Main {
    public static void main(String[] args) {
        new Point(4).show();
    }
}
""", """
class Point {
    int x;
    Point(int x) { this.x = x; }
    void show() { System.out.println(x); }
}

public class Main {
    public static void main(String[] args) {
        new Point(4).show();
    }
}
""", "`x = x` writes the parameter onto itself. `this.x = x` writes it onto the field.", full=True)
u.write("Read width and height. Build a `Box` with a constructor that uses `this`, and print the area. Input `3 4` prints `12`.", """
import java.util.*;

class Box {
    int w;
    int h;
    Box(int w, int h) { w = w; h = h; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Box b = new Box(sc.nextInt(), sc.nextInt());
        System.out.println(b.w * b.h);
    }
}
""", """
import java.util.*;

class Box {
    int w;
    int h;
    Box(int w, int h) { this.w = w; this.h = h; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Box b = new Box(sc.nextInt(), sc.nextInt());
        System.out.println(b.w * b.h);
    }
}
""", ["3 4\n", "0 5\n", "2 2\n", "-3 4\n"], "`this.w = w` stores each parameter. Then print `w * h`.", full=True)

# 3 ---------------------------------------------------------------- encapsulation
u = oop_unit(L, "Private fields", """
`private` means only code inside the class can touch that field. Other classes go through methods.

```java
class Account {
    private int balance = 0;
    public void deposit(int n) { if (n > 0) balance += n; }
    public int getBalance() { return balance; }
}
```

The check lives in one place. Callers cannot set `balance` to a negative number directly.
""")
u.predict("""
class Account {
    private int balance = 0;
    public void deposit(int n) { if (n > 0) balance += n; }
    public int getBalance() { return balance; }
}

public class Main {
    public static void main(String[] args) {
        Account a = new Account();
        a.deposit(30);
        a.deposit(-5);
        a.deposit(12);
        System.out.println(a.getBalance());
    }
}
""", "30 is stored, -5 is rejected, 12 is added. The balance is 42.", full=True)
u.choice("From `main` in another class, who can read a `private` field?",
         ["Any class in the file", "Only methods of the class that declares it", "Any subclass", "Only static methods"], 1,
         "`private` stops other classes, including `Main`. They call a method instead.")
u.blank("Finish the getter and call it.", """
class Account {
    private int balance = 0;
    public void deposit(int n) { if (n > 0) balance += n; }
    public int ___() { return balance; }
}

public class Main {
    public static void main(String[] args) {
        Account a = new Account();
        a.deposit(10);
        System.out.println(a.___());
    }
}
""", [["getBalance"], ["getBalance"]], "The method is the public door. The field stays `private`.", full=True)
u.order("Arrange the lines so the program prints `15`.", """
class Account { private int balance = 0; public void deposit(int n) { if (n > 0) balance += n; } public int getBalance() { return balance; } }
public class Main {
    public static void main(String[] args) {
        Account a = new Account();
        a.deposit(15);
        System.out.println(a.getBalance());
    }
}
""", "Deposit through the method, then read with the getter.", full=True)
u.fix("Age must stay at or above 0. After `setAge(20)` and `setAge(-3)`, print `20`.", """
class Person {
    private int age = 0;
    public void setAge(int n) { age = n; }
    public int getAge() { return age; }
}

public class Main {
    public static void main(String[] args) {
        Person p = new Person();
        p.setAge(20);
        p.setAge(-3);
        System.out.println(p.getAge());
    }
}
""", """
class Person {
    private int age = 0;
    public void setAge(int n) { if (n >= 0) age = n; }
    public int getAge() { return age; }
}

public class Main {
    public static void main(String[] args) {
        Person p = new Person();
        p.setAge(20);
        p.setAge(-3);
        System.out.println(p.getAge());
    }
}
""", "The setter is where the rule lives. Ignore a negative argument.", full=True)
u.write("""
Read `n`, then `n` amounts. Add an amount to an `Account` only when it is greater than 0, and print the balance.
Input `3` / `10` / `-4` / `5` prints `15`.
""", """
import java.util.*;

class Account {
    private int balance = 0;
    public void deposit(int n) { balance += n; }
    public int getBalance() { return balance; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Account a = new Account();
        int n = sc.nextInt();
        for (int i = 0; i < n; i++) a.deposit(sc.nextInt());
        System.out.println(a.getBalance());
    }
}
""", """
import java.util.*;

class Account {
    private int balance = 0;
    public void deposit(int n) { if (n > 0) balance += n; }
    public int getBalance() { return balance; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Account a = new Account();
        int n = sc.nextInt();
        for (int i = 0; i < n; i++) a.deposit(sc.nextInt());
        System.out.println(a.getBalance());
    }
}
""", ["3\n10\n-4\n5\n", "1\n0\n", "2\n-8\n-1\n", "4\n20\n0\n7\n3\n"], "Reject amounts that are not positive, then print `getBalance()`.", full=True)

# 4 ---------------------------------------------------------------- static
u = oop_unit(L, "Static members", """
A `static` field belongs to the class, not to one object. Every object sees the same one.
A `static` method is called on the class: `Ticket.issued()`.

```java
class Ticket {
    static int next = 1;
    int id;
    Ticket() { id = next++; }
}
```

`id` is different on each ticket. `next` is the shared counter.
""")
u.predict("""
class Ticket {
    static int next = 1;
    int id;
    Ticket() { id = next++; }
    static int issued() { return next - 1; }
}

public class Main {
    public static void main(String[] args) {
        Ticket a = new Ticket();
        Ticket b = new Ticket();
        System.out.println(a.id);
        System.out.println(b.id);
        System.out.println(Ticket.issued());
    }
}
""", "One shared `next` hands out 1, then 2. `issued` reads that same counter.", full=True)
u.choice("A `static` field is stored…",
         ["separately inside every object", "once, on the class, shared by every object", "only inside main", "on the first object, and copied after that"], 1,
         "Change it from any object and the others see the new value.")
u.blank("Count calls with one shared field.", """
class Counter {
    ___ int n = 0;
    static void add() { n++; }
}

public class Main {
    public static void main(String[] args) {
        Counter.add();
        Counter.add();
        System.out.println(Counter.___);
    }
}
""", [["static"], ["n"]], "`static` puts `n` on the class, so both calls update the same number.", full=True)
u.order("Arrange the lines so the program prints `2`.", """
class Counter { static int n = 0; }
public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 2; i++) Counter.n++;
        System.out.println(Counter.n);
    }
}
""", "Bump the shared field twice, then print it.", full=True)
u.fix("The second ticket should be id `2`. Both print `1`.", """
class Ticket {
    int next = 1;
    int id;
    Ticket() { id = next++; }
}

public class Main {
    public static void main(String[] args) {
        Ticket a = new Ticket();
        Ticket b = new Ticket();
        System.out.println(a.id);
        System.out.println(b.id);
    }
}
""", """
class Ticket {
    static int next = 1;
    int id;
    Ticket() { id = next++; }
}

public class Main {
    public static void main(String[] args) {
        Ticket a = new Ticket();
        Ticket b = new Ticket();
        System.out.println(a.id);
        System.out.println(b.id);
    }
}
""", "Without `static`, each ticket has its own `next` starting at 1. `static` makes them share one counter.", full=True)
u.write("Read `n` and create `n` tickets from a class with a `static` counter. Print how many were issued. Input `3` prints `3`.", """
import java.util.*;

class Ticket {
    int issued = 0;
    Ticket() { issued++; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        for (int i = 0; i < n; i++) new Ticket();
        System.out.println(0);
    }
}
""", """
import java.util.*;

class Ticket {
    static int issued = 0;
    Ticket() { issued++; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        for (int i = 0; i < n; i++) new Ticket();
        System.out.println(Ticket.issued);
    }
}
""", ["3\n", "0\n", "1\n", "10\n"], "The counter has to be `static`, or each ticket would count only itself.", full=True)

# 5 ---------------------------------------------------------------- inheritance
u = oop_unit(L, "Inheritance", """
`class Dog extends Animal` means a dog is an animal and starts with Animal's fields and methods.
The subclass constructor calls `super(...)` first, so the parent part is built before the child part.

```java
class Dog extends Animal {
    Dog(String name) { super(name); }
}
```

Building a `Dog` runs Animal's constructor, then Dog's.
""")
u.predict("""
class A {
    A() { System.out.println("A"); }
}
class B extends A {
    B() { System.out.println("B"); }
}
class C extends B {
    C() { System.out.println("C"); }
}

public class Main {
    public static void main(String[] args) {
        new C();
    }
}
""", "Each constructor calls `super()` first, even when you don't write it. Parent runs, then child.", full=True)
u.choice("A dog is a kind of animal. Which declaration says that?",
         ["class Dog extends Animal", "class Animal extends Dog", "class Dog { Animal animal; }", "Dog dog = new Animal();"], 0,
         "`extends` points at the parent. The child is the more specific type.")
u.blank("Pass the name up to Animal.", """
class Animal {
    String name;
    Animal(String name) { this.name = name; }
}
class Dog ___ Animal {
    Dog(String name) { ___(name); }
}

public class Main {
    public static void main(String[] args) {
        Dog d = new Dog("Rex");
        System.out.println(d.name);
    }
}
""", [["extends"], ["super"]], "`extends` names the parent. `super(name)` calls the parent constructor.", full=True)
u.order("Arrange the lines so the program prints `Animal` and then `Dog`.", """
class Animal { Animal() { System.out.println("Animal"); } }
class Dog extends Animal { Dog() { System.out.println("Dog"); } }
public class Main {
    public static void main(String[] args) {
        new Dog();
    }
}
""", "The parent constructor runs before the child's body.", full=True)
u.fix("This should print `A` then `B`, but it does not compile.", """
class A {
    A() { System.out.println("A"); }
}
class B extends A {
    B() {
        System.out.println("B");
        super();
    }
}

public class Main {
    public static void main(String[] args) {
        new B();
    }
}
""", """
class A {
    A() { System.out.println("A"); }
}
class B extends A {
    B() {
        super();
        System.out.println("B");
    }
}

public class Main {
    public static void main(String[] args) {
        new B();
    }
}
""", "`super()` has to be the first line of the constructor. The parent is built before the child prints.", full=True)
u.write("Read a name. Build a `Dog` that `extends` an animal with that name, and print `dog ` plus the name. Input `Rex` prints `dog Rex`.", """
import java.util.*;

class Animal {
    String name;
    Animal(String name) { this.name = name; }
}
class Dog extends Animal {
    Dog(String name) { super(name); }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Dog d = new Dog(sc.next());
        System.out.println(d.name);
    }
}
""", """
import java.util.*;

class Animal {
    String name;
    Animal(String name) { this.name = name; }
}
class Dog extends Animal {
    Dog(String name) { super(name); }
    String tag() { return "dog " + name; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Dog d = new Dog(sc.next());
        System.out.println(d.tag());
    }
}
""", ["Rex\n", "A\n", "Milo\n"], "`super(name)` stores the name on the animal. The dog adds the word `dog`.", full=True)

# 6 ---------------------------------------------------------------- overriding
u = oop_unit(L, "Overriding", """
A child can replace a parent method. The variable can be the parent type; the call still runs the object's own method.

```java
class Dog extends Animal {
    @Override
    String sound() { return "woof"; }
}
```

`@Override` asks the compiler to check that the method really replaces one from the parent. A mismatched parameter list will not compile.
""")
u.predict("""
class Animal {
    String sound() { return "..."; }
}
class Dog extends Animal {
    @Override String sound() { return "woof"; }
}
class Cat extends Animal {
    @Override String sound() { return "meow"; }
}

public class Main {
    public static void main(String[] args) {
        Animal[] pets = { new Dog(), new Cat(), new Dog() };
        for (Animal p : pets) System.out.println(p.sound());
    }
}
""", "The array type is Animal. Each call uses the real object's `sound`.", full=True)
u.choice("The variable type is `Animal` and the object is a `Dog`. Which `sound` runs?",
         ["Animal.sound, because the variable says Animal", "Dog.sound, picked while the program runs", "Both, Animal first", "It fails to compile"], 1,
         "Java looks at the object, not only the variable, when it calls the method.")
u.blank("Mark the method as a real override.", """
class Animal {
    String sound() { return "..."; }
}
class Dog extends Animal {
    ___
    String sound() { return "woof"; }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        System.out.println(a.___());
    }
}
""", [["@Override"], ["sound"]], "`@Override` checks the signature. The call still uses the dog's method.", full=True)
u.order("Arrange the lines so the program prints `woof`.", """
class Animal { String sound() { return "..."; } }
class Dog extends Animal { @Override String sound() { return "woof"; } }
public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        System.out.println(a.sound());
    }
}
""", "Store a Dog in an Animal variable, then call `sound`.", full=True)
u.fix("`@Override` is right to want, but this does not compile. `a.sound()` should print `woof`.", """
class Animal {
    String sound() { return "..."; }
}
class Dog extends Animal {
    @Override
    String sound(int n) { return "woof"; }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        System.out.println(a.sound());
    }
}
""", """
class Animal {
    String sound() { return "..."; }
}
class Dog extends Animal {
    @Override
    String sound() { return "woof"; }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        System.out.println(a.sound());
    }
}
""", "The parameter list has to match. `sound(int)` is a different method, so `@Override` is rejected.", full=True)
u.write("""
Read `n`, then `n` words, each `dog` or `cat`. Print `woof` or `meow` by calling `sound()` on an animal reference.
Input `2` / `dog` / `cat` prints `woof` then `meow`.
""", """
import java.util.*;

class Animal {
    String sound() { return "..."; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        for (int i = 0; i < n; i++) {
            sc.next();
            System.out.println("...");
        }
    }
}
""", """
import java.util.*;

class Animal {
    String sound() { return "..."; }
}
class Dog extends Animal {
    @Override String sound() { return "woof"; }
}
class Cat extends Animal {
    @Override String sound() { return "meow"; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        for (int i = 0; i < n; i++) {
            Animal a = sc.next().equals("dog") ? new Dog() : new Cat();
            System.out.println(a.sound());
        }
    }
}
""", ["2\ndog\ncat\n", "1\ndog\n", "3\ncat\ncat\ndog\n"], "One parent variable, two child classes. `sound()` follows the object.", full=True)

# 7 ---------------------------------------------------------------- abstract and interfaces
u = oop_unit(L, "Abstract and interfaces", """
An `abstract` class can hold fields and a constructor, and it can leave methods without a body. You cannot `new` it.
An `interface` is a list of methods a class promises to have. A class `extends` one class and can `implements` several interfaces.

```java
class Lamp implements Switchable, Named {
    public void toggle() { on = !on; }
    public String label() { return on ? "bright" : "dark"; }
}
```

Interface methods are public, so the methods that fill them in are public too.
""")
u.predict("""
interface Switchable { void toggle(); }
interface Named { String label(); }

class Lamp implements Switchable, Named {
    boolean on = false;
    public void toggle() { on = !on; }
    public String label() { return on ? "bright" : "dark"; }
}

public class Main {
    public static void main(String[] args) {
        Lamp lamp = new Lamp();
        System.out.println(lamp.label());
        lamp.toggle();
        System.out.println(lamp.label());
    }
}
""", "One class can fill in two interfaces. `toggle` flips the field `label` reads.", full=True)
u.choice("Which line fails to compile?",
         ["class Square extends Shape { int area() { return 1; } }", "Shape s = new Shape();", "Shape s = new Square();", "abstract class Shape { int side = 1; }"], 1,
         "An abstract class is incomplete, so `new Shape()` is rejected. A concrete subclass is fine.",
         code="abstract class Shape {\n    abstract int area();\n}\nclass Square extends Shape {\n    int area() { return 1; }\n}")
u.blank("Leave `area` without a body, then fill it in on the square.", """
abstract class Shape {
    ___ int area();
}
class Square extends Shape {
    int side;
    Square(int side) { this.side = side; }
    public int area() { return side * side; }
}

public class Main {
    public static void main(String[] args) {
        Shape s = new Square(3);
        System.out.println(s.area());
    }
}
""", [["abstract"]], "The parent declares `area`. The square is the class you can actually `new`.", full=True)
u.order("Arrange the lines so the program prints `16`.", """
abstract class Shape { abstract int area(); }
class Square extends Shape { int side; Square(int side) { this.side = side; } int area() { return side * side; } }
public class Main {
    public static void main(String[] args) {
        Shape s = new Square(4);
        System.out.println(s.area());
    }
}
""", "The variable can be the abstract type. The object is a Square.", full=True)
u.fix("`Square` says it extends `Shape`, but the program does not compile. Printing `s.area()` should show `9`.", """
abstract class Shape {
    abstract int area();
}
class Square extends Shape {
    int side;
    Square(int side) { this.side = side; }
}

public class Main {
    public static void main(String[] args) {
        Shape s = new Square(3);
        System.out.println(s.area());
    }
}
""", """
abstract class Shape {
    abstract int area();
}
class Square extends Shape {
    int side;
    Square(int side) { this.side = side; }
    int area() { return side * side; }
}

public class Main {
    public static void main(String[] args) {
        Shape s = new Square(3);
        System.out.println(s.area());
    }
}
""", "A concrete class has to fill in every abstract method, or it has to be abstract itself.", full=True)
u.write("Read a side length and print the area of a `Square` that extends an abstract `Shape`. Input `4` prints `16`.", """
import java.util.*;

abstract class Shape {
    abstract int area();
}
class Square extends Shape {
    int side;
    Square(int side) { this.side = side; }
    int area() { return 0; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Shape s = new Square(sc.nextInt());
        System.out.println(s.area());
    }
}
""", """
import java.util.*;

abstract class Shape {
    abstract int area();
}
class Square extends Shape {
    int side;
    Square(int side) { this.side = side; }
    int area() { return side * side; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Shape s = new Square(sc.nextInt());
        System.out.println(s.area());
    }
}
""", ["4\n", "1\n", "0\n", "5\n"], "`area` returns `side * side`. The variable can stay typed as `Shape`.", full=True)

# 8 ---------------------------------------------------------------- toString and equals
u = oop_unit(L, "Printing and equality", """
`System.out.println(obj)` calls `toString()`. The default text is the class name and a code, which is rarely what you want.

`==` asks whether two variables point at the same object. `equals` is yours to define: same coordinates, same book id, and so on.
If you override `equals`, override `hashCode` too, with the same fields.

```java
public String toString() { return x + "," + y; }
public boolean equals(Object other) { /* compare fields */ }
```
""")
u.predict("""
class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    public String toString() { return x + "," + y; }
    public boolean equals(Object other) {
        if (!(other instanceof Point)) return false;
        Point p = (Point) other;
        return x == p.x && y == p.y;
    }
    public int hashCode() { return 31 * x + y; }
}

public class Main {
    public static void main(String[] args) {
        Point a = new Point(1, 2);
        Point b = new Point(1, 2);
        System.out.println(a);
        System.out.println(a == b);
        System.out.println(a.equals(b));
    }
}
""", "`println` uses `toString`. `==` is false because `a` and `b` are two objects. `equals` compares the numbers.", full=True)
u.choice("You wrote `equals` using `x` and `y`. What else should you override?",
         ["toString", "hashCode", "compare", "clone"], 1,
         "Equal objects should land in the same hash bucket. `hashCode` has to use those same fields.")
u.blank("Teach `println` to show the coordinates.", """
class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    public String ___() { return x + "," + y; }
}

public class Main {
    public static void main(String[] args) {
        Point p = new Point(3, 4);
        System.out.println(p);
    }
}
""", [["toString"]], "`println` looks for `toString` and prints whatever that method returns.", full=True)
u.order("Arrange the lines so the program prints `true`.", """
class Point { int x, y; Point(int x, int y) { this.x = x; this.y = y; } public boolean equals(Object o) { Point p = (Point) o; return x == p.x && y == p.y; } public int hashCode() { return 31 * x + y; } }
public class Main {
    public static void main(String[] args) {
        Point a = new Point(1, 2);
        Point b = new Point(1, 2);
        System.out.println(a.equals(b));
    }
}
""", "`equals` compares the fields. `==` would have compared the two references.", full=True)
u.fix("The two points both hold `(1, 2)`. The program should print `true`.", """
class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    public boolean equals(Object other) {
        if (!(other instanceof Point)) return false;
        Point p = (Point) other;
        return x == p.x && y == p.y;
    }
    public int hashCode() { return 31 * x + y; }
}

public class Main {
    public static void main(String[] args) {
        Point a = new Point(1, 2);
        Point b = new Point(1, 2);
        System.out.println(a == b);
    }
}
""", """
class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    public boolean equals(Object other) {
        if (!(other instanceof Point)) return false;
        Point p = (Point) other;
        return x == p.x && y == p.y;
    }
    public int hashCode() { return 31 * x + y; }
}

public class Main {
    public static void main(String[] args) {
        Point a = new Point(1, 2);
        Point b = new Point(1, 2);
        System.out.println(a.equals(b));
    }
}
""", "`==` is true only when both variables are the same object. `equals` is the field comparison.", full=True)
u.write("Read four integers `x1 y1 x2 y2`. Build two points and print `true` or `false` from `equals`. Input `1 2 1 2` prints `true`.", """
import java.util.*;

class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Point a = new Point(sc.nextInt(), sc.nextInt());
        Point b = new Point(sc.nextInt(), sc.nextInt());
        System.out.println(false);
    }
}
""", """
import java.util.*;

class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }
    public boolean equals(Object other) {
        if (!(other instanceof Point)) return false;
        Point p = (Point) other;
        return x == p.x && y == p.y;
    }
    public int hashCode() { return 31 * x + y; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Point a = new Point(sc.nextInt(), sc.nextInt());
        Point b = new Point(sc.nextInt(), sc.nextInt());
        System.out.println(a.equals(b));
    }
}
""", ["1 2 1 2\n", "1 2 1 3\n", "0 0 0 0\n", "-1 4 -1 4\n"], "Compare fields inside `equals`. `==` would stay false for two different objects.", full=True)

# 9 ---------------------------------------------------------------- composition
u = oop_unit(L, "Composition", """
A car is not a kind of engine. A car **has** an engine. That is a field, not `extends`.

```java
class Car {
    String model;
    Engine engine;
    Car(String model, Engine engine) {
        this.model = model;
        this.engine = engine;
    }
}
```

Use `extends` when the new type really is the parent type. Use a field when one object uses another.
""")
u.predict("""
class Engine {
    int hp;
    Engine(int hp) { this.hp = hp; }
    String status() { return hp + "hp"; }
}
class Car {
    String model;
    Engine engine;
    Car(String model, Engine engine) { this.model = model; this.engine = engine; }
    String spec() { return model + " " + engine.status(); }
}

public class Main {
    public static void main(String[] args) {
        Car c = new Car("Civic", new Engine(150));
        System.out.println(c.spec());
    }
}
""", "`spec` asks the engine it holds. The car does not extend the engine.", full=True)
u.choice("A car is built around an engine it uses. Which shape fits?",
         ["class Car extends Engine", "Car holds an Engine field", "class Engine extends Car", "One class, and a boolean that switches job"], 1,
         "Has-a is a field. Is-a is `extends`. A car is not an engine.")
u.blank("Read the horsepower from the engine the car holds.", """
class Engine {
    int hp;
    Engine(int hp) { this.hp = hp; }
    String status() { return hp + "hp"; }
}
class Car {
    String model;
    Engine engine;
    Car(String model, Engine engine) { this.model = model; this.engine = engine; }
    String spec() { return model + " " + ___.status(); }
}

public class Main {
    public static void main(String[] args) {
        Car c = new Car("Civic", new Engine(150));
        System.out.println(c.spec());
    }
}
""", [["engine"]], "The car keeps an `Engine` and calls methods on that field.", full=True)
u.order("Arrange the lines so the program prints `Civic 150hp`.", """
class Engine { int hp; Engine(int hp) { this.hp = hp; } String status() { return hp + "hp"; } }
class Car { Engine engine; String model; Car(String model, Engine engine) { this.model = model; this.engine = engine; } String spec() { return model + " " + engine.status(); } }
public class Main {
    public static void main(String[] args) {
        Car c = new Car("Civic", new Engine(150));
        System.out.println(c.spec());
    }
}
""", "Build the engine, hand it to the car, then ask the car for its spec.", full=True)
u.fix("`spec` should include the engine's horsepower. It prints `Civic 0hp`.", """
class Engine {
    int hp;
    Engine(int hp) { this.hp = hp; }
}
class Car {
    String model;
    int hp;
    Engine engine;
    Car(String model, Engine engine) { this.model = model; this.engine = engine; }
    String spec() { return model + " " + hp + "hp"; }
}

public class Main {
    public static void main(String[] args) {
        Car c = new Car("Civic", new Engine(150));
        System.out.println(c.spec());
    }
}
""", """
class Engine {
    int hp;
    Engine(int hp) { this.hp = hp; }
}
class Car {
    String model;
    Engine engine;
    Car(String model, Engine engine) { this.model = model; this.engine = engine; }
    String spec() { return model + " " + engine.hp + "hp"; }
}

public class Main {
    public static void main(String[] args) {
        Car c = new Car("Civic", new Engine(150));
        System.out.println(c.spec());
    }
}
""", "The horsepower lives on the engine. The car reads `engine.hp` instead of a field it never set.", full=True)
u.write("Read a model and a horsepower. Build a `Car` that has an `Engine`, and print `model hp` with `hp` stuck on the end, like `Civic 150hp`.", """
import java.util.*;

class Engine {
    int hp;
    Engine(int hp) { this.hp = hp; }
}
class Car {
    String model;
    Engine engine;
    Car(String model, Engine engine) { this.model = model; this.engine = engine; }
    String spec() { return model; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Car c = new Car(sc.next(), new Engine(sc.nextInt()));
        System.out.println(c.spec());
    }
}
""", """
import java.util.*;

class Engine {
    int hp;
    Engine(int hp) { this.hp = hp; }
}
class Car {
    String model;
    Engine engine;
    Car(String model, Engine engine) { this.model = model; this.engine = engine; }
    String spec() { return model + " " + engine.hp + "hp"; }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Car c = new Car(sc.next(), new Engine(sc.nextInt()));
        System.out.println(c.spec());
    }
}
""", ["Civic\n150\n", "Van\n90\n", "Bus\n0\n"], "The car stores the engine and reads `engine.hp` when it builds the line.", full=True)

# 10 --------------------------------------------------------------- bank account
u = oop_unit(L, "Bank account", """
Put the rules on the object. A `Bank` starts at 0 and is the only thing allowed to change its balance.

- `deposit N` adds `N` when `N > 0` and prints the balance; otherwise it prints `Invalid`
- `withdraw N` prints `Invalid` when `N <= 0`, `Insufficient funds` when `N` is too big, otherwise subtracts and prints the balance
- `balance` prints the balance

```java
class Bank {
    private int balance = 0;
    void deposit(int n) { /* check, then update */ }
}
```
""")
u.predict("""
class Bank {
    private int balance = 0;
    void deposit(int n) {
        if (n <= 0) { System.out.println("Invalid"); return; }
        balance += n;
        System.out.println(balance);
    }
    void withdraw(int n) {
        if (n <= 0) { System.out.println("Invalid"); return; }
        if (n > balance) { System.out.println("Insufficient funds"); return; }
        balance -= n;
        System.out.println(balance);
    }
}

public class Main {
    public static void main(String[] args) {
        Bank b = new Bank();
        b.deposit(50);
        b.withdraw(80);
        b.withdraw(20);
    }
}
""", "50 is stored. 80 is more than 50, so the balance stays 50. 20 then leaves 30.", full=True)
u.choice("Which line belongs in `withdraw` before it subtracts?",
         ["balance = n;", "if (n > balance) { System.out.println(\"Insufficient funds\"); return; }", "balance = 0;", "n = balance;"], 1,
         "Say no, and return, before changing the field. The balance stays as it was.")
u.blank("Reject a non-positive deposit.", """
class Bank {
    private int balance = 0;
    void deposit(int n) {
        if (n ___ 0) { System.out.println("Invalid"); return; }
        balance += n;
        System.out.println(balance);
    }
}

public class Main {
    public static void main(String[] args) {
        Bank b = new Bank();
        b.deposit(0);
        b.deposit(15);
    }
}
""", [["<="]], "`<= 0` catches 0 and negatives. A positive amount falls through and is added.", full=True)
u.order("Arrange the lines so the program prints `Insufficient funds`.", """
class Bank { private int balance = 0; void withdraw(int n) { if (n > balance) { System.out.println("Insufficient funds"); return; } balance -= n; System.out.println(balance); } }
public class Main {
    public static void main(String[] args) {
        Bank b = new Bank();
        b.withdraw(80);
    }
}
""", "The account starts at 0, so 80 is too much.", full=True)
u.fix("""
`deposit` must reject non-positive amounts, and `withdraw` must refuse to go below 0.

- `withdraw 80` prints `Insufficient funds`
- `deposit 50` then `withdraw 80` prints `50` then `Insufficient funds`
- `deposit -4` prints `Invalid`
- `deposit 20`, `withdraw 20`, `withdraw 5` prints `20`, `0`, `Insufficient funds`
""", """
import java.util.*;

class Bank {
    private int balance = 0;
    void deposit(int n) {
        balance += n;
        System.out.println(balance);
    }
    void withdraw(int n) {
        if (n <= 0) { System.out.println("Invalid"); return; }
        balance -= n;
        System.out.println(balance);
    }
    void show() { System.out.println(balance); }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Bank bank = new Bank();
        while (sc.hasNext()) {
            String cmd = sc.next();
            if (cmd.equals("deposit")) bank.deposit(sc.nextInt());
            else if (cmd.equals("withdraw")) bank.withdraw(sc.nextInt());
            else if (cmd.equals("balance")) bank.show();
        }
    }
}
""", """
import java.util.*;

class Bank {
    private int balance = 0;
    void deposit(int n) {
        if (n <= 0) { System.out.println("Invalid"); return; }
        balance += n;
        System.out.println(balance);
    }
    void withdraw(int n) {
        if (n <= 0) { System.out.println("Invalid"); return; }
        if (n > balance) { System.out.println("Insufficient funds"); return; }
        balance -= n;
        System.out.println(balance);
    }
    void show() { System.out.println(balance); }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Bank bank = new Bank();
        while (sc.hasNext()) {
            String cmd = sc.next();
            if (cmd.equals("deposit")) bank.deposit(sc.nextInt());
            else if (cmd.equals("withdraw")) bank.withdraw(sc.nextInt());
            else if (cmd.equals("balance")) bank.show();
        }
    }
}
""", "Check the amount before you change `balance`. A rejected command leaves the field as it was.",
   full=True, tests=["withdraw 80\n", "deposit 50\nwithdraw 80\n", "deposit -4\n", "deposit 20\nwithdraw 20\nwithdraw 5\n"])
u.write("""
Read commands until the input ends. Keep the balance `private` on a `Bank` that starts at 0.

- `deposit N` — if `N > 0`, add it and print the balance; otherwise print `Invalid`
- `withdraw N` — if `N <= 0`, print `Invalid`; if `N` is greater than the balance, print `Insufficient funds`; otherwise subtract and print the balance
- `balance` — print the balance
""", """
import java.util.*;

class Bank {
    private int balance = 0;
    void deposit(int n) { }
    void withdraw(int n) { }
    void show() { }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Bank bank = new Bank();
        while (sc.hasNext()) {
            String cmd = sc.next();
            if (cmd.equals("deposit")) bank.deposit(sc.nextInt());
            else if (cmd.equals("withdraw")) bank.withdraw(sc.nextInt());
            else if (cmd.equals("balance")) bank.show();
        }
    }
}
""", """
import java.util.*;

class Bank {
    private int balance = 0;
    void deposit(int n) {
        if (n <= 0) { System.out.println("Invalid"); return; }
        balance += n;
        System.out.println(balance);
    }
    void withdraw(int n) {
        if (n <= 0) { System.out.println("Invalid"); return; }
        if (n > balance) { System.out.println("Insufficient funds"); return; }
        balance -= n;
        System.out.println(balance);
    }
    void show() { System.out.println(balance); }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Bank bank = new Bank();
        while (sc.hasNext()) {
            String cmd = sc.next();
            if (cmd.equals("deposit")) bank.deposit(sc.nextInt());
            else if (cmd.equals("withdraw")) bank.withdraw(sc.nextInt());
            else if (cmd.equals("balance")) bank.show();
        }
    }
}
""", ["deposit 50\nwithdraw 20\nbalance\n", "withdraw 80\n", "deposit 40\nwithdraw 40\nwithdraw 1\n", "deposit 0\ndeposit -3\ndeposit 15\n", "balance\n"],
   "The object owns the number. Each command either prints a refusal or the new balance.", full=True)
