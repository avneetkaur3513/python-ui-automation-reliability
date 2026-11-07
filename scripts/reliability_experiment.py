"""Compare a fragile fixed wait with Playwright's condition-based assertion.

The search delays are deliberately controlled. This is a timing experiment,
not a claim about real production flakiness or a random bug found in the app.
Run with: python -m scripts.reliability_experiment
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import expect, sync_playwright

from test_support.server import serve_app


def run_experiment(iterations, wait_ms):
    observations = []
    with serve_app() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for index in range(iterations):
                delay_ms = 20 if index % 2 == 0 else 260
                page = browser.new_page()
                try:
                    page.goto(f"{base_url}?searchDelay={delay_ms}")
                    page.locator("#search").fill("payment")

                    # Intentionally weak approach: assumes every response finishes
                    # within an arbitrary fixed time. This is *only* the baseline.
                    page.wait_for_timeout(wait_ms)
                    fixed_wait_passed = page.get_by_test_id("ticket-item").count() == 1

                    page.reload()
                    page.locator("#search").fill("payment")
                    try:
                        expect(page.get_by_test_id("ticket-item")).to_have_count(1, timeout=3000)
                        condition_wait_passed = True
                    except PlaywrightTimeout:
                        condition_wait_passed = False

                    observations.append({
                        "iteration": index + 1,
                        "simulated_delay_ms": delay_ms,
                        "fixed_wait_passed": fixed_wait_passed,
                        "condition_wait_passed": condition_wait_passed,
                    })
                finally:
                    page.close()
        finally:
            browser.close()
    return {
        "experiment": "controlled delayed search vs fixed wait",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "iterations": iterations,
        "fixed_wait_ms": wait_ms,
        "fixed_wait_passes": sum(item["fixed_wait_passed"] for item in observations),
        "condition_wait_passes": sum(item["condition_wait_passed"] for item in observations),
        "observations": observations,
        "note": "The delays are intentionally injected. Counts describe this experiment only.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=12)
    parser.add_argument("--fixed-wait-ms", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path("artifacts/reliability.json"))
    args = parser.parse_args()
    if args.iterations < 2 or args.fixed_wait_ms < 0:
        parser.error("iterations must be at least 2 and fixed wait must be non-negative")
    result = run_experiment(args.iterations, args.fixed_wait_ms)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        f"Fixed wait: {result['fixed_wait_passes']}/{args.iterations} passed; "
        f"condition-based wait: {result['condition_wait_passes']}/{args.iterations} passed."
    )
    print(f"Measurements written to {args.output}")
    if result["condition_wait_passes"] != args.iterations:
        raise SystemExit("The condition-based approach was not fully reliable.")


if __name__ == "__main__":
    main()
