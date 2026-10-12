from bc import oop_unit

L = "javascript"

READ = 'const lines = require("fs").readFileSync(0, "utf8").split("\\n");'

# 1 ---------------------------------------------------------------- classes and objects
u = oop_unit(L, "Classes and objects", """
A class is a blueprint. `new Dog()` builds one object. Fields can be added on that object, and methods use `this` for the object they were called on.

```js
class Dog {
  bark() {
    console.log(this.name + " says woof");
  }
}
const rex = new Dog();
rex.name = "Rex";
```

`const milo = new Dog()` is a different object. Setting `rex.name` leaves `milo` alone.
""")
u.predict("""
class Counter {
  add() { this.n += 1; }
}
const a = new Counter();
const b = new Counter();
a.n = 0;
b.n = 0;
a.add();
a.add();
b.add();
console.log(a.n);
console.log(b.n);
""", "Each `new Counter()` has its own `n`. Calling `add` changes only that object.")
u.choice("What does `new Dog()` do?",
         ["It renames the class", "It builds one Dog object", "It runs the file again", "It copies every existing dog"], 1,
         "`new` builds an object from the class. The class itself is only the blueprint.")
u.blank("Two dogs, two names.", """
class Dog {
  label() { console.log(___.name); }
}
const a = new Dog();
const b = ___ Dog();
a.name = "Rex";
b.name = "Milo";
a.label();
b.label();
""", [["this"], ["new"]], "`this` is the object the method was called on. `new` builds the second dog.")
u.order("Arrange the lines so the program prints `Rex`.", """
class Dog { label() { console.log(this.name); } }
const d = new Dog();
d.name = "Rex";
d.label();
""", "Build the object with `new`, set the field, then call the method.")
u.fix("Both lines should be different names, `Rex` then `Milo`.", """
class Dog {
  label() { console.log(this.name); }
}
const a = new Dog();
const b = a;
a.name = "Rex";
b.name = "Milo";
a.label();
b.label();
""", """
class Dog {
  label() { console.log(this.name); }
}
const a = new Dog();
const b = new Dog();
a.name = "Rex";
b.name = "Milo";
a.label();
b.label();
""", "`b = a` is one object with two names. `new Dog()` builds a second object.")
u.write("Read a name and an age, one per line. Store them on a `Person` and print `name is age`. Input `Ana` then `21` prints `Ana is 21`.", READ + """
class Person {
  line() { console.log(this.name); }
}
const p = new Person();
p.name = lines[0].trim();
p.age = Number(lines[1]);
p.line();
""", READ + """
class Person {
  line() { console.log(this.name + " is " + this.age); }
}
const p = new Person();
p.name = lines[0].trim();
p.age = Number(lines[1]);
p.line();
""", ["Ana\n21\n", "Bo\n0\n", "Ravi\n7\n"], "Keep both values on the object and build the sentence from `this`.")

# 2 ---------------------------------------------------------------- constructor, this, new
u = oop_unit(L, "Constructors and new", """
`constructor` runs when `new` builds the object. Inside it, `this` is that new object.

```js
class Box {
  constructor(w) { this.w = w; }
}
```

The bare name `w` is the parameter. `this.w` is the field. Call the class without `new` and it throws: a class constructor cannot be called as a plain function.
""")
u.predict("""
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}
const a = new Point(1, 2);
const b = new Point(3, 4);
console.log(a.x + a.y);
console.log(b.x);
""", "`new` runs `constructor` for that object. `a` and `b` keep different fields.")
u.choice("What happens if you call a class as `Point(4)`, with no `new`?",
         ["You get a Point", "TypeError: the class must be called with new", "You get undefined, and the code keeps going", "You get 4"], 1,
         "Class constructors refuse a call that is missing `new`.")
u.blank("Store the parameter on the object.", """
class Point {
  constructor(x) { ___.x = x; }
}
console.log(new Point(4).x);
""", [["this"]], "`this.x` is the field. The bare `x` is only the parameter.")
u.order("Arrange the lines so the program prints `10`.", """
class Box { constructor(w, h) { this.w = w; this.h = h; } }
const b = new Box(2, 5);
console.log(b.w * b.h);
""", "`new` runs the constructor, which stores both fields before the print.")
u.fix("`show` should print `4`. The call throws.", """
class Point {
  constructor(x) { this.x = x; }
  show() { console.log(this.x); }
}
const p = Point(4);
p.show();
""", """
class Point {
  constructor(x) { this.x = x; }
  show() { console.log(this.x); }
}
const p = new Point(4);
p.show();
""", "Put `new` in front of the class. Without it the constructor throws and `p` is never assigned.")
u.write("Read width and height from one line. Store them with `constructor` and print the area. Input `3 4` prints `12`.", READ + """
class Box {
  constructor(w, h) { w = w; h = h; }
}
const [w, h] = lines[0].split(" ").map(Number);
console.log(new Box(w, h).w * new Box(w, h).h);
""", READ + """
class Box {
  constructor(w, h) { this.w = w; this.h = h; }
}
const [w, h] = lines[0].split(" ").map(Number);
const b = new Box(w, h);
console.log(b.w * b.h);
""", ["3 4\n", "0 5\n", "2 2\n", "-3 4\n"], "`this.w = w` stores the parameter. Then multiply the two fields.")

# 3 ---------------------------------------------------------------- private fields
u = oop_unit(L, "Private fields", """
A field that starts with `#` is private to the class. Code outside cannot read `#balance` at all; that line is a syntax error.

`get` and `set` are the door. Reading `account.balance` runs the getter. Assigning `account.balance = n` runs the setter, which can ignore a bad value.

```js
class Account {
  #balance = 0;
  get balance() { return this.#balance; }
}
```
""")
u.predict("""
class Account {
  #balance = 0;
  deposit(n) { if (n > 0) this.#balance += n; }
  get balance() { return this.#balance; }
}
const a = new Account();
a.deposit(30);
a.deposit(-5);
a.deposit(12);
console.log(a.balance);
""", "30 is stored, -5 is rejected, 12 is added. The getter returns 42.")
u.choice("What is true of a `#balance` field?",
         ["Any code can read it if it spells the name", "Only methods inside the class can use it", "It is shared by every object", "It is just a naming habit and still public"], 1,
         "The `#` name is checked by the language. Outside the class, mentioning it will not run.")
u.blank("Expose the private number through a getter named `balance`.", """
class Account {
  #balance = 0;
  deposit(n) { if (n > 0) this.#balance += n; }
  get ___() { return this.#balance; }
}
const a = new Account();
a.deposit(10);
console.log(a.balance);
""", [["balance"]], "The getter's name is what callers write. The field stays `#balance`.")
u.order("Arrange the lines so the program prints `15`.", """
class Account { #balance = 0; deposit(n) { if (n > 0) this.#balance += n; } get balance() { return this.#balance; } }
const a = new Account();
a.deposit(15);
console.log(a.balance);
""", "Deposit through the method, then read the getter.")
u.fix("After setting 20 and then -3, the balance should still be `20`.", """
class Person {
  #age = 0;
  set age(n) { this.#age = n; }
  get age() { return this.#age; }
}
const p = new Person();
p.age = 20;
p.age = -3;
console.log(p.age);
""", """
class Person {
  #age = 0;
  set age(n) { if (n >= 0) this.#age = n; }
  get age() { return this.#age; }
}
const p = new Person();
p.age = 20;
p.age = -3;
console.log(p.age);
""", "The setter is where the rule lives. Ignore a negative assignment.")
u.write("""
Read `n`, then `n` amounts, one per line. Add an amount only when it is greater than 0, and print the balance through a getter.
Input `3` / `10` / `-4` / `5` prints `15`.
""", READ + """
class Account {
  #balance = 0;
  deposit(n) { this.#balance += n; }
  get balance() { return this.#balance; }
}
const a = new Account();
const n = Number(lines[0]);
for (let i = 0; i < n; i++) a.deposit(Number(lines[i + 1]));
console.log(a.balance);
""", READ + """
class Account {
  #balance = 0;
  deposit(n) { if (n > 0) this.#balance += n; }
  get balance() { return this.#balance; }
}
const a = new Account();
const n = Number(lines[0]);
for (let i = 0; i < n; i++) a.deposit(Number(lines[i + 1]));
console.log(a.balance);
""", ["3\n10\n-4\n5\n", "1\n0\n", "2\n-8\n-1\n", "4\n20\n0\n7\n3\n"], "Reject amounts that are not positive, then print the getter.")

# 4 ---------------------------------------------------------------- static
u = oop_unit(L, "Static members", """
A `static` field belongs to the class. Every object sees the same one. Call a static method on the class: `Ticket.issued()`.

```js
class Ticket {
  static next = 1;
  constructor() { this.id = Ticket.next++; }
}
```

`id` is different on each ticket. `Ticket.next` is the shared counter.
""")
u.predict("""
class Ticket {
  static next = 1;
  constructor() { this.id = Ticket.next++; }
  static issued() { return Ticket.next - 1; }
}
const a = new Ticket();
const b = new Ticket();
console.log(a.id);
console.log(b.id);
console.log(Ticket.issued());
""", "One shared `next` hands out 1, then 2. `issued` reads that same field.")
u.choice("A `static` field is stored…",
         ["separately inside every object", "once on the class, shared by every object", "only inside the constructor", "on the first object, then copied"], 1,
         "Change `Ticket.next` and every object sees the new value.")
u.blank("Count calls on the class.", """
class Counter {
  ___ n = 0;
  static add() { Counter.n += 1; }
}
Counter.add();
Counter.add();
console.log(Counter.___);
""", [["static"], ["n"]], "`static` puts `n` on `Counter`, so both calls update the same number.")
u.order("Arrange the lines so the program prints `2`.", """
class Counter { static n = 0; }
for (let i = 0; i < 2; i++) Counter.n += 1;
console.log(Counter.n);
""", "Bump the shared field twice, then print it.")
u.fix("The second ticket should be id `2`. Both print `1`.", """
class Ticket {
  constructor() {
    this.next = 1;
    this.id = this.next++;
  }
}
const a = new Ticket();
const b = new Ticket();
console.log(a.id);
console.log(b.id);
""", """
class Ticket {
  static next = 1;
  constructor() { this.id = Ticket.next++; }
}
const a = new Ticket();
const b = new Ticket();
console.log(a.id);
console.log(b.id);
""", "A field set in the constructor belongs to that object and starts over at 1. `static next` is shared.")
u.write("Read `n` and create `n` tickets from a class with a `static` counter. Print how many were issued. Input `3` prints `3`.", READ + """
class Ticket {
  constructor() {}
}
const n = Number(lines[0]);
for (let i = 0; i < n; i++) new Ticket();
console.log(0);
""", READ + """
class Ticket {
  static issued = 0;
  constructor() { Ticket.issued += 1; }
}
const n = Number(lines[0]);
for (let i = 0; i < n; i++) new Ticket();
console.log(Ticket.issued);
""", ["3\n", "0\n", "1\n", "10\n"], "The counter has to be `static`. A field on `this` would count only that one ticket.")

# 5 ---------------------------------------------------------------- inheritance
u = oop_unit(L, "Inheritance", """
`class Dog extends Animal` means a dog starts with Animal's methods. The child constructor must call `super(...)` before it uses `this`.

```js
class Dog extends Animal {
  constructor(name) { super(name); }
}
```

Building a `Dog` runs Animal's constructor first, then the rest of Dog's. Leave `super` out and the constructor throws.
""")
u.predict("""
class A {
  constructor() { console.log("A"); }
}
class B extends A {
  constructor() { super(); console.log("B"); }
}
class C extends B {
  constructor() { super(); console.log("C"); }
}
new C();
""", "`super()` walks one step up. C calls B, B calls A, then the logs run A, B, C.")
u.choice("A dog is a kind of animal. Which declaration says that?",
         ["class Dog extends Animal", "class Animal extends Dog", "class Dog { Animal() {} }", "const Dog = new Animal();"], 0,
         "`extends` points at the parent. The child is the more specific type.")
u.blank("Pass the name up to Animal.", """
class Animal {
  constructor(name) { this.name = name; }
}
class Dog ___ Animal {
  constructor(name) { ___(name); }
}
console.log(new Dog("Rex").name);
""", [["extends"], ["super"]], "`extends` names the parent. `super(name)` runs its constructor.")
u.order("Arrange the lines so the program prints `Animal` and then `Dog`.", """
class Animal { constructor() { console.log("Animal"); } }
class Dog extends Animal { constructor() { super(); console.log("Dog"); } }
new Dog();
""", "`super()` runs the parent constructor before the child logs.")
u.fix("This should print `A` then `B`. It throws instead.", """
class A {
  constructor() { console.log("A"); }
}
class B extends A {
  constructor() { console.log("B"); }
}
new B();
""", """
class A {
  constructor() { console.log("A"); }
}
class B extends A {
  constructor() {
    super();
    console.log("B");
  }
}
new B();
""", "A child constructor has to call `super()` before it does anything else. The parent runs first.")
u.write("Read a name. Build a `Dog` that `extends` an animal with that name, and print `dog ` plus the name. Input `Rex` prints `dog Rex`.", READ + """
class Animal {
  constructor(name) { this.name = name; }
}
class Dog extends Animal {
  constructor(name) { super(name); }
}
console.log(new Dog(lines[0].trim()).name);
""", READ + """
class Animal {
  constructor(name) { this.name = name; }
}
class Dog extends Animal {
  constructor(name) { super(name); }
  tag() { return "dog " + this.name; }
}
console.log(new Dog(lines[0].trim()).tag());
""", ["Rex\n", "A\n", "Milo\n"], "`super(name)` stores the name. `tag` adds the word `dog`.")

# 6 ---------------------------------------------------------------- overriding
u = oop_unit(L, "Overriding methods", """
Define the same method on the child and the child's version wins. Call `super.sound()` when the child wants the parent text and then its own.

```js
class Dog extends Animal {
  sound() { return super.sound() + " woof"; }
}
```

A list can mix children. The call uses the object in that slot. A mismatched name does not override anything, and nothing warns you.
""")
u.predict("""
class Animal {
  sound() { return "..."; }
}
class Dog extends Animal {
  sound() { return super.sound() + " woof"; }
}
class Cat extends Animal {
  sound() { return "meow"; }
}
const pets = [new Dog(), new Cat(), new Dog()];
for (const p of pets) console.log(p.sound());
""", "`super.sound()` runs the parent method. Cat replaces `sound` completely. The list holds both.")
u.choice("The list holds animals, and one slot is a Dog. Which `sound` runs for that slot?",
         ["Animal.sound only, because the list is mixed", "Dog.sound, because that object is a Dog", "Both, and the outputs are added by the loop", "It throws"], 1,
         "The call looks up the method on the object. Dog's `sound` is the one that runs.")
u.blank("Add the parent text in front of `woof`.", """
class Animal {
  sound() { return "..."; }
}
class Dog extends Animal {
  sound() { return ___.sound() + " woof"; }
}
console.log(new Dog().sound());
""", [["super"]], "`super.sound()` calls Animal's method, then the string adds ` woof`.")
u.order("Arrange the lines so the program prints `... woof`.", """
class Animal { sound() { return "..."; } }
class Dog extends Animal { sound() { return super.sound() + " woof"; } }
console.log(new Dog().sound());
""", "The child calls `super.sound()` and appends its own word.")
u.fix("`a.sound()` should print `woof`. It prints `...`.", """
class Animal {
  sound() { return "..."; }
}
class Dog extends Animal {
  Sound() { return "woof"; }
}
const a = new Dog();
console.log(a.sound());
""", """
class Animal {
  sound() { return "..."; }
}
class Dog extends Animal {
  sound() { return "woof"; }
}
const a = new Dog();
console.log(a.sound());
""", "`Sound` and `sound` are different names, so the parent method is still the one that runs.")
u.write("""
Read `n`, then `n` words, each `dog` or `cat`. Print `woof` or `meow` by calling `sound()` on that object.
Input `2` / `dog` / `cat` prints `woof` then `meow`.
""", READ + """
class Animal {
  sound() { return "..."; }
}
const n = Number(lines[0]);
for (let i = 0; i < n; i++) console.log("...");
""", READ + """
class Animal {
  sound() { return "..."; }
}
class Dog extends Animal {
  sound() { return "woof"; }
}
class Cat extends Animal {
  sound() { return "meow"; }
}
const n = Number(lines[0]);
for (let i = 0; i < n; i++) {
  const pet = lines[i + 1].trim() === "dog" ? new Dog() : new Cat();
  console.log(pet.sound());
}
""", ["2\ndog\ncat\n", "1\ndog\n", "3\ncat\ncat\ndog\n"], "Build the matching object and call `sound()`. The method on the object is the one that runs.")

# 7 ---------------------------------------------------------------- duck typing
u = oop_unit(L, "Duck typing", """
There is no `interface` keyword to implement. If a function calls `shape.area()`, any object with `area` will do. That is duck typing: the methods matter, not a parent class.

A base class can still demand a method by throwing:

```js
class Shape {
  area() { throw new Error("must be implemented"); }
}
```

A child replaces `area`. Call the base version and the error fires.
""")
u.predict("""
class Shape {
  area() { throw new Error("must be implemented"); }
}
class Square extends Shape {
  constructor(side) { super(); this.side = side; }
  area() { return this.side * this.side; }
}
function areaOf(shape) { return shape.area(); }
const duck = { area() { return 7; } };
console.log(areaOf(new Square(3)));
try {
  console.log(new Shape().area());
} catch (e) {
  console.log(e.message);
}
console.log(areaOf(duck));
""", "`areaOf` only needs an `area` method, so the plain object works. The base `Shape` throws, and the message is caught.")
u.choice("`areaOf` only calls `shape.area()`. Which values work?",
         ["Only objects created with `new Square`", "A Square, and any object that has an area method", "Only Shape itself", "Any value, even a number"], 1,
         "Duck typing checks for the method at the call. A class is not required.")
u.blank("Refuse to run the unfinished method.", """
class Shape {
  area() { ___ new Error("must be implemented"); }
}
class Square extends Shape {
  constructor(side) { super(); this.side = side; }
  area() { return this.side * this.side; }
}
console.log(new Square(4).area());
""", [["throw"]], "`throw` stops the base method. Square replaces `area`, so this call never throws.")
u.order("Arrange the lines so the program prints `16`.", """
class Shape { area() { throw new Error("must be implemented"); } }
class Square extends Shape { constructor(side) { super(); this.side = side; } area() { return this.side * this.side; } }
console.log(new Square(4).area());
""", "The child replaces `area`. `super()` in the constructor still runs the parent constructor.")
u.fix("`new Square(3).area()` should print `9`. It throws `must be implemented`.", """
class Shape {
  area() { throw new Error("must be implemented"); }
}
class Square extends Shape {
  constructor(side) { super(); this.side = side; }
}
console.log(new Square(3).area());
""", """
class Shape {
  area() { throw new Error("must be implemented"); }
}
class Square extends Shape {
  constructor(side) { super(); this.side = side; }
  area() { return this.side * this.side; }
}
console.log(new Square(3).area());
""", "Without its own `area`, Square uses the base method, and that method throws. Replace it.")
u.write("Read a side length and print the area of a `Square` that replaces a base `area` method. Input `4` prints `16`.", READ + """
class Shape {
  area() { throw new Error("must be implemented"); }
}
class Square extends Shape {
  constructor(side) { super(); this.side = side; }
  area() { return 0; }
}
console.log(new Square(Number(lines[0])).area());
""", READ + """
class Shape {
  area() { throw new Error("must be implemented"); }
}
class Square extends Shape {
  constructor(side) { super(); this.side = side; }
  area() { return this.side * this.side; }
}
console.log(new Square(Number(lines[0])).area());
""", ["4\n", "1\n", "0\n", "5\n"], "`area` returns `this.side * this.side` instead of throwing.")

# 8 ---------------------------------------------------------------- toString and ===
u = oop_unit(L, "Printing and identity", """
`console.log` on an object shows its fields. Turning the object into a string calls `toString()`. The default result is `[object Object]`.

`===` compares references. Two objects with the same fields are still not `===`. Compare the fields yourself, or write a method that does.

```js
toString() { return this.x + "," + this.y; }
```
""")
u.predict("""
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
  toString() { return this.x + "," + this.y; }
}
const a = new Point(1, 2);
const b = new Point(1, 2);
console.log(a.toString());
console.log({}.toString());
console.log(a === b);
console.log(a === a);
""", "`toString` builds the text. `{}` still has the default. `===` is false for two objects and true for a value and itself.")
u.choice("Two different Point objects both hold `1, 2`. What is `a === b`?",
         ["true, because the fields match", "false, because they are two objects", "true after toString runs", "It throws"], 1,
         "`===` does not look at the fields. It asks whether both names are the same object.")
u.blank("Teach string conversion to show the coordinates.", """
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
  ___() { return this.x + "," + this.y; }
}
console.log(String(new Point(3, 4)));
""", [["toString"]], "`String(obj)` calls `toString`. Name the method that, or you still get `[object Object]`.")
u.order("Arrange the lines so the program prints `true`.", """
class Point { constructor(x, y) { this.x = x; this.y = y; } same(other) { return this.x === other.x && this.y === other.y; } }
const a = new Point(1, 2);
const b = new Point(1, 2);
console.log(a.same(b));
""", "`===` on the objects would be false. Comparing the numbers is a method on the point.")
u.fix("The coordinates match. The program should print `true`.", """
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
}
const a = new Point(1, 2);
const b = new Point(1, 2);
console.log(a === b);
""", """
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
  same(other) { return this.x === other.x && this.y === other.y; }
}
const a = new Point(1, 2);
const b = new Point(1, 2);
console.log(a.same(b));
""", "`===` compares references, so two points are not equal that way. Compare `x` and `y`.")
u.write("Read four integers `x1 y1 x2 y2` from one line. Build two points and print `true` or `false` by comparing their fields. Input `1 2 1 2` prints `true`.", READ + """
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
}
const [x1, y1, x2, y2] = lines[0].split(" ").map(Number);
const a = new Point(x1, y1);
const b = new Point(x2, y2);
console.log(false);
""", READ + """
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
  same(other) { return this.x === other.x && this.y === other.y; }
}
const [x1, y1, x2, y2] = lines[0].split(" ").map(Number);
const a = new Point(x1, y1);
const b = new Point(x2, y2);
console.log(a.same(b));
""", ["1 2 1 2\n", "1 2 1 3\n", "0 0 0 0\n", "-1 4 -1 4\n"], "Compare the fields. `===` on the two objects stays false.")

# 9 ---------------------------------------------------------------- composition and callbacks
u = oop_unit(L, "Composition", """
A car is not a kind of engine. A car **has** an engine, stored on `this`.

```js
class Car {
  constructor(model, engine) {
    this.model = model;
    this.engine = engine;
  }
}
```

Use `extends` only when the new type really is the parent. One more trap: `const show = engine.status` pulls the function off the object. Call `show()` and `this` is gone. An arrow wraps the call, `() => engine.status()`, or `engine.status.bind(engine)` sticks `this` back on.
""")
u.predict("""
class Engine {
  constructor(hp) { this.hp = hp; }
  status() { return this.hp + "hp"; }
}
class Car {
  constructor(model, engine) { this.model = model; this.engine = engine; }
  spec() { return this.model + " " + this.engine.status(); }
}
const c = new Car("Civic", new Engine(150));
console.log(c.spec());
""", "`spec` asks the engine object stored on the car.")
u.choice("A car is built around an engine it uses. Which shape fits?",
         ["class Car extends Engine", "Car stores an Engine on this", "class Engine extends Car", "One class, and a boolean that switches job"], 1,
         "Has-a is a field. `extends` means the child is that kind of thing.")
u.blank("Read the horsepower from the engine the car holds.", """
class Engine {
  constructor(hp) { this.hp = hp; }
  status() { return this.hp + "hp"; }
}
class Car {
  constructor(model, engine) { this.model = model; this.engine = engine; }
  spec() { return this.model + " " + this.___.status(); }
}
console.log(new Car("Civic", new Engine(150)).spec());
""", [["engine"]], "The car keeps an engine and calls `status` on that field.")
u.order("Arrange the lines so the program prints `Civic 150hp`.", """
class Engine { constructor(hp) { this.hp = hp; } status() { return this.hp + "hp"; } }
class Car { constructor(model, engine) { this.model = model; this.engine = engine; } spec() { return this.model + " " + this.engine.status(); } }
console.log(new Car("Civic", new Engine(150)).spec());
""", "Build the engine, hand it to the car, then ask the car for its spec.")
u.fix("`show()` should print `150hp`. Pulling the method off the object throws.", """
class Engine {
  constructor(hp) { this.hp = hp; }
  status() { return this.hp + "hp"; }
}
const engine = new Engine(150);
const show = engine.status;
console.log(show());
""", """
class Engine {
  constructor(hp) { this.hp = hp; }
  status() { return this.hp + "hp"; }
}
const engine = new Engine(150);
const show = () => engine.status();
console.log(show());
""", "A bare `engine.status` does not keep `this`. An arrow calls it as a method. `engine.status.bind(engine)` does too.", )
u.write("Read a model and a horsepower, one per line. Build a `Car` that holds an `Engine`, and print `model hp` like `Civic 150hp`.", READ + """
class Engine {
  constructor(hp) { this.hp = hp; }
}
class Car {
  constructor(model, engine) { this.model = model; this.engine = engine; }
  spec() { return this.model; }
}
const c = new Car(lines[0].trim(), new Engine(Number(lines[1])));
console.log(c.spec());
""", READ + """
class Engine {
  constructor(hp) { this.hp = hp; }
}
class Car {
  constructor(model, engine) { this.model = model; this.engine = engine; }
  spec() { return this.model + " " + this.engine.hp + "hp"; }
}
const c = new Car(lines[0].trim(), new Engine(Number(lines[1])));
console.log(c.spec());
""", ["Civic\n150\n", "Van\n90\n", "Bus\n0\n"], "Store the engine on the car and read `this.engine.hp` in `spec`.")

# 10 --------------------------------------------------------------- bank account
u = oop_unit(L, "Bank account", """
Put the rules on the object. A `Bank` starts at 0, keeps the number in `#balance`, and is the only code that changes it.

- `deposit N` adds `N` when `N > 0` and prints the balance; otherwise it prints `Invalid`
- `withdraw N` prints `Invalid` when `N <= 0`, `Insufficient funds` when `N` is too big, otherwise subtracts and prints the balance
- `balance` prints the balance

```js
class Bank {
  #balance = 0;
  deposit(n) { /* check, then update */ }
}
```
""")
u.predict("""
class Bank {
  #balance = 0;
  deposit(n) {
    if (n <= 0) { console.log("Invalid"); return; }
    this.#balance += n;
    console.log(this.#balance);
  }
  withdraw(n) {
    if (n <= 0) { console.log("Invalid"); return; }
    if (n > this.#balance) { console.log("Insufficient funds"); return; }
    this.#balance -= n;
    console.log(this.#balance);
  }
}
const b = new Bank();
b.deposit(50);
b.withdraw(80);
b.withdraw(20);
""", "50 is stored. 80 is more than 50, so the field stays 50. 20 then leaves 30.")
u.choice("Which check belongs in `withdraw` before it subtracts?",
         ["this.#balance = n", "if (n > this.#balance) { console.log(\"Insufficient funds\"); return; }", "this.#balance = 0", "n = this.#balance"], 1,
         "Return before changing the field. A refused withdrawal leaves the balance as it was.")
u.blank("Reject a non-positive deposit.", """
class Bank {
  #balance = 0;
  deposit(n) {
    if (n ___ 0) { console.log("Invalid"); return; }
    this.#balance += n;
    console.log(this.#balance);
  }
}
const b = new Bank();
b.deposit(0);
b.deposit(15);
""", [["<="]], "`<= 0` catches 0 and negatives. A positive amount is added and printed.")
u.order("Arrange the lines so the program prints `Insufficient funds`.", """
class Bank { #balance = 0; withdraw(n) { if (n > this.#balance) { console.log("Insufficient funds"); return; } this.#balance -= n; console.log(this.#balance); } }
const b = new Bank();
b.withdraw(80);
""", "A new account is at 0, so 80 is too much.")
u.fix("""
`deposit` must reject non-positive amounts, and `withdraw` must refuse to go below 0.

- `withdraw 80` prints `Insufficient funds`
- `deposit 50` then `withdraw 80` prints `50` then `Insufficient funds`
- `deposit -4` prints `Invalid`
- `deposit 20`, `withdraw 20`, `withdraw 5` prints `20`, `0`, `Insufficient funds`
""", READ + """
class Bank {
  #balance = 0;
  deposit(n) { this.#balance += n; console.log(this.#balance); }
  withdraw(n) {
    if (n <= 0) { console.log("Invalid"); return; }
    this.#balance -= n;
    console.log(this.#balance);
  }
  show() { console.log(this.#balance); }
}
const bank = new Bank();
for (const line of lines) {
  const parts = line.trim().split(/\\s+/);
  if (!parts[0]) continue;
  const cmd = parts[0];
  const n = Number(parts[1]);
  if (cmd === "deposit") bank.deposit(n);
  else if (cmd === "withdraw") bank.withdraw(n);
  else if (cmd === "balance") bank.show();
}
""", READ + """
class Bank {
  #balance = 0;
  deposit(n) {
    if (n <= 0) { console.log("Invalid"); return; }
    this.#balance += n;
    console.log(this.#balance);
  }
  withdraw(n) {
    if (n <= 0) { console.log("Invalid"); return; }
    if (n > this.#balance) { console.log("Insufficient funds"); return; }
    this.#balance -= n;
    console.log(this.#balance);
  }
  show() { console.log(this.#balance); }
}
const bank = new Bank();
for (const line of lines) {
  const parts = line.trim().split(/\\s+/);
  if (!parts[0]) continue;
  const cmd = parts[0];
  const n = Number(parts[1]);
  if (cmd === "deposit") bank.deposit(n);
  else if (cmd === "withdraw") bank.withdraw(n);
  else if (cmd === "balance") bank.show();
}
""", "Check the amount before you change `#balance`. A rejected command leaves the field as it was.",
   tests=["withdraw 80\n", "deposit 50\nwithdraw 80\n", "deposit -4\n", "deposit 20\nwithdraw 20\nwithdraw 5\n"])
u.write("""
Read commands until the input ends. Keep the balance in a private field on a `Bank` that starts at 0.

- `deposit N` — if `N > 0`, add it and print the balance; otherwise print `Invalid`
- `withdraw N` — if `N <= 0`, print `Invalid`; if `N` is greater than the balance, print `Insufficient funds`; otherwise subtract and print the balance
- `balance` — print the balance
""", READ + """
class Bank {
  #balance = 0;
  deposit(n) {}
  withdraw(n) {}
  show() {}
}
const bank = new Bank();
for (const line of lines) {
  const parts = line.trim().split(/\\s+/);
  if (!parts[0]) continue;
  const cmd = parts[0];
  const n = Number(parts[1]);
  if (cmd === "deposit") bank.deposit(n);
  else if (cmd === "withdraw") bank.withdraw(n);
  else if (cmd === "balance") bank.show();
}
""", READ + """
class Bank {
  #balance = 0;
  deposit(n) {
    if (n <= 0) { console.log("Invalid"); return; }
    this.#balance += n;
    console.log(this.#balance);
  }
  withdraw(n) {
    if (n <= 0) { console.log("Invalid"); return; }
    if (n > this.#balance) { console.log("Insufficient funds"); return; }
    this.#balance -= n;
    console.log(this.#balance);
  }
  show() { console.log(this.#balance); }
}
const bank = new Bank();
for (const line of lines) {
  const parts = line.trim().split(/\\s+/);
  if (!parts[0]) continue;
  const cmd = parts[0];
  const n = Number(parts[1]);
  if (cmd === "deposit") bank.deposit(n);
  else if (cmd === "withdraw") bank.withdraw(n);
  else if (cmd === "balance") bank.show();
}
""", ["deposit 50\nwithdraw 20\nbalance\n", "withdraw 80\n", "deposit 40\nwithdraw 40\nwithdraw 1\n", "deposit 0\ndeposit -3\ndeposit 15\n", "balance\n"],
   "The object owns the number. Each command either prints a refusal or the new balance.")
