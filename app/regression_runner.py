"""Run a folder of sample log files and produce a JSON regression summary."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from app.log_parser import analyze_log_file

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "sample_logs"
REPORT_DIR = ROOT / "reports"

def run_regression() -> dict:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for log_file in sorted(LOG_DIR.glob("*.log")):
        result = analyze_log_file(log_file)
        results.append(result)

    counts = {
        "PASS": sum(item["status"] == "PASS" for item in results),
        "FAIL": sum(item["status"] == "FAIL" for item in results),
        "UNKNOWN": sum(item["status"] == "UNKNOWN" for item in results),
    }
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_tests": len(results),
        "summary": counts,
        "results": results,
    }
    report_path = REPORT_DIR / "regression_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

if __name__ == "__main__":
    report = run_regression()
    print("AI Verification Assistant - Regression Summary")
    print(f"Total logs: {report['total_tests']}")
    for status, count in report["summary"].items():
        print(f"{status}: {count}")
    print(f"Report saved to: {REPORT_DIR / 'regression_report.json'}")
