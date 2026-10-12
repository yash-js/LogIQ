from bc import oop_unit

L = "python"

# 1 ---------------------------------------------------------------- classes and objects
u = oop_unit(L, "Classes and objects", """
A class is a blueprint. An object is one built thing. You add fields by assigning them, and methods take the object as `self`.

```python
class Dog:
    def bark(self):
        print(self.name + " says woof")

rex = Dog()
rex.name = "Rex"
```

`milo = Dog()` is a second object. Setting `rex.name` does not change `milo.name`.
""")
u.predict("""
class Counter:
    def ready(self):
        self.n = 0
    def add(self):
        self.n += 1

a = Counter()
b = Counter()
a.ready()
b.ready()
a.add()
a.add()
b.add()
print(a.n)
print(b.n)
""", "Each call of `Counter()` is its own object. `a.n` and `b.n` are separate.")
u.choice("What does `Dog()` do?",
         ["It renames the class", "It builds one Dog object", "It runs only the methods", "It copies every existing dog"], 1,
         "Calling the class builds an object. The class stays the blueprint.")
u.blank("Two dogs, two names.", """
class Dog:
    def label(self):
        print(___.name)

a = Dog()
b = ___()
a.name = "Rex"
b.name = "Milo"
a.label()
b.label()
""", [["self"], ["Dog"]], "`self` is the object the method was called on. `Dog()` builds the second one.")
u.order("Arrange the lines so the program prints `Rex`.", """
class Dog:
    def label(self):
        print(self.name)
d = Dog()
d.name = "Rex"
d.label()
""", "Build the object, set its field, then call the method.", )
u.fix("Both lines should be different names. The second call crashes.", """
class Dog:
    def label(self):
        print(self.name)

a = Dog()
b = a
a.name = "Rex"
b.name = "Milo"
a.label()
c.label()
""", """
class Dog:
    def label(self):
        print(self.name)

a = Dog()
b = Dog()
a.name = "Rex"
b.name = "Milo"
a.label()
b.label()
""", "`b = a` is one object with two names. `b = Dog()` builds another. `c` was never created.")
u.write("Read a name and an age. Store them on a `Person` and print `name is age`. Input `Ana` then `21` prints `Ana is 21`.", """
class Person:
    def line(self):
        print(self.name)

p = Person()
p.name = input()
p.age = int(input())
p.line()
""", """
class Person:
    def line(self):
        print(self.name + " is " + str(self.age))

p = Person()
p.name = input()
p.age = int(input())
p.line()
""", ["Ana\n21\n", "Bo\n0\n", "Ravi\n7\n"], "Keep both values on the object, and build the sentence from `self`.")

# 2 ---------------------------------------------------------------- __init__ and self
u = oop_unit(L, "__init__ and self", """
`__init__` runs when you call the class. The first parameter is the new object. Everyone names it `self`.

```python
class Dog:
    def __init__(self, name):
        self.name = name
```

`rex = Dog("Rex")` builds the object and passes it in as `self`. Forget `self` on a method and the call crashes: the object is passed anyway. `name = name` never creates a field.
""")
u.predict("""
class Dog:
    def __init__(self, name):
        self.name = name
    def label(self):
        print(self.name)

Dog("Rex").label()
Dog("Milo").label()
""", "Each call runs `__init__` for that object and stores the name on it.")
u.choice("Calling `c.add()` when `add` is defined `def add():` raises…",
         ["nothing, self is optional", "TypeError: the object is passed and the method doesn't accept it", "the method runs with self set to None", "a syntax error at the call"], 1,
         "Instance calls always pass the object as the first argument. The definition has to accept it.")
u.blank("Store the parameter on the object.", """
class Point:
    def __init__(self, x):
        ___.x = x
    def show(self):
        print(___.x)

Point(4).show()
""", [["self"], ["self"]], "`self.x` is the field. The bare `x` is only the parameter.")
u.order("Arrange the lines so the program prints `4`.", """
class Point:
    def __init__(self, x):
        self.x = x
p = Point(4)
print(p.x)
""", "`__init__` stores `x` before the print reads it.")
u.fix("`show` should print `4`. It crashes with AttributeError.", """
class Point:
    def __init__(self, x):
        x = x
    def show(self):
        print(self.x)

Point(4).show()
""", """
class Point:
    def __init__(self, x):
        self.x = x
    def show(self):
        print(self.x)

Point(4).show()
""", "`x = x` writes the parameter onto itself. `self.x = x` creates the field.")
u.write("Read width and height. Store them in `__init__` and print the area. Input `3 4` prints `12`.", """
class Box:
    def __init__(self, w, h):
        w = w
        h = h
    def area(self):
        return self.w * self.h

w, h = map(int, input().split())
print(Box(w, h).area())
""", """
class Box:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def area(self):
        return self.w * self.h

w, h = map(int, input().split())
print(Box(w, h).area())
""", ["3 4\n", "0 5\n", "2 2\n", "-3 4\n"], "`self.w` and `self.h` keep the numbers after `__init__` returns.")

# 3 ---------------------------------------------------------------- properties
u = oop_unit(L, "Properties", """
A single leading underscore, `_balance`, is a convention: other code should leave it alone. Nothing stops a caller from touching it.

`@property` is the checked door. Reading `account.balance` calls the getter. Assigning `account.balance = n` calls the setter, which can refuse a bad value.

```python
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
```
""")
u.predict("""
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, n):
        if n >= 0:
            self._balance = n

a = Account()
a.balance = 20
a.balance = -3
print(a.balance)
""", "20 is stored. The setter ignores -3, so the property still reads 20.")
u.choice("What does the leading underscore in `_balance` mean?",
         ["Other modules cannot see the attribute", "A convention: use the property, not this attribute", "The attribute is shared by every object", "Reading it raises AttributeError"], 1,
         "The underscore is a warning to people. `@property` is what actually checks the value.")
u.blank("Wire the setter to the same name as the property.", """
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
    @___.setter
    def balance(self, n):
        if n >= 0:
            self._balance = n

a = Account()
a.balance = 8
print(a.___)
""", [["balance"], ["balance"]], "The decorator is `@balance.setter`. Callers still write `a.balance`.")
u.order("Arrange the lines so the program prints `8`.", """
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
a = Account()
a._balance = 8
print(a.balance)
""", "The getter reads `_balance`. The assignment has to happen before the print.")
u.fix("After setting 20 and then -3, the balance should still be `20`.", """
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, n):
        self._balance = n

a = Account()
a.balance = 20
a.balance = -3
print(a.balance)
""", """
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, n):
        if n >= 0:
            self._balance = n

a = Account()
a.balance = 20
a.balance = -3
print(a.balance)
""", "The setter is the place for the rule. Skip the assignment when `n` is negative.")
u.write("""
Read `n`, then `n` amounts. Add an amount only when it is greater than 0, using a property setter, and print the balance.
Input `3` / `10` / `-4` / `5` prints `15`.
""", """
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, n):
        self._balance = n

a = Account()
n = int(input())
for _ in range(n):
    a.balance += int(input())
print(a.balance)
""", """
class Account:
    def __init__(self):
        self._balance = 0
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, n):
        if n >= 0:
            self._balance = n

a = Account()
n = int(input())
for _ in range(n):
    amount = int(input())
    if amount > 0:
        a.balance += amount
print(a.balance)
""", ["3\n10\n-4\n5\n", "1\n0\n", "2\n-8\n-1\n", "4\n20\n0\n7\n3\n"], "Ignore amounts that are not positive. Print the property at the end.")

# 4 ---------------------------------------------------------------- class data
u = oop_unit(L, "Class data", """
Assign a value on the class and every object sees that same value. Assign on `self` and only that object changes.

```python
class Counter:
    n = 0
    def __init__(self):
        Counter.n += 1
    @classmethod
    def how_many(cls):
        return cls.n
```

`@classmethod` receives the class as `cls`. `@staticmethod` receives neither the object nor the class. A list stored on the class is one list: `append` from any object changes it for all of them.
""")
u.predict("""
class Team:
    members = []
    def add(self, name):
        self.members.append(name)

a = Team()
b = Team()
a.add("Ana")
b.add("Bo")
print(" ".join(a.members))
print(" ".join(b.members))
""", "`members` lives on the class, so both objects append to one list.")
u.choice("A method that uses neither the object nor the class should be a…",
         ["staticmethod", "classmethod", "property", "abstractmethod"], 0,
         "`@staticmethod` takes no `self` and no `cls`. `@classmethod` is for when you need the class.")
u.blank("Count objects from the class.", """
class Tally:
    n = 0
    def __init__(self):
        Tally.n += 1
    @___
    def how_many(cls):
        return cls.n

Tally()
Tally()
print(Tally.how_many())
""", [["classmethod"]], "`cls` is the class. `@classmethod` passes it in, so `how_many` can read `cls.n`.")
u.order("Arrange the lines so the program prints `pen`.", """
class Bag:
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(item)
a = Bag()
a.add("pen")
print(a.items[0])
""", "Create the list on the object inside `__init__`, then append.")
u.fix("Each team should keep its own member. The print shows both names on both teams.", """
class Team:
    members = []
    def add(self, name):
        self.members.append(name)

a = Team()
b = Team()
a.add("Ana")
b.add("Bo")
print(" ".join(a.members))
print(" ".join(b.members))
""", """
class Team:
    def __init__(self):
        self.members = []
    def add(self, name):
        self.members.append(name)

a = Team()
b = Team()
a.add("Ana")
b.add("Bo")
print(" ".join(a.members))
print(" ".join(b.members))
""", "A list on the class is shared. Build a new list on `self` inside `__init__`.")
u.write("Read `n`, then `n` names. Each name becomes a `Member`. Print how many were created, using a class attribute. Input `2` / `Ana` / `Bo` prints `2`.", """
class Member:
    total = 0
    def __init__(self, name):
        self.name = name

n = int(input())
for _ in range(n):
    Member(input())
print(0)
""", """
class Member:
    total = 0
    def __init__(self, name):
        self.name = name
        Member.total += 1

n = int(input())
for _ in range(n):
    Member(input())
print(Member.total)
""", ["2\nAna\nBo\n", "0\n", "1\nSam\n", "3\nA\nB\nC\n"], "`Member.total` is one number for the class. Bump it in `__init__`.")

# 5 ---------------------------------------------------------------- inheritance
u = oop_unit(L, "Inheritance", """
List the parent in parentheses: `class Dog(Animal)`. The child starts with the parent's methods.

`super().__init__(...)` runs the parent setup. Skip it and the parent fields are never stored. With a chain of classes, the prints run parent first, then child.

```python
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)
```
""")
u.predict("""
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        super().__init__()
        print("B")

class C(B):
    def __init__(self):
        super().__init__()
        print("C")

C()
""", "`super()` walks one step up. C calls B, B calls A, then the prints unwind A, B, C.")
u.choice("How does Dog inherit from Animal?",
         ["class Dog(Animal):", "class Dog: Animal", "Dog = Animal()", "class Animal(Dog):"], 0,
         "The parent goes in parentheses on the child class.")
u.blank("Run the parent setup before the child uses the name.", """
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name):
        ___().__init__(name)

print(Dog("Rex").name)
""", [["super"]], "`super()` finds Animal, and `__init__` stores the name.")
u.order("Arrange the lines so the program prints `Animal` then `Dog`.", """
class Animal:
    def __init__(self): print("Animal")
class Dog(Animal):
    def __init__(self):
        super().__init__()
        print("Dog")
Dog()
""", "Call `super().__init__()` before the child prints.")
u.fix("Building a C should print `A`, then `B`, then `C`. `B` never calls up.", """
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        print("B")

class C(B):
    def __init__(self):
        super().__init__()
        print("C")

C()
""", """
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        super().__init__()
        print("B")

class C(B):
    def __init__(self):
        super().__init__()
        print("C")

C()
""", "Each class that writes `__init__` has to call `super().__init__()`, or the chain stops there.")
u.write("Read a name. Build a `Dog` whose parent stores that name, and print `dog ` plus the name. Input `Rex` prints `dog Rex`.", """
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

print(Dog(input()).name)
""", """
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)
    def tag(self):
        return "dog " + self.name

print(Dog(input()).tag())
""", ["Rex\n", "A\n", "Milo\n"], "`super().__init__(name)` stores the name. `tag` adds the word `dog`.")

# 6 ---------------------------------------------------------------- overriding
u = oop_unit(L, "Overriding methods", """
Define the same method name on the child and the child's version wins. A list can hold a mix of children; the call uses the object you actually put in.

```python
class Dog(Animal):
    def sound(self):
        return "woof"
```

Names are case-sensitive. `Sound` does not replace `sound`, and nothing warns you.
""")
u.predict("""
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "woof"

class Cat(Animal):
    def sound(self):
        return "meow"

pets = [Dog(), Cat(), Dog()]
for p in pets:
    print(p.sound())
""", "The list has no single type. `p.sound()` runs the method on that object.")
u.choice("What decides which `sound` runs?",
         ["The class written on the list", "The class of the object in that slot", "Whichever class was defined first", "The name of the variable `p`"], 1,
         "The call looks up the method on the object. Dog and Cat each supply their own.")
u.blank("Replace the parent method.", """
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def ___(self):
        return "woof"

print(Dog().sound())
""", [["sound"]], "The names match, so `Dog().sound()` finds the child's method first.")
u.order("Arrange the lines so the program prints `woof`.", """
class Animal:
    def sound(self): return "..."
class Dog(Animal):
    def sound(self):
        return "woof"
print(Dog().sound())
""", "The child defines `sound`, then the call uses a Dog.")
u.fix("`a.sound()` should print `woof`. It prints `...`.", """
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def Sound(self):
        return "woof"

a = Dog()
print(a.sound())
""", """
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "woof"

a = Dog()
print(a.sound())
""", "`Sound` and `sound` are different names, so the parent method is still the one that runs.")
u.write("""
Read `n`, then `n` words, each `dog` or `cat`. Print `woof` or `meow` from a method on that object.
Input `2` / `dog` / `cat` prints `woof` then `meow`.
""", """
class Animal:
    def sound(self):
        return "..."

n = int(input())
for _ in range(n):
    input()
    print("...")
""", """
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "woof"

class Cat(Animal):
    def sound(self):
        return "meow"

n = int(input())
for _ in range(n):
    pet = Dog() if input() == "dog" else Cat()
    print(pet.sound())
""", ["2\ndog\ncat\n", "1\ndog\n", "3\ncat\ncat\ndog\n"], "Build the matching object and call `sound()`. The parent version is the fallback.")

# 7 ---------------------------------------------------------------- abstract and duck typing
u = oop_unit(L, "Abstract classes", """
`abc.ABC` plus `@abstractmethod` means the class is unfinished. Calling it raises `TypeError` until a child supplies the method.

A lot of code never uses that machinery. If the function only calls `thing.quack()`, any object with `quack` will do. That is duck typing: the methods matter, not the parent class.

```python
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```
""")
u.predict("""
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

try:
    Shape()
    print("made one")
except TypeError:
    print("TypeError")

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side

print(Square(3).area())
""", "Calling `Shape()` raises TypeError. `Square` fills in `area`, so it can be built.")
u.choice("A function only calls `thing.quack()`. Which callers are fine?",
         ["Only objects whose class lists Duck as a parent", "A Duck, and a Person that also defines quack", "Any object, even with no quack method", "Only Duck, because of the class name"], 1,
         "Duck typing looks for the method. The class name is not checked.",
         code="def speak(thing):\n    return thing.quack()")
u.blank("Mark the method that children must supply.", """
from abc import ABC, abstractmethod

class Shape(ABC):
    @___
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side

print(Square(4).area())
""", [["abstractmethod"]], "Without the method on the child, building a Square would raise TypeError.")
u.order("Arrange the lines so the program prints `16`.", """
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self): pass
class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side
print(Square(4).area())
""", "Import abc, declare the method, fill it in, then call it.")
u.fix("`Square(3).area()` should print `9`. Building the square crashes.", """
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side

print(Square(3).area())
""", """
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side

print(Square(3).area())
""", "A child of an ABC still has abstract methods until it defines them. `area` has to return `side * side`.")
u.write("Read a side length and print the area of a `Square` that implements an abstract `area`. Input `4` prints `16`.", """
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return 0

print(Square(int(input())).area())
""", """
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side

print(Square(int(input())).area())
""", ["4\n", "1\n", "0\n", "5\n"], "`area` returns `self.side * self.side`.")

# 8 ---------------------------------------------------------------- str, repr, eq
u = oop_unit(L, "Printing and equality", """
`print(obj)` uses `__str__`. The prompt and containers use `__repr__`, which should be a clearer description.

`==` calls `__eq__` when you define it. `is` does not: it asks whether both names point at the same object.

```python
def __eq__(self, other):
    return isinstance(other, Point) and self.x == other.x and self.y == other.y
```
""")
u.predict("""
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

a = Point(1, 2)
b = Point(1, 2)
print(a)
print(repr(a))
print(a is b)
print(a == b)
""", "`print` uses `__str__`. `repr` uses `__repr__`. `is` is false for two objects; `==` uses `__eq__`.")
u.choice("What is the difference between `is` and `==` here?",
         ["`is` checks the fields, `==` checks identity", "`is` checks identity, `==` calls `__eq__` when it exists", "They always give the same answer", "`is` is only for numbers"], 1,
         "Two points with the same numbers are `==` and still not `is`.")
u.blank("Make `print` show the coordinates.", """
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def ___(self):
        return f"({self.x}, {self.y})"

print(Point(3, 4))
""", [["__str__"]], "`print` looks for `__str__`. `__repr__` is the other one, used by `repr()`.")
u.order("Arrange the lines so the program prints `True`.", """
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
a = Point(1, 2)
b = Point(1, 2)
print(a == b)
""", "`==` calls `__eq__`. `is` would be False for these two objects.")
u.fix("The points match. The program should print `True`.", """
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

a = Point(1, 2)
b = Point(1, 2)
print(a is b)
""", """
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

a = Point(1, 2)
b = Point(1, 2)
print(a == b)
""", "`is` asks if `a` and `b` are the same object. `==` uses `__eq__` and compares the numbers.")
u.write("Read four integers `x1 y1 x2 y2`. Build two points and print whether they are equal with `==`. Input `1 2 1 2` prints `True`.", """
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

nums = list(map(int, input().split()))
a = Point(nums[0], nums[1])
b = Point(nums[2], nums[3])
print(False)
""", """
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

nums = list(map(int, input().split()))
a = Point(nums[0], nums[1])
b = Point(nums[2], nums[3])
print(a == b)
""", ["1 2 1 2\n", "1 2 1 3\n", "0 0 0 0\n", "-1 4 -1 4\n"], "`__eq__` compares the fields. `is` would stay False.")

# 9 ---------------------------------------------------------------- composition
u = oop_unit(L, "Composition", """
A car is not a kind of engine. A car **has** an engine, stored on `self`.

```python
class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
```

Put a parent in parentheses only when the new type really is that parent. Otherwise keep the other object in a field and call its methods.
""")
u.predict("""
class Engine:
    def __init__(self, hp):
        self.hp = hp
    def status(self):
        return f"{self.hp}hp"

class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
    def spec(self):
        return f"{self.model} {self.engine.status()}"

print(Car("Civic", Engine(150)).spec())
""", "`spec` asks the engine object stored on the car.")
u.choice("A car is built around an engine it uses. Which shape fits?",
         ["class Car(Engine):", "Car stores an Engine on self", "class Engine(Car):", "One class with a flag that switches job"], 1,
         "Has-a is a field. Listing a parent means the child is that kind of thing.")
u.blank("Read the horsepower from the engine the car holds.", """
class Engine:
    def __init__(self, hp):
        self.hp = hp
    def status(self):
        return f"{self.hp}hp"

class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
    def spec(self):
        return self.model + " " + self.___.status()

print(Car("Civic", Engine(150)).spec())
""", [["engine"]], "The car keeps an engine and calls `status` on that field.")
u.order("Arrange the lines so the program prints `Civic 150hp`.", """
class Engine:
    def __init__(self, hp):
        self.hp = hp
class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
c = Car("Civic", Engine(150))
print(c.model, str(c.engine.hp) + "hp")
""", "Build an Engine, pass it into Car, then read the engine's horsepower.")
u.fix("`spec` should include the engine's horsepower. It crashes with AttributeError.", """
class Engine:
    def __init__(self, hp):
        self.hp = hp

class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
    def spec(self):
        return f"{self.model} {self.hp}hp"

print(Car("Civic", Engine(150)).spec())
""", """
class Engine:
    def __init__(self, hp):
        self.hp = hp

class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
    def spec(self):
        return f"{self.model} {self.engine.hp}hp"

print(Car("Civic", Engine(150)).spec())
""", "The horsepower lives on the engine. Read `self.engine.hp`, not a field the car never stored.")
u.write("Read a model and a horsepower. Build a `Car` that holds an `Engine`, and print `model hp` like `Civic 150hp`.", """
class Engine:
    def __init__(self, hp):
        self.hp = hp

class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
    def spec(self):
        return self.model

model = input()
hp = int(input())
print(Car(model, Engine(hp)).spec())
""", """
class Engine:
    def __init__(self, hp):
        self.hp = hp

class Car:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
    def spec(self):
        return self.model + " " + str(self.engine.hp) + "hp"

model = input()
hp = int(input())
print(Car(model, Engine(hp)).spec())
""", ["Civic\n150\n", "Van\n90\n", "Bus\n0\n"], "Store the engine on the car and read `self.engine.hp` in `spec`.")

# 10 --------------------------------------------------------------- bank account
u = oop_unit(L, "Bank account", """
Put the rules on the object. A `Bank` starts at 0, keeps the number on `self._balance`, and is the only code that changes it.

- `deposit N` adds `N` when `N > 0` and prints the balance; otherwise it prints `Invalid`
- `withdraw N` prints `Invalid` when `N <= 0`, `Insufficient funds` when `N` is too big, otherwise subtracts and prints the balance
- `balance` prints the balance

```python
class Bank:
    def __init__(self):
        self._balance = 0
```
""")
u.predict("""
class Bank:
    def __init__(self):
        self._balance = 0
    def deposit(self, n):
        if n <= 0:
            print("Invalid")
            return
        self._balance += n
        print(self._balance)
    def withdraw(self, n):
        if n <= 0:
            print("Invalid")
            return
        if n > self._balance:
            print("Insufficient funds")
            return
        self._balance -= n
        print(self._balance)

b = Bank()
b.deposit(50)
b.withdraw(80)
b.withdraw(20)
""", "50 is stored. 80 is more than 50, so the field stays 50. 20 then leaves 30.")
u.choice("Which check belongs in `withdraw` before it subtracts?",
         ["self._balance = n", "if n > self._balance: print a refusal and return", "self._balance = 0", "n = self._balance"], 1,
         "Return before changing the field. A refused withdrawal leaves the balance as it was.")
u.blank("Reject a non-positive deposit.", """
class Bank:
    def __init__(self):
        self._balance = 0
    def deposit(self, n):
        if n ___ 0:
            print("Invalid")
            return
        self._balance += n
        print(self._balance)

b = Bank()
b.deposit(0)
b.deposit(15)
""", [["<="]], "`<= 0` catches 0 and negatives. A positive amount is added and printed.")
u.order("Arrange the lines so the program prints `Insufficient funds`.", """
class Bank:
    def __init__(self):
        self._balance = 0
    def withdraw(self, n):
        if n > self._balance:
            print("Insufficient funds")
            return
b = Bank()
b.withdraw(80)
""", "A new account is at 0, so 80 is too much.")
u.fix("""
`deposit` must reject non-positive amounts, and `withdraw` must refuse to go below 0.

- `withdraw 80` prints `Insufficient funds`
- `deposit 50` then `withdraw 80` prints `50` then `Insufficient funds`
- `deposit -4` prints `Invalid`
- `deposit 20`, `withdraw 20`, `withdraw 5` prints `20`, `0`, `Insufficient funds`
""", """
import sys

class Bank:
    def __init__(self):
        self._balance = 0
    def deposit(self, n):
        self._balance += n
        print(self._balance)
    def withdraw(self, n):
        if n <= 0:
            print("Invalid")
            return
        self._balance -= n
        print(self._balance)
    def show(self):
        print(self._balance)

bank = Bank()
for line in sys.stdin:
    parts = line.split()
    if not parts:
        continue
    cmd = parts[0]
    if cmd == "balance":
        bank.show()
    elif cmd == "deposit":
        bank.deposit(int(parts[1]))
    elif cmd == "withdraw":
        bank.withdraw(int(parts[1]))
""", """
import sys

class Bank:
    def __init__(self):
        self._balance = 0
    def deposit(self, n):
        if n <= 0:
            print("Invalid")
            return
        self._balance += n
        print(self._balance)
    def withdraw(self, n):
        if n <= 0:
            print("Invalid")
            return
        if n > self._balance:
            print("Insufficient funds")
            return
        self._balance -= n
        print(self._balance)
    def show(self):
        print(self._balance)

bank = Bank()
for line in sys.stdin:
    parts = line.split()
    if not parts:
        continue
    cmd = parts[0]
    if cmd == "balance":
        bank.show()
    elif cmd == "deposit":
        bank.deposit(int(parts[1]))
    elif cmd == "withdraw":
        bank.withdraw(int(parts[1]))
""", "Check the amount before you change `_balance`. A rejected command leaves the field as it was.",
   tests=["withdraw 80\n", "deposit 50\nwithdraw 80\n", "deposit -4\n", "deposit 20\nwithdraw 20\nwithdraw 5\n"])
u.write("""
Read commands until the input ends. Keep the balance on a `Bank` that starts at 0.

- `deposit N` — if `N > 0`, add it and print the balance; otherwise print `Invalid`
- `withdraw N` — if `N <= 0`, print `Invalid`; if `N` is greater than the balance, print `Insufficient funds`; otherwise subtract and print the balance
- `balance` — print the balance
""", """
import sys

class Bank:
    def __init__(self):
        self._balance = 0
    def deposit(self, n):
        pass
    def withdraw(self, n):
        pass
    def show(self):
        pass

bank = Bank()
for line in sys.stdin:
    parts = line.split()
    if not parts:
        continue
    cmd = parts[0]
    if cmd == "balance":
        bank.show()
    elif cmd == "deposit":
        bank.deposit(int(parts[1]))
    elif cmd == "withdraw":
        bank.withdraw(int(parts[1]))
""", """
import sys

class Bank:
    def __init__(self):
        self._balance = 0
    def deposit(self, n):
        if n <= 0:
            print("Invalid")
            return
        self._balance += n
        print(self._balance)
    def withdraw(self, n):
        if n <= 0:
            print("Invalid")
            return
        if n > self._balance:
            print("Insufficient funds")
            return
        self._balance -= n
        print(self._balance)
    def show(self):
        print(self._balance)

bank = Bank()
for line in sys.stdin:
    parts = line.split()
    if not parts:
        continue
    cmd = parts[0]
    if cmd == "balance":
        bank.show()
    elif cmd == "deposit":
        bank.deposit(int(parts[1]))
    elif cmd == "withdraw":
        bank.withdraw(int(parts[1]))
""", ["deposit 50\nwithdraw 20\nbalance\n", "withdraw 80\n", "deposit 40\nwithdraw 40\nwithdraw 1\n", "deposit 0\ndeposit -3\ndeposit 15\n", "balance\n"],
   "The object owns the number. Each command either prints a refusal or the new balance.")
