"""Desktop e2e for Basecamp: completes whole units in the real app by answering
every exercise from src/content/basecamp.json (fix/write run through the real
Java/Python/Node runners).

    tauri-driver &
    python3 e2e/run_basecamp_e2e.py
"""

import json
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "src-tauri", "target", "debug", "logicquest")
OUT = os.environ.get("E2E_OUT", os.path.join(ROOT, "e2e", "out"))
os.makedirs(OUT, exist_ok=True)
BC = json.load(open(os.path.join(ROOT, "src", "content", "basecamp.json")))

UNITS = [("python", "python-01"), ("java", "java-04"), ("javascript", "javascript-05")]


def seed(lang):
    return {
        "state": {
            "problems": {}, "docs": {}, "basecamp": {}, "xp": 0, "activity": {}, "bestStreak": 0,
            "settings": {"lang": lang, "pythonCmd": "", "javaHome": "", "nodeCmd": "", "fontSize": 14},
            "updatedAt": "2026-01-01T00:00:00.000Z",
        },
        "version": 3,
    }


def click_text(d, xpath_text, scope="//"):
    WebDriverWait(d, 30).until(EC.element_to_be_clickable((By.XPATH, f"{scope}button[normalize-space()='{xpath_text}']"))).click()


def paste_into_editor(d, text):
    editor = d.find_element(By.CSS_SELECTOR, ".ex-editor .cm-content")
    editor.click()
    editor.send_keys(Keys.CONTROL, "a")
    d.execute_script(
        "const dt = new DataTransfer(); dt.setData('text/plain', arguments[0]);"
        "document.querySelector('.ex-editor .cm-content').dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));",
        text,
    )


def answer(d, ex):
    k = ex["kind"]
    if k == "choice":
        d.find_elements(By.CSS_SELECTOR, ".quiz-opt")[ex["answer"]].click()
    elif k == "predict":
        box = d.find_element(By.CSS_SELECTOR, "textarea.ex-out")
        for j, line in enumerate(ex["expected"].rstrip("\n").split("\n")):
            if j:
                box.send_keys(Keys.ENTER)  # WebKitWebDriver drops "\n" inside send_keys text
            box.send_keys(line)
    elif k == "blank":
        for inp, alts in zip(d.find_elements(By.CSS_SELECTOR, ".blank-input"), ex["blanks"]):
            inp.send_keys(alts[0])
    elif k == "order":
        for line in ex["lines"]:
            for b in d.find_elements(By.CSS_SELECTOR, ".order-pool .order-line"):
                if b.find_element(By.TAG_NAME, "code").get_attribute("textContent") == line:
                    b.click()
                    break
    elif k in ("fix", "write"):
        paste_into_editor(d, ex["solution"])
        time.sleep(0.3)


def main():
    opts = ArgOptions()
    opts.set_capability("tauri:options", {"application": APP})
    opts.set_capability("browserName", "wry")
    d = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=opts)
    wait = WebDriverWait(d, 60)
    ok = True
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar")))
        for lang, uid in UNITS:
            d.execute_async_script(
                "const done = arguments[arguments.length - 1];"
                "window.__TAURI_INTERNALS__.invoke('save_state', {value: arguments[0]}).then(() => done(true));",
                json.dumps(seed(lang)),
            )
            d.execute_script(f"location.hash = '#/basecamp/{uid}'; location.reload();")
            time.sleep(1.5)
            unit = next(u for u in BC[lang] if u["id"] == uid)
            click_text(d, "Start")
            for i, ex in enumerate(unit["exercises"]):
                time.sleep(0.4)
                answer(d, ex)
                click_text(d, "Check")
                fb = WebDriverWait(d, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feedback > b"))).text
                if not fb.startswith("Correct"):
                    ok = False
                    detail = d.find_element(By.CSS_SELECTOR, ".feedback").text
                    print(f"  {uid} #{i + 1} {ex['kind']}: {detail[:300]}")
                    d.save_screenshot(os.path.join(OUT, f"bc-fail-{uid}-{i + 1}.png"))
                    break
                if ex["kind"] in ("fix", "write"):
                    d.save_screenshot(os.path.join(OUT, f"bc-{uid}-{ex['kind']}.png"))
                last = i == len(unit["exercises"]) - 1
                click_text(d, "Finish unit" if last else "Continue")
            else:
                big = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".big-xp"))).text
                d.save_screenshot(os.path.join(OUT, f"bc-{uid}-done.png"))
                print(f"{uid}: completed, {big}")
                ok &= big.startswith("+")
    finally:
        d.quit()
    print("BASECAMP E2E", "PASSED" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
