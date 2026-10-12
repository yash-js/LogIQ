# LogicQuest

A desktop app for building programming logic **before** starting DSA. 145 problems across six worlds, each with a short guide and a check you must pass before its problems open. Solve in Java, Python or JavaScript; your code runs on your own machine.

| Phase | World | Problems |
| --- | --- | --- |
| 1 | The Crossroads: conditional logic | 20 |
| 2 | The Looping Woods: loops and patterns | 26 |
| 3 | The Mirror Caves: recursion | 19 |
| 4 | The Iron Rails: arrays | 32 |
| 5 | The Scroll Library: strings | 22 |
| 6 | The Summit: combining logic | 26 |

## How it plays

- **Study first.** Each world opens with a guide (code shown in your chosen language) and a 5-question check. Score 4/5 to open the problems.
- **Run and Submit.** Run checks the visible examples. Submit runs the hidden tests too and shows the first failing case.
- **Pure challenge.** Library shortcuts (sort, Set/Map, max/min, reverse, pow, sum/reduce, indexOf/includes, toLowerCase, split/replace, bin/toString(2), BigInt/BigInteger, date libraries…) are detected as you type. A solution that uses them is still accepted, then the app asks you to solve it again without them for +50% bonus XP.
- **Hints cost XP.** Three hints per problem, from a nudge to the approach. Each one opened before solving takes 25% off that problem's XP.
- **Rewards.** XP and levels, a daily streak, a clean-solve bonus (first submit, no hints), and a daily quest worth double XP.
- **Next world** opens after solving 60% of the current one.
- Every problem links to a similar LeetCode or HackerRank problem for extra practice.

## Requirements

- Node 20+ and Rust (stable) to build.
- To run code, whichever languages you use: **JDK 17+** (e.g. Temurin from adoptium.net), **Python 3**, **Node.js 18+**. The app finds them on PATH, via `JAVA_HOME`, or via paths you set in Settings.
- Linux build deps: `libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev`.

## Run it

```bash
npm install
npm run tauri dev       # development
npm run tauri build     # installers in src-tauri/target/release/bundle
```

Windows builds produce `.msi` and `.exe` (NSIS); Linux builds produce `.deb`, `.rpm` and `.AppImage`. Pushing a tag like `v0.1.0` runs `.github/workflows/release.yml`, which builds both and attaches them to a draft GitHub release.

## Sign-in and sync (optional)

Without Supabase everything works offline and progress is saved on that computer. To sync between machines:

1. Create a Supabase project and run `supabase/migrations/0001_user_progress.sql` in the SQL editor.
2. Copy `.env.example` to `.env` and fill in the project URL and anon key. For release builds, add them as repository secrets with the same names.
3. **Auth → URL Configuration → Redirect URLs:** add `logicquest://auth-callback`.
4. **GitHub login:** Auth → Providers → GitHub, using a GitHub OAuth app whose callback URL is `https://<project>.supabase.co/auth/v1/callback`.
5. **Email code login:** Auth → Email Templates → Magic Link, include `{{ .Token }}` in the template so the email contains the 6-digit code.

Progress is one JSON document per user (`user_progress`, protected by row-level security). When two machines disagree, the app merges them: solves, quiz passes and activity are never lost.

## Project layout

```
content/           problem sources (Python) and the build/verify script
  phase1.py …      each problem = statement, tests, 3 hints, reference solution
  build.py         generates src/content/problems.json
src/content/       generated problems, phase metadata + quizzes, guides (Markdown)
src/               React UI (map, guides, workspace, profile, settings)
  lib/builtins.ts  shortcut detector behind the Pure challenge
src-tauri/src/     Rust: runner.rs compiles/runs Java, Python and JavaScript with time limits
supabase/          database migration
e2e/               WebDriver test that drives the real desktop app
```

## Adding or changing problems

Problems are written once in Python. The reference solution produces every expected output, and starter code for Java, Python and JavaScript is generated from the parameter types.

```python
@problem(phase=2, title="Steps to Zero", returns="int", concepts=["while loop"],
         statement="""...""", params=[("n", "int")],
         tests=[(14,), (8,), (0,)], gen=lambda r: (r.randint(0, 10**6),), gen_count=3,
         hints=["…", "…", "…"])
def steps_zero(n):
    ...
```

```bash
python3 content/build.py            # regenerate problems.json
python3 content/build.py --verify   # run every reference through real Python; check the Java and JavaScript I/O of every problem
```

Supported parameter types: `int long double char str int[] int[K] str[] int[][]`. Return types: `int long double bool str int[] int_list long_list bool_list double_list str_list int[][] int_list_2d`, or `mode="print"` for problems where the learner prints the output.

## Tests

```bash
cargo test --manifest-path src-tauri/Cargo.toml     # runner: Java, Python, JavaScript, timeouts, JSON contract
node --experimental-strip-types tests/builtins.test.ts   # shortcut detector
python3 content/build.py --verify                    # all 145 problems
# desktop end-to-end (Linux): needs tauri-driver and webkit2gtk-driver
npx tauri build --debug --no-bundle && tauri-driver & python3 e2e/run_e2e.py
```
