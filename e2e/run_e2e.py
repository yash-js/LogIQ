"""Desktop end-to-end test: drives the real Tauri app through WebDriver.

Requires: tauri-driver (cargo install tauri-driver), WebKitWebDriver (Linux:
webkit2gtk-driver), selenium, and a built app (npx tauri build --debug --no-bundle).

    tauri-driver &            # listens on :4444
    python3 e2e/run_e2e.py    # (use xvfb-run on a headless machine)
"""

import json
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "src-tauri", "target", "debug", "logiq")
OUT = os.environ.get("E2E_OUT", os.path.join(ROOT, "e2e", "out"))
os.makedirs(OUT, exist_ok=True)

JAVA_SOLUTION = """import java.io.*;
import java.util.*;

public class Main {
    static String solve(int n) {
        if (n > 0) return "Positive";
        if (n < 0) return "Negative";
        return "Zero";
    }
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.println(solve(Integer.parseInt(br.readLine().trim())));
    }
}
"""

# Forgets that 0 is even; only a hidden test catches it.
PY_BUGGY = """def solve(n):
    return "Even" if n % 2 == 0 and n != 0 else "Odd"


n = int(input())
ans = solve(n)
print(ans)
"""

PY_MAX = """def solve(a, b, c):
    return max(a, b, c)
"""

PY_PURE = """def solve(a, b, c):
    best = a
    if b > best:
        best = b
    if c > best:
        best = c
    return best
"""

PY_TAIL = """

# ---------- input / output is handled below, no need to change it ----------

a = int(input())
b = int(input())
c = int(input())
ans = solve(a, b, c)
print(ans)
"""

JS_LEAP = """function solve(year) {
  return year % 400 === 0 || (year % 4 === 0 && year % 100 !== 0);
}

// ---------- input / output is handled below, no need to change it ----------

const lines = require("fs").readFileSync(0, "utf8").split(/\\r?\\n/);
console.log(String(solve(Number(lines[0]))));
"""

PY_LOOP = """def solve(n):
    while True:
        pass


n = int(input())
print(solve(n))
"""


def seed():
    return {
        "state": {
            "problems": {
                "p1-01": {"attempts": 0, "hintsUsed": 0, "xpEarned": 0, "code": {"java": JAVA_SOLUTION}},
                "p1-02": {"attempts": 0, "hintsUsed": 0, "xpEarned": 0, "code": {"python": PY_BUGGY}},
                "p1-03": {"attempts": 0, "hintsUsed": 0, "xpEarned": 0, "code": {"python": PY_LOOP}},
                "p1-04": {"attempts": 0, "hintsUsed": 0, "xpEarned": 0, "code": {"python": PY_MAX + PY_TAIL}},
                "p1-05": {"attempts": 0, "hintsUsed": 0, "xpEarned": 0, "code": {"javascript": JS_LEAP}},
            },
            "docs": {"1": {"read": True, "quizPassed": True, "bestScore": 5}},
            "xp": 0,
            "activity": {},
            "bestStreak": 0,
            "settings": {"lang": "java", "pythonCmd": "", "javaHome": "", "nodeCmd": "", "fontSize": 14},
            "updatedAt": "2026-01-01T00:00:00.000Z",
        },
        "version": 2,
    }


def main():
    opts = ArgOptions()
    opts.set_capability("tauri:options", {"application": APP})
    opts.set_capability("browserName", "wry")
    d = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=opts)
    wait = WebDriverWait(d, 60)
    ok = True
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar")))
        # Progress lives in SQLite; seed it through the same command the app uses.
        d.execute_async_script(
            "const done = arguments[arguments.length - 1];"
            "window.__TAURI_INTERNALS__.invoke('save_state', {value: arguments[0]}).then(() => done(true), (e) => done(String(e)));",
            json.dumps(seed()),
        )
        d.execute_script("location.reload()")
        time.sleep(1.5)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar")))

        # 1. Correct Java solution -> Accepted + XP.
        d.execute_script("location.hash = '#/problem/p1-01'")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))).click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".celebrate")))
        big = d.find_element(By.CSS_SELECTOR, ".celebrate .big").text
        d.save_screenshot(os.path.join(OUT, "1-java-accepted.png"))
        print("java accepted, celebration shows", big)
        ok &= big == "+15"  # 10 base + 5 clean; no Pure bonus because this file's own main() uses .trim()

        # 2. Buggy Python -> Wrong answer on a hidden negative test.
        d.execute_script("location.hash = '#/problem/p1-02'")
        time.sleep(0.5)
        d.find_element(By.XPATH, "//div[@class='lang-tabs']//button[normalize-space()='Python']").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))).click()
        verdict = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".verdict"))).text
        d.save_screenshot(os.path.join(OUT, "2-python-wrong.png"))
        print("python buggy verdict:", verdict.splitlines()[0])
        ok &= verdict.startswith("Wrong answer")

        # 3. Infinite loop -> time limit, app stays responsive.
        d.execute_script("location.hash = '#/problem/p1-03'")
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Run']"))).click()
        verdict = WebDriverWait(d, 30).until(
            lambda drv: (v := drv.find_elements(By.CSS_SELECTOR, ".verdict")) and v[0].text or False
        )
        d.save_screenshot(os.path.join(OUT, "3-python-tle.png"))
        print("infinite loop verdict:", verdict.splitlines()[0])
        ok &= verdict.startswith("Time limit")

        # 4. Python with max() -> accepted + Pure challenge offered; then pure version -> bonus.
        def submit_and_celebrate():
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))).click()
            return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".celebrate")))

        d.execute_script("location.hash = '#/problem/p1-04'")
        time.sleep(0.6)
        d.find_element(By.XPATH, "//div[@class='lang-tabs']//button[normalize-space()='Python']").click()
        time.sleep(0.8)
        chip = d.find_element(By.CSS_SELECTOR, ".sc-chip").text
        print("shortcut chip:", chip)
        ok &= "max" in chip
        cel = submit_and_celebrate()
        time.sleep(0.6)
        d.save_screenshot(os.path.join(OUT, "4-shortcut-challenge.png"))
        offered = "without shortcuts" in cel.text
        print("pure challenge offered:", offered, "| xp", cel.find_element(By.CSS_SELECTOR, ".big").text)
        ok &= offered and cel.find_element(By.CSS_SELECTOR, ".big").text == "+15"
        d.find_element(By.XPATH, "//button[normalize-space()='Take the Pure challenge']").click()
        # Replace the code through the editor: select all, type the pure version.
        from selenium.webdriver.common.keys import Keys
        editor = d.find_element(By.CSS_SELECTOR, ".cm-content")
        editor.click()
        editor.send_keys(Keys.CONTROL, "a")
        # Paste the new code, the way a person would.
        d.execute_script(
            "const dt = new DataTransfer(); dt.setData('text/plain', arguments[0]);"
            "document.querySelector('.cm-content').dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));",
            PY_PURE + PY_TAIL,
        )
        time.sleep(0.6)
        cel = submit_and_celebrate()
        time.sleep(0.6)
        d.save_screenshot(os.path.join(OUT, "5-pure-solve.png"))
        print("pure solve:", cel.find_element(By.CSS_SELECTOR, "h2").text, cel.find_element(By.CSS_SELECTOR, ".big").text)
        ok &= cel.find_element(By.CSS_SELECTOR, ".big").text == "+5"

        # 5. JavaScript through Node.
        d.execute_script("location.hash = '#/problem/p1-05'")
        time.sleep(0.6)
        d.find_element(By.XPATH, "//div[@class='lang-tabs']//button[normalize-space()='JavaScript']").click()
        cel = submit_and_celebrate()
        print("javascript accepted:", cel.find_element(By.CSS_SELECTOR, ".big").text)
        ok &= cel.find_element(By.CSS_SELECTOR, ".big").text == "+20"  # 10 base + 5 clean + 5 pure
        d.save_screenshot(os.path.join(OUT, "6-javascript.png"))

        # 6. Settings page detects the toolchain through Rust.
        d.execute_script("location.hash = '#/settings'")
        WebDriverWait(d, 20).until(lambda drv: "checking…" not in drv.page_source)
        d.save_screenshot(os.path.join(OUT, "7-settings.png"))
        src = d.page_source
        found = "Python 3." in src and ("javac 2" in src or "javac 1" in src) and "Node.js v" in src
        print("toolchain detected:", found)
        ok &= found
        # 7. Restart the app: progress must come back from SQLite.
        time.sleep(1)  # let the debounced save land
        d.quit()
        d = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=opts)
        WebDriverWait(d, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".side-level-xp")))
        d.execute_script("location.hash = '#/profile'")
        time.sleep(1)
        xp_text = d.find_element(By.CSS_SELECTOR, ".profile-head").text
        print("after restart:", " ".join(xp_text.split()[-8:]))
        ok &= "55 XP total" in xp_text  # 15 + 15 + 5 + 20 earned above
        info = d.execute_async_script(
            "const done = arguments[arguments.length - 1];"
            "window.__TAURI_INTERNALS__.invoke('data_info').then(done, (e) => done(String(e)));"
        )
        print("daily backups:", info.get("backups"))
        ok &= bool(info.get("backups"))
        d.save_screenshot(os.path.join(OUT, "8-after-restart.png"))
    finally:
        d.quit()
    print("E2E", "PASSED" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
