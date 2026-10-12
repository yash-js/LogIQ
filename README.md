# LogIQ

**Learn a language, then build programming logic before you start DSA.** A desktop app with a Basecamp that teaches Java, Python or JavaScript from zero, then 145 hand-picked problems across six worlds, a short guide before each one, and a game layer (XP, levels, streaks, daily quests) that keeps you practicing. Solve in **Java, Python or JavaScript**; your code runs on your own computer.

No account, no internet needed, no server. Your progress stays on your machine.

---

## Contents

- [What's inside](#whats-inside)
- [How it plays](#how-it-plays)
- [Quick start](#quick-start)
  - [Windows](#windows)
  - [Linux](#linux)
- [Build an installer](#build-an-installer)
- [Releasing](#releasing)
- [Your data and backups](#your-data-and-backups)
- [Troubleshooting](#troubleshooting)
- [For developers](#for-developers)

---

## What's inside

| Phase | World | Topic | Problems |
| --- | --- | --- | --- |
| 0 | Basecamp | Language basics, then objects (separate track for Java, Python, JavaScript) | 10 core units + 10 OOP units per language |
| 1 | The Crossroads | Conditional logic | 20 |
| 2 | The Looping Woods | Loops, repetition and patterns | 26 |
| 3 | The Mirror Caves | Recursive thinking | 19 |
| 4 | The Iron Rails | Arrays | 32 |
| 5 | The Scroll Library | Strings | 22 |
| 6 | The Summit | Combining logic | 26 |

Every problem has its own statement, examples, hidden tests, three hints and starter code for all three languages. Each one also links to a similar LeetCode or HackerRank problem if you want more practice.

## How it plays

0. **Basecamp: learn the language.** Ten short units per language: output, variables, operators, strings, input, conditions, loops, arrays, functions and reading errors. Each unit is 6 bite-size exercises:
   - **predict the output**
   - **fill the blanks**
   - **put the lines in order**
   - **fix the bug**
   - **write it yourself**
   - multiple choice

   You get 3 lives per unit and a combo bonus for answers in a row. The answer is only revealed after two wrong tries. Already know the language? A 10-question **placement test** (8 to pass) marks Basecamp complete.

### OOP section

Below the core units, **Objects (OOP)** is a second track of ten units: classes and objects, constructors, encapsulation, static members, inheritance, overriding, abstract types, equality, composition, and a small bank-account project. The exercises are written separately for Java, Python and JavaScript.

The section is always open. Until you finish the functions unit, Basecamp shows "Recommended after Functions". OOP progress does not change the "Basecamp complete" status, the placement test, or when The Crossroads unlocks. Finishing all ten OOP units in any one language earns the **Object Thinker** badge.

1. **Study first.** Every world opens with a guide. Code examples appear in the language you picked. A 5-question check at the end (4 correct to pass) unlocks that world's problems.
2. **Solve.** You only write the `solve()` function. Reading input and printing output are already done for you.
   - **Run** checks the visible examples (`Ctrl+Enter`).
   - **Submit** runs the hidden tests too and shows the first test that failed (`Ctrl+Shift+Enter`).
3. **Hints cost XP.** Each problem has three hints, from a nudge to the approach. Every hint you open before solving takes 25% off that problem's XP.
4. **Pure challenge.** Library shortcuts are detected as you type: `sort`, `Set`/`Map`, `max`/`min`, `reverse`, `pow`, `sum`/`reduce`, `indexOf`/`includes`, `toLowerCase`, `split`/`replace`, base conversion, `BigInt`/`BigInteger`, date libraries and more. A solution that uses them is still accepted. The app then asks you to solve it again with only loops and conditions, for **+50% bonus XP**.
5. **Rewards.**
   - XP and levels.
   - A daily streak.
   - +5 XP for solving on the first submit with no hints.
   - A daily quest worth double XP.
   - Badges.
6. **Next world** opens after you solve 60% of the current one.

---

## Quick start

You need two kinds of tools:

- **To build the app:** Node.js and Rust (plus system libraries on Linux).
- **To run your solutions:** only the language(s) you plan to practice in. That's a JDK for Java, Python 3, and/or Node.js for JavaScript.

The app finds these on your `PATH` automatically. You can also point to them in **Settings → Code runners**.

### Windows

Open **PowerShell** and run these one by one.

**1. Build tools**

```powershell
# Node.js (LTS)
winget install -e --id OpenJS.NodeJS.LTS

# Rust
winget install -e --id Rustlang.Rustup

# C++ build tools (Rust needs these to compile on Windows)
winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

> Already have Visual Studio? Open **Visual Studio Installer** and tick the **Desktop development with C++** workload instead of running the last command.

**2. Languages you want to practice in** (pick any)

```powershell
winget install -e --id EclipseAdoptium.Temurin.21.JDK   # Java
winget install -e --id Python.Python.3.12               # Python
# JavaScript uses the Node.js you installed above
```

**3. Close PowerShell and open a new one** so the new tools are on your `PATH`. Then check:

```powershell
rustup default stable-msvc
cargo --version
node --version
```

**4. Run LogIQ**

```powershell
cd D:\path\to\logiq
npm install
npm run tauri dev
```

The first run takes 5–10 minutes because Rust compiles everything once. After that it starts in seconds.

> Windows 10/11 already include **WebView2**. If the app window doesn't open and mentions WebView2, run `winget install -e --id Microsoft.EdgeWebView2Runtime`.

### Linux

**1. System libraries** (pick your distro)

<details open>
<summary><b>Ubuntu / Debian / Linux Mint / Pop!_OS</b></summary>

```bash
sudo apt update
sudo apt install -y libwebkit2gtk-4.1-dev build-essential curl wget file \
  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```
</details>

<details>
<summary><b>Fedora</b></summary>

```bash
sudo dnf check-update
sudo dnf install -y webkit2gtk4.1-devel openssl-devel curl wget file \
  libappindicator-gtk3-devel librsvg2-devel libxdo-devel
sudo dnf group install -y "c-development"
```
</details>

<details>
<summary><b>Arch / Manjaro</b></summary>

```bash
sudo pacman -Syu --needed webkit2gtk-4.1 base-devel curl wget file openssl \
  appmenu-gtk-module libappindicator-gtk3 librsvg xdotool
```
</details>

**2. Rust and Node.js**

```bash
# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"

# Node.js 22 via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 22
```

**3. Languages you want to practice in** (pick any)

```bash
# Ubuntu / Debian
sudo apt install -y openjdk-21-jdk python3

# Fedora
sudo dnf install -y java-21-openjdk-devel python3

# Arch
sudo pacman -S --needed jdk21-openjdk python
```

JavaScript uses the Node.js you installed above.

**4. Run LogIQ**

```bash
cd ~/path/to/logiq
npm install
npm run tauri dev
```

The first run takes a few minutes while Rust compiles; later runs are quick.

---

## Build an installer

```bash
npm run tauri build
```

Installers land in `src-tauri/target/release/bundle/`:

| OS | Files | Folder |
| --- | --- | --- |
| Windows | `.exe` (setup) and `.msi` | `nsis/`, `msi/` |
| Linux | `.deb`, `.rpm`, `.AppImage` | `deb/`, `rpm/`, `appimage/` |

On Linux, the `.AppImage` runs on almost any distro: `chmod +x LogIQ*.AppImage && ./LogIQ*.AppImage`.

**Build on GitHub instead.** Push this repo to GitHub and push a tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

`.github/workflows/release.yml` builds the Windows and Linux installers and publishes a GitHub Release. You don't need Rust installed locally for this. See [Releasing](#releasing).

---

## Releasing

- One-time setup: on GitHub, open **Settings → Actions → General → Workflow permissions** and choose **Read and write permissions**.
- First release: `git tag v0.1.0` then `git push origin v0.1.0`.
- Later releases: `npm run release 0.1.1`.
- The build takes about 10–15 minutes and attaches `.exe`, `.msi`, `.AppImage` and `.deb` to the release.
- The landing page picks up the latest release automatically.

---

## Your data and backups

Renamed from LogicQuest: existing progress carries over automatically.

Everything is saved in a local **SQLite** database:

| OS | Location |
| --- | --- |
| Windows | `%APPDATA%\in.yashpurani.logicquest\logicquest.db` // legacy name kept so existing progress loads |
| Linux | `~/.local/share/in.yashpurani.logicquest/logicquest.db` // legacy name kept so existing progress loads |

It stores your XP, solved problems, quiz results, streak, settings and the code you wrote for every problem.

From **Settings → Your data**:

- **Show in folder:** opens the data folder.
- **Export backup:** saves everything to one `.json` file.
- **Import and merge:** combines a backup with this computer's progress. Nothing on either side is lost, which makes it the way to move between a Windows and a Linux machine.
- **Import and replace:** overwrites this computer's progress with the backup.
- **Automatic daily copies:** a copy of the database is saved once a day and the last 14 are kept. You can restore any of them.

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `cargo metadata ... program not found` | Rust isn't installed or the terminal is old. Install Rust (see above), then open a **new** terminal. |
| `link.exe not found` (Windows) | Install the C++ build tools (step 1 for Windows). |
| `webkit2gtk-4.1 not found` (Linux) | Install the system libraries for your distro (step 1 for Linux). |
| "JDK not found" / "Python 3 not found" / "Node.js not found" when you Run | Install that language, restart LogIQ, or set its path in **Settings → Code runners**. |
| `python` opens the Microsoft Store (Windows) | Install Python from python.org or winget and tick **Add python.exe to PATH**, or set the full path in Settings. |
| Blank or flickering window on Linux in a VM | Start with `WEBKIT_DISABLE_COMPOSITING_MODE=1 npm run tauri dev`. |
| Code always "Time limit exceeded" | Look for a loop whose condition never becomes false. Java gets an extra 1.5 s for JVM start-up. |
| Your code was flagged for a shortcut you didn't use in `solve()` | Keep the starter's `input / output is handled below` line. Only code above it is checked. |

---

## For developers

### Project layout

```
content/                 problem sources (Python) and the build/verify scripts
  basecamp/              Basecamp units (bc.py, java.py, python.py, javascript.py, java_oop.py, python_oop.py, javascript_oop.py)
  phase1.py … phase6.py  each problem: statement, tests, 3 hints, reference solution
  core.py                input/output formats and starter-code generators
  build.py               writes src/content/problems.json; --verify runs every check
src/
  content/               generated problems, phases + quizzes, guides (Markdown)
  lib/                   checker, runner bridge, game rules, shortcut detector, storage, backup
  pages/ components/     React UI
src-tauri/src/
  runner.rs              runs Java / Python / JavaScript with time limits and output caps
  store.rs               SQLite storage and daily backups
e2e/run_e2e.py           drives the real desktop app through WebDriver
tests/builtins.test.ts   shortcut detector tests
```

### Basecamp content

Core units live in `content/basecamp/java.py`, `python.py` and `javascript.py`, built with `unit(...)`. The OOP track lives in `java_oop.py`, `python_oop.py` and `javascript_oop.py`, built with `oop_unit(...)`. Each unit has `"section": "core"` or `"section": "oop"`. Each exercise is one call on a unit:

```python
u = unit("python", "Loops", "intro markdown")
u.predict("for i in range(3):\n    print(i)", "why it prints that")
u.blank("Count down.", "for i in range(5, ___, ___):\n    print(i)", [["0"], ["-1"]], "why")
u.fix("prompt", buggy_code, fixed_code, "why")
u.write("prompt", starter, solution, ["5\n", "0\n"], "why")   # stdin tests
```

```bash
python3 content/build_basecamp.py   # runs every snippet with real Java/Python/Node and writes src/content/basecamp.json
```

The build fills in expected outputs from real runs. It fails if a buggy "fix" already works, a starter already passes, or an alternative blank answer changes the output. Java snippets are statements that get wrapped in `class Main { main() }`, unless the exercise uses `full=True`. OOP Java exercises are complete programs (`full=True`): one `public class Main`, plus other classes in the same file with no `public` modifier.

### Adding a problem

Problems are written once, in Python. The reference solution produces every expected output, and starter code for Java, Python and JavaScript is generated from the parameter types.

```python
@problem(phase=2, title="Steps to Zero", returns="int", concepts=["while loop"],
         statement="""
         In one step: if `n` is even, halve it; otherwise subtract 1.
         Return the number of steps to reach 0.

         **Constraints:** 0 ≤ n ≤ 10^6
         """,
         params=[("n", "int")],
         tests=[(14,), (8,), (0,)],
         gen=lambda r: (r.randint(0, 10**6),), gen_count=3,   # extra random tests
         hints=["What is the loop condition?",
                "Inside the loop, which two actions are possible?",
                "while n > 0: n = (n even) ? n / 2 : n - 1; steps++."])
def steps_zero(n):
    s = 0
    while n:
        n = n // 2 if n % 2 == 0 else n - 1
        s += 1
    return s
```

```bash
python3 content/build.py            # regenerate src/content/problems.json
python3 content/build.py --verify   # check every problem end to end (needs java, javac, node, python3)
python3 content/build.py --verify p2-05   # check one problem
```

- **Parameter types:** `int long double char str int[] int[K] str[] int[][]`
- **Return types:** `int long double bool str int[] int_list long_list bool_list double_list str_list int[][] int_list_2d`
- Use `mode="print"` (the reference returns a list of lines) when the learner should print output themselves, and `strict=True` when spacing matters, as in patterns.

### Tests

```bash
cargo test --manifest-path src-tauri/Cargo.toml          # runner + SQLite store
node --experimental-strip-types tests/builtins.test.ts   # shortcut detector
npx tsc --noEmit                                         # types
python3 content/build.py --verify                        # all 145 problems in 3 languages
python3 content/build_basecamp.py                        # all 360 Basecamp exercises (core + OOP)
python3 content/lint_lang.py                             # no other-language text in any language's view

# Desktop end-to-end (Linux). Needs tauri-driver and webkit2gtk-driver.
cargo install tauri-driver
npx tauri build --debug --no-bundle
tauri-driver & python3 e2e/run_e2e.py              # problems, shortcuts, Pure bonus, SQLite restart
tauri-driver & python3 e2e/run_basecamp_e2e.py     # completes Basecamp units in all three languages
```

### Tech

Tauri 2 (Rust) · React 19 + TypeScript + Vite · CodeMirror 6 · SQLite (rusqlite) · zustand
