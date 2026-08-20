import json
import requests

ENDPOINT = "http://localhost:8000/normalize"

def run_eval():
    with open("evals/cases.json") as f:
        cases = json.load(f)

    results = []
    correct = 0

    for case in cases:
        resp = requests.post(ENDPOINT, json={"title": case["title"]})
        if resp.status_code != 200:
            results.append({**case, "actual": f"ERROR {resp.status_code}", "pass": False})
            continue

        actual = resp.json()["canonical_title"]
        passed = actual == case["expected"]
        correct += passed
        results.append({**case, "actual": actual, "pass": passed})

    print(f"\nScore: {correct}/{len(cases)} ({correct/len(cases)*100:.0f}%)\n")
    print("Failures:")
    for r in results:
        if not r["pass"]:
            print(f"  '{r['title']}' -> expected {r['expected']}, got {r['actual']}")

if __name__ == "__main__":
    run_eval()

    # to run : python evals/run.py