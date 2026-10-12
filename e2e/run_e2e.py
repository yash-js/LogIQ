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
APP = os.path.join(ROOT, "src-tauri", "target", "debug", "logicquest")
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
            },
            "docs": {"1": {"read": True, "quizPassed": True, "bestScore": 5}},
            "xp": 0,
            "activity": {},
            "bestStreak": 0,
            "settings": {"lang": "java", "pythonCmd": "", "javaHome": "", "fontSize": 14},
            "updatedAt": "2026-01-01T00:00:00.000Z",
        },
        "version": 1,
    }


def main():
    opts = ArgOptions()
    opts.set_capability("tauri:options", {"application": APP})
    opts.set_capability("browserName", "wry")
    d = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=opts)
    wait = WebDriverWait(d, 60)
    ok = True
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".topbar")))
        d.execute_script("localStorage.setItem('logicquest-progress', arguments[0]); location.reload();", json.dumps(seed()))
        time.sleep(1.5)

        # 1. Correct Java solution -> Accepted + XP.
        d.execute_script("location.hash = '#/problem/p1-01'")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))).click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".celebrate")))
        big = d.find_element(By.CSS_SELECTOR, ".celebrate .big").text
        d.save_screenshot(os.path.join(OUT, "1-java-accepted.png"))
        print("java accepted, celebration shows", big)
        ok &= big == "+15"  # 10 base + 5 clean-solve bonus

        # 2. Buggy Python -> Wrong answer on a hidden negative test.
        d.execute_script("location.hash = '#/problem/p1-02'")
        time.sleep(0.5)
        d.find_element(By.XPATH, "//div[@class='editor-bar']//button[normalize-space()='Python']").click()
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

        # 4. Settings page detects the toolchain through Rust.
        d.execute_script("location.hash = '#/settings'")
        WebDriverWait(d, 20).until(lambda drv: "checking…" not in drv.page_source)
        d.save_screenshot(os.path.join(OUT, "4-settings.png"))
        src = d.page_source
        found = "Python 3." in src and ("javac 2" in src or "javac 1" in src)
        print("toolchain detected:", found)
        ok &= found
    finally:
        d.quit()
    print("E2E", "PASSED" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
